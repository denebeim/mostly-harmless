# Changelog

## 2026-11-07 — Eddie brought to life

- Rebuilt the former Hermes VM as Eddie (Proxmox VM 314), with a serial console,
  explicit LAN DNS settings, and Quadro K5200 passthrough.
- Added a base-VM smoke-test entrypoint without first-boot package upgrades and
  a full provisioning path with Ubuntu updates and conditional reboot, IPA/SSSD
  identity and NFS automount, Docker, and a dedicated Hermes service account.
- Installed the legacy NVIDIA 470 driver and Ollama 0.40.15; verified local
  Qwen3.5 4B inference with all model layers on the GPU through Vulkan.
- Connected Hermes to local Ollama and verified the reply: “Eddie is online.”
- Added controller Kerberos-ticket enrollment using private, one-time host
  credentials rather than an Ansible administrator-password prompt.
- Added final functional acceptance checks and bounded retries for Hermes's
  first-session `session.create` timeout.
- Recorded future DNS/DHCP design work: Pi-hole owns LAN DNS for now; evaluate
  BIND9 and a separate DHCP service later. Private configuration stays excluded.

Validation: base rebuild and DNS checks passed. The latest full provisioning run
passed identity/home, Docker, GPU driver, and Ollama setup, then failed on the
first Hermes session startup deadline. A targeted retry returned the expected
reply. Playbook/helper syntax checks pass. A clean full-run recap after the retry
change, and an end-to-end test of ticket-based fresh-host enrollment, are still
pending. This milestone does not claim those checks passed.

### PR review follow-up

- Review #1: include EFI and TPM state disks in both destructive allowlist checks.
- Review #2: replace the separate digest-check/delete sequence with a shared,
  digest-acquired Proxmox lock held through graceful shutdown and destruction.
- Review #6: verify the tracked entrypoint/role files in an exported checkout and
  explicitly allowlist reviewed provisioning dependencies for future changes.
- Review #9: recognize the cold-session timeout in stdout, stderr, or both.
- Add eight offline regression tests for disk coverage, locking/cleanup behavior,
  and retry stream handling. Live destructive testing is intentionally excluded.
