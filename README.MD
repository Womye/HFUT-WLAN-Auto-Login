1. **自动判断是否插网线**
2. **插网线 → 调用你之前用的 Drcom 登录脚本**
3. **未插网线 → 自动连接 hfut-wlan + 自动提交认证（模拟浏览器登录）**
4. **静默运行（无黑框）**
5. **开机自启动设置方法（一步到位）**

------

# 🌟 **一、**完整 Python 自动登录脚本（网线 + WiFi 全自动）

可以直接下载上传好的脚本也可以复制代码自己创建文件

PASSWORD_MD5这一项请按照以下操作（一步步照做）

## ▲ 1. 打开 http://172.18.3.3

浏览器直接访问你的校园网认证界面。

## ▲ 2. 按 F12 → Network(网络)

清空一下列表。

## ▲ 3. 输入学号 + 密码 → 点击登录

然后观察 Network 中有**红色/绿色/POST/GET 请求**出现。

## ▲ 4. 找到真正的登录请求（非常关键）

- ### 在 Network 中点击 `0.htm` 之后

  上方有几个标签：

  - 标头（Headers）
  - **载荷 / Payload（或 Form Data）**
  - 预览（Preview）
  - 响应（Response）
  - 启动器（Initiator）
  - 时间（Timing）

  👉 **真正的账号密码参数在 Payload 里。** 

  1. 在 Network 中点选 **0.htm**
  2. 在右边的面板点开 **载荷（Payload）**
     - 有的浏览器叫 **Form Data**
     - 有的叫 **Request Payload**
  3. 找到**upass**这一项，右键复制值，这就是PASSWORD_MD5的数据

```python
import subprocess
import requests
import time
import os
import sys
import ctypes

# =========== 你的登录信息（修改这里） ==========
USERNAME = "你的学号"
PASSWORD_MD5 = "控制台中已加密的密码"
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
```

------

# 📌 **二、把脚本打包成静默 exe（要先安装Python）**

在键盘上按WIN + R打开cmd先安装：

```bash
pip install pyinstaller
```

接着在auto_hfut_login.py所在文件夹按**Shift+右键**，选择在此处打开Powershell，然后输入：

```bash
pyinstaller --noconsole --onefile auto_hfut_login.py
```

生成文件在：

```
dist/auto_hfut_login.exe
```

这是你要放进自启动的文件。

------

# 📌 **三、开机自动启动（最稳定方法）**

把生成的 exe 复制到：

```
C:\Users\你的用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

或在“shell:startup”里放进去：

1. Win + R
2. 输入：`shell:startup`
3. 把 `auto_hfut_login.exe` 拖进去

即可开机自动静默运行。

------

# 💡 **四、说明**

✔ 自动判断是否插有线网
 ✔ 若有 → Drcom 登录
 ✔ 若无 → 自动连接 hfut-wlan + 自动认证
 ✔ 不弹窗、不显示控制台
 ✔ 不需要判断掉线
 ✔ 可直接放进开机启动项

------

