# ISC DNS & DHCP (`isc_dns_dhcp`)

This role and [`testservices.yaml`](../../../testservices.yaml) deploy **ISC BIND9** (authoritative DNS), **ISC Kea DHCPv4** (DHCP server with MAC-based client classification), and **ISC Kea DHCP-DDNS** (dynamic DNS updates) on an Ubuntu VM.

## Where Data Lives (Edit Before Running)

- **Host & DHCP Reservations:** [`files/hosts.csv`](files/hosts.csv)
  - Columns: `name,ip,mac,in_etc_hosts,zone_group`
  - Add or update rows here before running the playbook. Any row with a `mac` gets a static Kea DHCP reservation; any row with `in_etc_hosts=true` is written to `/etc/hosts`; all rows are added to BIND9 DNS.
- **Role Defaults:** [`defaults/main.yaml`](defaults/main.yaml) (domain name, subnet CIDRs, and `KEA_DDNS_KEY_SECRET` lookup).

## Prerequisites

1. **Controller Python environment & `direnv`:**
   - Ensure `.envrc` is loaded (`direnv allow` if prompted) so `PROXMOX_USER`, `PROXMOX_PASSWORD`, and (optionally) `KEA_DDNS_KEY_SECRET` are set in your shell.
   - Activate the project virtual environment:
     ```sh
     source .venv/bin/activate
     ```
2. **Kerberos ticket (only if the `ipa` tag is enabled):**
   ```sh
   kinit admin
   ```

## How to Run the Playbook

1. **Check syntax first (safe, makes no changes):**
   ```sh
   ansible-playbook --syntax-check testservices.yaml
   ```

2. **Deploy `testservices` (creates the VM if absent, enrolls in IPA, and installs BIND9 + Kea):**
   ```sh
   PYTHONUNBUFFERED=1 ansible-playbook testservices.yaml --ssh-common-args="-F /dev/null"
   ```

## How It Organizes IPs & MAC Filtering

- **Low-level system hosts (`192.168.42.1 – .31`):** Static reservations written to both BIND9 DNS and `/etc/hosts`.
- **User machines (`192.168.42.70 – .99`):** 20-IP dynamic pool (`user_machines` class) plus static reservations (e.g., `giles`, `willow`).
- **VMs (`192.168.42.200 – .239`):** Dynamic pool matched by Proxmox/QEMU/KVM MAC OUI prefixes (`52:54:00`, `bc:24:11`, `00:16:3e`).
- **IoT VLAN (`192.168.43.0/24`, `.100 – .250`):** Separate `/24` subnet for IoT devices matched by MAC OUI.

## Verifying on the Target VM

```sh
sudo named-checkconf
sudo kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
sudo kea-dhcp-ddns -t /etc/kea/kea-dhcp-ddns.conf
sudo systemctl status bind9 kea-dhcp4-server kea-dhcp-ddns-server
```
