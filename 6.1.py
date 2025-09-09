try:
    import os
    import sys
    import time
    import json
    import random
    import string
    import requests
    import string
    import base64
    import subprocess
    from time import sleep
    import uuid
    import hashlib
    from colorama import Fore, init
    from collections import defaultdict    
    from datetime import datetime, timedelta
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    from colorama import init
    from pystyle import Colors, Colorate
except ModuleNotFoundError as e:
    lib = e.name
    print(f"Thiếu thư viện {lib}, đang cài đặt 💻...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
        print(f"Đã cài đặt {lib} thành công! 📂")
        os.system("cls" if os.name == "nt" else "clear")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except subprocess.CalledProcessError:
        print(f"Không thể cài đặt {lib}, thoát tool ...")
        sys.exit(1)

        
        
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
AQUA = "\033[96m"
LIME = "\033[92m"

os.system("cls" if os.name == "nt" else "clear")
# import lại
import string
import requests
import random
from collections import defaultdict    
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from colorama import init
import cloudscraper
from colorama import Fore, init
from pystyle import Colors, Colorate 

import requests
import random
import string
import hashlib,os

trang = "\033[1;37m\033[1m"
xanh_la = "\033[1;32m\033[1m"
xanh_duong = "\033[1;34m\033[1m"
xanhnhat = '\033[1m\033[38;5;51m'
do = "\033[1;31m\033[1m\033[1m"
xam = '\033[1;30m\033[1m'
vang = "\033[1;33m\033[1m"
tim = "\033[1;35m\033[1m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
AQUA = "\033[96m"
LIME = "\033[92m"
hongnhat = "#FFC0CB"
kt_code = "🌸"
dac_biet = "\033[32;5;245m\033[1m\033[38;5;39m"
vua = "\033[1;39m[\033[1;32m ¤ \033[1;39m] \033[32;5;245m\033[1m\033[38;5;39m=> "

import threading
import base64
import os
import time
import re
import json
import random
import requests
import socket
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box
from colorama import Fore, init
from colorama import init
from pystyle import Colors, Colorate 
from time import sleep
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
AQUA = "\033[96m"
LIME = "\033[92m"


colors = [
    "\033[1;37m\033[1m",  # Trắng
    "\033[1;32m\033[1m",  # Xanh lá
    "\033[1;34m\033[1m",  # Xanh dương 
    "\033[1m\033[38;5;51m",  # Xanh nhạt
    "\033[1;31m\033[1m\033[1m",  # Đỏ
    "\033[1;30m\033{1m",  # Xám
    "\033[1;33m\033[1m",  # Vàng
    "\033[1;35m\033[1m",  # Tím
    "\033[32;5;245m\033[1m\033[38;5;39m",  # Màu đặc biệt
]

# Kiểm tra mạng
def kiem_tra_mang():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
    except OSError:
        print("Mạng không ổn định hoặc bị mất kết nối. Vui lòng kiểm tra lại mạng.")

kiem_tra_mang()

# Banner
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colorate.Horizontal(Colors.blue_to_green, """
██╗  ██╗ █████╗ ██╗  ██╗██╗████████╗ ██████╗ 
██║  ██║██╔══██╗██║ ██╔╝██║╚══██╔══╝██╔═══██╗
███████║███████║█████╔╝ ██║   ██║   ██║   ██║
██╔══██║██╔══██║██╔═██╗ ██║   ██║   ██║   ██║
██║  ██║██║  ██║██║  ██╗██║   ██║   ╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝    ╚═════╝ 

ADMIN : HAKITO                           
════════════════════════════════════════════════  
            Telegram : NONE
            Tiktok   : NONE
            Youtube  : NONE
════════════════════════════════════════════════                                                
"""))

# Nhập Auth
try:
    Authorization = open("Authorization.txt", "x")
    t = open("token.txt", "x")
except:
    pass
Authorization = open("Authorization.txt", "r")
t = open("token.txt", "r")
author = Authorization.read()
token = t.read()
if author == "":
    author = input(Colorate.Diagonal(Colors.blue_to_white, " 💸 NHẬP AUTHORIZATION GOLIKE : "))
    token = input(Colorate.Diagonal(Colors.red_to_white, "💸  NHẬP TOKEN (T CỦA GOLIKE): "))
    Authorization = open("Authorization.txt", "w")
    t = open("token.txt", "w")
    Authorization.write(author)
    t.write(token)
Authorization.close()
t.close()

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': author,
    't': token,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://app.golike.net/account/manager/snapchat',
}

scraper = cloudscraper.create_scraper()

# API
def chonacc():
    try:
        response = scraper.get('https://gateway.golike.net/api/snapchat-account', headers=headers).json()
        return response
    except Exception:
        sys.exit()

def nhannv(account_id):
    try:
        params = {
            'account_id': account_id,
            'data': 'null',
        }
        response = scraper.get('https://gateway.golike.net/api/advertising/publishers/snapchat/jobs', headers=headers, params=params).json()
        return response
    except Exception:
        sys.exit()

def hoanthanh(ads_id, account_id):
    try:
        json_data = {
            'ads_id': ads_id,
            'account_id': account_id,
            'async': True,
            'data': None,
        }
        response = scraper.post('https://gateway.golike.net/api/advertising/publishers/snapchat/complete-jobs', headers=headers, json=json_data, timeout=6)
        return response.json()
    except Exception:
        sys.exit()

def baoloi(ads_id, object_id, account_id, loai):
    try:
        json_data2 = {
            'ads_id': ads_id,
            'object_id': object_id,
            'account_id': account_id,
            'type': loai,
        }
        scraper.post('https://gateway.golike.net/api/advertising/publishers/snapchat/skip-jobs', headers=headers, json=json_data2)
    except Exception:
        sys.exit()

# Danh sách acc
chontk = chonacc()
def dsacc():
    if chontk.get("status") != 200:
        print("\033[1;31mAuthorization hoặc T sai 😂")
        quit()
    for i in range(len(chontk["data"])):
        print(f"[{i+1}] {chontk['data'][i]['name']} | Online")
dsacc()

# Chọn acc
while True:
    try:
        luachon = int(input("Chọn tài khoản Snapchat bạn muốn chạy 🤑: "))
        while luachon > len((chontk)["data"]):
            luachon = int(input("Acc này không có, nhập lại: "))
        account_id = chontk["data"][luachon - 1]["id"]
        break
    except:
        print("Sai định dạng")

# Delay
while True:
    try:
        delay = int(input("Delay thực hiện job ⏰: "))
        break
    except:
        print("Sai định dạng")

# Chạy job
banner()
dem = 0
tong = 0

while True:
    print('\033[1;35mĐANG GET JOB ✅', end="\r")
    nhanjob = nhannv(account_id)
    if not nhanjob or nhanjob.get("status") != 200:
        continue

    ads_id = nhanjob["data"]["id"]
    link = nhanjob["data"]["link"]
    object_id = nhanjob["data"]["object_id"]
    job_type = nhanjob["data"]["type"]

    if job_type != "follow":
        baoloi(ads_id, object_id, account_id, job_type)
        continue

    # Mở link Snapchat để bạn tự follow
    os.system(f'termux-open-url {link}')

    # Delay
    for remaining_time in range(delay, -1, -1):
        print(f"\rĐang chờ bạn follow... [{remaining_time}s]", end="")
        time.sleep(1)
    print("\r                          \r", end="")

    # Thử hoàn thành job
    nhantien = hoanthanh(ads_id, account_id)
    if nhantien and nhantien.get("status") == 200:
        dem += 1
        tien = nhantien["data"]["prices"]
        tong += tien
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("STT", style="bold yellow")
        table.add_column("Status", style="green")
        table.add_column("Tiền", style="bold green")
        table.add_column("Tổng Tiền", style="bold white")
        table.add_row(str(dem), "SUCCESS", f"+{tien}đ", f"{tong} vnđ")
        os.system('cls' if os.name == 'nt' else 'clear')
        banner()
        console.print(table)
        time.sleep(0.7)
    else:
        # Nếu không follow hoặc lỗi → skip job
        baoloi(ads_id, object_id, account_id, job_type)
        print("Job lỗi, bỏ qua và lấy job mới...", end="\r")
        sleep(1.5)
