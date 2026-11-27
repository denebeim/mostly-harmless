# LibreChat on Eddie

[eddie.yaml](../../eddie.yaml) provisions Eddie and reconciles LibreChat after
Ollama and Hermes. [librechat.yaml](../../librechat.yaml) reconciles LibreChat
on the existing VM using the same Proxmox inventory. Both paths use the
deployment user's Docker access and project under
`~/.local/share/librechat-eddie`. Keep that account consistent across runs.
For an existing installation, set `librechat_deploy_user` to the account
that owns the project before applying either playbook. The production Eddie
installation uses the owner’s IPA account and network home.

## Enable and disable

Add `librechat` to the VM's Proxmox tags to enable the application. Add this
tag to the existing Eddie before its first apply with this version.
Fresh Eddie builds start with the tag by default. Override
`eddie_initial_optional_tags` with an empty list for a fresh Eddie without
LibreChat. On existing VMs the playbook preserves the live LibreChat tag
while maintaining Eddie's core Ollama and Hermes features.

Remove the tag in Proxmox and rerun to remove the LibreChat containers,
networks and rendered configuration. The Docker volumes, instance
encryption secrets, certificate files and externally configured Authentik
provider are retained for re-enabling the service. The role never removes
Ollama or Hermes. On first deployment, check convergence with a second run.
For a disposable VM, exercise tag removal, a second absent run, and
re-enabling with existing data. A replacement VM can use `eddie_vm_id` with
an unused ID and `eddie_host` / `eddie_ip` with an unused name and address.
Give the test VM its own GPU setting with `eddie_gpu_pci` if the production GPU is in use.

From any directory inside the checkout, discover the repository path and
run with the controller's private settings. For AWX use the same playbook
with Proxmox inventory, credentials and extra variables attached to the job.

```sh
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT"
python3 scripts/log-session.py .venv/bin/ansible-playbook librechat.yaml \
  --extra-vars "@$LIBRECHAT_SITE_VARS" \
  --extra-vars "@$LIBRECHAT_VAULT_VARS"
```

For site settings, use ordinary Ansible variables. The following example
assumes the Authentik target is resolvable through Ansible inventory, and
Eddie has its certificate and key available before the run.

```yaml
librechat_deploy_user: ansible
librechat_oidc_enabled: true
librechat_url: https://eddie.example.net
librechat_oidc_discovery_url: https://auth.example.net/application/o/eddie/.well-known/openid-configuration
librechat_authentik_host: authentik
librechat_authentik_container: authentik_server_1
librechat_authentik_group: Household
librechat_authentik_extra_user: guest
librechat_oidc_client_id: eddie
librechat_oidc_allow_registration: true
```

Vault `librechat_oidc_client_secret` and `librechat_oidc_session_secret`.
Supply a distinct persistent session secret of at least 32 characters.
If an existing vault already defines site values, migrate those values to
the site settings file when convenient. The callback is the configured
`librechat_url` followed by `/oauth/openid/callback`.

Set `librechat_authentik_host` to have the tagged deployment converge the
provider and bindings. Omit it when Authentik is managed independently.
[librechat-authentik.yaml](../../librechat-authentik.yaml) can configure
the provider independently. Restrict provider access before enabling
first-sign-in registration. Local admin sign-in remains available and
ordinary self-registration stays disabled. Keep a dedicated local recovery account
and test its HTTPS login in a fresh browser session. Authentik owns normal user
access. Removing someone from the Authentik policy does not revoke a separate
local password or necessarily end an existing LibreChat session.

On a fresh database, enable `librechat_oidc_allow_registration` after
restricting access in Authentik so authorized users can create their
LibreChat accounts on first sign-in. For a local recovery account or local
pilot, use [LibreChat’s user creation script](https://www.librechat.ai/docs/configuration/authentication)
from the deployed Compose directory:

```sh
./docker-cli compose --project-name librechat-eddie exec -w /app api npm run create-user
```

On a fresh single-tenant database, create the local recovery account first if
it should receive the initial admin role. For an existing database, verify
the recovery account's role and access separately.

## HTTPS

Supply a matching certificate and key on Eddie under
`librechat_tls_dir` (default `/etc/librechat-eddie/tls`). Set
`librechat_tls_certificate` and `librechat_tls_key` if the filenames
differ from `fullchain.pem` and `key.pem`. A site-provided wildcard
certificate and key can be mounted read-only from an existing local or
shared directory readable by Docker. The certificate checksum triggers
proxy recreation after renewal when the playbook runs.

The existing host-specific certificate can continue to be used at the
default location. To use the original DMZ DNS-challenge workflow, set
`librechat_acme_ssh_target` to the SSH destination of that service and
use the default TLS path and filenames. The helper keeps the key on Eddie,
uses strict SSH host verification and moves only the certificate request
and the public chain. It expects the Cloudflare token on the DNS challenge
host in its existing Traefik configuration. This provisioning mode runs
only when its SSH destination is configured.

Nginx listens on port 443 on Eddie's LAN address with TLS 1.2 and 1.3.
It reaches LibreChat by service name on the Compose network. MongoDB
uses the internal database network with LibreChat. For a trusted-LAN pilot, explicitly set
`librechat_allow_plain_http: true` with OIDC disabled. LibreChat then listens
on port 80 on the configured LAN address and its passwords and session
traffic travel unencrypted. Use HTTPS for the normal Eddie deployment.

## Local inference and acceptance

LibreChat's [custom endpoint](https://www.librechat.ai/docs/quick_start/custom_endpoints)
uses the host Ollama API. New chats default to Eddie's [persona](files/SOUL.md).
Plain Ollama uses the same model without the persona. See LibreChat's
[model spec reference](https://www.librechat.ai/docs/configuration/librechat_yaml/object_structure/model_specs)
and [configuration overview](https://www.librechat.ai/docs/configuration)
for the mounted configuration and restart behavior.

The role checks the configured model from the application container and
the web page from the controller. For acceptance, verify a permitted user
can sign in and get an Ollama reply, a user outside the Authentik policy is
denied, and local admin sign-in still works. Preserve MongoDB and the
instance secrets together for backups.

## Optional Inkling 2 Mini

Run `eddie.yaml` with `-e eddie_enable_inkling=true` to install and verify
Inkling before adding it to LibreChat. The Eddie VM profile allocates 28 GiB
of RAM and a 64 GiB boot disk for this model. The opt-in requires Ollama
0.40.18 or later. The Inkling profile uses the CPU with a 4K context and
has an empty persona prompt. Eddie's Qwen preset remains the default.

Run the same playbook with `-e eddie_enable_inkling=false` to remove Inkling
from LibreChat. The downloaded weights and installed Ollama version are
retained for the next opt-in.
