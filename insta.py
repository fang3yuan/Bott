import json
import os
import random
import re
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests


class InstagramBot:
    BASE = "https://www.instagram.com/api/v1"

    def __init__(self, cookies_file: str = "cookies.json"):
        self.cookies_file = cookies_file
        self.session = requests.Session()
        self.user_id: Optional[str] = None
        self.csrftoken: Optional[str] = None
        self.session_id: Optional[str] = None
        self.is_running = False
        self._fb_dtsg: Optional[str] = None
        self._lsd: Optional[str] = None

    def log_action(self, message: str):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

    def log_error(self, error: str):
        line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {error}"
        print(line)

        try:
            with open("bot_errors.log", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

    def _extract_cookies(self, raw_data: Any) -> Dict[str, str]:
        cookies: Dict[str, str] = {}

        if isinstance(raw_data, dict):
            for key, value in raw_data.items():
                if isinstance(value, (str, int, float, bool)):
                    cookies[str(key)] = str(value)

        elif isinstance(raw_data, list):
            for item in raw_data:
                if isinstance(item, dict):
                    name = item.get("name")
                    value = item.get("value")

                    if name is not None and value is not None:
                        cookies[str(name)] = str(value)

        return cookies

    def login(self) -> bool:
        if not os.path.exists(self.cookies_file):
            self.log_error(f"Cookies file not found: {self.cookies_file}")
            return False

        try:
            with open(self.cookies_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)

        except Exception as e:
            self.log_error(f"Failed to read cookies file: {e}")
            return False

        cookies = self._extract_cookies(raw_data)

        session_id = cookies.get("sessionid", "").strip()
        ds_user_id = cookies.get("ds_user_id", "").strip()
        csrftoken = cookies.get("csrftoken", "").strip()
        mid = cookies.get("mid", "").strip()
        ig_did = cookies.get("ig_did", "").strip()
        datr = cookies.get("datr", "").strip()
        ps_l = cookies.get("ps_l", "1").strip()
        ps_n = cookies.get("ps_n", "1").strip()
        oo = cookies.get("oo", "v1").strip()
        dpr_cookie = cookies.get("dpr", "3").strip()
        wd = cookies.get("wd", "360x728").strip()
        rur = cookies.get("rur", "").strip()

        if not session_id or not csrftoken:
            self.log_error(
                "Cookies file must contain at least sessionid and csrftoken"
            )
            return False

        self.session.cookies.clear()

        for name, value in cookies.items():
            self.session.cookies.set(name, value)

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 10; K) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/139.0.0.0 Mobile Safari/537.36"
            ),
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/apng,*/*;q=0.8,"
                "application/signed-exchange;v=b3;q=0.7"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "https://www.instagram.com/direct/inbox/",
            "Origin": "https://www.instagram.com",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "sec-ch-ua": (
                '"Chromium";v="139", '
                '"Not;A=Brand";v="99"'
            ),
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-ch-ua-platform-version": '"12.0.0"',
            "sec-ch-ua-model": '"TECNO CH6n"',
            "sec-ch-ua-full-version-list": (
                '"Chromium";v="139.0.7339.0", '
                '"Not;A=Brand";v="99.0.0.0"'
            ),
            "sec-ch-prefers-color-scheme": "light",
            "dpr": "3",
            "viewport-width": "980",
            "X-CSRFToken": csrftoken,
            "X-IG-App-ID": "936619743392459",
            "X-Requested-With": "XMLHttpRequest",
        })

        self.session.cookies.update({
            "sessionid": session_id,
            "ds_user_id": ds_user_id,
            "csrftoken": csrftoken,
            "mid": mid,
            "ig_did": ig_did,
            "datr": datr,
            "ps_l": ps_l,
            "ps_n": ps_n,
            "oo": oo,
            "dpr": dpr_cookie,
            "wd": wd,
            "rur": rur,
        })

        self.user_id = ds_user_id or None
        self.csrftoken = csrftoken
        self.session_id = session_id

        try:
            r = self.session.get(
                f"{self.BASE}/direct_v2/inbox/",
                params={
                    "limit": "1",
                    "visual_message_return_type": "unseen",
                },
                timeout=20,
            )

            if r.status_code == 200:
                try:
                    data = r.json()
                except ValueError:
                    data = {}

                if "inbox" in data or "data" in data:
                    self.log_action(
                        "Successfully logged in using cookies.json"
                    )
                    return True

            self.log_error(
                f"Session test failed: {r.status_code} | {r.text[:300]}"
            )
            return False

        except Exception as e:
            self.log_error(f"Error during session test: {e}")
            return False

    def get_unread_messages(self) -> List[Dict[str, Any]]:
        try:
            r = self.session.get(
                f"{self.BASE}/direct_v2/inbox/",
                params={
                    "selected_filter": "unread",
                    "limit": "20",
                    "visual_message_return_type": "unseen",
                },
                timeout=20,
            )

            if r.status_code != 200:
                self.log_error(
                    f"Error fetching messages: "
                    f"{r.status_code} | {r.text[:200]}"
                )
                return []

            data = r.json()

            inbox = (
                data.get("inbox")
                or data.get("data", {}).get("inbox", {})
            )

            return inbox.get("threads", [])

        except Exception as e:
            self.log_error(f"Exception while fetching messages: {e}")
            return []

    def _fetch_tokens(self):
        urls_to_try = [
            "https://www.instagram.com/direct/inbox/",
            "https://www.instagram.com/",
        ]

        for url in urls_to_try:
            try:
                r = self.session.get(
                    url,
                    headers={
                        "Accept": (
                            "text/html,application/xhtml+xml,"
                            "application/xml;q=0.9,*/*;q=0.8"
                        ),
                        "Accept-Encoding": "gzip, deflate",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-Dest": "document",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-User": "?1",
                        "Upgrade-Insecure-Requests": "1",
                    },
                    timeout=20,
                )

                html = r.text

                patterns_dtsg = [
                    r'"DTSGInitData",\[\],\{"token":"([^"]+)"',
                    r'"DTSGInitData"[^}]*"token":"([^"]+)"',
                    r'"fb_dtsg"\s*:\s*"([^"]+)"',
                    r'fb_dtsg[^"]*"[^"]*"\s*,\s*"([^"]+)"',
                    r'"name":"fb_dtsg","value":"([^"]+)"',
                ]

                patterns_lsd = [
                    r'"LSD",\[\],\{"token":"([^"]+)"',
                    r'"LSD"[^}]*"token":"([^"]+)"',
                    r'"lsd"\s*:\s*"([^"]+)"',
                    r'"name":"lsd","value":"([^"]+)"',
                ]

                for pat in patterns_dtsg:
                    m = re.search(pat, html)

                    if m:
                        self._fb_dtsg = m.group(1)
                        break

                for pat in patterns_lsd:
                    m = re.search(pat, html)

                    if m:
                        self._lsd = m.group(1)
                        break

                if self._fb_dtsg and self._lsd:
                    self.log_action(
                        "Sending tokens successfully extracted"
                    )
                    return

            except Exception as e:
                self.log_error(
                    f"Error during token extraction: {e}"
                )

        self.log_error("Failed to extract fb_dtsg and lsd")

    def send_reply(
        self,
        thread_id: str,
        message: str,
        thread_v2_id: Optional[str] = None,
    ) -> bool:

        offline_id = (
            str(int(time.time() * 1000))
            + str(uuid.uuid4().int)[:6]
        )

        ig_thread_id = thread_v2_id or thread_id

        if not self._fb_dtsg or not self._lsd:
            self._fetch_tokens()

        if self._fb_dtsg and self._lsd:
            try:
                variables = {
                    "ig_thread_igid": ig_thread_id,
                    "offline_threading_id": offline_id,
                    "recipient_igids": None,
                    "replied_to_client_context": None,
                    "replied_to_item_id": None,
                    "reply_to_message_id": None,
                    "sampled": None,
                    "text": {
                        "sensitive_string_value": message
                    },
                    "mentions": [],
                    "mentioned_user_ids": [],
                    "commands": None,
                }

                post_data = {
                    "av": self.user_id,
                    "__d": "www",
                    "__user": "0",
                    "__a": "1",
                    "dpr": "3",
                    "fb_dtsg": self._fb_dtsg,
                    "lsd": self._lsd,
                    "fb_api_caller_class": "RelayModern",
                    "fb_api_req_friendly_name": (
                        "IGDirectTextSendMutation"
                    ),
                    "server_timestamps": "true",
                    "variables": json.dumps(
                        variables,
                        separators=(",", ":"),
                    ),
                    "doc_id": "25288447354146606",
                }

                r = self.session.post(
                    "https://www.instagram.com/api/graphql",
                    headers={
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Content-Type": (
                            "application/x-www-form-urlencoded"
                        ),
                        "Origin": "https://www.instagram.com",
                        "Referer": (
                            "https://www.instagram.com/direct/t/"
                            f"{ig_thread_id}"
                        ),
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "x-asbd-id": "359341",
                        "x-csrftoken": self.csrftoken,
                        "x-fb-friendly-name": (
                            "IGDirectTextSendMutation"
                        ),
                        "x-fb-lsd": self._lsd,
                        "x-ig-app-id": "1217981644879628",
                    },
                    data=post_data,
                    timeout=20,
                )

                if r.status_code == 200:
                    try:
                        resp = r.json()
                    except ValueError:
                        self.log_error(
                            "GraphQL returned invalid JSON"
                        )
                        return False

                    if resp.get("data") or not resp.get("errors"):
                        self.log_action(
                            f"Reply successfully sent to "
                            f"{ig_thread_id}"
                        )
                        return True

                    self.log_error(
                        f"GraphQL error: {str(resp)[:200]}"
                    )

                else:
                    self.log_error(
                        f"GraphQL status {r.status_code}: "
                        f"{r.text[:200]}"
                    )

                    if r.status_code in (400, 401, 403):
                        self._fb_dtsg = None
                        self._lsd = None

            except Exception as e:
                self.log_error(
                    f"Exception in GraphQL send: {e}"
                )

        return False


class APIClient:
    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.0-flash",
    ):
        self.api_key = api_key.strip()
        self.model = model
        self.http = requests.Session()

        self.base_url = (
            "https://generativelanguage.googleapis.com/"
            f"v1beta/models/{self.model}:generateContent"
        )

        self.thread_history: Dict[
            str,
            List[Dict[str, Any]]
        ] = {}

        self.system_instruction = (
            "You are an assistant replying on behalf of "
            "an Instagram account owner. "
            "Politely inform the sender that the account owner "
            "is currently unavailable, "
            "and that you are here to assist them until they return. "
            "Keep your responses very short, natural, and friendly. "
            "Do NOT state that you are an AI model. "
            "Avoid overly formal language. "
            "Usually start with an idea like: "
            "'I'm here to help until the owner gets back, "
            "how can I help you?' "
            "If asked about the account owner, state that they "
            "are currently unavailable and their message "
            "will be passed on later. "
            "Do not break character."
        )

    def send_message(
        self,
        thread_id: str,
        message: str,
    ) -> str:

        if thread_id not in self.thread_history:
            self.thread_history[thread_id] = []

        history = self.thread_history[thread_id]

        history.append({
            "role": "user",
            "parts": [
                {
                    "text": message
                }
            ],
        })

        payload = {
            "system_instruction": {
                "parts": [
                    {
                        "text": self.system_instruction
                    }
                ]
            },
            "contents": history,
        }

        max_retries = 3
        retry_delay = 3.0

        for attempt in range(1, max_retries + 1):
            try:
                response = self.http.post(
                    f"{self.base_url}?key={self.api_key}",
                    json=payload,
                    headers={
                        "Content-Type": "application/json"
                    },
                    timeout=(8, 25),
                )

                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])

                    if candidates:
                        parts = (
                            candidates[0]
                            .get("content", {})
                            .get("parts", [])
                        )

                        if parts:
                            reply = (
                                parts[0]
                                .get("text", "")
                                .strip()
                            )

                            if reply:
                                history.append({
                                    "role": "model",
                                    "parts": [
                                        {
                                            "text": reply
                                        }
                                    ],
                                })

                                return reply

                elif response.status_code in (503, 429):
                    self.log_api_error(
                        f"Gemini API ({response.status_code}) - High demand. "
                        f"Retrying attempt {attempt}/{max_retries} in {retry_delay}s..."
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2.0
                    continue

                else:
                    print(
                        f"Gemini API Error "
                        f"({response.status_code}): "
                        f"{response.text}"
                    )
                    break

            except requests.RequestException as e:
                self.log_api_error(
                    f"Gemini request network error (Attempt {attempt}/{max_retries}): {e}"
                )
                time.sleep(retry_delay)
                retry_delay *= 2.0
                continue

            except Exception as e:
                self.log_api_error(
                    f"Gemini error: {e}"
                )
                break

        if history and history[-1].get("role") == "user":
            history.pop()

        self.log_api_error(
            "Gemini failed to return a valid response after retries."
        )

        return ""

    def log_api_error(self, message: str):
        print(
            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
            f"ERROR: {message}"
        )


class MessageHandler:
    def __init__(
        self,
        bot: InstagramBot,
        api_client: APIClient,
    ):
        self.bot = bot
        self.api_client = api_client
        self.processed_messages = set()

    def _is_private_1to1_thread(
        self,
        thread: Dict[str, Any],
    ) -> bool:

        users = thread.get("users", []) or []

        return len(users) == 1

    def process_thread(
        self,
        thread: Dict[str, Any],
    ) -> bool:

        try:
            thread_id = str(
                thread.get("thread_id", "")
            )

            thread_v2_id = str(
                thread.get("thread_v2_id", "")
            )

            items = thread.get("items", []) or []

            if not thread_id or not items:
                return False

            if not self._is_private_1to1_thread(thread):
                return False

            last_message = items[0]

            message_id = str(
                last_message.get("item_id", "")
            )

            if (
                not message_id
                or message_id in self.processed_messages
            ):
                return False

            sender_id = str(
                last_message.get("user_id", "")
            )

            if (
                self.bot.user_id
                and sender_id == str(self.bot.user_id)
            ):
                self.processed_messages.add(message_id)
                return False

            item_type = last_message.get(
                "item_type",
                "",
            )

            if item_type != "text":
                self.processed_messages.add(message_id)
                return False

            message_text = (
                last_message
                .get("text", "")
                .strip()
            )

            if not message_text:
                return False

            self.bot.log_action(
                f"New private message from "
                f"{sender_id}: {message_text[:100]}"
            )

            reply = self.api_client.send_message(
                thread_id,
                message_text,
            )

            if not reply:
                self.bot.log_error(
                    "No reply generated by Gemini. "
                    "The Instagram message will not receive "
                    "an automatic reply."
                )

                self.processed_messages.add(message_id)

                return False

            ok = self.bot.send_reply(
                thread_id,
                reply,
                thread_v2_id=thread_v2_id,
            )

            if not ok:
                self.bot.log_error(
                    f"Could not reply to private "
                    f"thread_id={thread_id}"
                )

            self.processed_messages.add(message_id)

            if len(self.processed_messages) > 5000:
                self.processed_messages = set(
                    list(self.processed_messages)[-2000:]
                )

            return ok

        except Exception as e:
            self.bot.log_error(
                f"Error processing thread: {e}"
            )
            return False

    def monitor_messages(
        self,
        poll_interval: float = 1.2,
    ):
        self.bot.log_action(
            "Starting message monitoring..."
        )

        while self.bot.is_running:
            try:
                threads = self.bot.get_unread_messages()

                if threads:
                    for thread in threads:
                        if not self.bot.is_running:
                            break

                        responded = self.process_thread(
                            thread
                        )

                        if responded:
                            delay = random.uniform(
                                15,
                                20,
                            )

                            self.bot.log_action(
                                f"Waiting for "
                                f"{delay:.2f} seconds before "
                                f"replying to the next thread..."
                            )

                            time.sleep(delay)

                time.sleep(poll_interval)

            except KeyboardInterrupt:
                self.bot.log_action(
                    "Manually stopped"
                )

                self.bot.is_running = False
                break

            except Exception as e:
                self.bot.log_error(
                    f"Monitoring error: {e}"
                )
                time.sleep(3)


def main():
    cookies_file = "cookies.json"

    gemini_api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if not gemini_api_key:
        print("=== Gemini API Key Required ===")
        gemini_api_key = input("Enter your Gemini API Key: ").strip()

    if not gemini_api_key:
        print("ERROR: GEMINI_API_KEY is required to start the bot.")
        return

    gemini_model = "gemini-2.0-flash"
    poll_interval = 1.2

    bot = InstagramBot(cookies_file=cookies_file)
    api_client = APIClient(api_key=gemini_api_key, model=gemini_model)
    handler = MessageHandler(bot, api_client)

    if not bot.login():
        bot.log_error("Failed to login using cookies.json")
        return

    bot.is_running = True
    handler.monitor_messages(poll_interval=poll_interval)


if __name__ == "__main__":
    main()
