# AI twiddles

**Disclaimer: personal local experiments captured November 14, 2026. The owner reports the existing desktop setup working on Ubuntu 26.04 LTS with GNOME Wayland and a Logitech M705. The playbooks have passed syntax checks only; they have never been applied, including on Ubuntu 26.04. No broad testing or support promise.**

Captured installed helpers for Logitech M705 on GNOME Wayland. Each playbook installs its helper, replaces its own mouse event while preserving other mappings, selects the shared preset for autoload, and configures its existing GNOME shortcut slot (custom0 for Gemini, custom1 for ChatGPT). These slots must already belong to these experiments. Ansible user facts select installation paths and preset names from the running user’s home. Run in the intended desktop user’s local session with its session bus and runtime directory; do not run via sudo, become, another account or a remote/headless session. Both shortcut commands use the logger in this checkout, so keep the checkout at its installed location. The shortcut slots and mouse event mappings are overwritten for these buttons; review them before running if your configuration differs. Tasks report changed on each run. Saved configuration and runtime JSON use indentation for readability.

Run from this checkout in your unlocked GNOME terminal, as your desktop user, without sudo. Existing prerequisites are assumed: Input Remapper/service, Python GI and evdev, wmctrl/xprop, existing /dev/uinput permission, Chrome signed into Gemini and /usr/bin/chatgpt. Packages, apps and permissions are not provisioned. The captured extension declares GNOME Shell 50; other Shell versions are unverified. The ChatGPT focus helper assumes its existing XWayland window; native Wayland or app updates may require changes. These scripts refuse input when lock/focus checks fail, but that is not exhaustive safety or start/stop validation.

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

Playbooks save configuration without reloading Input Remapper or restarting GNOME, and do not automate the in-app Voice setting. The owner’s working report concerns the existing live setup, not deployment by these playbooks; exhaustive start/stop, cold-launch and cross-system acceptance is not established. No playbooks were applied or desktop settings changed while capturing or revising these files. See [historical setup and rollback notes](../MOUSE-VOICE.md); older pending acceptance wording there predates the owner's working report.
