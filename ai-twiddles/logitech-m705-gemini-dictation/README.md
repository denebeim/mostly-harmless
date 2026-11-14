# Logitech M705 mouse — Gemini dictation

Button 275 / BTN_SIDE emits Ctrl+Alt+Shift+G to focus or launch the Gemini Chrome app. First click starts dictation; second stops it, waits 0.6 seconds, then submits with Return. The playbook installs the launcher and GNOME helper and configures GNOME shortcut custom0.

## Platform and prerequisites

Personal local setup: Ubuntu 26.04 LTS, GNOME Wayland and Logitech M705. Run from this checkout in the intended desktop user's unlocked GNOME terminal, with that user's session bus and runtime directory; no sudo/become, other account or remote/headless session. Ansible user facts derive installation paths and the preset name from that user's home.

Input Remapper and its service must already be installed. The playbook does not install packages, apps or device permissions. It preserves other mouse mappings, overwrites this button and its existing GNOME shortcut slot, and selects the shared mouse preset for autoload. Review those slots before running on a different setup. Both shortcut commands use `ai-twiddles/log-session.py`, so keep the checkout in place. The wrapper appends redacted command output to the checkout's private `chat.log` (never commit it); redaction is best effort. Tasks report changed each run; saved JSON is indented.

Gemini additionally needs system Python GI, Chrome at `/opt/google/chrome/google-chrome`, and a Chrome profile signed into Gemini with microphone access. The captured extension declares GNOME Shell 50; other Shell versions are unverified.

## Usage

From the checkout root, with Ansible already installed in `.venv` (or substitute your installed `ansible-playbook` executable):

```sh
python3 ai-twiddles/log-session.py .venv/bin/ansible-playbook -i localhost, ai-twiddles/logitech-m705-gemini-dictation/playbook.yaml
```

`gemini_chrome_profile` defaults to `Default`. Add `-e 'gemini_chrome_profile="Profile 4"'` if that is your signed-in profile. Enable `gemini-focus@local` through GNOME Extensions; log out/in if needed to discover or reload it. After manually changing the microphone, run `~/.local/bin/gemini-toggle --reset` to clear the click tracker without sending input.

## Activate the saved mouse mapping

Apply the home-derived preset for Logitech M705 in Input Remapper. Its name replaces slashes in your home path with underscores (for example, `/home/alex` becomes `_home_alex`). Alternatively, from the checkout root in Bash:

```sh
python3 ai-twiddles/log-session.py sudo input-remapper-control --command start --device "Logitech M705" --preset "${HOME//\//_}" --config-dir "$HOME/.config/input-remapper-2"
```

The playbook saves configuration without reloading Input Remapper or restarting GNOME.

## Caveats

The owner reports the existing live setup working on Ubuntu 26.04 LTS. This playbook has passed syntax checks only and has never been applied, including on Ubuntu 26.04. Exhaustive start/stop, cold-launch and cross-system acceptance is not established. Lock/focus checks refuse input when they fail; this is not exhaustive safety validation. No broad testing or support promise. No desktop settings changed during capture or revision.

[Back to AI twiddles](../README.md). Historical inspection and rollback notes remain in [mouse setup notes](../MOUSE-VOICE.md), including the limits of earlier checks and rollback guidance.

The two-click tracker can desynchronize after manual microphone changes. App/window matching and timing reflect the captured setup and may need adjustment after updates.
