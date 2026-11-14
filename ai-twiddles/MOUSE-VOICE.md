# Logitech M705 mouse voice setup notes

These notes retain the relevant inspection and rollback material behind the two experiments without requiring the original machine's paths or private backups. The owner reports the installed Ubuntu 26.04 LTS / GNOME Wayland setup working. The captured playbooks are unapplied and syntax-checked only.

## Mapping and installed files

Input Remapper reads hardware events and emits chords; GNOME custom shortcuts invoke user launchers. Paths below are relative to the desktop user's home, derived by Ansible user facts.

| Button | Input | Mouse chord | GNOME slot | Launcher | Action |
| --- | --- | --- | --- | --- | --- |
| Gemini dictation | EV_KEY 275 / BTN_SIDE | Ctrl+Alt+Shift+G | custom0 | `~/.local/bin/gemini-toggle` | Dictate; next click stop, wait 0.6 seconds, submit Return |
| ChatGPT Voice | EV_KEY 276 / BTN_EXTRA | Ctrl+Alt+Shift+V | custom1 | `~/.local/bin/chatgpt-voice-toggle` | Focus/launch app, emit distinct Ctrl+Alt+Shift+F12 |

The preset is `~/.config/input-remapper-2/presets/Logitech M705/<preset>.json`, with autoload in `~/.config/input-remapper-2/config.json`. The preset name is the home path with slashes replaced by underscores. Both playbooks share it and preserve other events. GNOME shortcut paths are `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/` and `custom1/`.

Gemini additionally installs `~/.local/share/gnome-shell/extensions/gemini-focus@local/`. Its narrow D-Bus interface supplies Focus/Send/Status and a persistent Clutter virtual keyboard. Window title/class, lock, focus and held modifiers are checked before input. The launcher serializes clicks and keeps per-window runtime state, retaining a pending submission for retry. Manual microphone changes may require `gemini-toggle --reset`.

ChatGPT uses wmctrl/xprop for its observed XWayland window, checks GNOME ScreenSaver lock state, and uses evdev/uinput for a virtual keyboard. It serializes actions with a runtime lock and releases pressed keys in finally. The native app Voice hotkey must manually be set to Ctrl+Alt+Shift+F12; reusing the mouse trigger would invoke the launcher recursively. App code inspection indicated a toggle can start a new Voice thread, stop an active session or cancel a pending start; this is version-specific source inspection, not a promise to resume the displayed chat.

## Evidence and limits

Earlier checks of the installed setup included Python compilation, ChatGPT focus-only behavior, simulated focus-loss refusal and chord release order, and virtual keyboard creation without sending keys. Existing Gemini shortcut fields and original preset entries were compared before and after adding ChatGPT. The owner subsequently reported the setup working. Exhaustive live start/stop, return to text, cold launch, Gemini regression and playbook deployment are not established by those checks. A sent chord alone does not prove an app changed Voice state.

The captured playbooks passed Ansible syntax checks and embedded Python compilation; these were not deployment tests. The current publication preparation did not apply them or change desktop settings.

## Applying and inspecting

Use the exact playbook and preset activation commands in each experiment's README. Input Remapper application may require desktop authentication or sudo to access devices. Privilege for that preset reload does not grant root access to launchers. Neither playbook reloads the preset, restarts GNOME, installs dependencies or changes the app's Voice setting.

From the checkout root, ChatGPT focus-only inspection without toggling Voice is:

```sh
python3 ai-twiddles/log-session.py "$HOME/.local/bin/chatgpt-voice-toggle" --focus-only
```

Shell commands and launcher output use `log-session.py`, which appends to private `chat.log`, retains command exit status and attempts secret redaction. Do not print credentials or commit logs. Connector/API operations are outside shell capture.

## Backups and rollback

Before applying either experiment, keep your own copies of the current shared preset, autoload config, affected GNOME shortcut fields/list and any files being replaced. The playbooks do not create backups or implement rollback. Earlier installed-setup backups were machine-local and are not shipped here.

To undo a button, restore its prior preset and reload that preset, restore/remove only its GNOME custom shortcut and list entry, and restore/remove its launcher. For Gemini, restore/remove the extension separately and reload the GNOME session if needed. Preserve the sister button's entries and helpers. Restore ChatGPT's manually changed Voice hotkey separately. No rollback was performed during capture.

- [Gemini dictation experiment](logitech-m705-gemini-dictation/README.md)
- [ChatGPT Voice experiment](logitech-m705-chatgpt-voice/README.md)
