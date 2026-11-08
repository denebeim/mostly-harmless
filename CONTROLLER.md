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

`patches/eddie-entrypoint.patch` records the playbook naming, explicit firmware
selection, verified host-key refresh, and authenticated-connection wait. It was
checked against the preserved historical `hermes.yaml`; after applying it to an
unmodified import, rename that file to `eddie.yaml`.

The `proxmox/ssh_host_key` role verifies VM and guest identity over the trusted
hypervisor connection, reads public host keys through the guest agent, backs up
the workstation's trust file privately, and refreshes only the verified guest's
entries. It leaves SSH verification enabled. An accessible guest agent and static
IPv4 cloud-init configuration are required. It does not change system-wide SSH
trust stores or IPA-managed SSH configuration.

The local `rebuild_eddie.yaml` is a one-time destructive entry point. Ordinary
reruns use `eddie.yaml`. Do not rerun the rebuild entry point to troubleshoot a
partially configured replacement; its expected-old-name guard deliberately
refuses that replacement.

Before running `eddie.yaml`, review its provisioning and guest-configuration
effects with the owner. It can resize disks, reconfigure a VM, upgrade guest
packages, enroll identity, and change Docker and agent services. A successful
inventory or syntax check does not authorize those changes.

## Eddie provisioning checkpoint (2026-11-07)

The reviewed Eddie entrypoints and their supporting local roles are now tracked;
other imported operational configuration remains ignored. The historical patches
above describe earlier imports, not the latest tracked entrypoints.

- `create_eddie.yaml`: create/boot the base VM without guest roles or cloud-init
  package upgrades. It does not destroy an existing VM.
- `eddie.yaml`: provision Eddie, update Ubuntu packages, reboot when required,
  configure IPA/NFS homes and Docker, then install Hermes, the K5200 driver,
  Ollama and Qwen, followed by functional acceptance checks.
- `destroy_hermes.yaml`: separate destructive operation guarded for the old
  Hermes identity; it deliberately refuses the renamed Eddie guest.

The fresh-guest bootstrap currently requires the host key established during the
base smoke test in `.ansible/eddie-smoke-known-hosts`. That local trust file is not
committed. Bootstrap installs the guest agent, then refreshes normal SSH trust
through the hypervisor. This is a current prerequisite, not a completed general
solution for arbitrary new controllers or replacement guests.

From the project root, load the private `.envrc` and activate `.venv`. Obtain an
IPA-authorized Kerberos ticket (`kinit admin` when needed), then run:

```bash
set -o pipefail
PYTHONUNBUFFERED=1 ansible-playbook eddie.yaml \
  --ssh-common-args='-F /dev/null' 2>&1 | tee -a eddie-session.log
```

The `-F /dev/null` option works around the known controller SSH-config issue.
The ticket check tests validity; it does not prove the principal has enrollment
rights. The local enrollment helper needs system Python's FreeIPA libraries and
controller IPA configuration. It uses the ticket for a one-time host enrollment
credential, handles that credential with `no_log`, and does not copy administrator
passwords, keytabs or tickets onto the guest. This new ticket path still requires
an end-to-end fresh-enrollment test.

See `CHANGELOG.md` for this checkpoint's validation limits. In particular, a
successful targeted Hermes reply is not a clean full acceptance-run recap.

## Destructive-operation guard

Both deletion paths call `proxmox/guarded_destroy`. On the Proxmox node it
atomically acquires a `create` configuration lock against the reviewed digest,
then keeps that logical lock through graceful shutdown and deletion. Only that
operation uses root's `--skiplock` to proceed through its own lock; ordinary
Proxmox configuration writers and competing guard runs remain blocked. The
helper rechecks the locked digest before removal and uses digest-checked cleanup
on failure. An unexpected configuration change leaves the lock for manual review.
Explicit root overrides and out-of-band file edits cannot be prevented by this
cooperative locking protocol. No force-stop or unreferenced-disk purge is used.

Disk review includes EFI and TPM state volumes. They must be explicitly allowed;
`destroy_hermes.yaml` additionally checks the expected EFI volume ownership.
The helper is tested offline with simulated commands; no destructive integration
test has been run against a live guest for this review update.
