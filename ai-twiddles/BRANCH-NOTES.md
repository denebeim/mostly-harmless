# Branch notes: user-home correction

Purpose: let the desktop user running either playbook install these experiments in their own home.

- Gather Ansible facts and use user_dir for install paths, preset naming and GNOME launcher commands. Explicitly disable privilege escalation; run as the logged-in desktop user.
- Pass home, preset name and checkout logger location as Python arguments, avoiding source-code interpolation of paths. Quote GNOME launcher command arguments.
- Template the Gemini Chrome profile (Default unless overridden); helper runtime UID/state already follow the invoking user. No personal home path remains in this directory.
- Correct the captured configuration writer to append a real newline, rather than literal backslash-n.
- Keep existing mouse events, hotkeys, GNOME slots, app paths and Shell 50 metadata assumptions. No dependency installation or live application.

Review: inspect scoped diff, parse playbook JSON, compile embedded configuration Python and rendered Gemini helper without executing them. No desktop actions or broad test suite.

Publication remains pending owner review. No push, issue, PR or merge authorized. Condense branch notes and final documentation to purpose, behavior and usage before merging.

Results: both Ansible syntax checks passed; embedded configuration Python and substituted Gemini helper compile; staged diff whitespace check passed. Original ai-twiddles snapshot was ignored/untracked by the repository top-level allowlist, so this commit explicitly adds its eight files without changing the unrelated dirty .gitignore. No live configuration or functional tests.

## Readability and caveats follow-up

README now distinguishes the owner-reported Ubuntu 26.04 LTS live setup from syntax-only playbook validation, and records desktop-user context, prerequisites and existing app/extension assumptions. Converted JSON-form playbooks to conventional YAML with literal blocks for embedded Python; parsed values were compared before and after. Extension metadata is indented JSON with unchanged values. Gemini runtime state JSON is now indented; preset/config writers already use indent=4. No live execution.

Validation: both Ansible syntax checks, embedded Python/helper compilation and scoped diff whitespace checks passed. YAML conversion and metadata formatting preserved parsed values. No deployment or functional testing.
