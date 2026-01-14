# l7net
cool tool
- Customizable color schemes
- Real-time performance metrics
- 14 test methods
- Rotating user agents
- 4 performance tiers
<img width="392" height="479" alt="Screenshot 2026-01-13 5 10 14 PM" src="https://github.com/user-attachments/assets/98a1d61e-2c49-4dd3-93ac-c4b1cf1f9bad" />

## Install

### Linux / macOS
```bash
git clone https://github.com/yourusername/perf-tester.git && cd perf-tester && pip3 install aiohttp && python3 l7net.py
```

### Termux
```bash
pkg install python git && git clone https://github.com/yourusername/perf-tester.git && cd perf-tester && pip install aiohttp && python l7net.py
```

### iSH Shell
```bash
apk add python3 py3-pip git && git clone https://github.com/yourusername/perf-tester.git && cd perf-tester && pip3 install aiohttp && python3 l7net.py
```

### Windows
```powershell
git clone https://github.com/yourusername/perf-tester.git; cd perf-tester; pip install aiohttp; python l7net.py
```

## Requirements

- Python 3.7+
- aiohttp

## Test Methods

| Method | Description | Plans |
|--------|-------------|-------|
| HTTP GET | Standard HTTP GET requests | All |
| HTTPS GET | Secure HTTPS GET requests | All |
| HTTP POST | HTTP POST with JSON data | Hard+ |
| HTTPS POST | Secure POST requests | Hard+ |
| RAPID FIRE | Fast requests, minimal delay | Hard+ |
| STRESS TEST | 2 requests per cycle | Hard+ |
| CURL | cURL-style requests | Pro+ |
| GET/POST MIX | Random GET/POST alternation | Pro+ |
| BURST MODE | 3 rapid requests per cycle | Pro+ |
| CONCURRENT FLOOD | 2 mixed requests per cycle | Pro+ |
| CUSTOM HEADERS | Custom header injection | VIP |
| BULK REQUEST | Batch request processing | VIP |
| SOCKET PRESSURE | 4 requests per cycle | VIP |
| AMPLIFIED LOAD | 5 requests per cycle (MAX) | VIP |

## Plans

| Plan | Workers | Duration |
|------|---------|----------|
| FREE | 50 | 10s |
| HARD | 250 | 20s |
| PRO | 1000 | 45s |
| VIP | 5000 | 90s |

## Metrics

- Requests: Total successful requests
- Errors: Failed request count
- RPS: Requests per second
- Avg Latency: Average response time in ms
- Status Codes: HTTP response distribution

## Contact

TikTok: @sql1337
