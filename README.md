# Daily Vocab

A word a day, delivered to your phone every morning via Telegram. Free to run:
no paid APIs, no servers. GitHub Actions fires the job on a schedule, and a
curated word list lives right in this repo.

## How it works

- `words.json` — the word corpus (word, definition, real-world note, example).
- `progress.json` — a one-line pointer tracking which word is next.
- `send_word.py` — picks the next word, sends it to Telegram, advances the pointer.
- `.github/workflows/daily-word.yml` — runs the script daily and commits the
  updated pointer back (which also keeps the scheduled workflow from being
  auto-disabled for inactivity).

When the list runs out it loops back to the start. Add more words anytime by
appending entries to `words.json`.

## One-time setup (~15 minutes)

### 1. Create your Telegram bot
1. Install Telegram and open it.
2. Message **@BotFather**, send `/newbot`, and follow the prompts.
3. It gives you a **bot token** like `123456789:AAH...`. Keep it handy.

### 2. Find your chat id
1. Open a chat with your new bot and send it any message (e.g. "hi").
2. In a browser, visit:
   `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   (paste your token in place of `<YOUR_TOKEN>`).
3. Find `"chat":{"id":...}` in the response. That number is your **chat id**.

### 3. Put this folder in a GitHub repo
- Create a new repo (Public keeps GitHub Actions free and unlimited).
- Upload these files. The token is NOT in the code — it goes in Secrets below —
  so a public repo is safe.

### 4. Add your secrets
In the repo: **Settings → Secrets and variables → Actions → New repository secret**
- `TELEGRAM_BOT_TOKEN` = your bot token
- `TELEGRAM_CHAT_ID` = your chat id

### 5. Test it
- Go to the **Actions** tab → "Daily word" → **Run workflow**.
- A message should hit your phone within a few seconds. Done.

## Notes
- **Send time:** edit the `cron` line in the workflow. Times are UTC.
  `0 14 * * *` is 7 AM Pacific in summer / 6 AM in winter. Use `0 15 * * *`
  for 7 AM in winter.
- **Scheduled runs can be a few minutes late** under GitHub load. Fine for a
  morning word.
- **Switching to email later** only means replacing `send_telegram` in
  `send_word.py` with an email send; the rest is unchanged.
