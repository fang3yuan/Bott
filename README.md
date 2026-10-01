# InstaAI-Bot

<div align="center">

**AI-powered Instagram DM auto-responder using Google Gemini**

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![Instagram](https://img.shields.io/badge/Instagram-Automation-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/)

</div>

---

## Overview

A lightweight Python bot that monitors **Instagram DMs**, generates replies with **Google Gemini**, and maintains conversation context during runtime.

```text
Instagram DM
     │
     ▼
Message Filter
     │
     ▼
Conversation Context
     │
     ▼
Google Gemini
     │
     ▼
Automatic Reply
```

---

## Features

| Feature | Description |
|---|---|
| Gemini AI | Automatic AI-generated replies |
| DM Automation | Monitors unread private messages |
| Context | Maintains runtime conversation history |
| Fallback | Automatically tries another Gemini model |
| Authentication | Instagram cookie-based sessions |
| Filtering | Ignores unsupported / duplicate messages |
| Timing | Randomized delay between replies |
| Logging | Error logging to `bot_errors.log` |

---

## Setup

```bash
git clone https://github.com/fang3yuan/InstaAI-Bot.git
cd InstaAI-Bot
pip install -r requirements.txt
python insta.py
```

### Gemini

Set your API key:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Windows:

```cmd
set GEMINI_API_KEY=YOUR_API_KEY
```

---

## Instagram Session

Export your Instagram cookies using **EditThisCookie (V3)** and save them as:

```text
cookies.json
```

```text
InstaAI-Bot/
├── insta.py
├── cookies.json
├── requirements.txt
├── runtime.txt
└── README.md
```

> Never publish real Instagram cookies or API keys.

---

## Configuration

Customize the assistant behavior through:

```python
self.system_instruction
```

This controls the AI's tone, personality, and response behavior.

---

## Runtime

```text
Unread DM
   │
   ├── Invalid → Ignore
   │
   └── Valid
        │
        ▼
     Gemini
        │
        ▼
      Reply
        │
        ▼
 Randomized Delay
```

Conversation context exists only while the bot is running.

---

## Security

Add sensitive files to `.gitignore`:

```gitignore
cookies.json
.env
bot_errors.log
__pycache__/
```

Treat `cookies.json` as a session credential.

---

## Notes

- Python **3.11+**
- Private 1-to-1 text conversations
- Duplicate messages are ignored
- Instagram internal endpoints may change
- Requires valid Instagram session cookies
- Requires a Google Gemini API key

---

## Disclaimer

For educational and personal automation purposes.

Use only with accounts and credentials you are authorized to access. Follow the applicable Instagram and Google Gemini policies.

---

<div align="center">

`Instagram` · `Gemini` · `Python`

**InstaAI-Bot**

</div>
