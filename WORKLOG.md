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

## Active priority: Eddie

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

1. Inspect the running QEMU command lines for Plex and Eddie.
2. Inspect Proxmox configuration backups for historical PCI assignments.
3. Reconstruct the last known working GPU-to-Eddie configuration.
4. Check IOMMU grouping and device isolation before making any changes.
5. Make the smallest justified change, with explicit approval, then verify GPU access in Eddie.

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

## How to maintain this log

At each meaningful work milestone, update:
- current objective and status;
- verified findings (with evidence or references where practical);
- changes actually made and how they were verified;
- unresolved questions, risks, and dependencies;
- the next concrete action.

Use dates when known. Do not invent timestamps or imply continuous monitoring. This log is a
session-maintained record, not an autonomous live feed.
