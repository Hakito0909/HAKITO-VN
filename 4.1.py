import json
import os
import time
import cloudscraper
import requests
from datetime import datetime
from colorama import Fore, init
from rich.table import Table
from rich.console import Console
from pystyle import Colors, Colorate, Center

# Khởi tạo colorama và rich
init(autoreset=True)
console = Console()

cookie_file = "twitter_cookie.txt"

banner = f"""

██╗  ██╗ █████╗ ██╗  ██╗██╗████████╗ ██████╗ 
██║  ██║██╔══██╗██║ ██╔╝██║╚══██╔══╝██╔═══██╗
███████║███████║█████╔╝ ██║   ██║   ██║   ██║
██╔══██║██╔══██║██╔═██╗ ██║   ██║   ██║   ██║
██║  ██║██║  ██║██║  ██╗██║   ██║   ╚██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝    ╚═════╝ 

ADMIN : HAKITO                           
\033════════════════════════════════════════════════  
            Telegram : HakitoVN
            Tiktok   : NONE
            Youtube  : NONE
            
\033════════════════════════════════════════════════                                               
"""
print(Colorate.Horizontal(Colors.blue_to_green, Center.XCenter(banner)))
os.system('cls' if os.name == 'nt' else 'clear')
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║     \033[1;33m  ĐĂNG NHẬP GOLIKE          \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")

# Xử lý Authorization và Token
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
    author = input("\033[1;32mNHẬP AUTHORIZATION : \033[1;33m")
    token = input("\033[1;32mNHẬP T (Token): \033[1;33m")
    Authorization = open("Authorization.txt", "w")
    t = open("token.txt", "w")
    Authorization.write(author)
    t.write(token)
else:
    print(f"\033[1;32m       Nhấn Enter để vào TOOL")
    print(f"\033[38;2;0;220;255m               HOẶC ")
    select = input(f"\033[1;32m  Nhập AUTHORIZATION {Fore.RED}(tại đây) \033[1;32mđể vào acc khác: \033[1;33m")

    if select != "":
        author = select
        token = input("\033[1;32m  Nhập T (Token) : \033[1;33m")
        Authorization = open("Authorization.txt", "w")
        t = open("token.txt", "w")
        Authorization.write(author)
        t.write(token)
Authorization.close()
t.close()
os.system('cls' if os.name == 'nt' else 'clear')
print(banner)
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║   \033[1;33m  DANH SÁCH ACC TWITTER      \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=utf-8',
    'Authorization': author,
    't': token,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    'Referer': 'https://app.golike.net/account/manager/twitter',
}

scraper = cloudscraper.create_scraper()

def chonacc():
    json_data = {}
    response = scraper.get(
        'https://gateway.golike.net/api/twitter-account',
        headers=headers,
        json=json_data
    ).json()
    return response

def nhannv(account_id):
    try:
        params = {
            'account_id': account_id,
            'data': 'null',
        }

        response = scraper.get(
            'https://gateway.golike.net/api/advertising/publishers/twitter/jobs',
            headers=headers,
            params=params,
            json={}
        )
        return response.json()
    except Exception as e:
        print()
        return {}

def parse_cookie_string(cookie_str):
    return {item.split("=")[0]: "=".join(item.split("=")[1:]) for item in cookie_str.split("; ")}

def create_headers(cookie_str, referer_link="https://x.com/"):
    cookies = parse_cookie_string(cookie_str)
    return {
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "x-csrf-token": cookies.get("ct0", ""),
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36",
        "referer": referer_link,
        "content-type": "application/x-www-form-urlencoded",
    }, cookies

def like_tweet(tweet_id, cookie_str):
    url = "https://x.com/i/api/1.1/likes/create.json"
    
    headers, cookies = create_headers(cookie_str, f"https://x.com/i/web/status/{tweet_id}")
    headers.update({
        "content-type": "application/json",
        "referer": f"https://x.com/i/web/status/{tweet_id}",
    })
    
    payload = {"tweet_mode": "extended", "id": tweet_id}

    try:
        response = requests.post(url, headers=headers, cookies=cookies, json=payload)
        if response.status_code == 200 and '"favorited":true' in response.text:
            print(f"\033[1;32mLike thành công tweet_id={tweet_id}")
            return True
        else:
            print(f"\033[1;31mLike lỗi, Đang bỏ qua job")
    except Exception as e:
        print(f"\033[1;31mLỗi Like")
    return False

def follow_twitter(user_id, cookie_str):
    headers, cookies = create_headers(cookie_str, f"https://x.com/i/user/{user_id}")
    url = f"https://api.twitter.com/1.1/friendships/create.json?user_id={user_id}&follow=true"
    try:
        response = requests.post(url, headers=headers, cookies=cookies)
        if response.status_code == 200 and '"following":true' in response.text:
            print(f"\033[1;32mFollow thành công user_id={user_id}")
            return True
        else:
            print(f"\033[1;31mFollow lỗi, Đang Bỏ qua job")
    except Exception as e:
        print(f"\033[1;31mLỗi Follow")
    return False

def hoanthanh(ads_id, account_id):
    try:
        json_data = {
            'ads_id': ads_id,
            'account_id': account_id,
            'async': True,
            'data': None,
        }

        response = scraper.post(
            'https://gateway.golike.net/api/advertising/publishers/twitter/complete-jobs',
            headers=headers,
            json=json_data,
            timeout=6
        )
        return response.json()
    except Exception as e:
        print()
        return {}

def baoloi(ads_id, object_id, account_id, loai):
    try:
        json_data1 = {
            'description': 'Tôi đã làm Job này rồi',
            'users_advertising_id': ads_id,
            'type': 'ads',
            'provider': 'twitter',
            'fb_id': account_id,
            'error_type': 6,
        }

        scraper.post('https://gateway.golike.net/api/report/send', headers=headers, json=json_data1)

        json_data2 = {
            'ads_id': ads_id,
            'object_id': object_id,
            'account_id': account_id,
            'type': loai,
        }

        scraper.post(
            'https://gateway.golike.net/api/advertising/publishers/twitter/skip-jobs',
            headers=headers,
            json=json_data2,
        )
    except Exception as e:
        print()

# Hàm hiển thị danh sách tài khoản bằng rich
def dsacc():
    if chontkTwitter.get("status") != 200:
        print("\033[1;31mAuthorization hoặc Token sai ")
        quit()

    data = chontkTwitter.get("data", [])
    if not data:
        print("\033[1;33mKhông có tài khoản Twitter nào được tìm thấy.")
        return

    # Tạo bảng với rich
    table = Table(title="Danh Sách Tài Khoản Twitter", show_header=True, header_style="bold cyan")
    table.add_column("STT", style="magenta", justify="center")
    table.add_column("Screen Name", style="yellow")
    table.add_column("Trạng Thái", style="green")

    for i, acc in enumerate(data):
        screen_name = acc.get("screen_name", acc.get("username", "Unknown"))
        table.add_row(str(i+1), screen_name, "Hoạt Động")

    console.print(table)

# Gọi hàm chọn tài khoản
chontkTwitter = chonacc()
dsacc()
print(f"{Fore.MAGENTA}═══════════════════════════════════")
while True:
    try:
        luachon = int(input("\033[1;32mChọn tài khoản Twitter: \033[1;33m"))
        while luachon > len((chontkTwitter)["data"]):
            luachon = int(input("\033[1;32mAcc Này Không Có Trong Danh Sách , Nhập Lại : \033[1;33m"))
        account_id = chontkTwitter["data"][luachon - 1]["id"]
        break  
    except:
        print("\033[1;31mChọn Tk twitter ") 
while True:
    try:
        delay = int(input(f"\033[1;32mDelay: \033[1;33m"))
        break
    except:
        print("\033[1;31mNhập Thời gian ⏰")
twitter_cookie = ""
if os.path.exists(cookie_file):
    with open(cookie_file, "r", encoding="utf-8") as f:
        twitter_cookie = f.read().strip()

    if twitter_cookie:
        new_cookie = input(f"\033[1;32mNhấn Enter dùng Cookie cũ {Fore.BLUE}or \033[1;32mnhập cookie mới {Fore.RED}(tại đây)\033[1;32m: \033[1;33m").strip()

        if new_cookie:
            twitter_cookie = new_cookie
            with open(cookie_file, "w", encoding="utf-8") as f:
                f.write(twitter_cookie)
            print("\033[1;36mĐã lưu cookie mới.")
        else:
            print("\033[1;36mTiếp tục dùng cookie cũ.")
    else:
        twitter_cookie = input("\033[1;32mNhập COOKIE TWITTER lần đầu: \033[1;33m").strip()
        with open(cookie_file, "w", encoding="utf-8") as f:
            f.write(twitter_cookie)
        print("\033[1;36mĐã lưu cookie lần đầu.")
else:
    twitter_cookie = input("\033[1;32m Nhập COOKIE TWITTER lần đầu: \033[1;33m").strip()
    with open(cookie_file, "w", encoding="utf-8") as f:
        f.write(twitter_cookie)
    print("\033[1;36mĐã lưu cookie lần đầu.")
while True:
    try: 
        doiacc = int(input(f"\033[1;32mThất bại bao nhiêu lần thì dừng tool: \033[1;33m"))
        break
    except:
        print("\033[1;31mNhập Vào 1 Số ")  
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║     \033[1;33m  CHỌN LOẠI NHIỆM VỤ      \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")
print("\033[1;36m[1] Follow")
print("\033[1;36m[2] Like")
print("\033[1;36m[3] Cả hai (Follow và Like)")

while True:
    try:
        loai_nhiem_vu = int(input("\033[1;32mChọn loại nhiệm vụ: \033[1;33m"))
        if loai_nhiem_vu in [1, 2, 3]:
            break
        else:
            print("\033[1;31mVui lòng chọn số từ 1 đến 3!")
    except:
        print("\033[1;31mSai định dạng! Vui lòng nhập số.")  

# Thêm phần chọn loại nhiệm vụ sau khi chọn tài khoản và trước khi bắt đầu làm nhiệm vụ
ads_id_da_lam = set()
object_id_da_lam = set()
dem = 0
lap_lai_ads = 0
tong = 0
checkdoiacc = 0
dsaccloi = []
accloi = ""
os.system('cls' if os.name == 'nt' else 'clear')

print(banner)
print("\033[1;35m╔═════════════════════════════════╗")
print("\033[1;35m║     \033[1;33m  Bắt Đầu Kiếm Tiền       \033[1;35m║")
print("\033[1;35m╚═════════════════════════════════╝")

while True:
    if checkdoiacc == doiacc:
        print(f"{Fore.GREEN}  Đã lỗi {doiacc} lần, tự động dừng tool  {Fore.WHITE}")
        exit()
    max_retries = 3
    retry_count = 0
    nhanjob = None

    while retry_count < max_retries:
        try:
            nhanjob = nhannv(account_id)
            if nhanjob and nhanjob.get("status") == 200 and nhanjob["data"].get("link") and nhanjob["data"].get("object_id"):
                break
            else:
                retry_count += 1
                time.sleep(2)
        except Exception as e:
            retry_count += 1
            time.sleep(1)

    if not nhanjob or retry_count >= max_retries:
        continue

    ads_id = nhanjob["data"]["id"]
    if ads_id in ads_id_da_lam:
        lap_lai_ads += 1
        print(f"\033[1;33m  Bỏ qua job trùng lặp: ads_id={ads_id} ({lap_lai_ads} lần)")

    if lap_lai_ads >= 5:
        baoloi(ads_id, nhanjob["data"]["object_id"], account_id, nhanjob["data"]["type"])
        print("\033[1;35m  Đã báo lỗi job trùng lặp quá nhiều.")
        lap_lai_ads = 0
        time.sleep(2)
        continue
    else:
        lap_lai_ads = 0

    ads_id_da_lam.add(ads_id)

    if len(ads_id_da_lam) > 100:
        ads_id_da_lam = set(list(ads_id_da_lam)[-100:])

    link = nhanjob["data"]["link"]
    object_id = nhanjob["data"]["object_id"]
    if object_id in object_id_da_lam:
        print(f"\033[1;33m  Đã follow/like object_id={object_id} trước đó. Bỏ qua.")
        baoloi(ads_id, object_id, account_id, nhanjob["data"]["type"])
        time.sleep(2)
        continue

    job_type = nhanjob["data"]["type"]

    if (loai_nhiem_vu == 1 and job_type != "follow") or \
       (loai_nhiem_vu == 2 and job_type != "like") or \
       (job_type not in ["follow", "like"]):
        baoloi(ads_id, object_id, account_id, job_type)
        continue

    try:
        success = False
        if job_type == "follow":
            success = follow_twitter(object_id, twitter_cookie)
        elif job_type == "like":
            success = like_tweet(object_id, twitter_cookie)
        else:
            baoloi(ads_id, object_id, account_id, job_type)
            continue

        if not success:
            baoloi(ads_id, object_id, account_id, job_type)
            checkdoiacc += 1
            continue

        for remaining_time in range(delay, -1, -1):
            color = "\033[1;36m" if remaining_time % 2 == 0 else "\033[1;33m"
            print(f"\r{color}   HAKITO |SUCCESS|⏰ {remaining_time}s           ", end="")
            time.sleep(1)

        print("\r                          \r", end="")
        print("\033[1;36mĐang Nhận Tiền    ", end="\r")
    except Exception as e:
        print(f"\033[1;31mLỗi thực hiện job: {e}")
        baoloi(ads_id, object_id, account_id, job_type)
        checkdoiacc += 1
        continue

    max_attempts = 2
    attempts = 0
    nhantien = None
    while attempts < max_attempts:
        try:
            nhantien = hoanthanh(ads_id, account_id)
            if nhantien and nhantien.get("status") == 200:
                break
        except:
            pass  
        attempts += 1

    if nhantien and nhantien.get("status") == 200:
        object_id_da_lam.add(object_id)
        if len(object_id_da_lam) > 200:
            object_id_da_lam = set(list(object_id_da_lam)[-100:])
        dem += 1
        tien = nhantien["data"]["prices"]
        tong += tien
        local_time = time.localtime()
        hour = local_time.tm_hour
        minute = local_time.tm_min
        second = local_time.tm_sec
        h = hour
        m = minute
        s = second
        if hour < 10:
            h = "0" + str(hour)
        if minute < 10:
            m = "0" + str(minute)
        if second < 10:
            s = "0" + str(second)
                                      
        chuoi = (f"\033[1;35m[\033[1;31m{dem}\033[1;35m]"
                 f" \033[1;35m[\033[1;32mDone\033[1;35m] 🔥"
                 f" \033[1;35m[\033[38;2;0;180;255m{job_type}\033[1;35m] ✅"
                 f" \033[1;35m[\033[1;33m+{tien}\033[1;35m] 💸"
                 f" \033[1;35m[\033[1;33mTổng: {tong}\033[1;35m] 💸"
                 f" \033[1;35m[\033[1;37mTime: {h}:{m}:{s}\033[1;35m] ⏰")

        print("                                                    ", end="\r")
        print(chuoi)
        time.sleep(0.7)
        checkdoiacc = 0
    else:
        try:
            baoloi(ads_id, object_id, account_id, nhanjob["data"]["type"])
            print("                                              ", end="\r")
            print("\033[1;31mBỏ qua nhiệm vụ ", end="\r")
            time.sleep(1)
            checkdoiacc += 1
        except:
            pass
