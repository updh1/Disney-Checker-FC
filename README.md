# Disney+ Account Checker

Multi-threaded Disney+ account checker with proxy support, multiple auth flows, and Telegram notifications.

> ⚠️ **Disclaimer:** For educational and research purposes only. Use at your own risk. Using this tool against accounts you do not own is illegal and violates Disney's Terms of Service.

---

## ✨ Features

- 🔐 Multiple auth flows (Web, Android, iOS REST)
- 🌍 Proxy support (HTTP/SOCKS) with rotation
- ⚡ Multi-threaded checking
- 📊 Live progress (HIT / FREE / BAD / RETRY, CPM, timer)
- 📁 Saves hits and free accounts to `output/`
- 📲 Optional Telegram bot notifications
- 🏳️ Country detection with flag emoji
- 📋 Detailed metadata (subscription, expiry, profiles, features)

---

## 🚀 Installation

Requires Python 3.9+.

```bash
pip install curl-cffi requests
```
## 🛠️ Usage
Clone the repo:

```bash
git clone https://github.com/yourname/disney-checker.git
cd disney-checker
```
## Prepare combos.txt (one per line):

```bash
user@example.com:password123
Prepare proxies.txt (optional):
```
```bash
http://user:pass@host:port
socks5://host:port
host:port
host:port:user:pass
```
## Run:
```bash
python disney_checker.py
Follow the prompts (combo path, proxy path, threads, Telegram token/chat ID).
```
## 📂 Output
Saved to output/ with timestamp:

```bash
File	Contents
disney_hits_<HHMMSS>.txt	Valid subscriptions
disney_free_<HHMMSS>.txt	Valid accounts without subscription
Format:
```
```bash
Capture
email:password | Country:US 🇺🇸 | Sub:Disney+ Premium | Expire:2025-08-14 | Profiles:Main,Kids
```
## 📲 Telegram Setup (Optional)
```bash
Create a bot via @BotFather → copy token.
Get your chat ID via @userinfobot.
Paste both when prompted.
Hits are sent as messages, and the final hits file is sent as a document.
```
