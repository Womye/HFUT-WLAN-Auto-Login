import requests
import psutil
import time

# -----------------------------
# 你的校园网账号配置
# -----------------------------
STUDENT_ID = "2024217299"
UPASS = "be0fcda56aa7065b2e1307eca9b09cbb123456782"

LOGIN_URL = "http://172.18.3.3/0.htm"

POST_DATA = {
    "DDDDD": STUDENT_ID,
    "upass": UPASS,
    "R1": "0",
    "R2": "1",
    "para": "00",
    "0MKKey": "123456",
    "v6ip": ""
}

# -----------------------------
# 检测以太网是否连接
# -----------------------------
def is_ethernet_connected():
    interfaces = psutil.net_if_stats()
    for name, stats in interfaces.items():
        # Windows 以太网适配器名称一般含 "Ethernet" 或 "以太网"
        if ("Ethernet" in name or "以太网" in name) and stats.isup:
            return True
    return False

# -----------------------------
# 主流程：有网线 → 登录
# -----------------------------
def main():
    # 轻微等待，确保系统网络状态已加载
    time.sleep(2)

    if is_ethernet_connected():
        try:
            requests.post(LOGIN_URL, data=POST_DATA, timeout=3)
        except:
            pass

if __name__ == "__main__":
    main()
