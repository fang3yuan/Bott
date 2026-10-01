# InstaAI-Bot

> AI-powered Instagram DM auto-responder using Google Gemini.

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-blue?style=flat-square)](https://ai.google.dev/)
[![Instagram](https://img.shields.io/badge/Platform-Instagram-E4405F?style=flat-square&logo=instagram)](https://www.instagram.com/)

---

## Overview

**InstaAI-Bot** is a lightweight Python bot that monitors Instagram private messages and generates automatic replies using **Google Gemini 2.5 Flash**.

It is designed to be simple, lightweight, and easy to configure.

## Features

- Google Gemini 2.5 Flash integration
- Automatic Instagram DM replies
- Private 1-to-1 conversation support
- Conversation context during runtime
- Random delay between replies
- Cookie-based authentication
- Error and activity logging
- Minimal dependencies

---

## Installation

### Clone the repository

```bash
git clone https://github.com/fang3yuan/InstaAI-Bot.git
cd InstaAI-Bot
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python insta.py
```

---

## Gemini API Key

The bot requires a Google Gemini API key.

Set your API key as an environment variable:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

Never commit your API key to the repository.

---

## Instagram Cookies

The bot uses Instagram session cookies for authentication.

The recommended browser extension for exporting cookies is:

**EditThisCookie (V3)**

[Chrome Web Store](https://chromewebstore.google.com/detail/editthiscookie-v3/ojfebgpkimhlhcblbalbfjblapadhbol)

### Setup

1. Log in to Instagram in your browser.
2. Open **EditThisCookie (V3)** while on `instagram.com`.
3. Export your cookies.
4. Save them as:

```text
cookies.json
```

5. Place the file next to `insta.py`.

```text
InstaAI-Bot/
├── insta.py
├── cookies.json
└── ...
```

---

## Important: cookies.json

The `cookies.json` included in this repository contains **dummy / expired cookie data** for demonstration purposes.

It is **not a real Instagram session** and cannot be used to log in.

Real Instagram cookies must **never** be published or shared publicly.

They may contain sensitive session credentials such as:

```text
sessionid
csrftoken
ds_user_id
```

Treat them as confidential credentials.

Add the following to `.gitignore`:

```gitignore
cookies.json
.env
bot_errors.log
__pycache__/
```

---

## How It Works

```text
Instagram
    │
    │  New DM
    ▼
InstaAI-Bot
    │
    │  Message
    ▼
Gemini 2.5 Flash
    │
    │  Generated reply
    ▼
Instagram
```

---

## Project Structure

```text
InstaAI-Bot/
│
├── insta.py
├── cookies.json
├── requirements.txt
├── runtime.txt
├── bot_errors.log
└── README.md
```

| File | Description |
|------|-------------|
| `insta.py` | Main bot implementation |
| `cookies.json` | Instagram cookies |
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Runtime configuration |
| `bot_errors.log` | Error log |
| `README.md` | Documentation |

---

## Notes

- The bot focuses on private text messages.
- Group conversations may be ignored.
- Replies include a delay between messages.
- Instagram's internal endpoints may change over time.
- Keep all session cookies and API keys private.
- Use the project responsibly and in accordance with the relevant platform policies.

---

## Disclaimer

This project is provided for educational and personal automation purposes.

You are responsible for the account, credentials, API keys, cookies, and usage of the software.

---

<div align="center">

**InstaAI-Bot**

`Instagram` · `Gemini` · `Python`

</div>
