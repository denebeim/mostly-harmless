# Logitech M705 mouse — ChatGPT Voice

Button 276 / BTN_EXTRA emits Ctrl+Alt+Shift+V to focus or launch ChatGPT and send its separate native Voice hotkey, Ctrl+Alt+Shift+F12. The playbook installs the launcher and configures GNOME shortcut custom1.

## Platform and prerequisites

Personal local setup: Ubuntu 26.04 LTS, GNOME Wayland and Logitech M705. Run from this checkout in the intended desktop user's unlocked GNOME terminal, with that user's session bus and runtime directory; no sudo/become, other account or remote/headless session. Ansible user facts derive installation paths and the preset name from that user's home.

Input Remapper and its service must already be installed. The playbook does not install packages, apps or device permissions. It preserves other mouse mappings, overwrites this button and its existing GNOME shortcut slot, and selects the shared mouse preset for autoload. Review those slots before running on a different setup. Both shortcut commands use this checkout's logger, so keep the checkout in place. Tasks report changed each run; saved JSON is indented.

ChatGPT additionally needs `/usr/bin/chatgpt`, system Python evdev, wmctrl/xprop and existing permission to use `/dev/uinput`. The focus helper assumes the observed XWayland ChatGPT window; native Wayland or app updates may require changes.

## Usage

From the checkout root:

```sh
python3 scripts/log-session.py .venv/bin/ansible-playbook -i localhost, ai-twiddles/logitech-m705-chatgpt-voice/playbook.yaml
```

Manually set ChatGPT Settings > Voice > Voice chat hotkey to **Ctrl+Alt+Shift+F12**. Keep this different from the mouse's Ctrl+Alt+Shift+V trigger to avoid recursively invoking the launcher. The playbook does not automate the in-app setting.

## Activate the saved mouse mapping

Apply the home-derived preset for Logitech M705 in Input Remapper. Its name replaces slashes in your home path with underscores (for example, `/home/alex` becomes `_home_alex`). Alternatively, from the checkout root in Bash:

```sh
python3 scripts/log-session.py sudo input-remapper-control --command start --device "Logitech M705" --preset "${HOME//\//_}" --config-dir "$HOME/.config/input-remapper-2"
```

The playbook saves configuration without reloading Input Remapper or restarting GNOME.

## Caveats

The owner reports the existing live setup working on Ubuntu 26.04 LTS. This playbook has passed syntax checks only and has never been applied, including on Ubuntu 26.04. Exhaustive start/stop, cold-launch and cross-system acceptance is not established. Lock/focus checks refuse input when they fail; this is not exhaustive safety validation. No broad testing or support promise. No desktop settings changed during capture or revision.

[Back to AI twiddles](../README.md). Historical inspection and rollback notes remain in [MOUSE-VOICE.md](../../MOUSE-VOICE.md); its older pending acceptance wording predates the owner's working report.

The app controls Voice start/stop behavior and may create a new Voice thread rather than resume the displayed chat. Sending the hotkey alone does not establish that Voice started or stopped.
