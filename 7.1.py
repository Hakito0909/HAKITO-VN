#!/usr/bin/env python3
# golike_linkedin_appium.py
import os
import time
import json
import requests
from appium import webdriver
from selenium.webdriver.common.by import By

# ========== CONFIG ==========
APPIUM_SERVER = "http://127.0.0.1:4723/wd/hub"
PLATFORM_NAME = "Android"
DEVICE_NAME = "Android"          # termux on-device: generic name ok
AUTOMATION_NAME = "UiAutomator2"
LINKEDIN_PACKAGE = "com.linkedin.android"
# If you want Appium to NOT reinstall and keep login state:
NO_RESET = True
# ============================

def create_driver():
    caps = {
        "platformName": PLATFORM_NAME,
        "deviceName": DEVICE_NAME,
        "automationName": AUTOMATION_NAME,
        "appPackage": LINKEDIN_PACKAGE,
        # appActivity can be omitted; Appium will start the package
        "noReset": NO_RESET,
        "autoGrantPermissions": True
    }
    driver = webdriver.Remote(APPIUM_SERVER, caps)
    driver.implicitly_wait(5)
    return driver

# ---------- GoLike API helpers ----------
def get_job(auth, account_id):
    headers = {
        "Authorization": auth,
        "t": "VFZSWk5VOUVVVEJQUkZGNFRXYzlQUT09",
        "User-Agent": "ok"
    }
    try:
        resp = requests.get(
            f"https://gateway.golike.net/api/advertising/publishers/linkedin/jobs?account_id={account_id}&data=null",
            headers=headers, timeout=15
        )
        data = resp.json()
        # Expect structure similar to earlier: {'data': {...}, 'lock': {...}, ...}
        return data.get("data")
    except Exception as e:
        print("❌ Lỗi get_job:", e)
        return None

def report_job_complete(auth, account_id, ads_id):
    headers = {
        "Authorization": auth,
        "t": "VFZSWk5VOUVVVEJQUkZGNFRXYzlQUT09",
        "User-Agent": "ok"
    }
    json_data = {"ads_id": ads_id, "account_id": account_id, "async": True, "data": None}
    try:
        resp = requests.post(
            "https://gateway.golike.net/api/advertising/publishers/linkedin/complete-jobs",
            headers=headers, json=json_data, timeout=15
        )
        return resp.json()
    except Exception as e:
        print("❌ Lỗi report_job_complete:", e)
        return None

def skip_job(auth, account_id, ads_id, object_id, job_type):
    headers = {
        "Authorization": auth,
        "t": "VFZSWk5VOUVVVEJQUkZGNFRXYzlQUT09",
        "User-Agent": "ok"
    }
    json_data = {
        "ads_id": ads_id,
        "object_id": object_id,
        "account_id": account_id,
        "type": job_type
    }
    try:
        requests.post("https://gateway.golike.net/api/advertising/publishers/linkedin/skip-jobs", headers=headers, json=json_data, timeout=10)
    except Exception as e:
        print("❌ Lỗi skip_job:", e)

# ---------- Mobile actions ----------
def open_link_in_app(link):
    """
    Trên chính thiết bị Android (Termux), dùng am start để mở link.
    """
    cmd = f'am start -a android.intent.action.VIEW -d "{link}"'
    print("🔗 Mở link bằng intent:", link)
    os.system(cmd)

def find_and_click_follow(driver):
    """
    Thử nhiều selector khác nhau để tìm nút Follow/Theo dõi/Kết nối.
    Trả về True nếu click thành công.
    """
    tries = [
        # tiếng Anh
        'new UiSelector().textContains("Follow")',
        'new UiSelector().text("Follow")',
        # tiếng Việt (nếu LinkedIn hiển thị tiếng Việt)
        'new UiSelector().textContains("Theo dõi")',
        'new UiSelector().textContains("Kết nối")',
        # thử theo content-desc / description chứa Follow
        'new UiSelector().descriptionContains("Follow")',
        # theo class và clickable
        'new UiSelector().clickable(true).className("android.widget.Button")'
    ]

    for sel in tries:
        try:
            els = driver.find_elements(By.ANDROID_UIAUTOMATOR, sel)
            if not els:
                continue
            # thử click element nào có text "Follow" hoặc clickable
            for el in els:
                try:
                    txt = el.text or ""
                    print("  → Tìm thấy button:", txt)
                    # if it's clearly not a disabled state, click
                    el.click()
                    time.sleep(1)
                    return True
                except Exception as e:
                    # thử tiếp
                    print("   ⚠️ Click lỗi:", e)
                    continue
        except Exception as e:
            # nếu selector lỗi, bỏ qua
            continue
    # nếu không tìm thấy
    return False

# ---------- Main flow ----------
def main():
    print("=== GoLike LinkedIn Auto Follow (Appium on Termux) ===")
    auth = input("Nhập AUTH GoLike: ").strip()
    account_id = input("Nhập account_id LinkedIn trong GoLike: ").strip()
    delay = int(input("Delay giữa job (giây): ").strip() or "3")
    max_jobs = int(input("Số job tối đa (max): ").strip() or "20")

    print("Khởi tạo Appium driver...")
    try:
        driver = create_driver()
    except Exception as e:
        print("❌ Không thể kết nối Appium server:", e)
        return

    done = 0
    consecutive_fail = 0
    while done < max_jobs:
        job = get_job(auth, account_id)
        if not job:
            print("⏳ Không lấy được job (None). Thử lại sau 3s.")
            time.sleep(3)
            continue

        # job có thể là dict (data)
        # kiểm tra job type
        job_type = job.get("type") if isinstance(job, dict) else None
        ads_id = job.get("id") if isinstance(job, dict) else None
        object_id = job.get("lock", {}).get("object_id") if isinstance(job, dict) else None
        link = job.get("link") if isinstance(job, dict) else None

        print(f"\n[JOB] id={ads_id} | type={job_type} | link={link}")

        # Chỉ chạy follow
        if job_type != "follow":
            print(f"⚠️ Bỏ qua job type={job_type} (chỉ chạy follow).")
            skip_job(auth, account_id, ads_id, object_id, job_type or "unknown")
            time.sleep(1)
            continue

        if not link:
            print("⚠️ Link job rỗng, skip.")
            skip_job(auth, account_id, ads_id, object_id, job_type)
            time.sleep(1)
            continue

        # Mở link vào LinkedIn app
        open_link_in_app(link)
        # chờ app load
        print("⏳ Đợi app load ...")
        time.sleep(5 + random.randint(1,3))

        # Thử tìm và click Follow nhiều lần
        clicked = False
        for attempt in range(3):
            try:
                clicked = find_and_click_follow(driver)
                if clicked:
                    print("✅ Đã click Follow (attempt {})".format(attempt+1))
                    break
                else:
                    print("⚠️ Chưa tìm thấy nút Follow (attempt {})".format(attempt+1))
                time.sleep(2)
            except Exception as e:
                print("⚠️ Lỗi khi click follow:", e)
                time.sleep(2)

        if not clicked:
            print("❌ Không thể nhấn Follow, sẽ Skip job để tránh bị khóa.")
            skip_job(auth, account_id, ads_id, object_id, job_type)
            consecutive_fail += 1
            if consecutive_fail >= 10:
                print("⚠️ Lỗi liên tiếp nhiều, dừng lại để kiểm tra.")
                break
            time.sleep(delay)
            continue

        # Nếu click thành công, báo về GoLike
        res = report_job_complete(auth, account_id, ads_id)
        if res and res.get("status") == 200:
            done += 1
            consecutive_fail = 0
            price = res.get("data", {}).get("prices", "0")
            print(f"🎉 Hoàn tất job {done}/{max_jobs} — +{price} xu")
        else:
            print("⚠️ API báo không thành công khi report job:", res)
            # thử skip để tránh lặp
            skip_job(auth, account_id, ads_id, object_id, job_type)
            consecutive_fail += 1

        # đợi trước job tiếp theo
        time.sleep(delay)

    print("✅ Hoàn thành quá trình (hoặc đạt max job).")
    try:
        driver.quit()
    except:
        pass

if __name__ == "__main__":
    main()
