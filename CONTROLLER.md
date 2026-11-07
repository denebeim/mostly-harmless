# Local Ansible controller

Run from this repository root. The historical checkout is preserved separately;
ongoing edits belong here. No old virtual environment was copied.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-controller.lock.txt
.venv/bin/ansible-galaxy role install -r roles/requirements.yml -p roles/galaxy_roles
.venv/bin/ansible-galaxy collection install -r collections/requirements.yml -p collections
source .envrc
```

`requirements.txt` and `modules/requirements.txt` retain the original controller
requirements; the lock file records the resolved clean installation. The original
`modules/requirements.yml` is empty. The imported collection manifest still tracks
`master` for its Git-sourced collection, so that entry is not immutable.

`ansible.cfg` selects `inventory/proxmox.py` directly. Activate `.venv` or source
the ignored `.envrc` before invoking Ansible so the executable inventory script
uses the controller Python. Inventory calls query live API and guest-agent data
and can take several minutes. Raw output may contain sensitive host variables.

The ignored, mode-0600 `.envrc` holds existing connection assignments and prepends
the new environment to PATH. It is deliberately not published. The existing vault
password file remains outside this repository. Never print either file in logs.

The working Ansible playbooks, local roles, operational inventory, and deployments
were imported at the repository root. They remain ignored pending privacy review;
they contain private addresses, topology, and potentially credentials. They are
**not backed up by the public Git remote yet**. A fresh public clone cannot restore
the private operational configuration. Do not force-add these paths wholesale.
Generated environments, installed roles/collections, and controller caches are
also ignored. The public allowlist currently covers only reviewed controller
configuration, manifests, the generic inventory generator, and documentation.

`patches/create-vm-explicit-id-and-firmware.patch` records the small changes to
the ignored historical provisioning role. It adds an explicit ID to cloud-init
network updates and invokes the versioned firmware role only when requested.
The patch was verified against the preserved source and reproduces the local
role changes exactly. Apply it only to an unmodified import of that source:

```bash
git apply --unidiff-zero --check patches/create-vm-explicit-id-and-firmware.patch
git apply --unidiff-zero patches/create-vm-explicit-id-and-firmware.patch
```

The local `rebuild_eddie.yaml` is a one-time destructive entry point. Ordinary
reruns use `eddie.yaml`. Do not rerun the rebuild entry point to troubleshoot a
partially configured replacement; its expected-old-name guard deliberately
refuses that replacement.

Before running `eddie.yaml`, review its provisioning and guest-configuration
effects with the owner. It can resize disks, reconfigure a VM, upgrade guest
packages, enroll identity, and change Docker and agent services. A successful
inventory or syntax check does not authorize those changes.
