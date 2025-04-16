# Made By Chen_yang_
# 加上功能填充与修补，这是第29个小版本
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import webbrowser
import time
import configparser


class BBDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BBDown 图形化界面")
        # 设置窗口默认最大化
        self.root.state('zoomed')
        self.root.minsize(600, 400)

        # 设置列和行的权重以实现自适应
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        for i in range(10):
            self.root.rowconfigure(i, weight=1)

        # 左侧输入区域
        self.left_frame = tk.Frame(root)
        self.left_frame.grid(row=0, column=0, rowspan=10, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)

        # 输入视频链接
        self.url_label = tk.Label(self.left_frame, text="视频链接:")
        self.url_label.pack(anchor=tk.W, padx=5, pady=2)
        self.url_entry = tk.Entry(self.left_frame, width=50)
        self.url_entry.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)

        # 登录模式选择
        self.login_frame = tk.Frame(self.left_frame)
        self.login_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.login_var = tk.StringVar()
        self.login_var.set("无")
        login_options = ["无", "网页账号登录", "电视账号登录"]
        self.login_label = tk.Label(self.login_frame, text="登录模式:")
        self.login_label.pack(side=tk.LEFT)
        self.login_combobox = ttk.Combobox(self.login_frame, textvariable=self.login_var, values=login_options)
        self.login_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 登录点击框
        self.login_button = tk.Button(self.login_frame, text="点击登录", command=self.start_login)
        self.login_button.pack(side=tk.LEFT, padx=5)

        # 解析模式选择
        self.api_frame = tk.Frame(self.left_frame)
        self.api_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.api_var = tk.StringVar()
        self.api_var.set("无")
        api_options = ["无", "TV 端解析模式", "APP 端解析模式", "国际版解析模式", "-intl, --use-intl-api"]
        self.api_label = tk.Label(self.api_frame, text="解析模式:")
        self.api_label.pack(side=tk.LEFT)
        self.api_combobox = ttk.Combobox(self.api_frame, textvariable=self.api_var, values=api_options)
        self.api_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 画质优先级下拉框
        self.dfn_priority_frame = tk.Frame(self.left_frame)
        self.dfn_priority_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.dfn_priority_label = tk.Label(self.dfn_priority_frame, text="画质优先级:")
        self.dfn_priority_label.pack(side=tk.LEFT)
        self.dfn_priority_var = tk.StringVar()
        b站画质选项 = ["默认"] + ["8K 超高清", "4K 超清", "1080P 高码率", "1080P 高清", "720P 高清", "480P 标清", "360P 流畅"]
        self.dfn_priority_combobox = ttk.Combobox(self.dfn_priority_frame, textvariable=self.dfn_priority_var,
                                                  values=b站画质选项)
        self.dfn_priority_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 视频编码优先级下拉框
        self.encoding_priority_frame = tk.Frame(self.left_frame)
        self.encoding_priority_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.encoding_priority_label = tk.Label(self.encoding_priority_frame, text="视频编码优先级:")
        self.encoding_priority_label.pack(side=tk.LEFT)
        self.encoding_priority_var = tk.StringVar()
        encoding_options = ["默认", "hevc,av1,avc", "avc,hevc,av1", "av1,avc,hevc"]
        self.encoding_priority_combobox = ttk.Combobox(self.encoding_priority_frame, textvariable=self.encoding_priority_var,
                                                       values=encoding_options)
        self.encoding_priority_combobox.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # 分 P 选择
        self.page_label = tk.Label(self.left_frame, text="选择指定分p或分p范围: (8 或 1,2 或 3-5 或 ALL 或 LAST 或 3,5,LATEST 均不带空格)")
        self.page_label.pack(anchor=tk.W, padx=5, pady=2)
        self.page_entry = tk.Entry(self.left_frame, width=50)
        self.page_entry.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)

        # 下载选项分类
        self.download_options_frame = tk.Frame(self.left_frame)
        self.download_options_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)

        # 下载类型选项和其他选项合并为两列布局
        option_labels = [
            "使用多线程下载", "仅下载视频", "仅下载音频", "仅下载弹幕", "仅下载字幕", "仅下载封面",
            "输出调试日志", "跳过混流步骤", "跳过字幕下载", "跳过封面下载", "强制使用 HTTP 协议", "下载弹幕",
            "视频升序(最小体积优先) --video-ascending",
            "音频升序(最小体积优先) --audio-ascending",
            "不替换PCDN域名 --allow-pcdn",
            "使用MP4Box来混流 --use-mp4box",
            "调用aria2c进行下载 -aria2, --use-aria2c",
            "--skip-ai 跳过AI字幕下载(默认开启)"
        ]
        self.option_vars = [tk.IntVar() for _ in range(len(option_labels))]
        self.option_vars[0].set(1)
        self.option_vars[10].set(1)
        self.option_vars[-1].set(1)  # 默认开启跳过AI字幕下载

        for i, label in enumerate(option_labels):
            col = i % 2
            row = i // 2
            checkbox = tk.Checkbutton(self.download_options_frame, text=label, variable=self.option_vars[i])
            checkbox.grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)

        # 按钮框架
        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(anchor=tk.S, padx=5, pady=2, fill=tk.X)

        # 解析视频按钮
        self.parse_button = tk.Button(self.button_frame, text="解析视频", command=self.parse_video)
        self.parse_button.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)

        # 下载按钮
        self.download_button = tk.Button(self.button_frame, text="下载", command=self.download_video, state="disabled")
        self.download_button.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.X, expand=True)

        # 备注信息
        self.note_label = tk.Label(self.left_frame, text="登陆之后才能下载高清视频或者VIP番剧，解析视频后再下可以看当前视频情况，如果下面不知道什么意思就别动", fg="red")
        self.note_label.pack(anchor=tk.W, padx=5, pady=2)

        # 配置文件参数编辑框
        self.config_frame = tk.Frame(self.left_frame)
        self.config_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)

        self.config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            # 自动识别 BBDown.exe 所在目录
            bbdown_path = os.path.abspath('BBDown.exe')
            work_dir = os.path.dirname(bbdown_path)
            self.config['Paths'] = {
                'work-dir': work_dir,
                'ffmpeg-path': '',
                'mp4box-path': '',
                'aria2c-path': ''
            }
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
        else:
            self.config.read('config.ini')

        self.work_dir_var = tk.StringVar()
        self.work_dir_var.set(self.config.get('Paths', 'work-dir', fallback=''))
        self.work_dir_label = tk.Label(self.config_frame, text="工作目录（大概是BBDown的路径，不太清楚):")
        self.work_dir_label.pack(anchor=tk.W, padx=5, pady=2)
        self.work_dir_entry = tk.Entry(self.config_frame, textvariable=self.work_dir_var, width=50)
        self.work_dir_entry.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.work_dir_entry.bind("<FocusOut>", self.save_config)

        self.ffmpeg_path_var = tk.StringVar()
        self.ffmpeg_path_var.set(self.config.get('Paths', 'ffmpeg-path', fallback=''))
        self.ffmpeg_path_label = tk.Label(self.config_frame, text="FFmpeg 路径:")
        self.ffmpeg_path_label.pack(anchor=tk.W, padx=5, pady=2)
        self.ffmpeg_path_entry = tk.Entry(self.config_frame, textvariable=self.ffmpeg_path_var, width=50)
        self.ffmpeg_path_entry.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.ffmpeg_path_entry.bind("<FocusOut>", self.save_config)

        self.mp4box_path_var = tk.StringVar()
        self.mp4box_path_var.set(self.config.get('Paths', 'mp4box-path', fallback=''))
        self.mp4box_path_label = tk.Label(self.config_frame, text="MP4Box 路径:")
        self.mp4box_path_label.pack(anchor=tk.W, padx=5, pady=2)
        self.mp4box_path_entry = tk.Entry(self.config_frame, textvariable=self.mp4box_path_var, width=50)
        self.mp4box_path_entry.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.mp4box_path_entry.bind("<FocusOut>", self.save_config)

        self.aria2c_path_var = tk.StringVar()
        self.aria2c_path_var.set(self.config.get('Paths', 'aria2c-path', fallback=''))
        self.aria2c_path_label = tk.Label(self.config_frame, text="Aria2c 路径:")
        self.aria2c_path_label.pack(anchor=tk.W, padx=5, pady=2)
        self.aria2c_path_entry = tk.Entry(self.config_frame, textvariable=self.aria2c_path_var, width=50)
        self.aria2c_path_entry.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)
        self.aria2c_path_entry.bind("<FocusOut>", self.save_config)

        # 右侧日志区域
        self.right_frame = tk.Frame(root)
        self.right_frame.grid(row=0, column=1, rowspan=10, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)

        # 日志框及滚动条
        self.log_frame = tk.Frame(self.right_frame)
        self.log_frame.pack(anchor=tk.W, padx=5, pady=2, fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(self.log_frame, height=10, width=40, font=("黑体", 10), fg="green")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.log_scrollbar.set)

        # 登录状态显示框
        self.login_status_text = tk.Text(self.right_frame, height=5, width=40, font=("黑体", 10), fg="blue")
        self.login_status_text.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)

        # 下载进度条
        self.progress_bar = ttk.Progressbar(self.right_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(anchor=tk.W, padx=5, pady=2, fill=tk.X)

        self.qr_code_file = "qrcode.png"
        self.login_refresh_thread = None
        self.login_refresh_stop_event = threading.Event()

        # 启动时读取 BBDown.data 文件
        self.read_bbdown_data()

    def read_bbdown_data(self):
        if os.path.exists("BBDown.data"):
            try:
                with open("BBDown.data", "r", encoding="utf-8") as f:
                    data = f.read()
                    dede_user_id = None
                    cookies = data.split(";")
                    for cookie in cookies:
                        if "DedeUserID=" in cookie:
                            dede_user_id = cookie.strip().split("=")[1]
                            break
                    if dede_user_id:
                        self.show_login_status(dede_user_id)
            except Exception as e:
                self.log_text.insert(tk.END, f"读取 BBDown.data 文件出错: {str(e)}\n")

    def start_login(self):
        login_mode = self.get_login_command(self.login_var.get())
        if not login_mode:
            messagebox.showerror("错误", "请选择有效的登录模式")
            return

        command = ["BBDown", login_mode]
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"执行命令: {' '.join(command)}\n")

        def run_login():
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                output = result.stdout + result.stderr
                self.log_text.insert(tk.END, output)

                if os.path.exists(self.qr_code_file):
                    webbrowser.open(self.qr_code_file)

                self.login_refresh_thread = threading.Thread(target=self.refresh_login_status)
                self.login_refresh_thread.start()

            except Exception as e:
                self.log_text.insert(tk.END, f"登录出错: {str(e)}")

        threading.Thread(target=run_login).start()

    def refresh_login_status(self):
        while not self.login_refresh_stop_event.is_set():
            if os.path.exists("BBDown.data"):
                try:
                    with open("BBDown.data", "r", encoding="utf-8") as f:
                        data = f.read()
                        dede_user_id = None
                        cookies = data.split(";")
                        for cookie in cookies:
                            if "DedeUserID=" in cookie:
                                dede_user_id = cookie.strip().split("=")[1]
                                break
                        if dede_user_id:
                            self.show_login_status(dede_user_id)
                        if dede_user_id:
                            self.login_refresh_stop_event.set()
                            if os.path.exists(self.qr_code_file):
                                os.remove(self.qr_code_file)
                except Exception as e:
                    self.log_text.insert(tk.END, f"读取 BBDown.data 文件出错: {str(e)}\n")
            time.sleep(2)

    def show_login_status(self, dede_user_id):
        self.login_status_text.delete(1.0, tk.END)
        self.login_status_text.insert(tk.END, f"登录用户UID：{dede_user_id}\n")
        link_text = f"主页：https://space.bilibili.com/{dede_user_id}"
        self.login_status_text.insert(tk.END, link_text)

    def parse_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("错误", "请输入视频链接")
            return

        command = ["BBDown", url, "--only-show-info"]

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"执行命令: {' '.join(command)}\n")

        def run_parse():
            try:
                result = subprocess.run(command, capture_output=True, text=True)
                output = result.stdout + result.stderr
                self.log_text.insert(tk.END, output)
                self.download_button['state'] = "normal"
            except Exception as e:
                self.log_text.insert(tk.END, f"解析出错: {str(e)}")

        threading.Thread(target=run_parse).start()

    def download_video(self):
        url = self.url_entry.get()
        api_mode = self.get_api_command(self.api_var.get())
        dfn_priority = self.dfn_priority_var.get()
        page_selection = self.page_entry.get()
        encoding_priority = self.encoding_priority_var.get()

        command = ["BBDown", url]
        if api_mode:
            command.append(self.get_api_command_line(api_mode))
        if dfn_priority and dfn_priority != "默认":
            command.extend(["-q", dfn_priority])
        if encoding_priority and encoding_priority != "默认":
            command.extend(["-e", encoding_priority])
        if page_selection:
            command.extend(["-p", page_selection])

        work_dir = self.work_dir_var.get()
        if work_dir:
            command.extend(["--work-dir", work_dir])
        ffmpeg_path = self.ffmpeg_path_var.get()
        if ffmpeg_path:
            command.extend(["--ffmpeg-path", ffmpeg_path])
        mp4box_path = self.mp4box_path_var.get()
        if mp4box_path:
            command.extend(["--mp4box-path", mp4box_path])
        aria2c_path = self.aria2c_path_var.get()
        if aria2c_path:
            command.extend(["--aria2c-path", aria2c_path])

        option_flags = [
            "--multi-thread", "--video-only", "--audio-only", "--danmaku-only", "--sub-only", "--cover-only",
            "--debug", "--skip-mux", "--skip-subtitle", "--skip-cover", "--force-http", "--download-danmaku",
            "--video-ascending", "--audio-ascending", "--allow-pcdn", "--use-mp4box", "-aria2",
            "--skip-ai"
        ]
        for i, var in enumerate(self.option_vars):
            if var.get():
                command.append(option_flags[i])

        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"执行命令: {' '.join(command)}\n")

        # 重置进度条
        self.progress_bar['value'] = 0

        def run_download():
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.log_text.insert(tk.END, output)
                        # 这里需要根据 BBDown 的输出格式来解析进度
                        # 假设 BBDown 输出包含类似 "Downloading: 50%" 的信息
                        if "Downloading: " in output:
                            try:
                                progress_str = output.split("Downloading: ")[1].split("%")[0]
                                progress = int(progress_str)
                                self.progress_bar['value'] = progress
                                self.root.update_idletasks()
                            except (IndexError, ValueError):
                                pass
                self.log_text.insert(tk.END, f"下载完成\n")
            except Exception as e:
                self.log_text.insert(tk.END, f"下载出错: {str(e)}")

        threading.Thread(target=run_download).start()

    def get_login_command(self, login_option):
        if login_option == "网页账号登录":
            return "login"
        elif login_option == "电视账号登录":
            return "logintv"
        return ""

    def get_api_command(self, api_option):
        if api_option == "TV 端解析模式":
            return "-tv"
        elif api_option == "APP 端解析模式":
            return "--use-app-api"
        elif api_option == "国际版解析模式" or api_option == "-intl, --use-intl-api":
            return "--use-intl-api"
        return ""

    def get_api_command_line(self, api_option):
        if api_option == "TV 端解析模式":
            return "-tv"
        elif api_option == "APP 端解析模式":
            return "--use-app-api"
        elif api_option == "国际版解析模式" or api_option == "-intl, --use-intl-api":
            return "--use-intl-api"
        return ""

    def save_config(self, event=None):
        self.config['Paths'] = {
            'work-dir': self.work_dir_var.get(),
            'ffmpeg-path': self.ffmpeg_path_var.get(),
            'mp4box-path': self.mp4box_path_var.get(),
            'aria2c-path': self.aria2c_path_var.get()
        }
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


if __name__ == "__main__":
    root = tk.Tk()
    app = BBDownGUI(root)
    root.mainloop()
    