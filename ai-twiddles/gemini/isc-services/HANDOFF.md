# Gemini Handoff — ISC BIND9 & Kea DHCPv4/DDNS

> Copy and paste this file into Gemini on Windows to resume with full context.

## Current State & Branches
- **Twiddle branch:** `gemini/isc-dhcp-dns` (`ai-twiddles/gemini/isc-services/`)
- **Integration branch (ready for PR):** `gemini/isc-dns-dhcp` (pushed to `origin/gemini/isc-dns-dhcp` at `27490ab`)
  - Role: `roles/services/isc_dns_dhcp/` (`tasks/main.yaml`, `handlers/main.yaml`, `defaults/main.yaml`, `templates/`, `files/hosts.csv`, `README.md`)
  - Playbooks: `testservices.yaml`, `services.yaml`, `vm.yaml` (gated on `tag_dns` or `tag_dhcp`)
  - PR URL: https://github.com/denebeim/mostly-harmless/pull/new/gemini/isc-dns-dhcp
- **Worklog branch:** `work-log` (pushed to `origin/work-log` at `6732541`, signed `Author: Zoo`)

## Test VM (`testservices`)
- **VM ID:** `8315` | **IP:** `192.168.42.202` | **Tags:** `[ipa, dns, dhcp]`
- **Verified on `testservices`:** `bind9`, `kea-dhcp4-server`, and `kea-dhcp-ddns-server` are installed, enabled, and running; `named-checkconf`, `kea-dhcp4 -t`, and `kea-dhcp-ddns -t` all pass.
- **Live `services` (`192.168.42.2`):** Untouched. Pi-hole is still serving live LAN DNS/DHCP. `services.yaml` is syntax-checked and ready for the owner to run when cutting over.

## IP Zones & Data Source (`hosts.csv`)
- Source of truth imported from `/etc/pihole/pihole.toml` on `services` into `roles/services/isc_dns_dhcp/files/hosts.csv` (`name,ip,mac,in_etc_hosts,zone_group`).
- **Ranges:**
  - `.1`: `router`
  - `.2 – .31`: Low-level system, Auth, DMZ, Core (in BIND9 DNS + `/etc/hosts`)
  - `.70 – .99`: User machines (20-IP `user_machines` pool + reservations `giles` `.98`, `willow` `.99`)
  - `.100 – .129`: Storage & Core Infra (`freenas` `.115`)
  - `.130 – .159`: Applications (`eddie` `.132`)
  - `.160 – .199`: Services
  - `.200 – .239`: Dynamic VMs (`vm_clients` MAC OUI class: `52:54:00`, `bc:24:11`, `00:16:3e`)
  - `192.168.43.100 – .250`: IoT VLAN (`192.168.43.0/24`, `iot_devices` MAC OUI class)
- **Pending renumbering note:** `valheim` (`.123`) belongs in **Applications**; `plex` (`.186`) and `arr` (`.131`) belong in their own **Media** group.
- **Secrets:** `KEA_DDNS_KEY_SECRET` is read from `.envrc` via `ansible.builtin.env` (no secrets committed).

## Next Steps
1. Open/review PR from `gemini/isc-dns-dhcp` -> `main`.
2. Add reverse zone templates (`db.192.168.42`, `db.192.168.43`) and refine IoT/user MAC OUI lists.
3. Read `/etc/pihole/dhcp.leases` on `services` (using `ansible` credentials) to classify any remaining active dynamic leases.
