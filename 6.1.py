import os
import sys
import time
import socket
import requests
from time import sleep
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from pystyle import Colors, Colorate
import cloudscraper
from pathlib import Path

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

# Tạo thư mục cookies nếu chưa có
Path("cookies_snapchat").mkdir(parents=True, exist_ok=True)

# Load Snapchat cookies theo account_id
def load_snapchat_cookies(account_id):
    cookie_path = f"cookies_snapchat/{account_id}.txt"
    with open(cookie_path, "r") as f:
        cookie_raw = f.read().strip()
    cookies = dict(item.strip().split("=", 1) for item in cookie_raw.split("; "))
    return cookies

# Kiểm tra đã follow hay chưa
def is_following(username, account_id):
    try:
        cookies = load_snapchat_cookies(account_id)
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
        }
        url = f"https://www.snapchat.com/add/{username}"
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        if response.status_code != 200:
            print(f"[!] Không thể truy cập Snapchat profile: {response.status_code}")
            return False
        soup = BeautifulSoup(response.text, "html.parser")
        return "Following" in soup.text
    except Exception as e:
        print(f"[!] Lỗi khi kiểm tra follow: {e}")
        return False

# Load auth + token Golike
try:
    open("Authorization.txt", "x")
    open("token.txt", "x")
except: pass
Authorization = open("Authorization.txt", "r")
t = open("token.txt", "r")
author = Authorization.read()
token = t.read()
if author == "":
    author = input(Colorate.Diagonal(Colors.blue_to_white, " 💸 NHẬP AUTHORIZATION GOLIKE : "))
    token = input(Colorate.Diagonal(Colors.red_to_white, "💸  NHẬP TOKEN (T CỦA GOLIKE): "))
    with open("Authorization.txt", "w") as Authorization, open("token.txt", "w") as t:
        Authorization.write(author)
        t.write(token)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': author,
    't': token,
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://app.golike.net/account/manager/snapchat',
}

scraper = cloudscraper.create_scraper()

# API GOLIKE
def chonacc():
    try:
        return scraper.get('https://gateway.golike.net/api/snapchat-account', headers=headers).json()
    except:
        sys.exit()

def nhannv(account_id):
    try:
        params = {'account_id': account_id, 'data': 'null'}
        return scraper.get('https://gateway.golike.net/api/advertising/publishers/snapchat/jobs', headers=headers, params=params).json()
    except:
        sys.exit()

def hoanthanh(ads_id, account_id):
    try:
        json_data = {'ads_id': ads_id, 'account_id': account_id, 'async': True, 'data': None}
        return scraper.post('https://gateway.golike.net/api/advertising/publishers/snapchat/complete-jobs', headers=headers, json=json_data, timeout=6).json()
    except:
        return None

def baoloi(ads_id, object_id, account_id, loai):
    try:
        json_data = {'ads_id': ads_id, 'object_id': object_id, 'account_id': account_id, 'type': loai}
        scraper.post('https://gateway.golike.net/api/advertising/publishers/snapchat/skip-jobs', headers=headers, json=json_data)
    except: pass

# Chọn tài khoản Snapchat
def chon_tai_khoan():
    global account_id
    chontk = chonacc()
    if chontk.get("status") != 200:
        print("\033[1;31mAuthorization hoặc T sai 😂")
        quit()
    for i, acc in enumerate(chontk["data"]):
        print(f"[{i+1}] {acc['name']} | Online")
    while True:
        try:
            luachon = int(input("Chọn tài khoản Snapchat bạn muốn chạy 🤑: "))
            if 1 <= luachon <= len(chontk["data"]):
                account_id = chontk["data"][luachon - 1]["id"]
                break
            else:
                print("Acc này không có, nhập lại")
        except:
            print("Sai định dạng")

    cookie_path = f"cookies_snapchat/{account_id}.txt"

    # Nếu chưa có cookie → yêu cầu nhập và lưu
    if not os.path.exists(cookie_path):
        print(f"🔐 Nhập COOKIE SNAPCHAT cho tài khoản ID {account_id}")
        print("→ Vào https://www.snapchat.com (đã login), mở DevTools → Application → Cookies")
        cookie_input = input("Dán toàn bộ cookie: ").strip()
        with open(cookie_path, "w") as f:
            f.write(cookie_input)

chon_tai_khoan()

while True:
    try:
        delay = int(input("Delay thực hiện job ⏰: "))
        break
    except:
        print("Sai định dạng")

while True:
    try:
        gioihan_loi = int(input("Sau bao nhiêu job lỗi thì quay lại chọn acc mới ⏰: "))
        break
    except:
        print("Sai định dạng")

# Vòng lặp chính
while True:
    banner()
    dem = 0
    tong = 0
    jobloi = 0
    while True:
        print('ĐANG GET JOB ✅', end="\r")
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

        username = link.strip().split("/")[-1]

        if is_following(username, account_id):
            nhantien = hoanthanh(ads_id, account_id)
            if nhantien and nhantien.get("status") == 200:
                dem += 1
                tien = nhantien["data"]["prices"]
                tong += tien
                jobloi = 0
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
                baoloi(ads_id, object_id, account_id, job_type)
                jobloi += 1
        else:
            print(f"[⛔] Bạn chưa follow @{username} → Bỏ qua job.")
            baoloi(ads_id, object_id, account_id, job_type)
            jobloi += 1

        if jobloi >= gioihan_loi:
            print("\nĐã vượt quá số job lỗi cho phép → quay lại chọn acc mới!")
            chon_tai_khoan()
            break

        time.sleep(delay)
