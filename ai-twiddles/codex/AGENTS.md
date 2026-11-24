# Codex experimental area

These instructions apply under `ai-twiddles/codex/` and supplement repository instructions.

- Use a `codex/` branch for this area's experiments. Inspect the actual remote default branch and current changes before starting. Keep other tasks' working changes intact.
- The owner authorizes autonomous work, commits and pushes on the isolated experimental branch. Anything reaching main (or a future actual default branch) needs the owner's explicit approval after a report, discussion and inspection of the concrete work. General workflow approval is not approval for future changes. Keep the correction/feature PR pending until that approval; do not merge or enable auto-merge beforehand. Use explicit staging paths and respect normal checks, required reviews and branch protection; no bypass flags or force pushes.
- This authorization does not cover publishing work in the owner's voice. Publication work needs a ticket, dedicated branch, collaborative refinement until the owner is satisfied with their voice, an owner-made commit, a work-log update, and a PR prepared together.
- Preserve Gemini and both existing mouse setups. Do not relocate or overwrite `ai-twiddles/logitech-m705-gemini-dictation/`, `ai-twiddles/logitech-m705-chatgpt-voice/`, live launchers, GNOME shortcuts or mouse presets for organizational convenience.
- Shared logging code and other assistants' files are outside this area's autonomous edit scope. Appending authorized significant findings to the established work log is allowed; preserve unrelated entries.
- Follow the root command-logging contract. Shell commands, including Git operations and failures, must stream through `/home/denebeim/projects/mostly-harmless/scripts/log-session.py` to the existing `/home/denebeim/projects/mostly-harmless/chat.log`. Do not nest wrappers, print secrets, truncate logs or stage logs.
- Record significant work in `WORKLOG.md` on the separate `work-log` branch and commit/push those updates there. Do not add or merge work-log updates into main. Reusable agent-neutral prompts belong in that separate work log. Report exact commit, PR/merge status, checks and remaining limitations.
- Do not silently replace built-in ChatGPT Voice with a custom API client. The free-first/paid-backup request needs a separate product decision and verified provider availability/pricing.
