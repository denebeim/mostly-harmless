# WORKLOG

> Living project log for `mostly-harmless`.
> Updated as work is performed in this repository and during infrastructure sessions.
> This repository is currently **public**. Keep credentials, private keys, exact internal
> addresses, sensitive topology, and other operational secrets out of this file.

## Current mission

Establish `mostly-harmless` as the reproducible, backed-up source of truth for Deepthot:
infrastructure configuration, automation, scripts, services, and operational documentation.

The existing home-lab systems are the operational baseline. They should not be rebuilt merely
for consistency. Preserve useful working state and knowledge while allowing the architecture
to evolve deliberately.

## Project principles

- Restore and stabilize before optimizing.
- Prefer understanding and documenting the existing state over guessing.
- Preserve data, experiments, and working services.
- Make changes reproducible and record why they were made.
- Keep credentials and sensitive operational details out of this public repository.
- No destructive or disruptive changes without explicit approval.
- Distinguish verified facts from assumptions and open questions.

## Collaboration workflow

- Make ongoing AI-assisted changes on branch `ai`; merge into `main` at the daily
  collaboration checkpoint. Earlier published commits remain in existing history.
- Read-only inspection is authorized. Show diagnostic commands before execution
  and report useful results so the owner can follow the work.
- This does not authorize consequential infrastructure changes or publishing
  sensitive operational information.
- Use Eddie as the project-facing agent name. The local playbook entry point is
  now `eddie.yaml`; the existing machine identity and upstream software names are
  preserved. The renamed operational file remains ignored pending privacy review.

## Active priority: Eddie playbook recovery

The immediate acceptance criterion is a successful run of the existing playbook, now named `eddie.yaml`.
Keep the existing VM name. Inspect actual dependencies and side effects, then address
one meaningful failure at a time with the smallest reproducible correction.
The historical survey below is context, not a statement of current live state.

The immediate goal is to restore the primary agent VM (formerly called Hermes; now referred to
as Eddie) to useful operation, then use it as the primary local agent with access to external
AI models as needed.

### Current findings

- The VM already exists and is running.
- The NVIDIA Quadro K5200 was previously moved from Plex to this VM using the Proxmox GUI,
  and the user reports that the arrangement worked.
- The current VM configuration inspected during this session does not contain a PCI passthrough
  (`hostpci`) assignment.
- The GPU is currently bound on the Proxmox host to `vfio-pci`.
- The exact change that removed or altered the previously working assignment is not yet known.
- The current task is recovery, not a fresh GPU-passthrough design or general VM optimization.

### Next investigation

1. Review the fresh read-only survey with the owner and clarify unfamiliar VMs.
2. Finish tracing the existing Eddie playbook, inventory, variables, and dependencies.
3. Review consequential side effects with the owner before an infrastructure-changing run.
4. Run the playbook within the approved scope and address the first meaningful failure.

No configuration changes are authorized by this investigation list alone.

## Infrastructure notes

- The current running systems are generally the intended operational baseline.
- The Proxmox host, TrueNAS storage VM, Synology storage, and their dependencies must be treated
  as distinct components.
- Local thin-provisioned storage is nearly full; do not provision new disks there without
  checking current capacity.
- Some NFS-backed VM storage depends on the TrueNAS VM being available.
- Storage inventory and backup design remain future work; do not infer that network storage
  capacity is equivalent to free local physical capacity.

## Repository roles

- `deepthot-configuration`: historical configuration and accumulated DevOps reference.
  Valuable material, but not yet the complete reproducible system envisioned.
- `mostly-harmless`: the new project and intended source of truth for reproducible Deepthot
  infrastructure, automation, scripts, services, and documentation.

## Follow-up: golden images

After Eddie recovery, rewrite the existing image-building scripts for five
Deepthot-configured targets: Ubuntu 24.04 LTS and 26.04 LTS, current Debian, and
current and previous Rocky Linux. The owner explicitly selected the Ubuntu LTS pair.
Preserve the existing storage placement; review numbering before allocating or
changing template IDs. Existing scripts require review before execution because
they delete the supplied target VM before creation. No image build is authorized
by this backlog entry alone.

## Recovery scope update

The owner requested an Ansible-driven rebuild after read-only inspection for
valuable guest data, with the replacement named Eddie and existing NFS placement
preserved. The initial playbook run was stopped at that request; it did not reach
clean completion. Generic rebuild and firmware roles are now reviewable in Git.
The rebuild is explicitly gated, checks the target and source template, refuses
unexpected devices, records configuration privately, and checks for concurrent
configuration edits before deletion. Its tagged read-only preflight passed.
Operational entry points and full inspection logs remain ignored locally.

The first reproducible provisioning failure was a cloud-init network update
without an explicit VM ID. Added the existing target-ID variable to that task.
A public, privacy-reviewed patch records this correction and the firmware hook;
applying it to an isolated copy of the preserved source reproduced the local
role exactly. Subsequent retries use the ordinary playbook, not the destructive
rebuild entry point. Clean playbook completion remains pending.

Added a reusable Ansible host-key refresh for rebuilt guests. It checks VM and
guest identity through the trusted hypervisor, reads public keys through the
guest agent, privately backs up the workstation trust file, and updates only
the verified guest's entries. Authenticated SSH access passed with verification
enabled. A privacy-reviewed entry-point patch reproduces the corresponding
local playbook changes. Progress is mirrored into an ignored local log so the
owner can observe runs; full diagnostic output remains private. The overall
playbook has not yet completed successfully.

## Session log

### 2026-11-07 — Project baseline and Eddie recovery

- Confirmed the project direction: start from the currently operating lab and build toward
  complete, reproducible configuration in `mostly-harmless`.
- Confirmed that Eddie is the immediate priority and that the GPU had previously worked in it.
- Compared current Plex and Eddie VM configurations. Neither currently shows a `hostpci`
  assignment; the host GPU is bound to `vfio-pci`.
- Identified historical Proxmox configuration and running QEMU command lines as the next
  evidence to inspect.
- No infrastructure changes made during this investigation.
- Next action: inspect Proxmox GPU history and running QEMU command lines.

### 2026-11-07 — Desktop inspection and fresh read-only survey

- Read the full recovery handoff and confirmed local shell/filesystem access.
- Located the reference playbook in the separate historical configuration checkout,
  on branch `ai`; it has existing inventory modifications, which were preserved.
- Confirmed the canonical checkout initially contained only project baseline files.
- Verified the historical checkout's existing virtual environment uses Ansible core
  2.21.5. A syntax-only playbook check passed with the static inventory, but neither
  playbook target matched that inventory. No playbook tasks were executed.
- Inspection found provisioning, VM reconfiguration, disk resizing, guest package
  upgrades, identity enrollment, Docker configuration, and agent installation/service
  management in the dependency chain. Execution requires scope review first.
- At the owner's request, performed a fresh read-only SSH survey using existing
  credentials. Verified Debian 12, Proxmox 8.2.4, kernel 6.8.8-1-pve, a Supermicro
  X10DAI motherboard, dual Xeon E5-2680 v4 CPUs, and 188 GiB RAM.
- The VM list and running/stopped states matched the historical handoff. The target
  is running; the list reports 16 GiB RAM and a 40 GB boot disk. This does not resolve
  the historical discrepancy with the saved VM configuration.
- No infrastructure changes made. Paused for the owner's VM context before further
  inspection or playbook execution. Sensitive inventory/topology details remain out
  of this public log.

### 2026-11-07 — Intended dynamic inventory traced

- Owner clarified that `inventory/proxmox.py` in the historical checkout is the
  intended inventory generator. The static inventory used for syntax checking is
  not authoritative for this workflow.
- Confirmed `ansible.cfg` selects the whole inventory directory, rather than the
  script alone; multiple inventory sources can therefore participate.
- Read the full script before execution. Its infrastructure calls retrieve API
  and guest-agent information; no infrastructure write calls were found.
- Direct `--list` invocation failed locally because the shebang-selected Python
  lacks `six`. Explicit invocation with the checkout virtual environment passed
  that import and failed with `KeyError: 'include'` while loading configuration.
  Neither invocation reached API authentication or generated inventory.
- The sibling JSON has an inventory-shaped top-level `all` key rather than the
  connection settings expected by the script. Required connection environment
  variables were absent in the tested shell. Values and credentials were not logged.
- Also found YAML output where the Ansible script inventory interface expects
  JSON. No corrections made yet; existing inventory edits remain preserved.

### 2026-11-07 — Working configuration imported and clean controller established

- At the owner's direction, imported 216 existing regular configuration/support
  files into this checkout at the repository root. Preserved the historical
  checkout, its existing edits, and its Python environment. Did not copy its Git
  metadata, virtualenvs, generated dependency trees, certificates, or private key.
- Imported both existing Python requirement files, both Galaxy manifests, and
  the empty modules Galaxy manifest. Built a fresh `.venv` with Python 3.12.4;
  installed the actual Python requirements and recorded resolved versions in
  `requirements-controller.lock.txt`. `pip check` passed; Ansible core is 2.21.6.
- Installed all five pinned Galaxy roles and all six collection entries into
  ignored project-local directories. The inherited Git collection entry tracks
  `master`; its lack of an immutable pin is documented in `CONTROLLER.md`.
- Configured the intended dynamic script directly and project-local controller
  cache/temp paths. Migrated only needed connection environment assignments to
  an ignored mode-0600 local file, using the new Python environment.
- Corrected inventory JSON output, optional filter defaults, missing-template
  handling, and node inclusion in this checkout only. The real API query and
  Ansible inventory parsing succeeded; both playbook targets are recognized.
  An offline check covers explicit/missing template flags and template exclusion.
- The imported playbook passed syntax checking through the intended dynamic
  inventory. Existing group-name warnings remain; no group renaming was attempted.
- Public tracking is restricted to reviewed controller configuration, generic
  inventory code, manifests, and documentation. Imported operational playbooks,
  roles, inventory data, and deployments remain local and ignored pending privacy
  review. They are not backed up by the public remote; this migration is not yet a
  complete reproducible public configuration backup.
- No infrastructure-changing tasks have run. The next gate is review of the
  existing playbook's consequential provisioning and guest configuration effects.

## How to maintain this log

At each meaningful work milestone, update:
- current objective and status;
- verified findings (with evidence or references where practical);
- changes actually made and how they were verified;
- unresolved questions, risks, and dependencies;
- the next concrete action.

Use dates when known. Do not invent timestamps or imply continuous monitoring. This log is a
session-maintained record, not an autonomous live feed.

### 2026-11-07 — Restore Galaxy IPA dependency

- Reference `~/ansible/deepthot-configuration/roles/machines/ipa` calls `freeipa.ansible_freeipa.ipaclient`. The collection was absent locally and from the current manifest.
- Installed FreeIPA collection 1.17.0 into project-local collections and pinned that version in collections/requirements.yml, preserving existing manifest edits. Galaxy reported installation successful. No guest configuration changed.
- The local machines/ipa wrapper is still absent and eddie.yaml does not invoke it. Review and restore the wrapper before enrollment automation runs.
- Design target: DHCP reservations and DHCP-provided network settings; keep current Hermes identity until the later DNS rename.
- Live services DHCP read is pending: SSH as ansible was rejected. Inspect reference connection settings next.
- Diagnostic command output is appended to eddie-session.log; historical logs are not current-state evidence.

### 2026-11-07 — Hermes static networking interim decision

- Owner directs static networking for Hermes for now: IP 192.168.42.132/24, gateway 192.168.42.1, DNS 192.168.42.2, search domain local.deepthot.org. No networking change applied in this step.
- Long-term design remains service-managed networking: when Eddie is created, automation should update its MAC in the Pi-hole TOML DHCP reservation, with DHCP supplying guest networking.
- Private Pi-hole snapshot is ~/projects/pihole.toml; never commit it. Future deployment should use a .j2 template with protected secrets. Snapshot shows DHCP enabled and a Hermes DNS record, but no matching reservation in dhcp.hosts. External dnsmasq files are enabled and have not been inspected.
- Next step: implement explicit static cloud-init settings and a reproducible correction for the existing Hermes guest, preserving other network configuration.

### 2026-11-07 — Hermes user SSH milestone achieved

- Added explicit static DNS/search settings to eddie.yaml and Proxmox create_vm IP configuration (module arguments nameservers/searchdomains); preserved current static IP and gateway. These Proxmox task changes have not been applied to VM metadata yet.
- Added machines/network role, invoked before Docker, to correct existing eth0 Netplan DNS settings using netplan set. Applied that role successfully to Hermes (ok=3, changed=2, failed=0).
- After DNS correction, short-name h2gt2g resolved and IPA returned denebeim with /nethome/denebeim. Autofs still reported its earlier DNS failure; restarting autofs cleared it. Added an autofs try-restart handler following network changes to reproduce the correction.
- Verified SSH by hostname using `ssh -F /dev/null -XA -o BatchMode=yes denebeim@hermes`: exit 0; identity denebeim, HOME and PWD /nethome/denebeim, expected NFSv4 mount, Docker active, forwarded SSH_AUTH_SOCK and DISPLAY present. -F /dev/null bypasses the controller SSH configuration ownership/permissions error previously observed. No X application was launched.
- Full eddie.yaml provisioning has not been rerun; machines/ipa wrapper restoration remains outstanding. Existing IPA enrollment worked for this milestone.
- Diagnostic output remains in eddie-session.log. Private Pi-hole TOML was not copied or committed.

### 2026-11-07 — Hermes Agent installed on Hermes

- Applied existing local Hermes role after adding acl to its apt dependencies and selecting /bin/bash for installer shell (uses pipefail). Added no_log to environment-file deployment.
- Ansible role completed: ok=20, changed=10, failed=0, unreachable=0. Installer took several minutes; observed runtime setup and storage I/O waits, with no recent kernel warnings.
- Verified Hermes Agent v0.23.0, stable, Python 3.14.9; --version and --help succeed as service user hermes. Cron timer active; messaging gateway disabled per existing defaults.
- No model inference verified: Ollama was inactive at preflight, and no cloud credentials were supplied in this isolated role run. Defaults select auto provider and anthropic/claude-opus-4.6; model/provider configuration is the next step.
- Full eddie.yaml provisioning remains untested; role run used targeted inline inventory to avoid unrelated provisioning changes. All diagnostic output appended to eddie-session.log.

### 2026-11-07 — Restore K5200 passthrough

- Host GPU 0000:81:00.0 (Quadro K5200) and audio 81:00.1 were bound to vfio-pci; VM 314 had no hostpci configuration. No matching GPU assignment found in other VM configs. Missing PCI attachment explains guest GPU absence independently of driver licensing. Prior working assignment mechanism not recovered from reference automation or selected shell history.
- Owner authorized restoring passthrough. Added hostpci0 0000:81:00,pcie=1 and serial display settings to eddie.yaml; parameterized vga/serial in create_vm. Added restore_hermes_gpu.yaml and applied hardware changes with graceful shutdown/start. Ansible completed without failures.
- Trusted guest-agent verification confirms guest sees K5200 at 01:00.0 and associated audio device. NVIDIA utilities and proprietary guest driver are not installed; compute acceleration remains unverified.
- After restart SSH keys were newly generated and DNS search domain was empty. Verified replacement keys via trusted guest agent and refreshed known_hosts with existing role and private backup. Set Proxmox metadata nameserver/searchdomain explicitly and reapplied existing guest DNS role; its autofs restart handler restored NFS home. The precise cloud-init trigger for key regeneration is not established.
- Final ssh -XA as denebeim succeeds, starts in /nethome/denebeim on the expected NFS mount; Docker active.
- Next: guest NVIDIA driver and Ollama compatibility with legacy K5200, before claiming GPU inference works.

### 2026-11-07 — GPU-backed local Hermes inference verified

- Restored setup_hermes_vm.yaml based on reference driver/Ollama flow. Installs matching kernel headers, nvidia-driver-470/nvidia-utils-470 without recommends, loads nvidia module, installs Ollama, and starts its local API. Excluded inherited unconditional NVIDIA container-runtime installation; no container GPU runtime was needed for native Ollama.
- NVIDIA DKMS build succeeded on 6.8.0-149-generic; nvidia-smi reports Quadro K5200, 8126 MiB, 470.256.02. No reboot required.
- Ollama 0.40.15 installed and API responds. Installer environment now pins 0.40.15 for future installs. Pulled reference qwen3.5:4b (Q4_K_M, 4.2B).
- CUDA documentation excludes this legacy card/driver, but actual Ollama auto-detected Vulkan and offloaded 33/33 model layers. ollama ps reports 100% GPU. Direct inference returned 'Eddie is online.' (6 output tokens in approximately 0.52s, excluding prompt processing and cold load); this is a smoke test, not a representative benchmark.
- Configured Hermes provider custom, model qwen3.5:4b, endpoint http://127.0.0.1:11434/v1 using its existing config template. Mirrored model/gateway settings in eddie.yaml so subsequent role runs preserve them.
- Initial Hermes prompt failed service_identity_unverified. Installed Hermes v0.23.0 requires a gateway runtime even for CLI requests; inherited disabled unit used EnvironmentFile and --no-supervise, conflicting with runtime identity checks. Updated template to explicit HOME/HERMES_HOME and --external-supervisor; .env remains loaded by Hermes itself. Enabled gateway through reproducible local_model role tasks.
- End-to-end Hermes CLI test as service user hermes returned 'Hermes is online.' with exit 0. Gateway active; Ollama reports 100% GPU. No cloud inference credentials were needed or supplied. This verifies a simple reply; tool execution and long-context agent workloads remain untested.
- Driver/Ollama installation play: failed=0; model deployment and gateway correction: failed=0. Full eddie.yaml end-to-end provisioning still outstanding (including IPA wrapper restoration). Logs appended to eddie-session.log.

### 2026-11-07 — Local checkpoint before destructive rebuild smoke test

- Owner requested committing current work, then destroying Hermes for a rebuild smoke test. Reviewed operational playbooks and supporting roles are explicitly included in the local commit; private inventory, credentials, Pi-hole snapshot, dependency installations, logs, and caches remain excluded. No push requested.
- Added separate destroy_hermes.yaml with exact VM identity/disk checks, private configuration record, graceful shutdown, configuration digest guard, and post-removal verification. Physical passthrough hardware and unrelated VMs/storage are not deletion targets.
- Pi-hole web endpoint http://services/admin/ redirects to its login page; web authentication requires an existing usable password, not available in this session. No Pi-hole settings changed.
- Checkpoint captures current working installation automation, not proof of a clean rebuild. IPA wrapper restoration and full end-to-end eddie.yaml execution remain outstanding.
