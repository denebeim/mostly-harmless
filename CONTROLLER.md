# Deepthot Ansible controller

Run from this checkout; `~/ansible/deepthot-configuration` is the working reference.

## Operating contract

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

The private `.envrc` selects the project Python and inventory environment. A valid controller Kerberos ticket (`kinit admin` if needed) is required only for a new `ipa` client enrollment, not for untagged guests or the local Hermes service user.

`create_vm.yaml` provisions/base-bootstraps, `join_deepthot.yaml` joins tagged clients, and `install_docker.yaml` configures tagged Docker hosts. `vm.yaml` composes these and the optional applications. Invoke a shared entrypoint with a private `-e @vm-spec.json` declaration, or use a minimal machine file such as `eddie.yaml`. Destructive cleanup is a separately reviewed operation, never implicit in provisioning.

A declaration requires `vm.name`, `vm.id` and `vm.ip`. Defaults: node/storage `heartogold`, template `deepthot-24-04`, 2 cores, 2048 MiB, 12G root disk, serial console, gateway `192.168.42.1`, DNS `192.168.42.2`, domain `local.deepthot.org`. Declare `vm.tags: []` for no optional roles. Disks only grow; NIC MACs are preserved. `vm.update_packages` defaults false; test guests do not upgrade. `vm.local_users` creates local service accounts; `vm.docker_members` optionally enforces exact Docker group membership. Eddie declares only local `hermes` in that group.

First-use SSH trust is isolated by VM ID and MAC, then checked/refreshed through the newly installed guest agent into that same file. It initially relies on the controlled LAN/expected IP (TOFU); it is not a claim of cryptographic pre-boot identity verification. Existing pins reject unexpected changed keys. No global host-key checking is disabled.

## Eddie and shared inference

Eddie is VM 314 at `192.168.42.132`, with the K5200 passed through at host `0000:81:00`. Its GPU runs local Qwen via Ollama's Vulkan backend; do not assume modern CUDA support. Eddie keeps `ollama_listen_host: 0.0.0.0` and a controller-side LAN API check. Other hosts default to loopback. Native desktop clients may use `http://192.168.42.132:11434/v1`; only trusted LAN access is intended. No firewall manager, public forwarding or broad browser-origin permission is added.

```bash
curl --fail --noproxy '*' http://192.168.42.132:11434/api/version
curl --fail --noproxy '*' http://192.168.42.132:11434/v1/models
```

Laptop files remain the source of truth. Docker migration and desktop/server workload split are tracked separately in issues #4 and #5. The old one-off recovery entrypoints remain available in Git history, not as current operational playbooks.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Record real deployment results separately from syntax/unit checks. Do not call a partial run accepted. Maintain a detailed handoff containing current branches/tickets, machine state, verification and pending actions before stopping.
