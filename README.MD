------

# 🌟 **一、**Python 自动登录脚本

可以直接下载上传好的脚本也可以复制代码自己创建文件

**UPASS**这一项请按照以下操作（一步步照做）

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
  3. 找到**upass**这一项，右键复制值，这就是**UPASS**的数据

```python
import requests
import psutil
import time

# -----------------------------
# 你的校园网账号配置
# -----------------------------
STUDENT_ID = "你的学号"
UPASS = "加密后的密码"

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
        if ("Ethernet" in name or "以太网" in name) and stats.isup:
            return True
    return False

# -----------------------------
# 主流程：有网线 → 登录
# -----------------------------
def main():
    time.sleep(2)

    if is_ethernet_connected():
        try:
            requests.post(LOGIN_URL, data=POST_DATA, timeout=3)
        except:
            pass

if __name__ == "__main__":
    main()

```

------

# 📌 **二、把脚本打包成静默 exe（要先安装Python）**

在键盘上按WIN + R打开cmd先安装：

```bash
pip install pyinstaller
pip install psutil
```

接着在auto_login_silent.py所在文件夹按**Shift+右键**，选择在此处打开Powershell，然后输入：

```bash
pyinstaller -F --noconsole auto_login_once.py
```

生成文件在：

```
dist/auto_login_silent.exe
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
3. 把 `auto_login_silent.exe` 拖进去

即可开机自动静默运行。

------

# 💡 **四、说明**

1. ✔ 不弹窗、不显示控制台
2. ✔ 可直接放进开机启动项
3. ✔ 目前只适用于以太网连接状态的校园网自动登录

------

