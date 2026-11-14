# AI twiddles

**Disclaimer: rough personal desktop experiments captured November 14, 2026. GNOME slots and app assumptions remain specific to this experiment. No portability/support promise. These playbooks have not been tested or applied.**

Captured installed helpers for Logitech M705 on GNOME Wayland. Each playbook installs its helper, replaces its own mouse event while preserving other mappings, selects the shared preset for autoload, and configures its existing GNOME shortcut slot (custom0 for Gemini, custom1 for ChatGPT). These slots must already belong to these experiments. Ansible facts select the current desktop user’s home; do not run with sudo or become. Both shortcut commands use the logger in this checkout, so keep the checkout at its installed location. Tasks report changed on each run.

Run from this checkout in your unlocked GNOME terminal, as your desktop user, without sudo. Existing prerequisites are assumed: Input Remapper/service, Python GI and evdev, wmctrl/xprop, existing /dev/uinput permission, Chrome signed into Gemini and /usr/bin/chatgpt. Packages, apps and permissions are not provisioned.

## Gemini

```sh
python3 scripts/log-session.py .venv/bin/ansible-playbook -i localhost, ai-twiddles/gemini-mouse-voice.yaml
```

The Gemini launcher is templated with `gemini_chrome_profile`, default `Default`; add `-e 'gemini_chrome_profile="Profile 4"'` to the command if that is your signed-in Chrome profile. Enable gemini-focus@local through GNOME Extensions after installation; log out/in if needed to discover or reload the extension. Captured metadata targets GNOME Shell 50. Button 275 / BTN_SIDE emits Ctrl+Alt+Shift+G. First click focuses/launches Gemini and starts dictation; second stops, waits 0.6 seconds and submits Return. After manual microphone changes, `~/.local/bin/gemini-toggle --reset` clears the click tracker without sending input.

## ChatGPT

```sh
python3 scripts/log-session.py .venv/bin/ansible-playbook -i localhost, ai-twiddles/chatgpt-mouse-voice.yaml
```

Manually set ChatGPT Settings > Voice > Voice chat hotkey to **Ctrl+Alt+Shift+F12**. Button 276 / BTN_EXTRA emits Ctrl+Alt+Shift+V, focuses/launches the observed XWayland app, then sends that distinct native Voice shortcut. Keep the chords different to avoid recursion. The app controls start/stop behavior and may start a new Voice thread rather than resume the displayed chat.

## Activate saved mouse configuration

After either playbook, apply the preset named after your home path with slashes replaced by underscores (for example, `/home/alex` becomes `_home_alex`) for Logitech M705 in Input Remapper, or run in Bash:

```sh
python3 scripts/log-session.py sudo input-remapper-control --command start --device "Logitech M705" --preset "${HOME//\//_}" --config-dir "$HOME/.config/input-remapper-2"
```

Playbooks save configuration without reloading Input Remapper or restarting GNOME. Owner reports the installed setup working; exhaustive start/stop acceptance is not established. No desktop settings changed during capture. See [historical setup and rollback notes](../MOUSE-VOICE.md); older pending acceptance wording there predates the owner's working report.
