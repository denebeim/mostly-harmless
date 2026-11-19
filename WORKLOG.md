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

### 2026-11-07 — Base Eddie rebuild smoke test

- Owner explicitly requested destroying Hermes, releasing resources, recreating VM 314 as Eddie without upgrades, then creating Pi-hole records through the visible browser.
- Ran destroy_hermes.yaml successfully (failed=0); verified no VM 314 remained and pvesm list heartogold --vmid 314 returned no allocated volumes. Preserved the old configuration privately under .ansible/rebuild-records.
- Added create_eddie.yaml, a base-VM-only playbook using the existing template/create_vm role. Explicit ciupgrade false is applied before first boot through a new optional create_vm task. No guest application roles or package upgrades ran. Static IP remains the authorized interim design.
- VM 314 named eddie is running, 8 cores/16 GiB/40G, serial console and K5200 passthrough configured. Guest SSH confirms eth0 MAC BC:24:11:47:69:B9 and IP 192.168.42.132/24. Cloud-init completed, errors empty; only deprecated user-field warnings.
- Source template lacks qemu-guest-agent. Interrupted the optional agent-only retry loop (controller exit 99) after successful creation, serial login prompt and SSH verification. Updated base playbook to wait for SSH without requiring agent installation. Verified SSH through an isolated first-use known-hosts file under .ansible; existing workstation entries were not changed.
- Authenticated Pi-hole session was available in visible browser; created local A records eddie and eddie.local.deepthot.org -> 192.168.42.132. UI confirmed both entries; direct DNS queries to 192.168.42.2 returned that address for each. Screenshot saved /tmp/eddie-dns-records.png. Existing Hermes DNS record retained; no DHCP reservation created in this static-network smoke test.
- Pi-hole record changes are recorded here; deployment templating/secret separation remains future work. Private Pi-hole TOML not copied or committed.
- Stopped at base VM + DNS milestone; IPA enrollment, user NFS-home login, Docker, Hermes and Ollama are deliberately not provisioned on fresh Eddie yet.

### TODO — LAN DNS/DHCP architecture (owner preference, 2026-11-07)

- [ ] Discuss Pi-hole versus IPA DNS versus traditional BIND9 and separate DHCP services on `services`. Owner prefers familiar, explicit zone/service configuration and is considering returning to BIND9 plus isc-dhcpd; evaluate the DHCP implementation when planning migration. This is a discussion item, not authorization to migrate now.
- Current decision: Pi-hole owns LAN DNS; do not use IPA as the LAN DNS authority. IPA remains intended for identity and automount. Actual IPA DNS/forwarding configuration has not been audited.
- Desired DNS model: zone local.deepthot.org with an SOA and one relative host A record per machine (e.g. eddie A 192.168.42.132). Verify Pi-hole SOA/domain behavior; do not equate its local host list with a BIND authoritative zone.
- [ ] Consolidate Eddie's duplicate short-name/FQDN Pi-hole entries after verifying local-domain expansion. Both entries currently remain; no DNS changes made for this documentation update.
- Long-term network source of truth: DHCP reservations map VM MACs to stable IPs and supply DNS/domain settings; creation automation updates the reservation MAC. Static guest settings are an interim decision. Future configuration uses templates with separately protected secrets; never commit the private Pi-hole TOML.

### 2026-11-07 — Prepare owner-run full Eddie provisioning

- Owner wants to execute Ansible from the VSCodium terminal. No infrastructure provisioning was executed during preparation.
- Updated eddie.yaml to target Eddie/VM 314, preserve ciupgrade false, bootstrap qemu-guest-agent over the smoke-tested isolated SSH trust file, then refresh normal controller trust through the existing verified guest-agent role. The terminal command supplies -F /dev/null for the known controller SSH-config issue. Bootstrap does not disable host-key verification.
- Restored machines/ipa using the existing Galaxy client role: explicit domain/realm/server, default automount location, NFS/SSSD prerequisites, hostname and autofs configuration. Omitted IPA DNS registration/resolver takeover, the generic package-upgrade wrapper, and unconditional automount uninstall. IPA enrollment password is a private runtime vars_prompt, skipped when already supplied as a variable; no password stored in playbooks.
- Added explicit Hermes service-account/group/home creation for a fresh guest. Corrected Docker swap fact reference to ansible_facts.swaptotal_mb.
- Imported existing GPU/Ollama/model playbook at the end, with configurable ai_target selecting Eddie. Syntax validation passes with a local test inventory. Actual enrollment, installation and final inference must be verified by the owner-run playbook; not claimed complete.
- New base entrypoint and IPA wrapper are allowlisted so they appear for review in Git. Existing uncommitted work preserved; no new commit or push.
- Run from project root after loading .envrc and .venv: PYTHONUNBUFFERED=1 ansible-playbook eddie.yaml --ssh-common-args='-F /dev/null' 2>&1 | tee -a eddie-session.log (enable shell pipefail). Output remains in the same append-only session log.

### 2026-11-07 — Full-run acceptance target includes package updates

- Owner clarified that the upcoming full run should deliver updated packages, IPA, Docker, and Hermes using Ollama. This supersedes the no-upgrade restriction for the earlier base-VM smoke test.
- Added explicit apt safe upgrade with refreshed indexes, a conditional reboot and fact refresh before application roles. Kept cloud-init automatic upgrades disabled so Ansible controls the upgrade stage.
- Added final checks for IPA account/home, autofs access, Docker daemon, required services and an actual Hermes response via the configured local Ollama model. Full provisioning remains owner-run and has not been executed by the agent.

### 2026-11-07 — Enrollment uses controller kinit admin ticket

- Owner clarified expected workflow: kinit admin, then run Ansible without password prompts. Removed the IPA vars_prompt. Added a local klist -s preflight before provisioning; missing/expired tickets stop with a kinit admin instruction.
- Galaxy ipaclient join requires a password/keytab rather than directly consuming the controller cache. The restored wrapper now runs a system-Python IPA helper locally, authenticating through the existing ticket to create/reset only the target host enrollment OTP. A stale host key is disabled only when the fresh guest has no IPA configuration; the existing host object is preserved.
- OTP handling uses no_log and noncached in-memory facts; only the one-time host credential goes to the guest. No admin password, keytab or ticket is copied. Existing configured clients skip OTP generation.
- Controller needs the system FreeIPA Python libraries and existing IPA configuration. Those libraries are installed here; actual ticket/RPC enrollment awaits the owner-run playbook. No infrastructure changes made during this edit.

### 2026-11-07 — Acceptance failure: cold Hermes session startup

- Owner-run acceptance reached the final prompt with IPA identity/home, Docker, driver, Ollama/model and all service checks passing. Final prompt failed: gateway did not answer session.create, rc 1; full-run recap Eddie ok=104, changed=51, failed=1.
- Current gateway remained active without crashes/restarts. Logs showed cold plugin/tool/model-metadata initialization completed about 12 seconds after the CLI disconnected. Installed source uses DEFAULT_RPC_TIMEOUT=30 with no configuration hook found. This identifies a cold-session startup deadline issue; no evidence of model inference failure in that attempt.
- Retested only the same Hermes prompt after initialization: 'Eddie is online.', exit 0.
- Added at most two retries with 5-second delay only for the exact gateway session.create timeout; other errors and incorrect/missing responses still fail. Syntax validated. A new full successful playbook recap is still required to claim a clean end-to-end acceptance run.

### 2026-11-07 — Prepare Eddie brought-to-life pull request

- Owner requested a commit, changelog and PR to main for manual diff review. Added CHANGELOG.md and updated controller instructions with current entrypoints, ticket/SSH bootstrap prerequisites and validation limits.
- Reviewed pending files for credential material; private inventory, .envrc, Pi-hole TOML, logs, caches, installed dependencies and SSH trust records remain excluded.
- PR includes prior ai-branch checkpoints plus the integrated Eddie provisioning changes. No infrastructure tasks run during PR preparation.

### 2026-11-07 — Address selected Sourcery review threads

- Owner selected issues 1, 2, 6 and 9 for implementation and requested resolving
  those conversations and resubmitting PR #1. Other findings remain open.
- Expanded both destructive disk allowlist checks to EFI/TPM keys. Introduced a
  shared guarded-destruction role using an atomic qm set --lock create --digest
  acquisition; normal config writers cannot change the VM between review and
  deletion. It holds the lock through graceful shutdown, verifies the locked
  digest and uses normal qm destroy with only its own lock bypassed. Cleanup
  refuses to clear a changed/uncertain lock. This also protects shutdown once the
  lock is acquired, but issue 4 was not selected for thread resolution.
- Read-only installed Proxmox source/help checks confirmed digest comparison and
  lock setting occur under the config mutex, and shutdown/destroy support root
  skiplock. No live VM changes or destructive tests were performed.
- Review #6's entrypoint/create_vm files were already tracked; added explicit
  allowlist entries for reviewed dependencies and a clean-export syntax check.
- Timeout retries now inspect combined stdout/stderr. Eight offline regression
  tests pass, along with integrated and destructive-entrypoint syntax checks.

## 2026-11-08 — Operating model reset (supersedes earlier workflow)

- Owner authorizes lifecycle refactoring, a disposable VM test and full ticket/branch/PR completion; then Docker-based Hermes migration on Eddie and current-feature/workload-split investigation. Issues: #3 optimization of deepthot base vm behaviors; #4 Docker Hermes; #5 desktop/server feature investigation.
- Significant changes belong in this tracked worklog. All command stdout/stderr appends to ignored eddie-session.log through a streaming redactor; never log passwords, tokens or private PEM material. Static IPs are acceptable. The log is not tracked.
- Per-machine playbooks must declare the machine minimally and converge absent-to-installed via shared roles gated by VM tags. One-off modification/recovery playbooks are not retained as normal entrypoints. VMs may omit IPA, Docker or all application roles.
- PR #1 was squash-merged into main as 5eb1a4d. Created codex/3-optimize-base-vms from main. Existing LAN-Ollama work in CONTROLLER.md, eddie.yaml and setup_hermes_vm.yaml was privately backed up in .ansible/change-backups/pre-optimization-20261108.patch and preserved while extracting it into shared roles.
- Eddie preflight: K5200/470.256.02 visible; Ollama 0.40.15 reports qwen3.5:4b at 100% GPU with context 65536; host Hermes and Ollama services active. Docker and Hermes privileged inspection will use sudo; initial unprivileged checks lacked permission. No migration yet.
- Added shared create_vm/join_deepthot/install_docker/vm entrypoints and base/GPU/Ollama roles. Proxmox helper compares live settings, preserves NIC MAC, resizes upward only and reports actual tags. Base bootstrap uses private per-MAC first-use SSH pinning, installs guest agent, then verifies trust through the hypervisor into the same file. Cloud-init upgrades disabled; declared guest upgrades are an explicit base-role option.
- Test target: deepthot-base-test, VM 8314, 192.168.42.250/24, 2 cores, 2 GiB, 12G, no tags; ID/name absent and IP had no ping/neighbor response. Storage heartogold has capacity; other storage/services were only observed and not modified. Tests must never use Eddie's ID or GPU.
- A file-generation command initially used system Python without PyYAML; it was rerun successfully with the project virtualenv. No managed host was affected.

- Owner steering: preserve the pending LAN Ollama listener changes. Test VMs must not run package upgrades. Eddie declares local user/group hermes and exact Docker membership [hermes]; that service account is not enrolled in Kerberos. Optional local-user and exact Docker-membership declarations now live in the shared roles.

- Disposable VM 8314 absent-to-running test passed with no optional tags. After replacing timestamp-only SSH backups with VM/keyset-keyed backups, the settled repeat run reported changed=0 for both deepthot-base-test and heartogold; IPA/Docker/app roles skipped and package-upgrade tasks skipped. Starting a Docker-only tag test on the same disposable guest, without IPA or upgrades. Docker role now delegates package installation to Galaxy and enforces membership only when explicitly declared; removed unrelated Kubernetes swap/kernel policy.

- Removed permanent one-off create-Eddie, restore-GPU, destroy-Hermes and setup-Hermes playbooks plus historical patch files from current entrypoints; their history remains in Git. Shared roles own behavior. Replaced controller documentation with the operating contract, generic entrypoints, tag gates, local-account policy and preserved LAN Ollama usage.

- Docker-only disposable deployment passed, and its settled repeat reported changed=0 on guest and hypervisor. IPA and package upgrades remained disabled. Guarded teardown of VM 8314 passed; cluster inventory and storage list confirm no VM or owned volumes remain. IPA confirms no test host entry existed. No controller/hypervisor global SSH entries matched the temporary name/FQDN/IP; its private per-MAC trust and backup files were removed. Unrelated Kerberos tickets and caches were retained.

- Lifecycle PR #6 opened at commit cfe9db2; security scan passed. Began separate issue #4 branch codex/4-eddie-hermes-docker. Official amd64 stable image pinned to digest 0dd31821…85ad76; container read-only device probe sees K5200 nodes. Native Ollama remains the working GPU inference backend. Docker migration stages private persistent state, keeps shipped default separate from local profile, and retains original native data for rollback. No Docker socket is mounted into the agent.

- PR #6 squash-merged at d0849ca; #3 closed automatically, GitGuardian clean. On Eddie the native state copy completed. First container gateway command rejected starting a named profile gateway: installed 0.23.0 multiplexes profiles through the default gateway. Adjusted the role to start the shared gateway while preserving the default model settings. Future migration copies run as the local service user.

- Eddie cutover succeeded: shared container gateway serves shipped default and local Qwen profiles, exact local smoke response passed, and a configuration-only repeat was ok=15/changed=0/failed=0. Ollama stayed at 100% GPU with 65536 context while the test ran; controller LAN model list passed. Smoke completion took several minutes, so no performance improvement is claimed. Container process runs as local hermes UID/GID 1001, sees GPU nodes and has no Docker socket. Hermes callback listener is loopback-only; Ollama remains LAN-accessible by design. Host native gateway and timer disabled; original data/install kept for rollback.
- Confirmed SSH as denebeim to Eddie enters /nethome/denebeim. SSSD domain online; both names resolve to 192.168.42.132. Docker group is the local group with only hermes, per prior instruction; no IPA fault accounts for a denebeim Docker socket denial.
- Recorded issue #5 investigation and recommended laptop-local file tools with Eddie inference in HERMES-DESKTOP.md. Added HANDOFF.md for current operational state and rollback. No automatic cloud fallback or remote Desktop UI acceptance run.

- PR #7 squash-merged at fdec47d and closes #4/#5. Removed ignored scratch test playbooks/inventory; kept private rollback data and log.
- Owner requested centrally managed Docker administration and login-once authorization as the broader design. Created IPA POSIX group docker-admins with denebeim, and sudo rule docker-admin-access for /usr/bin/docker, order 100, !authenticate, explicitly scoped to verified enrolled hosts. Hostgroup-only matching did not surface in SSSD; direct Eddie membership did. Removed temporary hostgroup and kept local Eddie docker group unchanged. Passwordless sudo Docker verified from fresh SSH on Eddie.
- Scoped rule to Mailcow and Mastodon after guest agent confirmed Docker and enrolled host identities. Their SSSD refreshes failed because root filesystems were already full. Regenerable APT cache cleanup restored both SSSD services without touching logs or Docker data. Mailcow still had IPA DNS resolution failures; Mastodon reached LDAP but needs verified sudo. Mailu lacks a matching directory host record, DMZ is not enrolled, and stopped guests were excluded. Opened #8 for these remaining hosts and durable capacity fixes. Added idempotent host registration to the IPA+Docker role path; live repeat against Eddie returned already registered.

## 2026-11-16 — Voice shortcut API fallback feasibility and logging correction

Inspected current /home/denebeim/.local/bin/chatgpt-voice-toggle: it launches/focuses /usr/bin/chatgpt and emits Ctrl+Alt+Shift+F12 through uinput. It has no API transport, model selection, key handling, quota signal or fallback provider. Left mouse/Voice setup unchanged. Built-in ChatGPT Voice account experience cannot be turned into a provider-routing client merely by changing that key-emission script; no supported API-key override/fallback was established in current official documentation.

Google comparison: repository roles/setup-gemini/scripts/agent.py has GEMINI_API_KEY and GEMINI_PAID_API_KEY branches, but the quota branch only replaces client, not existing chat; the retry/preservation path is incomplete. roles/setup-gemini/files/gemini-toggle references a web_agent.py absent at that location. Live ~/.local/bin/gemini-toggle is still the distinct browser-focus implementation inspected previously. Do not treat this source as proof a working Google API failover is deployed. No Google changes or credential probes.

Official OpenAI sources fetched November 16: https://learn.chatgpt.com/docs/features/voice (built-in subscription-based Voice, task integration); https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini (Free tier not supported); https://developers.openai.com/api/docs/pricing (mini audio $10 input/$20 output per million tokens, text $0.60/$2.40; GPT-Live $0.05/minute plus backend/tools); https://developers.openai.com/api/docs/guides/chatgpt-api-credits (eligible paid Pro/Business subscription benefits can cover Realtime/GPT-Live, credits-first then purchased credits, do not increase signed-in ChatGPT/Codex limits; eligibility/account activation unverified). No unconditional free OpenAI voice API tier promised. Existing Pro/Business credits are a possible allowance, not an independently free tier.

Recommendation: preserve working built-in Voice shortcut. If API failover is required, add a separate optional client rather than silently replace the current assistant/task experience. Candidate lower-cost paid direct speech model is gpt-realtime-2.1-mini; GPT-Live is closer to a separate voice frontend/backend design and adds per-minute plus backend/tool costs. Custom client does not automatically inherit ChatGPT history, tasks, tools or permissions. Required next decision: whether a separate API voice client is acceptable; if yes check credit eligibility, select free-primary meaning (eligible credits or separately evaluated local/other provider), and spending budget before billable use. No API request, billing change or client replacement performed.

Logging audit found checked-out scripts/log-session.py had reverted to eddie-session.log default and logged argv despite current AGENTS instructions. First three wrapped diagnostic runs landed in that old file; recovered their output into existing /home/denebeim/projects/mostly-harmless/chat.log, left old logs intact, restored default and current CONTROLLER/HANDOFF paths, removed argv metadata, set existing chat.log mode 0600 and creation mode 0600. Verified random stdout marker in exact chat.log, then explicit stdout/stderr marker plus exit 7 preserved in that same file. All commands remain wrapped. Source/browser tool results are summarized here, not shell-intercepted. Preserved unrelated requirements.txt change.


## 2026-11-17 — Read-only browser-history investigation for November 16

Owner request: inspect benjymouse browser history for November 16, 2026 local time, locating YouTube videos reached from Facebook or Mastodon about Pete Hegseth, dismissed officers subsequently elected to Congress, and an incoming member who says he attended school with Hegseth. Follow-up explicitly authorized this WORKLOG entry; no other repository edits authorized. Referenced ChatGPT chat: 6afc0745-839c-83e8-8b9d-ad77764bf8ef, “Draft Post Analysis.” Its assertions were treated as leads, not evidence.

Method and scope:
- Local hostname confirmed benjymouse.local.deepthot.org. Search interval America/Phoenix (UTC−07:00), 2026-11-16 00:00:00 inclusive through 2026-11-17 00:00:00 exclusive; UTC interval 2026-11-16 07:00:00 through 2026-11-17 07:00:00. Converted Chromium microseconds since 1601 and Firefox Unix microseconds explicitly.
- Discovered 17 history databases under ~/.config, ~/.mozilla and ~/snap: current Chrome Default/Profile 2/Profile 4; seven google-chrome.old profiles; two Firefox profiles; snap Chromium Profile 2; snap Skype Firefox; and three Codex browser/partition databases. No history databases discovered under ~/.var/app.
- Initial SQLite mode=ro/query_only reads encountered locks on active Chrome/Firefox and an inaccessible Firefox database. Retried using temporary byte copies of databases and available -wal/-shm companions, opened copied databases mode=ro with query_only enabled. Temporary copies were removed automatically. Originals were never opened for writing; no browser restart, configuration change, history deletion or checkpoint requested. Byte copies of live databases are not guaranteed transactional snapshots.
- Active Firefox profile had 157 visits in the interval and Chrome Profile 4 had four; remaining databases returned zero. Firefox had two watch-page candidates, both unrelated music; neither supports the requested topic. One music visit had a Mastodon referrer, but it is excluded from this report. No matching Hegseth/Lacore URL or title and no matching YouTube video found. Social redirect URLs containing YouTube were also checked in that Firefox day window; none found. No relevant exact video URL/title/visit timestamp can therefore be reported from local history. Counts are diagnostics, not a disclosure of unrelated browsing content.

Independently retrieved evidence (accessed November 17):
1. “Women veterans increase their ranks in Congress, including ousted admiral,” Jennifer H. Svan, Stars and Stripes, November 9, 2026: https://www.stripes.com/veterans/2026-11-09/women-veterans-midterms-hegseth-23411610.html . Opened full article. Reports Nancy Lacore won a House race after Hegseth removed her as Navy Reserve chief. Identifies numerous other veteran winners but does not establish that those winners were officers fired by Hegseth. Thus supports a singular example, not the broader plural claim.
2. CBS’s November 8 interview identifies Lacore as congresswoman-elect and confirms Hegseth removed her in August 2025. Transcript: https://www.cbsnews.com/news/nancy-lacore-south-carolina-democrat-face-the-nation-transcript-11-08-2026/ . Opened transcript, including interview discussion of removal. Source video landing page: https://www.cbsnews.com/video/rep-elect-nancy-lacore-says-she-was-never-given-a-reason-why-pete-hegseth-fired-her/ . Listed duration 05:26. This is a public source lead, not a recovered history match or proof of watching it. No YouTube equivalent or personal viewing timestamp established.
3. AP election-call search result, November 6, 2026 23:52:11 UTC: “Democrat Nancy Lacore wins election to U.S. House in South Carolina’s 1st Congressional District,” https://apnews.com/article/748d4a53926f4372bae5ca5118d65ec6 . Search result supports election; direct open failed, so not claimed as full-text verification. AP syndication search result: https://www.chron.com/news/politics/article/democrat-nancy-lacore-wins-election-to-u-s-house-22517457.php . Not independently opened.
4. Corroborating election-report leads from search results, not full-page verification: https://scdailygazette.com/2026/11/04/nancy-lacore-declares-victory-in-scs-1st-congressional-district/ and https://www.live5news.com/2026/11/04/lacore-claims-sc-01-victory-says-costa-honeycutt-conceded-race/ . Do not confuse victory declarations with certification.

Searches for Hegseth plus schoolmate/classmate/went-to-school/went-to-college and Congress/elected, including YouTube-specific searches, did not identify a verified incoming member making the remembered claim. An exploratory name search did not establish a match; no identity assigned. Prior ChatGPT confidence is not substituted for evidence.

Findings and unresolved questions:
- Confirmed public-source example: Nancy Lacore, retired vice admiral, dismissed Navy Reserve chief and incoming South Carolina House member. Election certification was not independently examined.
- Unresolved: exact remembered YouTube videos, their titles, publication times, personal visit timestamps, Facebook/Mastodon referral chain, schoolmate identity and exact statement, and additional fired officers elected to Congress.
- Local absence does not prove the videos were not watched: embedded playback, browser history retention/deletion, private browsing, another device/account, or a different day could explain missing records. These possibilities were not established. No account watch-history, social-media account content or browser session/cache content was inspected; date scope was not expanded.
- Privacy incident: one overly broad diagnostic emitted two unrelated watch entries, a social referrer and an account redirect URL into the mandatory shared command log. Details are intentionally not reproduced here. The existing log was not rewritten or truncated under the standing logging contract. Subsequent report omits unrelated history. No claim of flawless filtering or machine-wide connector capture is made.
- All shell commands used /home/denebeim/projects/mostly-harmless/scripts/log-session.py; normal stdout/stderr appended to ignored chat.log. Web/chat connector retrieval is not intercepted by the shell logger. No commit/push or browser-profile mutation performed. Existing dirty CONTROLLER.md, HANDOFF.md, requirements.txt, scripts/log-session.py and earlier WORKLOG content preserved; only this entry was appended by this investigation.
