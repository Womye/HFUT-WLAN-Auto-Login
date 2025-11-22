import subprocess
import requests
import time
import os
import sys
import ctypes

# =========== 你的登录信息（修改这里） ==========
USERNAME = "你的学号"
PASSWORD_MD5 = "浏览器中MD5加密的密码"
OMKKEY = "123456"

WIFI_NAME = "hfut-wlan"
DRCOM_URL = "http://172.18.3.3/0.htm"
# =================================================


# ------- 判断是否插网线 -------
def ethernet_connected():
    try:
        output = subprocess.check_output(
            'powershell "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Select-Object -ExpandProperty InterfaceDescription"',
            shell=True, encoding='gbk', errors='ignore'
        )
        return ("Realtek" in output) or ("Ethernet" in output) or ("PCIe" in output)
    except:
        return False


# ------- 连接校园网 WiFi -------
def connect_wifi():
    print("正在连接校园网 WiFi ...")

    cmd = f'netsh wlan connect name="{WIFI_NAME}"'
    try:
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        return True
    except:
        return False


# ------- WiFi 登录认证（模拟浏览器） -------
def wifi_login():
    print("正在进行 WiFi 认证 ...")

    login_url = DRCOM_URL

    data = {
        "DDDDD": USERNAME,
        "upass": PASSWORD_MD5,
        "R1": "0",
        "R2": "1",
        "para": "00",
        "0MKKey": OMKKEY
    }

    try:
        r = requests.post(login_url, data=data, timeout=5)
        if r.status_code == 200:
            print("WiFi 登录成功!")
            return True
        else:
            print("WiFi 登录失败!!")
    except:
        pass

    return False


# ------- 网线登录（调用 Drcom） -------
def ethernet_login():
    print("正在进行有线 Drcom 登录...")

    data = {
        "DDDDD": USERNAME,
        "upass": PASSWORD_MD5,
        "R1": "0",
        "R2": "1",
        "para": "00",
        "0MKKey": OMKKEY
    }

    try:
        r = requests.post(DRCOM_URL, data=data, timeout=5)
        if r.status_code == 200:
            print("有线登录成功!")
            return True
    except:
        pass

    print("有线登录失败!")
    return False


# ------------------- 入口 -------------------
def main():
    # 静默
    if not sys.stdout.isatty():
        pass

    if ethernet_connected():
        ethernet_login()
    else:
        connect_wifi()
        time.sleep(2)
        wifi_login()


if __name__ == "__main__":
    main()
