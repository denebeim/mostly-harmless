# Deepthot Ansible controller

Run from this checkout: `mostly-harmless` is the forward source of truth.
`~/ansible/deepthot-configuration` is legacy reference only.

## Operating contract

- VM capabilities belong in the global user environment: SSH into a VM should expose its installed tools through system-wide PATH/startup configuration, without per-user setup.

- Record significant observations, changes, verification and pending work in tracked `WORKLOG.md`.
- Append command stdout/stderr to untracked `eddie-session.log`. Use `python3 scripts/log-session.py COMMAND ...`; it redacts secret-like values and private PEM blocks before writing/displaying output. Never print credentials or raw private configuration deliberately; Ansible secret tasks must use `no_log`.
- Static IPs may be documented. Never commit `.envrc`, inventory secrets, ticket caches, private certificates/keys or the private Pi-hole TOML.
- Per-machine playbooks declare a `vm` and import `vm.yaml`. Shared roles converge absent-to-installed. Do not add permanent fix/repair playbooks; apply the change, record it and update the owning role.
- VM tags gate roles: `ipa`, `docker`, `gpu`, `ollama`, `hermes`. An empty tag list is supported. IPA is optional and handles identity/automount, not LAN DNS; Pi-hole owns DNS.

## Setup and run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-controller.lock.txt
.venv/bin/ansible-galaxy role install -r roles/requirements.yml -p roles/galaxy_roles
.venv/bin/ansible-galaxy collection install -r collections/requirements.yml -p collections
source .envrc
python3 scripts/log-session.py .venv/bin/ansible-playbook eddie.yaml --ssh-common-args='-F /dev/null'
```

The private `.envrc` selects the project Python and inventory environment. A valid controller Kerberos ticket (`kinit admin` if needed) is required for a new `ipa` enrollment and for managing the Docker sudo rule on hosts with both `ipa` and `docker` tags. Untagged guests and the local Hermes account do not need a ticket.

`create_vm.yaml` provisions/base-bootstraps, `join_deepthot.yaml` joins tagged clients, and `install_docker.yaml` configures tagged Docker hosts. `vm.yaml` composes these and the optional applications; `hermes.yaml` is the shared Hermes application entrypoint, with prerequisites and usage explained in its GPLv3 header. Invoke a shared entrypoint with a private `-e @vm-spec.json` declaration, or use a minimal machine file such as `eddie.yaml`. Destructive cleanup is a separately reviewed operation, never implicit in provisioning.

A declaration requires `vm.name`, `vm.id` and `vm.ip`. Defaults: node/storage `heartogold`, template `deepthot-24-04`, 2 cores, 2048 MiB, 12G root disk, serial console, gateway `192.168.42.1`, DNS `192.168.42.2`, domain `local.deepthot.org`. Declare `vm.tags: []` for no optional roles. Disks only grow; NIC MACs are preserved. `vm.update_packages` defaults false; test guests do not upgrade. `vm.local_users` creates local service accounts; `vm.docker_members` optionally enforces exact Docker group membership. Eddie declares the local service account `hermes` and uses `vm.docker_ipa_group: docker-admins` to add members resolved through SSSD. Ansible reconciles the combined list on each run. Users need a new login to pick up membership changes.

First-use SSH trust is isolated by VM ID and MAC, then checked/refreshed through the newly installed guest agent into that same file. It initially relies on the controlled LAN/expected IP (TOFU); it is not a claim of cryptographic pre-boot identity verification. Existing pins reject unexpected changed keys. No global host-key checking is disabled.

## Eddie and shared inference

Eddie is VM 314 at `192.168.42.132`, with the K5200 passed through at host `0000:81:00`. Its GPU runs local Qwen via Ollama's Vulkan backend; do not assume modern CUDA support. Eddie keeps `ollama_listen_host: 0.0.0.0` and a controller-side LAN API check. Other hosts default to loopback. Native desktop clients may use `http://192.168.42.132:11434/v1`; only trusted LAN access is intended. No firewall manager, public forwarding or broad browser-origin permission is added.

```bash
curl --fail --noproxy '*' http://192.168.42.132:11434/api/version
curl --fail --noproxy '*' http://192.168.42.132:11434/v1/models
```

Hermes runs in the pinned official Docker image. Its private persistent data is under `/opt/hermes/data`, with a shipped `default` profile and an Ansible-managed `local` profile that uses Ollama. Both profiles use one shared gateway. The container and s6 supervisors start as root; actual gateway/model processes run as the local Hermes UID/GID 1001. `Privileged=false` and no explicit Docker user namespace mode were reported in the November 8 investigation. This is application privilege dropping, not a rootless container. Ollama and its NVIDIA/Vulkan driver stay on the host; container-to-host inference uses loopback. The agent is not given the host Docker socket or Joy’s home directory. The dashboard is disabled.

On Eddie, fresh logins as either `hermes` or `denebeim` can run:

```bash
hermes                         # interactive local Qwen CLI
hermes --version               # reports Docker installation
hermes profile list            # local is the managed active profile
hermes -p default gateway status
```

The Hermes role installs root-owned `/usr/local/bin/hermes`. It runs `/usr/bin/docker exec` with the discovered service UID/GID (currently 1001:1001), absolute container CLI `/opt/hermes/bin/hermes`, and explicit HOME/HERMES_HOME=/opt/data. Stdin stays attached; a container TTY is allocated only when host stdin and stdout are terminals. Arguments pass through unchanged. Global `/etc/profile.d/deepthot-tools.sh` ensures /usr/local/bin is on PATH; `/etc/profile` loads it for login shells and a managed `/etc/bash.bashrc` block loads it for interactive non-login Bash shells. No per-user startup files or command links are required. The service account's old native command is preserved as `~/.local/bin/hermes.native`; its former command path is removed. Both users require their already-declared Docker access.

Profile selection was resolved November 9: `/opt/data/active_profile` was absent, so the CLI chose shipped `default` (Claude/provider auto), rather than configured `local` (Qwen/provider custom). Both configs were readable; CLI and observed gateway shared HERMES_HOME. Ansible now manages `active_profile` as `local` via `hermes_cli_profile`. Explicit `-p` still overrides it; a later Ansible run restores the declared active profile. Shared-gateway lifecycle commands explicitly select `-p default`. The local template explicitly disables shared-metrics collection and upload and settles the first-run choice.

Fresh SSH version/profile checks passed for both accounts, and the actual interactive host command reached the local/Qwen chat prompt without provider setup. One local inference through the host command as denebeim returned exactly `Eddie is online.` with exit 0. Targeted CLI/local-template convergence settled changed=0. The response took several minutes; full zero-to-configured rebuild validation is still pending. See HANDOFF.md/WORKLOG.md for evidence. Never dump raw environment or private configuration during diagnostics.

The original native installation and files are retained for rollback; its services are disabled after migration. See `HANDOFF.md` for state and rollback. Laptop files remain the source of truth; see `HERMES-DESKTOP.md` for the proposed workload split. The old one-off recovery entrypoints remain in Git history.

## Central Docker administration

Authenticate at SSH login. IPA group `docker-admins` controls passwordless `sudo docker` through rule `docker-admin-access` on explicitly listed enrolled hosts. This is root-equivalent access; manage the group in IPA. The host-local `docker` group grants direct socket access to the members declared for that host. No Docker TCP listener is needed.

The directory policy is a POSIX `docker-admins` group, the `/usr/bin/docker` sudo command, and the enabled `docker-admin-access` rule for that group and command with option `!authenticate` and order 100. The Docker role adds the enrolled FQDN idempotently for guests tagged both `docker` and `ipa`, using the controller ticket. Direct host membership was verified on this deployment. On retiring a host, remove its rule membership and IPA host record, then remove its scoped SSH trust artifacts. A Docker-only or DMZ VM is outside the IPA rule.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Record real deployment results separately from syntax/unit checks. Do not call a partial run accepted. Maintain a detailed handoff containing current branches/tickets, machine state, verification and pending actions before stopping.

## Pending terminal investigation

Owner reported `Warning: Input is not a terminal (fd=0)` during an interactive Hermes session, followed by unexpected command-input behavior. Reproduce the exact SSH invocation and inspect terminal handling in a later step. Earlier successful TUI launch does not establish that every SSH path handles stdin correctly. No change or extra inference test was made for this report.
