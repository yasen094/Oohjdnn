# EDX Bot (Yassin-Uncle)

A Highrise virtual-room bot ("EDX Bot") imported from github.com/yasen094/Yassin-Uncle, with a Flask web dashboard for managing outfits, moderators, custom commands, and AI chat responses.

## Run & Operate

- The bot runs as the "Highrise Bot" workflow: `cd bot && PORT=9000 ../.pythonlibs/bin/python run.py`
- `pnpm --filter @workspace/api-server run dev` — run the (separate, currently unused) API server
- `pnpm run typecheck` — full typecheck across the pnpm packages
- Required secret: `HIGHRISE_BOT_TOKEN` — the bot's Highrise login token
- Optional secret: `GEMINI_API_KEY` — enables the AI chat/assistant features (not set yet; bot runs fine without it, just without AI chat)

## Stack

- Python 3.10, `highrise-bot-sdk` 24.1.0, Flask (web dashboard), `google-generativeai`
- pnpm workspaces scaffold also present (Node.js 24, TypeScript, Express API server, Drizzle) but not used by the bot — leftover from the original Replit template this repo was built on.

## Where things live

- `bot/main.py` — bot logic, commands, event handlers (large file)
- `bot/run.py` — Flask web dashboard + bot process bootstrap; reads `PORT` env var
- `bot/config.py` — bot/room/security config; token now read from `HIGHRISE_BOT_TOKEN` env var (was previously hardcoded)
- `bot/modules/` — feature managers (moderation, AI chat, emotes, positions, VIP, custom commands, etc.)
- `bot/data/` — persisted JSON state (users, moderators, outfits, custom commands, etc.)
- `bot/templates/` + `bot/static/` — dashboard HTML/CSS/JS

## Architecture decisions

- Kept as a standalone Python workflow rather than a pnpm-workspace artifact — the artifact system has no "Python bot" type, and this bot doesn't fit the web-app/mobile-app/slides/video artifact molds.
- Moved to port 9000 for its Flask dashboard since port 8080 is already used by the workspace's own API server artifact.

## Product

Discord-bot-equivalent for Highrise: joins a configured room, handles chat commands, moderation, automatic dances/emotes, outfit management, and optional AI chat replies — all manageable through the bundled web dashboard.

## User preferences

_Populate as you build — explicit user instructions worth remembering across sessions._

## Gotchas

- The original repo hardcoded the bot token directly in `config.py`, publicly exposed on GitHub — it's now read from the `HIGHRISE_BOT_TOKEN` secret instead. If bot login is rejected, the token was likely already compromised/rotated on Highrise's end.
- If you see repeated "Multilogin closing connection" errors in the workflow logs, it means the same bot account is already logged in elsewhere (e.g., still running on the original Replit/host) — Highrise only allows one active session per bot token.
- AI chat features need `GEMINI_API_KEY` — not currently set; the bot logs a warning and runs without AI replies until it's added.

## Pointers

- See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details (only relevant to the unused Express/Drizzle scaffold, not the bot).
