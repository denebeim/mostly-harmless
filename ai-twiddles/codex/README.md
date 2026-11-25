# Codex experiments

This is Codex's area for personal experiments in mostly-harmless. Keep new Codex experiments here, on a `codex/` branch. Follow the [owner acceptance workflow](../../CONTROLLER.md#review-and-acceptance).

## Two workflows

### Personal experiments

1. Start an isolated `codex/` branch from the current remote default branch. Use a worktree when the owner's checkout has other changes.
2. Keep implementation, notes and scoped instructions under `ai-twiddles/codex/`. Record significant actions in WORKLOG.md on the separate `work-log` branch.
3. Review the diff and run checks appropriate to the actual change. Stage explicit paths only.
4. Commit and push the scoped experiment on the pull branch. Address review feedback and move deployable files to the regular layout. Target the PR at an acceptance branch from main and leave both merges to Joy.

This permission covers the experimental implementation and its technical operating notes. It does not authorize publishing writing in the owner's name.

### Work intended for publication in the owner's voice

1. The owner or assistant creates a ticket for the work.
2. Create a dedicated branch.
3. Work together on the content until the owner feels it says what they mean in their own voice. Do not substitute generic assistant prose for that collaboration.
4. The owner makes the commit.
5. Update the work log and prepare the pull request together.

Autonomous experimental commits and pushes do not shorten this publication workflow.

## Existing mouse buttons

The existing captured setups remain where they are:

- [ChatGPT Voice](../logitech-m705-chatgpt-voice/README.md): Mouse Button 5 / code 276, GNOME custom1, `~/.local/bin/chatgpt-voice-toggle`.
- [Gemini dictation](../logitech-m705-gemini-dictation/README.md): Mouse Button 4 / code 275, GNOME custom0, `~/.local/bin/gemini-toggle`, `gemini-focus@local`.

Do not move, reinstall or overwrite either setup just to organize this folder. Gemini's work is outside this area. Coordinate an explicit shared change before editing another assistant's files, shared presets, GNOME bindings or logging code. The ChatGPT-specific launcher remains Codex's responsibility, but changes to its existing captured location or live installation need an explicitly scoped task.

## Logging

Follow the checkout's current `AGENTS.md`. The established shell wrapper is:

```sh
python3 /home/denebeim/projects/mostly-harmless/scripts/log-session.py COMMAND ARG ...
```

The required live destination is `/home/denebeim/projects/mostly-harmless/chat.log`. Keep stdout/stderr visible as commands run; no credentials, environment dumps or command tracing. Never truncate or commit logs. Pipelines and compound shell commands go inside one logged shell; do not nest wrappers. `ai-twiddles/log-session.py` is the separate logger used by the committed mouse playbooks and also targets the root `chat.log`. Do not modify either shared logger as part of an unrelated experiment.

The established significant-work record is [WORKLOG.md on the separate work-log branch](https://github.com/denebeim/mostly-harmless/blob/work-log/WORKLOG.md). Commit and push work-log updates there independently. Do not merge the work-log branch into main or add a new work log to main for convenience. Preserve unrelated log entries. Reusable agent-neutral workflow prompts also live in that work log.

## Current product boundary

The working ChatGPT button invokes the app's built-in Voice toggle. This organizational setup does not replace it with an API client. A free-first/paid-backup API client remains a separate product choice; no free OpenAI Realtime tier, account credit eligibility, or conversation/tool continuity is assumed.
