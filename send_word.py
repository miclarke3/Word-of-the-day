#!/usr/bin/env python3
"""Send the next word of the day to Telegram, then advance the pointer.

Reads words.json (the corpus) and progress.json (which index is next),
formats a message, sends it via the Telegram Bot API, and writes the
incremented index back to progress.json so the GitHub Action can commit it.

Required environment variables:
    TELEGRAM_BOT_TOKEN  - the token from @BotFather
    TELEGRAM_CHAT_ID    - your personal chat id (see README)
"""

import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS_PATH = os.path.join(HERE, "words.json")
PROGRESS_PATH = os.path.join(HERE, "progress.json")


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def build_message(entry):
    # Telegram supports a small subset of HTML when parse_mode=HTML.
    return (
        f"\U0001F4D6 <b>Word of the day: {entry['word']}</b>"
        f"  <i>({entry['part_of_speech']})</i>\n\n"
        f"<b>Meaning:</b> {entry['definition']}\n\n"
        f"<b>Where it earns its keep:</b> {entry['real_world']}\n\n"
        f"<b>Try it:</b> \u201C{entry['example']}\u201D"
    )


def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    ).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        result = json.loads(body)
        if not result.get("ok"):
            raise RuntimeError(f"Telegram API error: {body}")
        return result


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID.")

    words = load_json(WORDS_PATH, [])
    if not words:
        sys.exit("words.json is empty or missing.")

    progress = load_json(PROGRESS_PATH, {"index": 0})
    index = progress.get("index", 0)

    # Wrap around to the start if we've reached the end of the list.
    entry = words[index % len(words)]

    send_telegram(token, chat_id, build_message(entry))
    print(f"Sent word #{index}: {entry['word']}")

    # Advance only after a successful send.
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump({"index": index + 1}, f)


if __name__ == "__main__":
    main()
