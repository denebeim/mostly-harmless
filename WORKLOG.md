# WORKLOG

> Living project log for `mostly-harmless`.
> Updated as work is performed in this repository and during infrastructure sessions.
> This repository is currently **public**. Keep credentials, private keys, exact internal
> addresses, sensitive topology, and other operational secrets out of this file.

## Current handoff for Eddie, Gemini, or Codex

Updated 2026-11-24. Summary by OpenAI Codex. Copy this section into a new prompt.
It describes the checkout and last recorded results. Before acting, verify the
actual files, branch and pending changes, and check live state when relevant.
Use the current request to determine scope and authorization.

- **Goal.** Make `mostly-harmless` the reproducible, backed-up source of truth for
  Deepthot infrastructure, automation, and operating documentation. Stabilize
  the working systems and preserve data and services as changes are tested.
  The public domain is `deepthot.org`. The LAN domain is `local.deepthot.org`.
- **Provisioning.** Machine declarations such as `eddie.yaml` use `vm.yaml`
  and shared, tag-gated Ansible roles. FreeIPA is optional and handles identity
  and automount. The documented LAN DNS uses Pi-hole, and the public zone uses
  Cloudflare. See `CONTROLLER.md` for the operating contract. PR #6 records
  successful disposable VM runs with no optional tags and with Docker only,
  including converged reruns. Fresh IPA-only enrollment still needs a retest.
- **Eddie.** The last recorded checks verified the pinned Hermes container,
  its shared gateway and local inference profile, GPU-backed Ollama, and
  Ollama access from the LAN. Ollama stays on the host with Vulkan for the
  legacy NVIDIA K5200. The native Hermes files were retained for rollback.
  Keep the existing FreeIPA setup while finishing Eddie. See `HANDOFF.md`,
  `eddie.yaml`, and PR #7 for the recorded deployment and rollback context.
- **Open work and blockers.** Verify Eddie's current services, GPU inference
  and LAN access with authorized read-only checks before planning changes.
  Review issue #14 and inventory the model, configuration and data paths to
  preserve before changing Ollama or adding LibreChat. LibreChat and the
  from-scratch rebuild are owner plans awaiting implementation and acceptance.
  For issue #8, prior checks confirmed IPA-managed Docker access on Eddie.
  Recheck disk headroom, Mailcow's IPA DNS resolution and Mastodon's sudo
  access before extending that rollout. `HERMES-DESKTOP.md` records the
  desktop/server split and pending desktop acceptance checks.
- **Owner plans, paraphrased by OpenAI Codex.** Finish Eddie with LibreChat,
  Ollama and Hermes on the existing FreeIPA setup, then plan a rebuild.
  Longer-term ideas include a separate portable Linux/Ansible repository
  without FreeIPA, assessing the inherited PC, managing existing FreeNAS,
  Plex and Arr services, and documenting Traefik 3, HTTPS, Cloudflare and local
  BIND/DHCP before eventual Kubernetes work. Other ideas include Windows
  network homes and possible machine management, easier WireGuard, Prometheus
  and a monitoring dashboard, local home automation and voice, and MikroTik
  configuration management with a separate private local repository and
  eventual private GitLab. Mastodon and Fediverse identity suffixes, the
  partly designed Pill Box project, and Blogger theme selection and drafting
  are also on the list. These ideas have no execution authorization here.
- **Working rules.** Read `AGENTS.md`, `CONTROLLER.md` and `HANDOFF.md`.
  Commit work-log updates locally and often in a dedicated checkout of
  `work-log` and push scoped work-log checkpoints there. Keep it separate
  from `main`. Preserve existing edits. Follow the acceptance workflow below. Treat branch and log instructions
  in older entries as historical. Run shell commands through
  `python3 /home/denebeim/projects/mostly-harmless/scripts/log-session.py COMMAND ...`.
  Keep the private local `chat.log` out of commits, pushes and shared prompts.
  Keep credentials and unrelated private output out of the work log.
- **Maintain this handoff.** At meaningful milestones, refresh the affected
  bullets and the date, then add a dated entry with the evidence, open issues
  and next action. Sign each new entry with its actual author, including the
  AI agent and provider where applicable. Attribute exact quotes to their
  speaker and label AI paraphrases and suggestions. Approval leaves
  authorship with the writer.

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

- Commit and push scoped `WORKLOG.md` checkpoints on the dedicated
  `work-log` branch.
- Develop in isolated twiddle directories and commit and push on the assistant's
  pull branch. Address feedback and move deployable files into the regular
  repository layout on that branch. Create an acceptance branch from current
  main and target the PR there. Joy reviews the full diff, performs the first
  merge and owns the acceptance branch afterward. Joy approves and performs
  the second merge into main.
- Put an `Author:` line under each new entry heading. Name the person who wrote the
  entry or the AI agent and its provider (for example, OpenAI Codex or Google Gemini).
  Credit each writer for their contribution to a jointly written entry. Human review
  or approval leaves the authorship of AI-written text with the AI.
- Identify user-authored text and attribute direct quotes to the speaker. Use
  quotation marks only for the speaker's exact words. Label AI paraphrases and
  suggestions as such. Add historical attribution only when the author is known.
- Read-only inspection is authorized. Show diagnostic commands before execution
  and report useful results so the owner can follow the work.
- This does not authorize consequential infrastructure changes or publishing
  sensitive operational information.
- Use Eddie as the project-facing agent name. The local playbook entry point is
  now `eddie.yaml`; the existing machine identity and upstream software names are
  preserved. The renamed operational file remains ignored pending privacy review.

### Shared principle: the seeing stone

AI is a seeing stone: it helps the owner examine more, organize ideas and explore possibilities. Its view can be incomplete or misleading, so verify claims and keep uncertainty visible. The owner's judgment, meaning and voice decide what becomes their public authored work. Use this principle with each reusable prompt below; assistance does not replace authorship or make output inherently reliable.

### Reusable prompt: scoped personal experiment (Codex or Gemini)

> Work on this personal experiment: <describe task>. Inspect current repository instructions, the actual remote default branch and existing changes first. Use your own isolated experimental branch and worktree when needed. Codex-owned experiments belong under ai-twiddles/codex/. Preserve Gemini's files, the existing ChatGPT and Gemini mouse setups, and shared logging code. Do not overwrite or relocate another assistant's work. Codex is authorized to work, commit and push its isolated experimental changes autonomously on its branch. Before anything reaches main or a future default branch, report the concrete work, discuss it with me, let me inspect it, and obtain my explicit approval for that reviewed change. Approval of this general workflow is not approval of future integrations. Target the PR at an acceptance branch from main. I review and execute both merges, and own the acceptance branch after the first one. Respect normal checks, required reviews and branch protection. This experimental authority does not extend to Gemini-owned files, shared infrastructure or publishing prose in my name. If you are Gemini, preserve the Codex area and follow the scope I give you. Stage exact paths only, run appropriate checks, and report what changed, validation, commit and merge status, and limitations. Stream command stdout/stderr through the established logger into the existing mostly-harmless/chat.log, protect secrets, and record significant developments in WORKLOG.md on the separate work-log branch.

### Reusable prompt: public work in my voice (Codex or Gemini)

> Help me develop <describe publishable work> in my own voice. Start from a ticket that I or the assistant creates, then use a dedicated branch. Work with me on the substance and wording until I say it sounds like me; do not replace that process with generic AI prose. I make the commit. Update WORKLOG.md on the separate work-log branch, then prepare the pull request together. Autonomous permission for isolated experimental branch work does not authorize committing or publishing this authored work for me. Anything reaching main still needs my explicit approval after review. Preserve unrelated changes and other assistants' files, keep commands visible through the existing logger, and keep secrets out of logs and public content.

### Reusable prompt: independent work-log checkpoint (Codex or Gemini)

> Update the existing WORKLOG.md on the separate work-log branch of denebeim/mostly-harmless. Use its own clean checkout, preserve prior entries and other work, and record meaningful results, failures, decisions and pending actions in a concise factual entry. Include only the work-log file in its commit. Do not merge work-log into main or move the work log onto main for convenience. Do not publish raw chat transcripts, credentials, raw chat.log or exact internal addresses. Commit and push scoped updates at meaningful checkpoints so the work is available for handoffs. If a protection or approval check blocks publication, stop that action, preserve the local result and report the reason; do not try another route around it.

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

## How to maintain this log

At each meaningful work milestone, update:
- current objective and status;
- verified findings (with evidence or references where practical);
- changes actually made and how they were verified;
- unresolved questions, risks, and dependencies;
- the next concrete action.

Use dates when known. Do not invent timestamps or imply continuous monitoring. This log is a
session-maintained record, not an autonomous live feed.

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

### 2026-11-07 — Restore Galaxy IPA dependency

- Reference `~/ansible/deepthot-configuration/roles/machines/ipa` calls `freeipa.ansible_freeipa.ipaclient`. The collection was absent locally and from the current manifest.
- Installed FreeIPA collection 1.17.0 into project-local collections and pinned that version in collections/requirements.yml, preserving existing manifest edits. Galaxy reported installation successful. No guest configuration changed.
- The local machines/ipa wrapper is still absent and eddie.yaml does not invoke it. Review and restore the wrapper before enrollment automation runs.
- Design target: DHCP reservations and DHCP-provided network settings; keep current Hermes identity until the later DNS rename.
- Live services DHCP read is pending: SSH as ansible was rejected. Inspect reference connection settings next.
- Diagnostic command output is appended to eddie-session.log; historical logs are not current-state evidence.

### 2026-11-07 — Hermes static networking interim decision

- Owner directs static networking for Hermes for now: host eddie.local.deepthot.org, gateway LAN gateway, DNS Pi-hole DNS host, search domain local.deepthot.org. No networking change applied in this step.
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
- Configured Hermes provider custom, model qwen3.5:4b, endpoint http://localhost:11434/v1 using its existing config template. Mirrored model/gateway settings in eddie.yaml so subsequent role runs preserve them.
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
- VM 314 named eddie is running, 8 cores/16 GiB/40G, serial console and K5200 passthrough configured. Guest SSH confirms eth0 MAC BC:24:11:47:69:B9 and host eddie.local.deepthot.org. Cloud-init completed, errors empty; only deprecated user-field warnings.
- Source template lacks qemu-guest-agent. Interrupted the optional agent-only retry loop (controller exit 99) after successful creation, serial login prompt and SSH verification. Updated base playbook to wait for SSH without requiring agent installation. Verified SSH through an isolated first-use known-hosts file under .ansible; existing workstation entries were not changed.
- Authenticated Pi-hole session was available in visible browser; created local A records eddie and eddie.local.deepthot.org -> eddie.local.deepthot.org. UI confirmed both entries; direct DNS queries to Pi-hole DNS host returned that address for each. Screenshot saved /tmp/eddie-dns-records.png. Existing Hermes DNS record retained; no DHCP reservation created in this static-network smoke test.
- Pi-hole record changes are recorded here; deployment templating/secret separation remains future work. Private Pi-hole TOML not copied or committed.
- Stopped at base VM + DNS milestone; IPA enrollment, user NFS-home login, Docker, Hermes and Ollama are deliberately not provisioned on fresh Eddie yet.

### TODO — LAN DNS/DHCP architecture (owner preference, 2026-11-07)

- [ ] Discuss Pi-hole versus IPA DNS versus traditional BIND9 and separate DHCP services on `services`. Owner prefers familiar, explicit zone/service configuration and is considering returning to BIND9 plus isc-dhcpd; evaluate the DHCP implementation when planning migration. This is a discussion item, not authorization to migrate now.
- Current decision: Pi-hole owns LAN DNS; do not use IPA as the LAN DNS authority. IPA remains intended for identity and automount. Actual IPA DNS/forwarding configuration has not been audited.
- Desired DNS model: zone local.deepthot.org with an SOA and one relative host A record per machine (e.g. eddie A eddie.local.deepthot.org). Verify Pi-hole SOA/domain behavior; do not equate its local host list with a BIND authoritative zone.
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
- Test target: deepthot-base-test, VM 8314, deepthot-base-test, 2 cores, 2 GiB, 12G, no tags; ID/name absent and IP had no ping/neighbor response. Storage heartogold has capacity; other storage/services were only observed and not modified. Tests must never use Eddie's ID or GPU.
- A file-generation command initially used system Python without PyYAML; it was rerun successfully with the project virtualenv. No managed host was affected.

- Owner steering: preserve the pending LAN Ollama listener changes. Test VMs must not run package upgrades. Eddie declares local user/group hermes and exact Docker membership [hermes]; that service account is not enrolled in Kerberos. Optional local-user and exact Docker-membership declarations now live in the shared roles.

- Disposable VM 8314 absent-to-running test passed with no optional tags. After replacing timestamp-only SSH backups with VM/keyset-keyed backups, the settled repeat run reported changed=0 for both deepthot-base-test and heartogold; IPA/Docker/app roles skipped and package-upgrade tasks skipped. Starting a Docker-only tag test on the same disposable guest, without IPA or upgrades. Docker role now delegates package installation to Galaxy and enforces membership only when explicitly declared; removed unrelated Kubernetes swap/kernel policy.

- Removed permanent one-off create-Eddie, restore-GPU, destroy-Hermes and setup-Hermes playbooks plus historical patch files from current entrypoints; their history remains in Git. Shared roles own behavior. Replaced controller documentation with the operating contract, generic entrypoints, tag gates, local-account policy and preserved LAN Ollama usage.

- Docker-only disposable deployment passed, and its settled repeat reported changed=0 on guest and hypervisor. IPA and package upgrades remained disabled. Guarded teardown of VM 8314 passed; cluster inventory and storage list confirm no VM or owned volumes remain. IPA confirms no test host entry existed. No controller/hypervisor global SSH entries matched the temporary name/FQDN/IP; its private per-MAC trust and backup files were removed. Unrelated Kerberos tickets and caches were retained.

- Lifecycle PR #6 opened at commit cfe9db2; security scan passed. Began separate issue #4 branch codex/4-eddie-hermes-docker. Official amd64 stable image pinned to digest 0dd31821…85ad76; container read-only device probe sees K5200 nodes. Native Ollama remains the working GPU inference backend. Docker migration stages private persistent state, keeps shipped default separate from local profile, and retains original native data for rollback. No Docker socket is mounted into the agent.

- PR #6 squash-merged at d0849ca; #3 closed automatically, GitGuardian clean. On Eddie the native state copy completed. First container gateway command rejected starting a named profile gateway: installed 0.23.0 multiplexes profiles through the default gateway. Adjusted the role to start the shared gateway while preserving the default model settings. Future migration copies run as the local service user.

- Eddie cutover succeeded: shared container gateway serves shipped default and local Qwen profiles, exact local smoke response passed, and a configuration-only repeat was ok=15/changed=0/failed=0. Ollama stayed at 100% GPU with 65536 context while the test ran; controller LAN model list passed. Smoke completion took several minutes, so no performance improvement is claimed. Container process runs as local hermes UID/GID 1001, sees GPU nodes and has no Docker socket. Hermes callback listener is loopback-only; Ollama remains LAN-accessible by design. Host native gateway and timer disabled; original data/install kept for rollback.
- Confirmed SSH as denebeim to Eddie enters /nethome/denebeim. SSSD domain online; both names resolve to eddie.local.deepthot.org. Docker group is the local group with only hermes, per prior instruction; no IPA fault accounts for a denebeim Docker socket denial.
- Recorded issue #5 investigation and recommended laptop-local file tools with Eddie inference in HERMES-DESKTOP.md. Added HANDOFF.md for current operational state and rollback. No automatic cloud fallback or remote Desktop UI acceptance run.

- PR #7 squash-merged at fdec47d and closes #4/#5. Removed ignored scratch test playbooks/inventory; kept private rollback data and log.
- Owner requested centrally managed Docker administration and login-once authorization as the broader design. Created IPA POSIX group docker-admins with denebeim, and sudo rule docker-admin-access for /usr/bin/docker, order 100, !authenticate, explicitly scoped to verified enrolled hosts. Hostgroup-only matching did not surface in SSSD; direct Eddie membership did. Removed temporary hostgroup and kept local Eddie docker group unchanged. Passwordless sudo Docker verified from fresh SSH on Eddie.
- Scoped rule to Mailcow and Mastodon after guest agent confirmed Docker and enrolled host identities. Their SSSD refreshes failed because root filesystems were already full. Regenerable APT cache cleanup restored both SSSD services without touching logs or Docker data. Mailcow still had IPA DNS resolution failures; Mastodon reached LDAP but needs verified sudo. Mailu lacks a matching directory host record, DMZ is not enrolled, and stopped guests were excluded. Opened #8 for these remaining hosts and durable capacity fixes. Added idempotent host registration to the IPA+Docker role path; live repeat against Eddie returned already registered.

- Addressed Sourcery’s IPA enabled-flag finding from PR #9. Docker host registration now requires an explicit enabled value and rejects disabled or missing flags before any directory write.

- Added denebeim to Eddie’s local docker group for direct socket access and declared both hermes and denebeim in eddie.yaml. The socket is root:docker with mode 0660. Plain docker ps listed Hermes from a fresh SSH login as denebeim. Eddie playbook syntax and git diff checks passed.

- Superseded the per-user Eddie Docker declaration. The Docker role reconciles local service accounts with the IPA docker-admins members resolved through SSSD. Verified the membership tasks on Eddie with zero changes.

## 2026-11-09 — Recover November 8 Docker/CLI context

- Read repository operating contract, historical worklog, handoff, current branches and diffs, Eddie declaration and Hermes container/migration/verification roles. Recovered additional November 8 evidence from the ignored private session log. Prior chat transcripts are unavailable through current tools; no claim of having reviewed them.
- Current local branch is main at 6aafdb0, with six pre-existing modified files covering documentation, Eddie Docker group policy and IPA registration validation. Preserved all pending changes; remote refs have not been refreshed. The removed setup_hermes_vm.yaml is historical; shared roles/hermes owns current deployment.
- Verified from retained log: Docker CLI v0.23.0; single observed bind mount /opt/hermes/data → /opt/data; UID 1001 CLI HOME=/opt/data and HERMES_HOME=/opt/data. Profile listing showed default Claude/auto and local Qwen/custom. Direct Ollama native and OpenAI-compatible requests returned OK later that evening; local gateway reported the default-profile multiplexer. Native host launcher still targeted the original installation when inspected. Earlier successful cutover inference remains historical acceptance, not proof of current interactive operation.
- Owner-reported November 8 checkpoint (not independently rechecked here): root container/s6 supervision with actual gateway/model UID/GID 1001, Privileged=false, no explicit Docker user namespace mode, working absolute CLI version command, and interactive TUI provider prompt.
- Hypotheses: unqualified CLI selects an unconfigured default provider; CLI/gateway profile or environment differs; required provider credentials are unavailable. Configuration invisibility and its cause remain unverified. Existing logged HOME/HERMES_HOME and profile discovery argue against assuming the persistent mount is absent.
- Updated CONTROLLER.md and HANDOFF.md to separate container root from application identity, qualify CLI acceptance, preserve rollback history and identify the configuration boundary as the next task. mostly-harmless remains authoritative; deepthot-configuration is legacy reference.
- Next: one read-only comparison of selected paths/profile/model/provider and allowlisted CLI/gateway environment; then choose the smallest correction from evidence. Host launchers for hermes and denebeim remain deferred until this is understood. No infrastructure changes made during documentation recovery.

### 2026-11-09 — First live CLI configuration-boundary diagnostic

- Read-only comparison succeeded over SSH from benjymouse as hermes, running container Python as UID/GID 1001. HOME and HERMES_HOME both /opt/data, cwd /opt/hermes. Both config files were readable and owned by UID 1001; narrowly selected model/provider fields remain default Claude/auto and local Qwen/custom.
- Previously logged gateway PID 195 currently has UID 1001, cwd /opt/data and the same HOME/HERMES_HOME. Other gateway-command-line matches include service/log helpers with HOME=/root but HERMES_HOME=/opt/data; they were not classified as gateway/model applications by this diagnostic.
- No HERMES_PROFILE or HERMES_PROFILE_NAME in the allowlisted CLI environment. Effective profile selection and credential availability remain unverified. Shared HERMES_HOME and readable files weaken the missing-configuration hypothesis; profile selection remains the leading explanation to test.
- Diagnostic setup failures: local SSH configuration ownership check required the documented -F /dev/null; sandbox networking required escalation; container system python3 lacks PyYAML, so the same read-only diagnostic was retried with standard-library inspection of only model-block default/provider lines. No dependencies installed or remote files changed. Successful output is in the private session log with BEGIN/END markers.
- Next single diagnostic: read installed CLI profile-selection logic and active-profile metadata, then test explicit local TUI selection. No host launcher or infrastructure changes made.

### 2026-11-09 — Owner priority clarification

- Sole current goal: get as much intelligence working locally as possible. Local resources first; focus remains Eddie/Hermes local inference and CLI recovery. No unrelated work has begun.
- Owner reports Mastodon and the mail subsystem are entirely down. This is reported state, not a fresh diagnostic; repairs remain outside the current scope. Earlier historical service observations must not be read as current availability.
- Google account access and ChatGPT secretarial workflows are desired future work for a separate session; no connections or account changes initiated.
- Continue one diagnostic at a time and log commands/output through scripts/log-session.py to eddie-session.log.

### 2026-11-09 — Stale Desktop tunnel log noise

- Identified leftover local SSH PID 2759191 forwarding localhost:19120 to Eddie port 19120 from the November 8 temporary Desktop experiment. Repeated channel-open connection refusals were burying current session entries; November 9 work was present in the log.
- Sent SIGTERM only after checking the process was still ssh with the exact experimental forwarding argument. Main Hermes container/gateway and persistent configuration were not changed. Existing log history retained.

### 2026-11-09 — Desktop experiment cleanup verified

- Owner requested completion of last nights Desktop SSH experiment cleanup. Host-level inspection found no remaining SSH local forwards after the identified stale tunnel was stopped.
- Read-only Eddie inspection found no hermes-desktop-test container, no TCP listeners on experimental ports 19119/19120/19121, and no matching host-visible Hermes/Python/timeout serve processes in the inspected executable-name set.
- No additional cleanup targets found. Main Hermes services and persistent data retained; session log history preserved. All inspection output recorded through the session logger.

### 2026-11-09 — Docker-backed host CLI implementation

- Owner authorizes autonomous local-equipment work toward working host CLI and local inference, with maintained playbooks and lightweight verification only. A later zero-to-configured rebuild is the acceptance target, not authorization to delete Eddie now. No unrelated host/application work.
- Read installed main.py profile pre-parser and profile helpers. No active_profile file existed; absent explicit -p, the CLI retained default, selecting shipped Claude/auto instead of local Qwen/custom. Files/environment were available: this was profile selection, not a missing persistent mount.
- Added roles/hermes/tasks/cli.yml and templates/hermes.sh.j2, imported by the existing container role. Installs root-owned /usr/local/bin/hermes; passes arbitrary arguments to absolute container CLI using docker exec -i, adds -t only when stdin/stdout are terminals, uses discovered service UID:GID and explicit HOME/HERMES_HOME=/opt/data. Does not use sudo or mount the host socket into the agent.
- Manages active_profile=local (hermes_cli_profile default); preserves old service-account command as ~/.local/bin/hermes.native and replaces its original path with a symlink. Explicit profile flags still work. Shared-gateway role lifecycle invocation now explicitly selects default to avoid dependence on sticky CLI profile.
- Applied owning role CLI tasks through a temporary /tmp invocation only; no retained repair playbook, full VM run, package upgrades or gateway restart. A repeat exposed symlink target ownership drift; setting follow=false fixed it. Final targeted convergence: ok=7, changed=0, failed=0, skipped=1.
- Fresh SSH as both hermes and denebeim resolved /usr/local/bin/hermes, reported v0.23.0/install method docker, and listed local Qwen as active. Actual ssh -tt host hermes launch as denebeim reached local/Qwen interactive prompt without provider setup and exited cleanly.
- Interactive telemetry choice was misread: confirmation reported sharing enabled despite intended opt-out. Immediately called the installed save_consent(False, False) API for local; it reported enabled=false, send=false, decided=true, reask=false. No assertion about whether any metrics were transmitted during that short interval. Added the explicit opt-out and offer_version=2 to the maintained local template and converged it without restarting gateway.
- Syntax check passed with explicit static inventory; default inventory invocation initially warned that its system interpreter lacked six. No dependencies changed. Dynamic inventory/controller environment and full rebuild remain untested this session.
- One host-command local inference request is pending (300-second bound). Ollama status shows qwen3.5:4b resident at 100% GPU, 65536 context; local gateway status reports the shared default multiplexer. No additional inference requests launched.

### 2026-11-09 — Host CLI/local agent accepted

- The single bounded local request, issued through plain host hermes as denebeim, returned exactly 'Eddie is online.' and agent_exit=0. Active profile was local/Qwen/Ollama. Response took several minutes; no speed claim.
- Combined acceptance: both users resolve the Docker-backed command and active local profile; interactive denebeim launch reaches local/Qwen chat without provider setup; one local inference succeeds. Targeted role/local-template run settled changed=0; syntax and diff checks passed. No heavy testing or destructive rebuild.
- Updated current handoff/controller usage. Future unassisted zero-to-configured Eddie rebuild remains a separate acceptance exercise after defining deletion scope and preserving required state. The default dynamic inventory interpreter issue is not diagnosed beyond the missing-six warning; use the established controller environment before a full run.
- Removed the temporary /tmp CLI-only invocation after applying maintained role tasks. Existing unrelated uncommitted changes preserved; no commit or publishing performed.

### 2026-11-09 — Global VM shell environment

- Owner clarified the Deepthot convention: SSH into a VM should expose that VM's tools globally, without per-user setup. Recorded this as an operating contract.
- Inspected Eddie /etc/profile and /etc/bash.bashrc. Added maintained /etc/profile.d/deepthot-tools.sh to ensure /usr/local/bin is on PATH and an idempotent global Bash block to source it in interactive non-login shells. Login shells already source profile.d through /etc/profile.
- Retired the service-account-specific command link; kept its native rollback backup. The command itself remains root-owned /usr/local/bin/hermes, using the accepted Docker launcher and local profile. Docker authorization policy was not broadened.
- Applied only owning role CLI tasks. Fresh SSH checks as hermes and denebeim, with HOME=/nonexistent and starting PATH=/usr/bin:/bin, found /usr/local/bin/hermes in both login and interactive non-login Bash. Expected no-job-control warnings came from invoking interactive Bash without a PTY. No inference request repeated.
- Narrow repeat: ok=6, changed=0, failed=0, skipped=2. Controller/handoff updated; temporary /tmp invocation removed. Existing historical symlink entries above describe earlier implementation, superseded by this global design.

### 2026-11-09 — Package Hermes follow-up for issue #4

- Owner requested a documented hermes.yaml with GPL licensing, work on the ticket branch, and publication to GitHub. Reported input-not-a-terminal fd=0 and unexpected interactive command behavior are recorded as follow-up, not fixed in this packaging step.
- GitHub issue #4 is the completed original Docker migration; no open PR existed. Continued its existing codex/4-eddie-hermes-docker branch. Preserved all pending work in a stash before switching, merged current origin/main without rewriting history, resolved old squash-merge documentation conflicts using main, then restored pending work. Stash backup retained.
- Added shared hermes.yaml with a top-of-file explanation of lifecycle, prerequisites, persistent state, service identity, global CLI, usage and verification control, plus GPL-3.0-only SPDX notice matching repository GPLv3 license. vm.yaml imports it after host application prerequisites; owning roles remain the implementation source.
- GPL notices also cover newly authored launcher, global PATH fragment and CLI tasks. No claim to relicense upstream Hermes or imported third-party roles.
- Includes pending IPA-group-to-local-Docker membership convergence because fresh-login denebeim access must be reproducible, not a manual host exception. The separate pre-existing IPA enabled-flag validation edit remains outside this Hermes change.
- No new live deployment or heavy tests for this entrypoint extraction. Preserve existing operational acceptance evidence and pending clean-rebuild/terminal limitations.

### 2026-11-09 — Published Hermes follow-up

- Committed implementation and documentation as 943d7d3 on codex/4-eddie-hermes-docker and pushed without rewriting branch history.
- Opened PR #10: https://github.com/denebeim/mostly-harmless/pull/10 against main, following up issue #4. PR describes actual acceptance evidence, terminal warning, response latency and untested rebuild.
- eddie.yaml and hermes.yaml syntax checks and staged diff checks passed. No private logs, credentials or ignored operational files included. Separate pre-existing IPA enabled-flag edit remains uncommitted; preserved stash backup retained.


## 2026-11-10 — WireGuard DMZ server and staged Benjymouse client

- Owner requested autonomous WireGuard setup, DMZ server on Deepthot and Benjymouse client, full output in chat.log and remarkable events here. Confirmed Benjymouse identity and VM 216 dmz on heartogold, host dmz. Commands are echoed before execution following owner's later instruction. Early read-only inspection preceded log creation; summarized retrospectively. Private keys never deliberately printed.
- Initially honored misspelled mostly-harmles log path; owner corrected to mostly-harmless and requested a regular file. chat.log is now a regular private file in this repository, earlier contents retained; link and empty typo directory removed.
- Found wg-easy container stopped for 16 months, historical Docker volume with legacy WireGuard subnet configuration. Preserved container and volume, did not restart it. Do not start the old container alongside this server: both use UDP 51820.
- Existing interrupted kernel package installation blocked APT. Simulation showed one missing linux-image-5.15.0-170-generic and seven pending configurations; completed apt-get --fix-broken install, then installed wireguard-tools without other package upgrades or removals. No reboot; running kernel remains 5.15.0-168-generic. Final dpkg --audit empty.
- Native server /etc/wireguard/wgdeepthot.conf and wgdeepthot.key are root-private. wg-quick@wgdeepthot active and enabled, UDP 51820, WireGuard server tunnel address, sole configured peer Benjymouse Benjymouse tunnel address. Server private key generated and retained remotely. IPv4 forwarding already enabled and now declared in /etc/sysctl.d/80-wireguard-deepthot.conf. Interface hooks add/remove peer-scoped LAN forwarding and NAT for WireGuard subnet through eth0. UFW inactive. Existing Docker/application services retained.
- Client key/config staged mode 0600 under mode-0700 /var/tmp/wireguard-1847800003 on Benjymouse. Endpoint deepthot.org:51820 currently resolves through LAN DNS to dmz. Intended split tunnel covers WireGuard subnet plus LAN LAN subnet at metric 800, allowing existing local LAN routes to win at home. No default internet route or DNS changes; 25-second keepalive.
- Client startup BLOCKED by AppArmor: /etc/apparmor.d/wg-quick allows configuration only under /etc/wireguard. Initial home/project-storage/root-squash hypothesis was incorrect, as identical denial occurred on local ext4 /var/tmp. Profile was inspected and restriction identified. Existing NOPASSWD sudo permits wg-quick only; sudo -n install to /etc/wireguard fails with interactive authentication required. Did not weaken AppArmor or use wg-quick hooks to bypass authorization.
- Staged user unit ~/.config/systemd/user/wireguard-deepthot.service was disabled/stopped after failed attempts; no remaining retry loop. Existing Linger=yes observed. Maintained scripts/setup-wireguard.py now installs the staged config to /etc/wireguard with sudo before writing/enabling the user unit, and prints subprocess commands before execution. Script is partial setup, not accepted end-to-end; requires authorized sudo install and must be rerun after administrative access is available. It does not install OS packages. /var/tmp staging is private but may be aged by system cleanup; retain until installation is completed. Removed redundant private staging under project .ansible/wireguard.
- Verification: server active/enabled; wg show lists intended peer with no handshake. Client interface absent, client service disabled, internet route unchanged. No end-to-end traffic, LAN forwarding, remote public DNS/NAT forwarding, restart, or reboot acceptance claimed. Router UDP 51820 forwarding and away-from-home reachability remain unverified. No Git commit or publication; unrelated existing Docker IPA file modification preserved.
- Remaining: an administrator must authorize copying the client configuration to /etc/wireguard; rerun scripts/setup-wireguard.py, verify handshake and ping WireGuard server tunnel address plus LAN traffic, then verify startup and external UDP forwarding. Server rollback: sudo systemctl disable --now wg-quick@wgdeepthot removes interface and its firewall rules; retained config/key and dedicated sysctl file may then be removed after review. Do not disable global forwarding, which predated this work and is used by Docker.

### 2026-11-10 — GNOME authorization completed; tunnel accepted on LAN

- Owner asked whether this session could request a password through GNOME. Confirmed pkexec and graphical session; pkexec --disable-internal-agent /usr/bin/install -m 600 -o root -g root installed the staged client config to /etc/wireguard/wgdeepthot.conf after successful system authentication. No password entered into chat or captured by agent. Earlier authorization blocker is resolved.
- Updated user unit to permitted /etc/wireguard config path, enabled and started it. Existing user lingering enables startup without a desktop login. Server remains enabled. Verified fresh WireGuard handshake and encrypted traffic, ping server WireGuard server tunnel address 3/3 and LAN DNS host Pi-hole DNS host explicitly through wgdeepthot 3/3, no loss. Client service restart and subsequent tunnel ping 2/2 passed; client active and enabled. Ordinary internet route remains via LAN gateway on physical Ethernet.
- End-to-end LAN tunnel and forwarding now accepted. Remote public DNS/router UDP forwarding and actual reboot remain untested. Existing script uses sudo -n install; if authorization is absent on a later run, use the same narrowly scoped pkexec installation as this session. Client management: systemctl --user start|stop|restart wireguard-deepthot.service.

## 2026-11-11 — Shared live command logging

Preserved the existing private eddie-session.log in place and strengthened
scripts/log-session.py: append-only 0600 log, sanitized live merged stdout/stderr,
inherited stdin, launch-failure records, signal exit codes, run IDs, and no argv
metadata. Added root AGENTS.md with mandatory wrapper guidance for cooperating
agents; added its ignore exception and linked the contract from CONTROLLER.md.
No universal command hook exists in the current SDK initialization runners.
Validated harmless stdout/stderr, live line delivery before exit, status 23,
missing executable 127, SIGTERM 143, existing history preservation, permissions,
and synthetic-secret redaction using a temporary isolated log. Current commands
are already appending to the default shared log; emitted LIVE LOG CHECK on both
stdout and stderr for the owner watching with tail. Child buffering/incomplete
lines and tools that require output TTYs remain limitations; redaction is best
effort and agents must avoid printing secrets.

### Standing visibility preference

Owner confirmed the live tail now receives output. Persisted the voice/chat/tail
workflow in AGENTS.md: visible coordinator requests and executor responses in
Codex chat/console, actual sanitized command output in the shared session log,
and continuous wrapper use by delegated executors through diagnostics, edits,
validation, and failures. Documented adoption and connector/API capture limits;
no claim of machine-wide interception. This update was itself executed through
the shared logger.

### November 11 — LibreChat voice input diagnostics on Ubuntu desktop

Owner-requested diagnostics used the shared session logger after the initial instruction read. LibreChat browser speech code emits the reported unsupported-recognition error when the browser recognition API/controller is unavailable. Firefox 153.0.3 is running; Google Chrome 157.0.8103.38 is installed. A temporary headless Chrome profile confirmed a recognition constructor is exposed; this did not test the microphone or actual recognition. The installed LibreChat STT service supports OpenAI-compatible and Azure OpenAI providers, not native Gemini STT. Approved directory environment supplies Gemini only; other checked STT credentials are absent/placeholders. No librechat.yaml, running transcription container, or checked local Whisper/Vosk tooling was found. No LibreChat configuration, browser preferences, or services changed. Recommended next test: open localhost:3080 in installed Google Chrome, sign in, leave speech-to-text engine Browser, allow microphone, and test dictation. Full voice acceptance remains pending a user microphone test; Firefox server-backed dictation would require a separately chosen transcription service.

### November 11 — LibreChat reported early failures and running out

Read-only inspection through the shared logger: all six LibreChat services remain running; application restart count 0 since 12:17 Arizona. Saved conversation settings select google/gemini-3.5-flash. Persisted provider failure at 13:20:10 Arizona is HTTP 429: free-tier generate-content requests-per-day quota exhausted, reported limit 20, provider quota dimension gemini-3.6-flash despite the selected 3.5 model. Provider retryDelay 41990 seconds corresponds to November 12 at 01:00 Arizona; official Gemini documentation states daily quota resets at midnight Pacific and is project-scoped. Earlier persisted failures at 13:14:57 and 13:15:02 report GoogleGenerativeAI failed to parse stream. These precede the recorded quota rejection; their underlying cause is not established. Latest successful response metadata shows roughly 7790 pre-prune context tokens and over 884000 remaining, with default output allowance 65535; no evidence these failures are caused by conversation/output exhaustion. Recent turn metadata reports toolCount 0, so this chat has no attached action tools. No prompt/response text printed, no generation probe made against the exhausted quota, no configuration/model/billing changes or restarts performed. Further reliable-use choice (paid quota, another provider/model, or local inference) requires owner preference; qualitative answer dissatisfaction requires one concrete example if it persists after transport/quota recovery.

### November 11 — Intended paid Gemini account versus free-tier rejection

Owner reports existing Google API billing with an approximately $20 limit. Read-only comparison in memory confirms the current LibreChat GOOGLE_KEY exactly equals GEMINI_API_KEY loaded from approved /home/denebeim/projects/.envrc; no secret values printed. The mounted .env has the user_provided placeholder, but Docker process environment supplies the actual server key and takes precedence. Safe running-key SHA-256 prefix recorded in private session log for future equality checks. The stored 429 error explicitly reports quotaMetric generate_content_free_tier_requests and quotaId GenerateRequestsPerDayPerProjectPerModel-FreeTier, limit 20; it provides no consumer/project/billing-account identifier. Selected model remains gemini-3.5-flash while provider quota dimension reports gemini-3.6-flash. gcloud/bq unavailable and ~/.config/gcloud absent, so no authenticated local billing/project lookup was possible. No alternate intended paid credential identified in inspected configuration; no credential switch, billing/budget mutation, or API generation performed. Next read-only account checks: AI Studio API Keys identify the project owning the existing directory key; Projects inspect that exact project Billing Tier/Status; Billing inspect linked account and any Prepay/No credits status; inspect whether the $20 setting is an alerts-only budget, a project spend cap, or prepaid balance. Current official documentation distinguishes alerts-only budgets (no automatic cap) from Gemini/project spend caps (enforced with latency/possible overages). Do not infer the owner means a consumer subscription; API project billing must be verified independently.

### November 11 — Retry after payment-method update

Owner updated Visa and reported no balance due, then authorized one minimal retry. At 14:03 Arizona, used the existing running LibreChat server credential with the same gemini-3.5-flash model, maxOutputTokens 32, thinking MINIMAL. LibreChat config endpoint HTTP 200. Exactly one provider generation request was made; it returned HTTP 402 RESOURCE_EXHAUSTED with explicit message that prepayment credits are depleted and directs to AI Studio billing. No provider retry/propagation delay supplied. This is a different explicit restriction from the previous Free Tier daily-quota rejection; do not infer fully active billing or available credit from no balance due. Next read-only check is available Prepay credit for the key-owning project/billing account in AI Studio. No billing, budget, credential, model, or service changes. Initial wrapper invocation lacked docker exec stdin attachment and executed no script/API request; corrected invocation used docker exec -i and both invocations are logged.

### November 11 — Single retry after further owner billing/credit step

At owner request, exactly one minimal generation at 14:34 Arizona using unchanged running LibreChat credential and gemini-3.5-flash, output allowance 32 and MINIMAL thinking. Google again returned HTTP 402 RESOURCE_EXHAUSTED: prepayment credits depleted. No text generated and no provider retry delay supplied. No additional generation requests, settings/billing/credential changes, or restarts performed.

## 2026-11-12 — AI Setup

- Objective: Set up Roo Code, Gemini, and establish the `mostly-harmless` baseline.
- Status: Setup complete.
- Verified findings: Verified Roo Code configured with Gemini (specifically `gemini-3.1-pro-preview`).
- Changes made: Enforced `WORKLOG.md` tracking by creating `.clinerules`.
- Unresolved questions, risks, and dependencies: None for this step.
- Next action: Await further instructions.

### 2026-11-12 — Hermes/Eddie synchronization from repository and logs

- Read the full worklog and operating contract; inspected Git, diffs, entrypoints, owning roles and retained diagnostic evidence. No provisioning, infrastructure changes, branch switches, commits or pushes performed. Command output appended to both private chat.log and the shared eddie-session.log through the mandated logger.
- Checkout: codex/4-eddie-hermes-docker at 7fda3c7; cached upstream agrees, nothing staged. Six pre-existing tracked modifications: .gitignore, CONTROLLER.md, WORKLOG.md, register_ipa_host.py, manage_vm.py and log-session.py; untracked AGENTS.md and scripts/setup-wireguard.py. Existing stash retained. Both operational logs are ignored. Remote freshness is unverified: default Git SSH failed the system SSH-config ownership check; retry with -F /dev/null failed DNS resolution for github.com.
- Latest retained Hermes application acceptance remains November 9: Docker-backed host CLI/local profile, exact response Eddie is online. with agent_exit=0 (private session log lines 186997-187002), targeted convergence without changes. This is historical evidence, not a fresh live-health check.
- Significant omitted failure: November 11 runs 9581440ff706 and ff22049b08aa failed in Proxmox convergence for VM 314 because boot order scsi0 referenced a nonexistent device (qm exit 255; Ansible exit 2). JSON parsing of helper output then obscured the underlying error. The uncommitted helper now selects the first present disk among scsi0/virtio0/sata0/ide0 for boot/resize and adds diagnostics; no successful subsequent deployment recap found in reviewed evidence. Actual disk identity and safety of this selection are not freshly verified.
- HANDOFF.md remains a November 9 checkpoint and misses the later provisioning failure/helper edit. Earlier worklog current-findings headings are historical and superseded. Standalone hermes.yaml configures an existing tagged guest; eddie.yaml imports vm.yaml for the full lifecycle. Clean-VM full-stack acceptance remains outstanding, as does the reported fd=0 interactive warning.
- Recommended next smallest step: read-only verification of VM 314 identity and disk/boot configuration, then review the pending helper correction against that evidence and verify it offline before any provisioning retry. Reconcile the observed 65536 Ollama context with maintained configuration as a separate reproducibility gap; no rebuild/deletion is authorized by this entry.

### 2026-11-12 — Owner cost constraint

- Owner sets a maximum monthly AI budget of $25; stop paid work at the cap until renewed authorization/funding. Treat this conservatively as total AI spending pending clarification of subscription versus additional usage. Prefer the cheapest suitable model, no unsolicited model escalation, paid API inference, credit purchases or parallel agents. Keep investigations narrow and handoffs concise.
- Agent cannot enforce an account billing cap or infer dollar spending from token/usage percentages. Account billing controls and model selection must be verified separately; no billing settings or model changed in this step.

### 2026-11-12 — Eddie boot configuration investigation

- Read-only log review found a November 7 saved Proxmox `qm config 314` snapshot with `scsi0` 40G and `boot: order=scsi0`; the November 11 `qm set` returned invalid bootorder for that device. Snapshot is historical and conflicts with the later error, so current VM disk state remains unverified. The uncommitted helper picks the first existing disk key in a preference list and could select a non-root disk if the root disk is absent; do not treat the fallback as validated.
- Attempted a read-only current `qm config 314` via Ansible. It did not run: `inventory/proxmox.py` failed to import `six` under the project venv; Ansible then exited 250 with Local RPC server did not start. No Proxmox command or infrastructure change occurred.
- Next: restore the controller dependency through the tracked lock/requirements workflow, then retry the read-only query with the documented SSH config override. Do not retry provisioning until current VM config and root-disk selection are confirmed.

### 2026-11-12 — Python formatting rule and ticket

- Owner requests all Python files prettified and future scripts formatted. Extensive formatting must be isolated on its own GitHub ticket branch and in a dedicated formatting-only commit, separate from functional changes. Preserve this as a standing workflow rule.
- Created issue #11, “Format Python scripts consistently and enforce formatting,” and branch `codex/11-python-formatting` from `main`. No formatting changes made in the active Eddie branch.

### 2026-11-12 — Fixed Proxmox helper JSON output

- Removed command debug prints from `roles/proxmox/create_vm/files/manage_vm.py`; successful stdout is now solely the JSON result consumed by Ansible. Existing command exceptions still fail the helper with a nonzero exit. Kept this functional fix separate from the Python-formatting issue/branch.
- Re-ran `eddie.yaml` with `--limit heartogold` under direnv, so only Proxmox plays ran. VM convergence and JSON fact parsing passed (`ok`); guest and application plays had no matching hosts. Verified running guest identity via Proxmox agent and refreshed its private controller SSH trust entries (the only changed recap task). Overall recap: failed=0, unreachable=0. No guest package/application provisioning was performed in this bounded run. Full unbounded application convergence remains pending.

### 2026-11-12 — Full Eddie run reached Docker IPA registration blocker

- After removing debug chatter from manage_vm.py, full `eddie.yaml` passed VM convergence, base guest SSH/cloud-init, package upgrades and reboot, service-account setup, hypervisor-verified SSH key refresh, and IPA client convergence. Docker packages/service converged. It failed at the controller-side central IPA sudo-rule registration (`roles/machines/docker/files/register_ipa_host.py`), whose exception handler intentionally emits a generic message.
- Safe controller check immediately after failure: `klist -s` reports no valid Kerberos ticket. The documented Docker registration flow requires `kinit admin`. Read-only `ipa` CLI checks could not initialize because the controller hostname did not resolve in this environment. No IPA policy change confirmed; helper failed. Stop before Ollama/Hermes plays; they did not execute. Full run recap: Eddie ok=58, changed=16, failed=1; heartogold ok=15, changed=1, failed=0.
- To continue, authenticate the controller with `kinit admin`, then rerun the full playbook. The prior completed tasks should converge idempotently.

### 2026-11-12 — Controller hostname resolution blocks IPA API startup

- Resumed full Eddie run with a valid admin Kerberos ticket. VM convergence, base/package steps, existing IPA client convergence and Docker setup passed; run again failed at controller-side Docker IPA registration. Ollama and Hermes plays did not execute.
- Read-only diagnosis confirms the controller configured hostname is `benjymouse.local.deepthot.org`, `/etc/hosts` maps only short name `benjymouse` to host-local loopback address, and `hostname -f` fails with name resolution. FreeIPA installed `ipapython.fqdn.gethostfqdn()` calls `socket.getaddrinfo(socket.gethostname())` during import; this raises before Kerberos-authenticated IPA API calls. `klist` showed a valid admin TGT, so ticket acquisition is not the current blocker.
- No system or infrastructure changes made to resolve hostname. Next repair should make the controller FQDN resolve reproducibly, then rerun full eddie.yaml. Need decide whether to declare/manage the controller hosts mapping in repository automation or rely on a managed DNS record.

### 2026-11-12 — Full Eddie playbook completed successfully

- After Wi-Fi came up, controller FQDN `benjymouse.local.deepthot.org` resolved via LAN DNS to benjymouse.local.deepthot.org and `hostname -f` succeeded. The wired static interface remained active and routed LAN DNS queries. No DNS or host configuration was changed.
- With a valid Kerberos ticket, reran full `eddie.yaml`: VM convergence, base packages/account, SSH identity refresh, existing IPA client, central Docker rule registration, Docker, K5200 driver, Ollama API/LAN check/model presence, Hermes container/profile/CLI and configured local inference all completed. Recap: Eddie ok=93 changed=15 failed=0 unreachable=0; heartogold ok=15 changed=0 failed=0 unreachable=0.
- Hermes local inference task returned success. This clears the prior full provisioning errors; next acceptance is interactive user chat with Eddie and workflow evaluation.

## 2026-11-13 — Gemini M705 Wayland investigation

Inspected local benjymouse GNOME 50.1 Wayland session. input-remapper daemon active; M705 code 275 maps to Control+Alt+Shift+g; GNOME custom0 runs ~/.local/bin/gemini-toggle. Existing toggle relies on wmctrl/xdotool and unavailable gemini executable, with an overbroad pgrep match. No Gemini desktop/PWA launcher found. System /usr/bin/python3 evdev can create /dev/uinput virtual keyboard under existing user ACL; probe emitted no keys. Shell Eval returns false and Introspect.GetWindows denies access. No configurations changed; timestamped backups saved under ~/.local/state/gemini-toggle/backups (script, input-remapper-2 tree, media-keys dconf). Awaiting owner identification of intended Gemini app and confirmation that Ctrl+Shift+D toggles dictation there; end-to-end focus/toggle remains untested. All shell diagnostics logged through shared wrapper; no remote-desktop portal invoked.

## 2026-11-13 — Gemini M705 Wayland implementation

Owner clarified Ctrl+Shift+D starts dictation when Gemini is focused and authorized input control. Identified four Gemini windows through a narrow GNOME integration: three Chrome app windows and one regular Chrome Gemini tab. Closed those using focus-verified Ctrl+W under the then-current cleanup instruction; opened a fresh regular Gemini webpage. Owner subsequently clarified a separate app window should be used, leaving regular browser available. Final targeting excludes normal Chrome windows; a standalone Gemini app window was launched in existing Chrome Profile 4 (AI Testing), while the fresh regular webpage was left available. Earlier conversation tab can be recovered through Chrome history/recently closed tabs.

Installed ~/.local/share/gnome-shell/extensions/gemini-focus@local (GNOME 50), active and enabled. Its local D-Bus API exposes only standalone Gemini focus/status, checks desktop lock, and does not enable Shell unsafe mode. Loaded live through local Looking Glass using virtual input; no logout or portal prompt. Replaced ~/.local/bin/gemini-toggle atomically (old script had a second hardlink) with /usr/bin/python3 script using system evdev and existing /dev/uinput ACL. It serializes clicks with flock, focuses existing standalone app or launches /opt/google/chrome/google-chrome --profile-directory=Profile 4 --app=https://gemini.google.com/app, waits for focus, registers a virtual keyboard and rechecks focus before Ctrl+Shift+D, releasing keys in finally. M705 preset and GNOME custom shortcut are unchanged. No packages, input permissions, or system services changed.

Original script, full input-remapper-2 tree and media-key dconf backup: ~/.local/state/gemini-toggle/backups/20261113-221056. Rollback: disable gemini-focus@local and atomically restore backed-up gemini-toggle; mapping needs no restoration because unchanged. Extension files may then be removed. No repository commit made.

Validation: Python/JavaScript syntax passed; active GNOME extension verified; close cleanup reduced Gemini window counts 4→0; cold launch and focus passed for webpage then final standalone app. Final wmclass chrome-gemini.google.com__app-Profile_4 was focused. Gemini accessibility exposed Dictate (^⇧D), confirming shortcut. Mocked input tests passed exact chord press/release order, no typing after focus change, and locked-desktop refusal. Accessibility reporting temporarily enabled for inspection and restored to original IsEnabled=false/ScreenReaderEnabled=false. Actual automated microphone toggle test was rejected by automatic approval review before execution because ambient audio could be transmitted to Google without explicit approval; no bypass attempted. Owner later said the microphone appears to be working, but full mouse-click start/stop/submission was not independently observed. No claim of end-to-end acceptance. Commands logged through shared wrapper throughout; connector/browser inventory actions are outside shell logging.

### Gemini stop-and-submit and latency follow-up — November 13

Owner confirmed Ctrl+Shift+D stops dictation and fills Gemini prompt but does not submit. Added per-window two-click state: first starts; second stops, waits 0.6s for final recognition, then Return submits. A failed submit remains pending and retries without restarting the microphone; new window ID resets state. Manual microphone changes can desynchronize this local tracker; ~/.local/bin/gemini-toggle --reset clears it without input. Next owner test should begin with microphone off. Removed repeated 0.8s evdev device registration and fixed 0.25s modifier sleep: GNOME extension now holds native Clutter virtual keyboard, exposes only dictate/submit actions, rechecks focus/lock and waits for shortcut modifiers to release. Script uses that narrow API; first launch readiness wait is 2.5s instead of 4s. Existing mouse/GNOME shortcut configuration remains unchanged. Pre-change backup: ~/.local/state/gemini-toggle/backups/20261113-223046 (script and extension). Original backup remains.

Python/JS syntax and simulated two-click sequence, new-window reset, and failed-submit retry tests passed. Live extension API verified using invalid-action refusal with no key emission; final status active. Live loader initially missed dir metadata, briefly unexporting old service; corrected and live API restored before installing replacement. Temporary read-only accessibility check restored original screen-reader state in finally. Diagnostic filename inspect.py shadowed Python module and was renamed. No automated microphone activation or text submission performed; owner end-to-end test still required. Click state reset after installation. Detailed stdout/stderr preserved in shared log.

### November 13 — On-demand weekly blog draft

Owner requested an on-demand recap of accomplishments across projects, stored in Mostly Harmless as a draft for a future blog; no recurring automation or publication requested. Created reports/weekly/2026-11-13.md for November 9–13 from work log, Git history and selected chats, distinguishing completed results from pending acceptance. Directly confirmed finalized assets/visual/deepthot_welcome.png (earlier save-thread failure was superseded by actual local file) and deepthot-conversation-recovered.html (seven embedded images). Both are currently ignored by Git. Draft links to both existing files and includes private editorial/source notes for later removal. No assets moved or modified, no commit/push/publication.

### November 13 — Detailed accomplishment inventory

Owner clarified that the desired artifact is detailed accomplishment bullets across AI-assisted work since starting the current effort, including visible Gemini work, rather than blog prose restricted to this calendar week. Created reports/accomplishments-through-2026-11-13.md covering documented November 6–13 work plus clearly separated earlier saved design artifacts. Sources include worklog/changelog/Git history, selected conversations, and actual files. Records creation of the working Eddie system, not merely its maintenance; marks plans, rolled-back personality activation and pending tests. Separate Gemini history is not connected, so attribution/coverage is qualified. Preserved prior blog draft. No commit, publication, sharing, or asset moves.

### November 13 — Saved reflective writing draft

At owner request, saved the current AI-assisted reflection as writing/drafts/when-it-starts-to-feel-like-mine.md, incorporating the explicitly approved revised opening and preserving the rest of the displayed draft. Marked remaining text unreviewed, added brief continuation context including voice versus keyboard preferences, and verified readback. Intended for later review or transfer to another AI. No publication, sharing, commit, or push.

## 2026-11-14 — ChatGPT mouse voice inspection checkpoint

Owner requested inspection and proposed minimal change before automation edits. Read CONTROLLER.md/HANDOFF.md and referenced ChatGPT conversation. No automation, browser, microphone, shortcut, or permission settings changed.

Live benjymouse session 3 is Wayland. input-remapper active. /home/denebeim/.config/input-remapper-2/config.json autoloads Logitech M705 preset _home_denebeim_; /home/denebeim/.config/input-remapper-2/presets/Logitech M705/_home_denebeim_.json maps EV_KEY 275 (BTN_SIDE) to Control_L + Alt_L + Shift_L + g. GNOME custom0 at /org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ invokes /home/denebeim/.local/bin/gemini-toggle. Script launches /opt/google/chrome/google-chrome --profile-directory=Profile 4 --app=https://gemini.google.com/app if its narrow focus API finds no standalone window. Active extension /home/denebeim/.local/share/gnome-shell/extensions/gemini-focus@local/extension.js matches Gemini Chrome app wmclass/title, checks lock/focus/modifiers, and uses persistent Clutter virtual keyboard through org.gnome.Shell.Extensions.GeminiFocus D-Bus API (Focus/Send/Status). No wmctrl/xdotool in current script. First click Ctrl+Shift+D; second Ctrl+Shift+D, 0.6 second wait, Return; flock serialization, per-window runtime JSON, pending-submit retry, --reset. Live Status found Gemini app Profile_4, unfocused, tracker phase dictating; microphone state not independently observed.

Upper physical button event unverified: raw /dev/input/event13 access denied even outside restricted execution; sysfs identifies Logitech M705 and key capability bitmap ffff0000 0 0 0 0. Do not assume adjacent code 276 is the requested physical button. Browser inventory exposed only empty in-app/MCP browsers, no existing Chrome tabs; missing ChatGPT Voice control cannot be diagnosed from this session yet. Official https://learn.chatgpt.com/docs/features/voice documents desktop Start/Stop voice chat and rollout/workspace dependencies, not proof of browser availability. No transient Try Voice control used.

Presented proposed minimal change in chat: isolated /home/denebeim/.local/bin/chatgpt-voice-toggle plus separate GNOME shortcut/focus helper and one additional M705 mapping, preserving Gemini; verify actual browser Start/Stop Voice controls and observed state before wiring. Pending: identify upper-button event, inspect actual signed-in ChatGPT browser and missing Voice control, then implement/test. No implementation claimed.

All shell commands used shared scripts/log-session.py; initial restricted live diagnostics failed and later read-only host queries succeeded. No automatic review rejection occurred. Sanitized output from this inspection is mirrored from eddie-session.log to private chat.log; connector/browser actions are outside shell capture. Existing unrelated working-tree changes preserved.

## 2026-11-14 — Standing command log renamed

Owner established chat.log as the ongoing default. Updated scripts/log-session.py, AGENTS.md, CONTROLLER.md and HANDOFF.md to use /home/denebeim/projects/mostly-harmless/chat.log. Existing log history retained; no log truncated or replaced. Shared wrapper and redaction remain in use. Historical worklog entries retain their original filenames.

### Voice session and Gemini shared history follow-up

Owner entered realtime Voice in this same task; spoken delegation arrived successfully. Owner reports Settings > Voice exposes a global Voice chat hotkey and a floating voice panel with mic/speaker/text controls. Focus-triggered panel movement remains a hypothesis, not observed evidence. Upper mouse press reportedly not captured by shortcut recorder. Suggested keyboard chord Ctrl+Alt+Shift+V is only a candidate, not saved or verified. Installed desktop launcher found at /usr/share/applications/chatgpt.desktop, Exec=chatgpt %U, executable /usr/bin/chatgpt. No launcher or mapping edits.

Read owner's shared Gemini conversation https://share.gemini.google/6s0iTqxHMJma via in-app browser after web fetch failed. Title: Wayland Mouse Macro for Gemini. Historical raw evtest excerpt confirms lower button EV_KEY 275 BTN_SIDE (press/release), matching current preset. History describes initial wmctrl/xdotool, incorrect/reused trigger shortcuts, duplicate launches and owner-reported remote interaction prompts; these are historical reports, not fresh causal verification. Working installed GNOME extension/Python implementation inspected earlier supersedes those scripts. Do not restore obsolete script from shared chat. Owner wants Input Remapper retained for specific Logitech M705 and upper button to focus/launch ChatGPT and enter conversation, next press to exit to text. Built-in global Voice hotkey may simplify this, but its second-press behavior and cold-launch behavior remain unverified. Browser/connector reads are not shell output and are summarized here.

Owner identified intended upper mouse button interactively in Input Remapper as Mouse Button 5. Installed inputremapper/configs/input_config.py mouse-button naming formula maps Mouse Button 5 to Linux code 276 (BTN_EXTRA), distinct from existing Gemini code 275. No mapping applied yet.

### Upper-button preset staged, not applied

Added EV_KEY 276 Mouse Button 5 -> Control_L + Alt_L + Shift_L + v in existing M705 _home_denebeim_.json preset. Verified original entries equal backed-up entries. Backup /home/denebeim/.local/state/chatgpt-voice-toggle/backups/20261114-102413/_home_denebeim_.json. Attempt to apply via input-remapper-control failed exit 4: no input devices visible to user tool. sudo -n --list-devices failed: interactive authentication required. No preset activation or Voice shortcut configuration verified. Owner then reiterated script must ensure target app is launched/focused before emitting Voice command; clarify spoken Gemini versus original ChatGPT target before wiring. New chord is currently only staged in preset; existing live Gemini behavior not intentionally changed.

### ChatGPT sister launcher installed, app hotkey/live acceptance pending

Desktop Polkit request succeeded: input-remapper-control enumerated Logitech M705 and started _home_denebeim_ preset, exit 0. Owner's initial button attempts occurred before launcher/Voice shortcut wiring and produced no observed Voice change.

Installed /home/denebeim/.local/bin/chatgpt-voice-toggle and GNOME custom1 binding Ctrl+Alt+Shift+V, invoking it through shared logger. Script focuses/launches observed XWayland ChatGPT app, checks desktop lock and focus, serializes concurrent clicks, then emits distinct Ctrl+Alt+Shift+F12 through evdev/uinput, releasing keys in finally. App's native Voice hotkey must be set to that combination. Requested user to record it in Settings > Voice; clarified this is one manual app-setting step because current connection cannot operate Settings UI. No app keybindings file edited.

Inspected installed app archive: global Voice command calls toggleGlobalHotkeySession; idle branch requests global_hotkey_new_thread, active branch stops session, pending branch cancels/reset. Thus global shortcut creates a new Voice thread rather than guaranteeing current-chat continuation.

Verified live ChatGPT focus-only exit 0. Simulated focus-loss refusal emitted zero keys, simulated chord press/release ordering passed, real virtual keyboard creation without keys passed. No actual Voice key sent by agent. Gemini script/extension left untouched and custom0 fields compared unchanged. Backed up prior GNOME shortcut list under ~/.local/state/chatgpt-voice-toggle/backups/20261114-111910. Added MOUSE-VOICE.md with paths, architecture, backup, activation, rollback and pending acceptance. Still pending app hotkey setting and end-to-end user start/stop/cold-launch/text-return/Gemini regression checks.

## Personal mouse voice snapshot — 2026-11-14

Added ai-twiddles/ with two playbooks, captured installed helpers and brief personal-use instructions. No tests or playbook application per owner request; no desktop settings changed, commit or push. Initial authoring command failed because system Python lacked PyYAML; used JSON (valid YAML) without installing anything. GitHub issue creation rejected by automatic approval review for external disclosure of personal desktop configuration to an unverified destination; pending explicit owner approval. Unrelated changes preserved.

## AI twiddles user-home correction — 2026-11-14

Created local branch codex/ai-twiddles-user-home. Both playbooks gather the running user home from Ansible facts, pass paths/preset/logger location as arguments, and template Gemini Chrome profile (Default, override supported). Removed personal username/home paths in ai-twiddles; fixed literal newline writing. Both Ansible syntax checks, Python compilation checks and scoped whitespace review passed. No playbook application or desktop changes. Original directory was ignored/untracked; explicitly staged only its eight files. Existing dirty files excluded from commit. Publication (issue/push/PR/merge) awaits owner review. Detailed notes: ai-twiddles/BRANCH-NOTES.md.

## AI twiddles readability and caveats — 2026-11-14

Clarified owner-reported Ubuntu 26.04 LTS working live setup versus syntax-only unapplied playbooks, local desktop-user context and existing GNOME/app assumptions. Converted playbooks from JSON representation to conventional YAML with unchanged parsed values; pretty-printed extension metadata and Gemini runtime state JSON (preset/config writers already indented). Both syntax checks, embedded Python/helper compilation and scoped whitespace check passed. No live application or publication; scoped ai-twiddles-only local commit on codex/ai-twiddles-user-home.

## Per-twiddle directories — 2026-11-14

Reorganized ai-twiddles into logitech-m705-gemini-dictation/ and logitech-m705-chatgpt-voice/, each with playbook.yaml, needed files/ and its own usage/platform/prerequisite/caveat README. Root README is a short rough-experiment index. Logger path updated for deeper playbook location; local source references retained. Branch history notes preserved. Moved references/links and both syntax checks pass; no live application/publication. Scoped local commit only; unrelated dirty files excluded.

## Mouse experiment publication preparation — 2026-11-14

Original feature branch had unrelated Hermes ancestry. Created codex/ai-twiddles-m705 from refreshed origin/main in /tmp/mostly-harmless-m705-pr and cherry-picked only three twiddle commits. Standalone directory now includes its logger and adapted mouse setup/rollback notes, concise per-experiment commands and caveats. Detailed original branch notes retain user philosophy and AI authorship disclosure (exact model identifier unavailable). Syntax/reference checks passed; no deployment. Issue creation again rejected by automatic approval review for external disclosure; no issue workaround attempted. User authorized open PR and no merge; review suggestions await user choice.

## Publication blocked by automatic review — 2026-11-14

Publication outcome: clean publication branch codex/ai-twiddles-m705 ends at aa805cf in /tmp/mostly-harmless-m705-pr. Its diff against origin/main is exactly 11 files under ai-twiddles; no unrelated repository files. Both syntax checks, source/logger/link resolution, Python compilation, JSON parsing and whitespace review passed without applying playbooks. Original detailed branch preserved at 1988871 before this outcome note. Automatic approval review rejected both issue creation and push for insufficient trusted authorization to disclose the personal desktop configuration/helper code to denebeim/mostly-harmless. No issue, push or PR succeeded; no review/check monitoring possible. No alternate publication route attempted. Need direct owner approval of this exact destination and content before retrying. No merge.

Publication succeeded after direct owner authorization: pushed codex/ai-twiddles-m705 at aa805cf and opened PR #12, https://github.com/denebeim/mostly-harmless/pull/12 (Capture Logitech M705 Gemini dictation and ChatGPT Voice experiments), against main. Verified open, not merged, 11 files under ai-twiddles. Authorship disclosure included; exact model identifier unavailable. Original detailed branch preserved; no merge or review-driven changes.

## 2026-11-14 — Durable independent work-log branch

Owner confirmed mostly-harmless is always the work-log destination and authorized
regular commits/pushes, including smaller meaningful developments. Created
`codex/work-log` in isolated `/tmp/mostly-harmless-work-log` from refreshed
`origin/main` at a4b88f6. Copied the existing log without feature code; original
dirty checkout and Eddie branches preserved. Main already contains mouse experiment
PR #12 at this refreshed baseline; this task did not merge it. Eddie follow-up
remains deferred for owner polish and was not merged.

Added WORKLOG-WORKFLOW.md and AGENTS.md guidance for event-based documentation,
explicit path staging, reviewed commits/pushes and remote-hash verification before
handoff. Installed the workflow reference in the original checkout as well. The
remote branch is durable; the temporary checkout is recreatable. No scheduled
automation or background syncing exists. Raw chat.log remains private/uncommitted.

Initial unprivileged fetch failed on Git metadata permissions and local SSH system
configuration permissions. Authorized elevated Git access with ssh -F /dev/null
refreshed origin successfully. Publication verification is recorded in the next
checkpoint; do not treat branch creation alone as a completed push.

### Work-log publication blocked — November 14

Documentation-only checkpoint c742f1b saved locally; staged whitespace review
passed and only AGENTS.md, WORKLOG-WORKFLOW.md and WORKLOG.md were included.
Automatic approval review rejected the combined commit/push request before
execution because the historical log may contain nonpublic infrastructure details
and the reviewer did not accept the relayed authorization for this exact payload
and GitHub destination. A separate local commit succeeded. No push or alternate
publication route was attempted after rejection. Direct owner approval of publishing
these three files to denebeim/mostly-harmless on codex/work-log is required.
Remote existence/hash remains unverified; initial publication is not complete.
No Eddie merge, feature-code commit, timed automation or background sync occurred.

### Owner scope correction — November 14

Owner requested only WORKLOG.md on the independent branch. Removed the unsolicited
WORKLOG-WORKFLOW.md from both checkouts after preserving its exact text for review;
removed only the setup-specific continuity section from AGENTS.md and preserved
all preexisting agent guidance. Replaced the unpublished setup commits with a
work-log-only commit. Earlier setup commit hashes above describe superseded local
history. Publication remains blocked; no push was attempted. The remote branch
is not verified or backed up yet. Ordinary tracked AGENTS.md content follows each
branch checkout; untracked local AGENTS.md does not gain branch-specific versions.

### Public log address sanitization — November 14

At owner request, replaced exact internal addresses with existing host names or
service/subnet roles, including DMZ, Eddie, Benjymouse, Pi-hole, LAN gateway,
WireGuard tunnel peers/subnets, test guest and loopback. No uncertain host mappings
were invented. Replaced the unpublished branch checkpoint so its newly introduced
WORKLOG.md history contains only the sanitized version. The origin/main baseline
already contains addresses in historical WORKLOG.md content; this local edit does
not erase existing remote history. No push attempted; approval blocker remains.
An initial masked diagnostic missed sentence-ending addresses and printed two
address occurrences to the existing private command log; the matcher was corrected
before edits and validation. Raw chat.log was not rewritten.

### Pending security discussions and publication approval — November 14

Owner reviewed the sanitized work log and explicitly approved pushing this
work-log-only branch to denebeim/mostly-harmless, accepting existing historical
address/topology disclosure without rewriting already-remote history. Keep exact
internal IP addresses out of future entries. Earlier approval-blocker entries are
historical; successful publication still requires remote verification.

Pending DMZ containment design/audit: owner wants a compromise, even with root,
to be unable to pivot into internal systems or obtain reusable privileged
credentials. Evaluate egress, identity/IPA trust, SSH administration, and placement
of credentials and private keys later. This is a desired security property to
evaluate, not verified current behavior or a guaranteed property. Owner wonders
whether the DMZ is directly internet-connected; topology is unverified here.

Pending SSH private-key inventory and laptop compromise/recovery discussion:
owner believes private SSH keys may exist only on the laptop, but is unsure.
Record this as an unverified belief requiring a later audit and recovery planning.
Owner is thinking about these questions and needs to think further. No key
inspection, infrastructure audit or security configuration changes were performed
for these notes. Eddie remains deferred and unmerged.

Publication retry after owner approval was rejected before execution by automatic
approval review: the reviewer did not accept relayed approval as trusted direct
authorization for this infrastructure-derived log and GitHub destination. No push
occurred; no alternate publication route attempted. Notes remain saved locally;
remote branch/upstream verification is pending.

## 2026-11-16 — Codex experiment boundary and reusable workflow prompts

Owner authorized a Codex-specific `ai-twiddles/codex/` directory, isolated experimental branches, and ~~autonomous scoped commits/merges through normal repository protections~~ (superseded by the owner acceptance workflow above). Work intended for publication in the owner's voice follows a separate collaborative process. Owner explicitly requested these reusable prompts be committed and pushed to GitHub on this independent `work-log` branch. This entry is an operating agreement, not a claim that every publication step below has already completed.

### November 16 verification and open items

- Main already contains separate captured mouse setups under `ai-twiddles/logitech-m705-chatgpt-voice/` and `ai-twiddles/logitech-m705-gemini-dictation/`. Both committed playbooks refer to `ai-twiddles/log-session.py`, which appends to the repository-root `chat.log`. It remains unchanged.
- Earlier inspection mistakenly treated ignored `roles/setup-gemini/` files as the current setup. Main's committed tree and matching local Git history contain no `web_agent.py` at either the spoken underscore path or the hyphenated path. No evidence of overwriting Gemini's file was found; the file may be elsewhere or not yet saved. No contact with Gemini.
- The separate `scripts/log-session.py` had the old Eddie-log default. This task changed its default to chat.log, removed argv metadata, and set private new-file creation permissions; changed two active documentation references and appended a local inspection note. Those pending edits remain unstaged in the owner's main checkout, outside the new experiment branch. No further shared logger edits after the owner requested coordination. Initial inspection output was recovered into existing chat.log; a stdout/stderr/failure-status probe verified that exact destination. Read-only conflict investigation deliberately made no log writes while compatibility was unclear.
- New isolated branch `codex/ai-twiddles-codex-workflow` starts from current origin/main. It adds only `ai-twiddles/codex/README.md` and `ai-twiddles/codex/AGENTS.md`; no mouse scripts or shared files are moved. The docs point to this independent work-log branch. Local GitHub CLI authentication failed; the connected GitHub service is available.
- Original API request remains a product choice. Existing ChatGPT launcher invokes built-in app Voice, not a custom API client. Official Realtime mini model docs say no free tier; eligible Pro/Business API credits may provide a credits-first balance before purchased credits, but do not extend built-in Voice limits. A separate API voice client would not automatically inherit this assistant's task/history/tool integration. No API calls, billing changes or Voice replacement.
- Next: validate/commit the two scoped docs, push the experimental branch, open a normal PR and merge only if normal requirements permit; publish this independent log update with an explicit-path commit and verify the remote hash. Preserve unrelated requirements.txt and all original dirty-checkout changes.

### Workflow publication results — November 16

The independent work-log update with reusable prompts was committed as fc581ab and pushed to origin/work-log. The owner then approved the seeing-stone principle above; it is included with this outcome checkpoint.

The experimental documentation commit 0ce9212 contains exactly two files under ai-twiddles/codex/. Opened https://github.com/denebeim/mostly-harmless/pull/16 (Document Codex experiment ownership and publication workflow). GitHub reported it mergeable; no submitted reviews, commit statuses or PR workflow runs were returned at inspection. Normal squash merge succeeded at 77fa0c6 on main, without bypass flags, a force push or branch-setting changes. The independent work-log branch was not merged into main.

Validation: staged whitespace checks passed for both branches; reviewed explicit file scope. This was documentation-only, so no runtime tests or deployments. Existing shared logger, Gemini and ChatGPT mouse playbooks/live launchers remain unchanged by the organizational commits. The owner's original dirty main checkout and unrelated requirements.txt change remain intact. Local metadata initially required the normal elevated worktree/staging permissions; ignored new files were explicitly staged by exact path. GitHub CLI reported bad credentials; connected GitHub PR APIs succeeded.

Remaining: optional API voice fallback still needs a product choice and account/budget verification. No API-based replacement implemented or billed. Pending earlier shared-logger edits remain outside these commits and require separate coordination if they are to be kept or reverted.

## 2026-11-16 — Owner review required before main (supersedes earlier merge permission)

The owner clarified the invariant: they hear the report, discuss it, inspect the work, and explicitly approve what goes onto main. Earlier broad autonomous experimental merge permission is superseded for future integrations. Codex may continue autonomous work, commits and pushes within its scoped experimental branch; approval of the workflow is not approval of every future change. Do not enable auto-merge or merge a pending correction before that review/approval.

Updated the reusable prompts above to reflect the current rule. Existing historical entries describe the authorization in effect when they were written; prior workflow PR already merged under that authorization is not undone. The separate public work-log commit/push authorization remains valid within its scope and does not authorize merging work-log into main.

Prepared isolated correction branch codex/ai-twiddles-review-before-main from current origin/main. Its only planned main-target changes are ai-twiddles/codex/README.md and AGENTS.md. Commit/push and a reviewable PR are authorized; the correction must remain unmerged pending explicit owner approval. No mouse setup, Gemini files, shared logger, API client or live system changes.

Correction publication checkpoint: scoped commit df1c190 pushed on codex/ai-twiddles-review-before-main; https://github.com/denebeim/mostly-harmless/pull/17 (Require owner approval before integrating Codex experiments) is open and unmerged, explicitly awaiting owner review/approval. No auto-merge enabled. Main remains at prior approved-era merge 77fa0c6. Scoped whitespace review passed; a literal wording check initially expected “auto-merge” while README used “automatic merge”; corrected wording check passed for both files. No runtime changes. This independent work-log update is separately authorized for commit/push; it is not a main integration.

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

## 2026-11-18 — Work-log authorship

Author: OpenAI Codex

Added work-log attribution rules so each new entry identifies its writer and readers can
distinguish the user's own words from AI paraphrases and suggestions.


## 2026-11-18 — Portable project handoff

Author: OpenAI Codex

Added a copyable current-state handoff for Eddie, Gemini, or Codex. Checked the
summary against controller documentation, the recorded operating handoff,
work-log history, and the current Eddie and shared VM declarations. Live hosts
were outside the scope of this documentation check.

## 2026-11-18 — Future Projects and blog preparation

Author: OpenAI Codex

Prepared proposed Future Projects entries and a first-pass Deepthot blog draft
for owner review in the local Codex area. The existing collection's location
could not be verified. The proposals reserve Pill Box for review in its
existing entry. Theme imagery and execution remain pending.


## 2026-11-18 — Dedicated work-log checkout

Author: OpenAI Codex

Placed today's authorship rules, portable handoff and draft-preparation entries
on the local work-log branch. Recorded ~~frequent local commits by the agent and~~
~~GitHub pushes by the owner, especially for AI handoffs~~. The current workflow
allows scoped work-log pushes by the agent. Preserved the explicit
review and approval requirement for main integration.

## 2026-11-20 — ISC BIND9 and Kea DHCPv4/DDNS prototype on testservices

Author: Zoo

- Created branch `gemini/isc-dhcp-dns` and subdirectory `ai-twiddles/gemini/isc-services/`.
- Spun up `testservices` (VM 8315, `192.168.42.202`, `tags: [ipa]`) using `vm.yaml` via `ai-twiddles/gemini/isc-services/testservices.yaml`.
- Populated `isc_services.yaml` and `kea-dhcp4.conf.j2` from `/etc/pihole/pihole.toml` on `services` (`192.168.42.2`), preserving user-owned machine IPs (`giles` `.98`, `willow` `.99`) and configuring the 20-IP `user_machines` pool at `192.168.42.70 - 192.168.42.99`, `vm_clients` at `.200 - .239`, and IoT VLAN `192.168.43.0/24` at `.100 - .250`.
- Verified on `testservices`: `named-checkconf`, `kea-dhcp4 -t`, and `kea-dhcp-ddns -t` passed; `bind9`, `kea-dhcp4-server`, and `kea-dhcp-ddns-server` are active and enabled (`ok=10 changed=2 failed=0`).
- Note for future IP renumbering: `valheim` (`.123`) is a game server and belongs in the **Applications** group; `plex` (`.186`) and `arr` (`.131`) belong in their own **Media** group. Both are currently up and should be moved when we get to them.
- Next: review reverse zone files (`db.192.168.42`, `db.192.168.43`), inventory `/etc/pihole/dhcp.leases` on `services` (via `ansible` credentials), and refine actual IoT/user MAC OUI lists.
- Future project note (owner direction): IoT sandboxing needs to be fleshed out in Future Projects—most IoT devices are on Wi-Fi, while Zigbee/Philips Hue can be isolated more easily; deferred for later engineering.
- Architecture & PR #20 review (2026-11-21, `Author: Zoo`): Split `roles/services/isc_dns_dhcp` into `roles/services/bind9` and `roles/services/kea`, declared explicitly in `services.yaml` (`tags: []`, no IPA/DNS/DHCP bootstrap dependency). Gated `bind9` and `kea` service startup on `bind9_cutover_pihole` / `kea_cutover_pihole` (default `false`), added `PTR` reconciliation to `nsupdate`, and replaced `failed_when: false` on `pihole-FTL` stop with `service_facts` check.
- IPA DNS note (2026-11-21, `Author: Zoo`): `services` (`192.168.42.2`) currently serves `_kerberos._tcp.local.deepthot.org` SRV records while `ipa` (`192.168.42.4`) is not serving DNS externally. Owner direction: `services` (BIND9) should be the primary DNS node and `ipa` the secondary (with FreeIPA SRV records served by `services` and optional AXFR to `ipa`), to be addressed when we get to the IPA automation.

## 2026-11-21 — Prepare Eddie for Authentik sign-in

Author: OpenAI Codex

Added opt-in OpenID Connect to the isolated Eddie LibreChat playbook
(commit e87d9aa). It uses the existing auth.deepthot.org Authentik instance,
keeps OIDC secrets in a private environment file sourced from vaulted
variables, and moves LibreChat to a loopback Docker listener behind an
Eddie HTTPS proxy when enabled. Authentik controls application access and
MFA. Local admin login remains available, and ordinary self-registration is
disabled. Documented the callback, provider settings, tests and rollback.

Ansible syntax and both rendered Compose modes passed with dummy values.
A dry run on Eddie with OIDC disabled reported changed=0 and failed=0.
Eddie's proposed HTTPS endpoint refused connections and Authentik returned
404 for the proposed eddie discovery URL. The publicly presented Let's
Encrypt certificate covers *.local.deepthot.org. A TLS route for Eddie,
an Authentik application/provider and secure credentials still need
configuration before an end-to-end sign-in test. No live change was made.

## 2026-11-21 — Eddie Authentik sign-in live

Author: OpenAI Codex

Issued a hostname-specific Let's Encrypt certificate for
eddie.local.deepthot.org through a Cloudflare DNS challenge run on the DMZ.
The certificate's private key remains on Eddie and the Cloudflare credential
remains on the DMZ. Eddie now terminates HTTPS directly with a pinned Nginx
container and proxies to LibreChat on localhost. There is no new DMZ route
or WAN forwarding. The renewal procedure is checked in, with no unattended
renewal configured. The current certificate expires February 20, 2027.

Registered Eddie as a confidential Authentik OpenID Connect application
with a single exact HTTPS callback. Access is scoped to Folks who Live Here
and an Eddie-only binding for ookami. Policy checks allowed Joy, Cheryl and
ookami and denied an active nonmember. Ookami has no email on their
Authentik profile. LibreChat requires an email-shaped identity for
account creation. Regular LibreChat registration is disabled and the
local administrator sign-in remains advertised. OIDC client settings are
in a private Ansible Vault on Benjymouse with no secrets committed.

Verified trusted HTTPS, both sign-in options, the authorization redirect
and the exact callback. Joy confirmed that Authentik returned her to
LibreChat. Live Ansible convergence succeeded and the immediate rerun
reported changed=0 and failed=0 with the Ollama check passing. The
deployment is in local experiment commit e3a3469.

## 2026-11-21 — Assemble the Eddie SSO rebuild playbooks

Author: OpenAI Codex

Added rebuild-sso.yaml and authentik.yaml to the isolated Eddie experiment
in commit 9b4f92a. The rebuild entrypoint applies the Eddie-specific Authentik
provider and bindings, checks or issues the Eddie certificate, and deploys
the Docker stack. It depends on the existing VM, DNS, Authentik and DNS
challenge infrastructure, and the private controller vault. It does not
rotate an existing provider secret. Local syntax, scoped inventory and
staged whitespace checks passed. The automatic approval review declined
a live run of the new combined entrypoint. Joy will review when ready.

## 2026-11-22 — Eddie persona and review draft

Author: OpenAI Codex

Added Joy's corrected soul file to the Eddie playbook in commit 2e17b71.
New chats use the Eddie model specification by default. Plain Ollama selects
the same local model with an empty persona prompt. Ansible rendered both
choices correctly, the rebuild syntax check passed, and a test merge against
origin/main found no conflicts. Automatic approval review declined the
live apply because a LibreChat restart was not explicitly authorized.
The working Eddie instance continues with its prior settings.

Published the isolated branch as draft PR #23 for review before integration.

## 2026-11-22 — Make eddie.yaml the full build entrypoint

Author: OpenAI Codex

Joy clarified the machine playbook contract. The machine-named entrypoint
must reach the complete configuration after a rebuild, while each feature
remains runnable on its own for changes to an existing machine. Eddie's
master now imports the LibreChat SSO setup after VM and application
provisioning. The existing Docker permission and the new VM's verified
host key are reused. An alternate VM ID can keep the powered-off original
available as a rollback. LAN DNS stays a prerequisite; no DNS changes were
made.

Local syntax and play order checks passed for the master and feature
entrypoints. The test merge found no conflicts. Updated draft PR #23
at commit 3ef0bb5. No Proxmox or live build was run.

## 2026-11-22 — Eddie clean-build test on VM 4242

Author: OpenAI Codex

Joy ran the full Eddie master on a fresh VM, keeping the previous Eddie
powered off. The first pass created, patched and pinned the new VM, then
stopped because the controller lacked an IPA Kerberos ticket. After kinit,
the next pass reached IPA enrollment, which failed on LDAPS TCP 636.
A packet trace showed an explicit administrative rejection from the IPA
VM; firewalld's active zone allowed FreeIPA LDAP but not LDAPS. After Joy
opened access for the test, enrollment and automount completed.

The next pass installed Docker, validated the K5200 driver, verified
Ollama over the LAN and downloaded Qwen. Hermes creation timed out on
Docker's default 60-second local API read timeout. The image and container
were absent at the follow-up check. Raised the Hermes task's timeout to
900 seconds in commit 9657e9b and updated draft PR #23. Syntax passed.
The retry, LibreChat first SSO login, and test chat are still pending.

### Master playbook retry on VM 4242

Author: OpenAI Codex

Joy reran the master with the longer Hermes Docker timeout. Hermes started
and the role passed its local inference check. The existing Authentik app
converged with no changes, an Eddie-specific certificate was installed on
the new VM, and LibreChat, MongoDB and Nginx started. The complete run
returned exit 0 with no failed or unreachable hosts. The controller checked
HTTPS and the app container reached Ollama. A separate probe confirmed
trusted HTTPS and Authentik's authorization redirect with the exact callback.

MongoDB had zero users before the human test. First-sign-in registration
was enabled. The running config showed Eddie as the default with a persona
prompt and Plain Ollama with an empty prompt. Joy's first interactive sign-in
and chat, and any Docker uninstall or VM retirement, are separate checks.

Joy completed the first interactive Authentik sign-in and got a reply. The
fresh database counted one OpenID account and one saved assistant reply;
the saved conversation used the Eddie preset. Checked counts and preset
only, without reading conversation contents from the database. Proxmox
listed eddie.good (314, stopped) and eddie (4242, running). Neither VM
was removed.

## 2026-11-22 — Production Eddie rebuild on VM 314

Author: OpenAI Codex

After Joy's confirmation, verified trusted LDAPS from test Eddie to IPA on
636. Joy enabled a runtime and permanent IPv4 firewalld rule for
192.168.42.0/24 on IPA VM 204. Revisit that rule during IPA playbook work.
No backups were found on the reachable Proxmox stores; PBS was unreachable.
Confirmed eddie.good (314, stopped) and test Eddie (4242, running), shut down
4242 cleanly and destroyed both confirmed VMs. Verified their IDs were clear
before starting production Eddie as 314 from draft PR #23 commit 483ea75.
Joy withdrew the additional IPA record deletion request. The production
playbook was briefly paused while inspecting the existing IPA record, then
resumed without deleting any IPA objects.


## 2026-11-24 — Prepare Eddie LibreChat for owner acceptance

Author: OpenAI Codex

Created acceptance/eddie-librechat from current main and retargeted PR #23.
Pushed 8e730c0 to the PR branch. Moved LibreChat into the regular playbook
and role layout and used the live Proxmox tag to reconcile the optional
service. Confirmed Eddie uses a host-specific certificate. The reference
configuration defines a wildcard certificate. A shared mount for it
remains unverified. The role accepts configurable certificate and key paths.

Ansible syntax checks, both rendered Compose configurations and 15 unit
tests passed. A disposable local Compose project confirmed tag-off removed
its containers and network, retained its volume and instance secret file,
and converged on a second run. Full disposable Proxmox rebuild and
interactive SSO acceptance remain pending. No deployment changes made to
Eddie or Authentik. Joy performs both merges. Issue #36 is deferred.

### Sourcery follow-up

Author: OpenAI Codex

Pushed 5e944b0 to PR #23. The tagged deployment now requires an explicit
opt-in for the HTTP pilot, passes Authentik's advertised issuer to LibreChat,
and supports the delegated Authentik account's sudo-only Docker access.
Documented first-sign-in provisioning and a local HTTPS recovery account.
The temporary per-VM renewal helper stays until the planned DMZ TLS cutover.
Serial deployments and tag edits outside a run remain the operator workflow.

Ansible syntax, 15 unit tests, and the tagged HTTP refusal check passed.
The direct Authentik discovery response on Services advertised the expected
issuer. The configured HTTPS address could not be reached from Eddie or
Benjymouse during this check. Interactive SSO and recovery logins remain
pending. Production was not changed.

## 2026-11-25 — Close out Eddie LibreChat

Author: OpenAI Codex

Joy and Codex agreed that the Eddie LibreChat implementation and review work
are done. PR #38 merged into the acceptance branch, then PR #39 brought those
fixes into main at 5407f6e. Compared the LibreChat files on main with the
reviewed diff and found no differences. The LAN DNS override on Services
restored Authentik discovery over HTTPS from Eddie and its LibreChat
container. Joy confirmed Authentik login in a regular and incognito browser.
A post-merge Eddie playbook run, its no-op rerun, and interactive LibreChat
SSO, local recovery login and Qwen reply on that revision are not recorded.
No production playbook run is required just to close the code review.
The LAN override needs to be carried forward when BIND9 takes the LAN listener.

The next Eddie decision is whether to pursue Inkling 2 Mini. Existing issue
#36 already tracks it. If Joy chooses to proceed, use that ticket to verify
Linux runtime compatibility and usable inference, then update Eddie's
opt-in profile and playbooks to persist the measured RAM and storage sizing.
Keep Qwen as the default. Offer Inkling as a separate plain model option,
like Plain Ollama, without applying Eddie's persona. No model or VM sizing
changes were made for this closeout.
