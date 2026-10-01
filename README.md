# SB24 — Word & Text Telegram Bot

SB24 is a focused Telegram word/text utility bot designed around a simple in-Telegram user flow.

## Core functions
- Sort Words — sort submitted words A–Z or Z–A.
- Count Words — count words, characters, and characters excluding spaces.
- Clean Text — normalize repeated whitespace and remove blank lines.

The main menu contains exactly three primary buttons.

## Requirements
- Python 3.12+
- Telegram bot token from BotFather

## Local setup
1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`.
3. Set the `BOT_TOKEN` environment variable.
4. Run: `python -m app.main`.

## Render
Deploy as a Background Worker using `render.yaml`, then add `BOT_TOKEN` as a secret environment variable.

## Telegram profile
The application configures the bot name, short description, description, and command list on startup.

Expected Telegram username: `@SBWordBot`.

## Scope
No external URLs, redirects, payments, gambling, betting, casino, or real-money gaming features are included.

Telegram Ads approval is determined by Telegram and cannot be guaranteed by this project.
