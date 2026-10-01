<div align="center">

# 🤖 InstaAI-Bot

**An intelligent, lightweight Instagram DM auto-responder powered by Google's Gemini 2.5 Flash API.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-orange.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

*Seamlessly handle 1-on-1 Instagram conversations when you are away with natural, human-like AI responses.*

---

</div>

## 🌟 Highlights

* **🧠 Smart AI Conversations**: Powered by `gemini-2.5-flash` to craft short, friendly, and authentic replies without revealing it's an AI.
* **🛡️ Anti-Bot Protection**: Includes randomized human-like delays (**15–20 seconds**) between replies to prevent rate limits.
* **🔑 Auto Token Retrieval**: Dynamically extracts required `fb_dtsg` and `lsd` tokens for Instagram GraphQL endpoints.
* **🎯 1-on-1 Focus**: Filters for private text messages, safely ignoring group chats and media-only messages.
* **📊 Comprehensive Logging**: Real-time terminal timestamps and detailed error logging saved to `bot_errors.log`.

---

## 🛠️ Architecture Flow
