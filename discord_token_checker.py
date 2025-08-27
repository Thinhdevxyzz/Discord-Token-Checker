import os
import shutil
import time
import sys
import requests
import re
import json
import uuid
import random
import base64
import threading
import tls_client
from pystyle import Colorate, Colors
from colorama import init
from datetime import datetime
import platform

init()

class DiscordBot:
    def __init__(self):
        self.tokens = []

    def get_user_agent(self):
        windows_versions = ["10.0", "11.0"]
        windows_ver = random.choice(windows_versions)
        return f"Mozilla/5.0 (Windows NT {windows_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

    def log(self, status, message):
        if status == "SUCCESS":
            formatted_msg = f"[{Colorate.Horizontal(Colors.green_to_white, 'SUCCESS')}] {Colorate.Horizontal(Colors.green_to_white, message)}"
        elif status == "INFO":
            formatted_msg = Colorate.Horizontal(Colors.green_to_white, message)
        else:
            formatted_msg = f"[{status}] {message}"
            color_map = {
                "WAITING": Colors.red_to_yellow,
                "ERROR": Colors.blue_to_red,
                "LOCK": Colors.red_to_yellow,
                "VERIFY": Colors.yellow_to_red
            }
            formatted_msg = Colorate.Horizontal(color_map.get(status, Colors.white_to_red), formatted_msg)
        terminal_width = shutil.get_terminal_size().columns
        padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
        print(" " * padding + formatted_msg)

class DiscordChecker:
    def __init__(self, bot):
        self.bot = bot
        self.valid = 0
        self.invalid = 0
        self.locked = 0
        self.verified = 0
        self.proxy_errors = 0
        self.lock = threading.Lock()
        self.proxies = []
        self.used_proxies = set()
        self.banned_proxies = set()
        self.device_id = str(uuid.uuid4())
        self.rate_limit_delay = 3.0
        self.max_attempts = 5
        self.flaresolverr_url = None
        self.invalid_tokens = []
        self.locked_tokens = []
        self.verified_tokens = []
        self.valid_tokens = []
        
    def load_proxies(self):
        try:
            with open("input/proxies.txt", 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
                return self.validate_proxies(proxies)
        except:
            return []

    def validate_proxies(self, proxies):
        valid_proxies = []
        for proxy in proxies:
            formatted_proxy = self.format_proxy(proxy)
            if not formatted_proxy or proxy in self.banned_proxies:
                continue
            try:
                session = tls_client.Session(client_identifier="chrome_128", random_tls_extension_order=True)
                session.proxies = formatted_proxy
                start_time = time.time()
                response = session.get("https://discord.com", timeout=4)
                latency = time.time() - start_time
                if response.status_code == 200 and latency < 1.5:
                    valid_proxies.append(proxy)
            except:
                continue
        return valid_proxies

    def format_proxy(self, proxy):
        if not proxy:
            return None
        try:
            if '@' in proxy:
                auth, proxy = proxy.split('@')
                username, password = auth.split(':')
                host, port = proxy.split(':')
                return {
                    "http": f"http://{username}:{password}@{host}:{port}",
                    "https": f"http://{username}:{password}@{host}:{port}"
                }
            else:
                host, port = proxy.split(':')
                return {
                    "http": f"http://{host}:{port}",
                    "https": f"http://{host}:{port}"
                }
        except:
            return None

    def get_unused_proxy(self):
        available_proxies = [p for p in self.proxies if p not in self.used_proxies and p not in self.banned_proxies]
        if not available_proxies:
            self.used_proxies.clear()
            available_proxies = [p for p in self.proxies if p not in self.banned_proxies]
        if available_proxies:
            proxy = random.choice(available_proxies)
            self.used_proxies.add(proxy)
            return proxy
        return None

    def save_invalid_tokens(self):
        if self.invalid_tokens:
            os.makedirs("data", exist_ok=True)
            with open("data/invalid_tokens.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(self.invalid_tokens) + "\n")

    def save_locked_tokens(self):
        if self.locked_tokens:
            os.makedirs("data", exist_ok=True)
            with open("data/locked_tokens.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(self.locked_tokens) + "\n")

    def save_verified_tokens(self):
        if self.verified_tokens:
            os.makedirs("data", exist_ok=True)
            with open("data/verified_tokens.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(self.verified_tokens) + "\n")

    def save_valid_tokens(self):
        if self.valid_tokens:
            os.makedirs("data", exist_ok=True)
            with open("data/valid_tokens.txt", "a", encoding="utf-8") as f:
                f.write("\n".join(self.valid_tokens) + "\n")

    def generate_x_super_properties(self):
        windows_versions = ["10.0", "11.0"]
        windows_ver = random.choice(windows_versions)
        user_agent = f"Mozilla/5.0 (Windows NT {windows_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        properties = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": random.choice(["en-US", "en-GB", "vi-VN"]),
            "client_version": "128.0.0.0",
            "client_build_number": str(random.randint(180000, 190000)),
            "native_build_number": "182",
            "client_event_source": None,
            "device_vendor_id": self.device_id,
            "browser_channel_type": "stable",
            "browser_name": "Chrome",
            "browser_version": "128.0.0.0",
            "os_version": windows_ver,
            "referring_domain": "discord.com",
            "referrer": "https://discord.com/",
            "ref_err": None,
            "release_channel": "stable",
            "client_event_source": None,
            "design_id": 0,
            "browser_user_agent": user_agent,
            "screen_width": random.choice([1920, 1366, 1440, 1600]),
            "screen_height": random.choice([1080, 768, 900, 1050]),
            "timezone_offset": -420,
            "is_webkit": False,
            "webgl_vendor": "Google Inc.",
            "webgl_renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0)",
            "cpu_core_count": 8,
            "memory_total": 16384,
            "browser_base_version": "128"
        }
        return base64.b64encode(json.dumps(properties, separators=(',', ':')).encode()).decode()

    def simulate_user_behavior(self, session, proxy=None):
        try:
            windows_versions = ["10.0", "11.0"]
            windows_ver = random.choice(windows_versions)
            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "vi-VN,vi;q=0.9"]),
                "User-Agent": self.bot.get_user_agent(),
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "Sec-CH-UA": f'"Chromium";v="128", "Not A(Brand";v="99", "Google Chrome";v="128"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
                "Sec-CH-UA-Platform-Version": windows_ver,
                "Connection": "keep-alive",
                "Priority": "u=0, i"
            }
            if proxy:
                formatted_proxy = self.format_proxy(proxy)
                if formatted_proxy:
                    session.proxies = formatted_proxy
            session.get("https://discord.com", headers=headers)
            time.sleep(random.uniform(3.0, 6.0))
            session.get("https://discord.com/login", headers=headers)
            time.sleep(random.uniform(2.0, 4.0))
            session.get("https://discord.com/api/v10/users/@me", headers=headers)
            time.sleep(random.uniform(1.5, 3.5))
            session.get("https://discord.com/api/v10/experiments", headers=headers)
            time.sleep(random.uniform(1.0, 3.0))
            session.get("https://discord.com/channels/@me", headers=headers)
            time.sleep(random.uniform(1.5, 4.0))
            session.get("https://discord.com/api/v10/auth/location-metadata", headers=headers)
            time.sleep(random.uniform(1.0, 3.0))
            session.get("https://discord.com/api/v10/users/@me/settings", headers=headers)
        except:
            pass

    def get_fingerprint(self, session, proxy=None):
        try:
            windows_versions = ["10.0", "11.0"]
            windows_ver = random.choice(windows_versions)
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "vi-VN,vi;q=0.9"]),
                "User-Agent": self.bot.get_user_agent(),
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-CH-UA": f'"Chromium";v="128", "Not A(Brand";v="99", "Google Chrome";v="128"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
                "Sec-CH-UA-Platform-Version": windows_ver,
                "X-Discord-Locale": "en-US",
                "X-Discord-Timezone": random.choice(["America/New_York", "Asia/Ho_Chi_Minh"]),
                "Connection": "keep-alive"
            }
            if proxy:
                formatted_proxy = self.format_proxy(proxy)
                if formatted_proxy:
                    session.proxies = formatted_proxy
            response = session.get("https://discord.com/api/v10/experiments", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "fingerprint" in data:
                    return data["fingerprint"]
            return None
        except Exception:
            return None

    def get_user_id(self, token, session, proxy=None):
        try:
            x_super_properties = self.generate_x_super_properties()
            user_agent = self.bot.get_user_agent()
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "vi-VN,vi;q=0.9"]),
                "Authorization": token,
                "User-Agent": user_agent,
                "X-Super-Properties": x_super_properties,
                "Origin": "https://discord.com",
                "Referer": "https://discord.com/channels/@me",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-CH-UA": f'"Chromium";v="128", "Not A(Brand";v="99", "Google Chrome";v="128"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
                "Sec-CH-UA-Platform-Version": user_agent.split("Windows NT ")[1].split(";")[0],
                "Connection": "keep-alive"
            }
            fingerprint = self.get_fingerprint(session, proxy)
            if fingerprint:
                headers["X-Fingerprint"] = fingerprint
            response = session.get("https://discord.com/api/v10/users/@me", headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get("id", "Không có")
            else:
                self.bot.log("ERROR", f"[DEBUG] Lỗi lấy ID: HTTP {response.status_code}, {response.text}")
                return "Không có"
        except Exception as e:
            self.bot.log("ERROR", f"[DEBUG] Lỗi lấy ID: {str(e)}")
            return "Không có"

    def check_token(self, token, session=None, proxy=None):
        if not session:
            session = tls_client.Session(
                client_identifier="chrome_128",
                random_tls_extension_order=True,
                ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0"
            )
        if proxy:
            formatted_proxy = self.format_proxy(proxy)
            if formatted_proxy:
                session.proxies = formatted_proxy
        x_super_properties = self.generate_x_super_properties()
        user_agent = self.bot.get_user_agent()
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "vi-VN,vi;q=0.9"]),
            "Authorization": token,
            "User-Agent": user_agent,
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": random.choice(["America/New_York", "Asia/Ho_Chi_Minh"]),
            "X-Super-Properties": x_super_properties,
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-CH-UA": f'"Chromium";v="128", "Not A(Brand";v="99", "Google Chrome";v="128"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-CH-UA-Platform-Version": user_agent.split("Windows NT ")[1].split(";")[0],
            "Connection": "keep-alive",
            "Priority": "u=1, i",
            "TE": "trailers"
        }
        fingerprint = self.get_fingerprint(session, proxy)
        if fingerprint:
            headers["X-Fingerprint"] = fingerprint
        try:
            response = session.get("https://discord.com/api/v10/users/@me", headers=headers)
            return response, None, session
        except Exception as e:
            return None, str(e), session

    def check_thread(self, tokens, thread_id):
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            attempt_count = 0
            while attempt_count < self.max_attempts:
                proxy = self.get_unused_proxy()
                session = None
                response, error, session = self.check_token(token, session, proxy)
                terminal_width = shutil.get_terminal_size().columns
                proxy_info = f"Proxy: {proxy}" if proxy else "No proxy"
                token_short = token[:8] + "..." if len(token) > 8 else token
                if response:
                    if response.status_code == 200:
                        user_id = self.get_user_id(token, session, proxy)
                        with self.lock:
                            self.valid += 1
                            self.valid_tokens.append(token)
                        formatted_msg = Colorate.Horizontal(Colors.green_to_white, f"[SUCCESS] Hợp lệ | Token: {token_short} | ID: {user_id} | {proxy_info}")
                        padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
                        print(" " * padding + formatted_msg)
                        break
                    elif response.status_code == 401:
                        with self.lock:
                            self.invalid += 1
                            self.invalid_tokens.append(token)
                        error_msg = json.loads(response.text).get("message", "Unauthorized")
                        formatted_msg = Colorate.Horizontal(Colors.red_to_yellow, f"[ERROR] Không hợp lệ | Token: {token_short} | Lỗi: {error_msg} | {proxy_info}")
                        padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
                        print(" " * padding + formatted_msg)
                        break
                    elif response.status_code == 403:
                        error_msg = json.loads(response.text).get("message", "Forbidden")
                        if "verify" in error_msg.lower():
                            with self.lock:
                                self.verified += 1
                                self.verified_tokens.append(token)
                            formatted_msg = Colorate.Horizontal(Colors.yellow_to_red, f"[VERIFY] Yêu cầu xác minh | Token: {token_short} | Lỗi: {error_msg} | {proxy_info}")
                        else:
                            with self.lock:
                                self.locked += 1
                                self.locked_tokens.append(token)
                            formatted_msg = Colorate.Horizontal(Colors.red_to_yellow, f"[LOCK] Bị khóa | Token: {token_short} | Lỗi: {error_msg} | {proxy_info}")
                        padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
                        print(" " * padding + formatted_msg)
                        break
                    elif response.status_code == 429:
                        with self.lock:
                            self.proxy_errors += 1
                        retry_after = json.loads(response.text).get("retry_after", 5)
                        formatted_msg = Colorate.Horizontal(Colors.red_to_yellow, f"[ERROR] Giới hạn tốc độ | Token: {token_short} | Chờ: {retry_after}s | {proxy_info}")
                        padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
                        print(" " * padding + formatted_msg)
                        if proxy:
                            self.banned_proxies.add(proxy)
                        time.sleep(retry_after + random.uniform(1.0, 3.0))
                        self.rate_limit_delay = min(self.rate_limit_delay * 1.5, 15.0)
                        attempt_count += 1
                    else:
                        with self.lock:
                            self.invalid += 1
                            self.invalid_tokens.append(token)
                        error_msg = json.loads(response.text).get("message", f"HTTP {response.status_code}")
                        formatted_msg = Colorate.Horizontal(Colors.red_to_yellow, f"[ERROR] Không hợp lệ | Token: {token_short} | Lỗi: {error_msg} | {proxy_info}")
                        padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
                        print(" " * padding + formatted_msg)
                        break
                else:
                    with self.lock:
                        self.proxy_errors += 1
                    formatted_msg = Colorate.Horizontal(Colors.red_to_yellow, f"[ERROR] Lỗi proxy | Token: {token_short} | Lỗi: {error} | {proxy_info}")
                    padding = (terminal_width - len(strip_ansi_codes(formatted_msg))) // 2
                    print(" " * padding + formatted_msg)
                    if proxy:
                        self.banned_proxies.add(proxy)
                    attempt_count += 1
                time.sleep(random.uniform(self.rate_limit_delay, self.rate_limit_delay + 4.0))

    def start(self, delay):
        try:
            tokens = []
            try:
                with open("input/tokens.txt", 'r', encoding='utf-8') as f:
                    tokens = f.read().splitlines()
            except FileNotFoundError:
                self.bot.log("WAITING", "File input/tokens.txt không tồn tại!")
                return
            self.proxies = self.load_proxies()
            if not tokens:
                self.bot.log("WAITING", "Không tìm thấy token nào trong input/tokens.txt!")
                return
            print_ascii_art()
            time.sleep(1.0)
            chunks = [tokens[i:i+5] for i in range(0, len(tokens), 5)]
            threads = []
            for i, chunk in enumerate(chunks):
                thread = threading.Thread(target=self.check_thread, args=(chunk, i))
                threads.append(thread)
                thread.start()
                if i < len(chunks) - 1:
                    time.sleep(float(delay) + random.uniform(0.2, 0.7))
            for thread in threads:
                thread.join()
            self.save_invalid_tokens()
            self.save_locked_tokens()
            self.save_verified_tokens()
            self.save_valid_tokens()
            self.bot.log("INFO", f"Kiểm tra thành công: {self.valid} | Không hợp lệ: {self.invalid} | Bị khóa: {self.locked} | Yêu cầu xác minh: {self.verified}")
            if self.invalid_tokens:
                self.bot.log("INFO", f"Số token không hợp lệ: {len(self.invalid_tokens)} (Đã lưu vào data/invalid_tokens.txt)")
            if self.locked_tokens:
                self.bot.log("INFO", f"Số token bị khóa: {len(self.locked_tokens)} (Đã lưu vào data/locked_tokens.txt)")
            if self.verified_tokens:
                self.bot.log("INFO", f"Số token yêu cầu xác minh: {len(self.verified_tokens)} (Đã lưu vào data/verified_tokens.txt)")
            if self.valid_tokens:
                self.bot.log("INFO", f"Số token hợp lệ: {len(self.valid_tokens)} (Đã lưu vào data/valid_tokens.txt)")
        except Exception as e:
            self.bot.log("WAITING", f"Lỗi: {str(e)}")

def strip_ansi_codes(text):
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_art():
    clear_screen()
    ascii_art = """
$$\   $$\  $$$$$$\  $$\    $$\  $$$$$$\  
$$$\  $$ |$$  __$$\ $$ |   $$ |$$  __$$\ 
$$$$\ $$ |$$ /  $$ |$$ |   $$ |$$ /  $$ |
$$ $$\$$ |$$ |  $$ |\$$\  $$  |$$$$$$$$ |
$$ \$$$$ |$$ |  $$ | \$$\$$  / $$  __$$ |
$$ |\$$$ |$$ |  $$ |  \$$$  /  $$ |  $$ |
$$ | \$$ | $$$$$$  |   \$  /   $$ |  $$ |
\__|  \__| \______/     \_/    \__|  \__|
    """.strip().split('\n')
    terminal_width = shutil.get_terminal_size().columns
    for line in ascii_art:
        padding = (terminal_width - len(strip_ansi_codes(line))) // 2
        print(Colorate.Horizontal(Colors.white_to_red, " " * padding + line))
        sys.stdout.flush()
        time.sleep(0.03)
    print()

def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
    except Exception:
        return []

def count_lines(file_path):
    return len(read_file(file_path))

def checker(bot):
    checker = DiscordChecker(bot)
    checker.start("0.7")
    input(Colorate.Horizontal(Colors.white_to_red, "Nhấn Enter để quay lại menu chính..."))

def print_menu():
    token_count = count_lines("input/tokens.txt")
    proxy_count = count_lines("input/proxies.txt")
    nova_logo = """
$$\   $$\  $$$$$$\  $$\    $$\  $$$$$$\  
$$$\  $$ |$$  __$$\ $$ |   $$ |$$  __$$\ 
$$$$\ $$ |$$ /  $$ |$$ |   $$ |$$ /  $$ |
$$ $$\$$ |$$ |  $$ |\$$\  $$  |$$$$$$$$ |
$$ \$$$$ |$$ |  $$ | \$$\$$  / $$  __$$ |
$$ |\$$$ |$$ |  $$ |  \$$$  /  $$ |  $$ |
$$ | \$$ | $$$$$$  |   \$  /   $$ |  $$ |
\__|  \__| \______/     \_/    \__|  \__|
    """.strip().splitlines()
    if platform.system() == "Windows":
        from ctypes import windll
        windll.kernel32.SetConsoleTitleW(f"Loaded: {token_count} tokens | {proxy_count} proxies")
    clear_screen()
    terminal_width = shutil.get_terminal_size().columns
    banner = "Developer ThinhDev | Discord.gg/anhemnova"
    for line in nova_logo:
        print(Colorate.Horizontal(Colors.white_to_red, line.center(terminal_width)))
    print(Colorate.Horizontal(Colors.white_to_red, banner.center(terminal_width)))
    menu_items = [("01", "Checker")]
    prefix_width = 5
    max_name_length = max(len(name) for _, name in menu_items)
    column_width = prefix_width + max_name_length + 2
    items_per_row = 1
    if terminal_width < column_width * items_per_row:
        bot = DiscordBot()
        return
    row_lines = []
    for row in range(0, len(menu_items), items_per_row):
        row_items = menu_items[row:row + items_per_row]
        row_line = ""
        for number, name in row_items:
            colored_number = Colorate.Horizontal(Colors.white_to_red, f"{number}")
            formatted_prefix = f"{colored_number} : ".ljust(prefix_width)
            colored_name = Colorate.Horizontal(Colors.white_to_red, name.ljust(max_name_length))
            row_line += f"{formatted_prefix}{colored_name}".ljust(column_width)
        if len(row_items) < items_per_row:
            row_line += " " * (column_width * (items_per_row - len(row_items)))
        row_lines.append(row_line.rstrip())
    max_row_length = max(len(strip_ansi_codes(row_line)) for row_line in row_lines)
    padding = (terminal_width - max_row_length) // 2
    print()
    for row_line in row_lines:
        print(" " * padding + row_line)
    print(f"\n{Colorate.Horizontal(Colors.white_to_red, 'nova~menu~> Lựa chọn ~> ')}", end="")

def run_application():
    bot = DiscordBot()
    try:
        while True:
            print_menu()
            choice = input(Colorate.Horizontal(Colors.white_to_red, "")).strip()
            if choice == "0":
                bot.log("INFO", "Đang thoát...")
                break
            elif choice in ["1", "01"]:
                checker(bot)
            else:
                bot.log("WAITING", "Lựa chọn không hợp lệ! Vui lòng chọn 01 cho Checker hoặc 0 để thoát.")
    except KeyboardInterrupt:
        bot.log("INFO", "Ứng dụng bị gián đoạn bởi người dùng.")
    except Exception as e:
        bot.log("ERROR", f"Đã xảy ra lỗi: {str(e)}")
        input(Colorate.Horizontal(Colors.white_to_red, "Nhấn Enter để thoát..."))

run_application()