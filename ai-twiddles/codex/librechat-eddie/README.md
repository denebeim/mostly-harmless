# LibreChat on Eddie

This experiment deploys LibreChat at http://eddie using an isolated Docker Compose
project. Eddie's existing Ollama serves qwen3.5:4b through its local
OpenAI-compatible API. LibreChat offers only this endpoint, with no cloud API
keys configured. MongoDB runs on a dedicated internal Docker network. Database
and application files persist in Docker volumes. Search and document retrieval
services are outside this deployment.

## Install and update

From the repository root, use the controller's existing Ansible environment and
the community.docker version pinned in collections/requirements.yml:

```sh
python3 /home/denebeim/projects/mostly-harmless/scripts/log-session.py \
  /home/denebeim/projects/mostly-harmless/.venv/bin/ansible-playbook \
  -i ai-twiddles/codex/librechat-eddie/inventory.ini \
  ai-twiddles/codex/librechat-eddie/playbook.yaml \
  --ssh-common-args='-F /dev/null -o BatchMode=yes -o StrictHostKeyChecking=yes'
```

Use the existing SSH account with Docker access and keep it consistent across
runs. The project lives in that account's ~/.local/share/librechat-eddie.
This design uses existing Docker access without requiring general sudo or
running Eddie's VM provisioning. Update the image references in the playbook
to adopt a reviewed release, then rerun. Back up MongoDB and instance secrets
before a version change. The playbook checks the published HTTP page and verifies
the configured model is visible to the app container. A signed-in chat is the
separate end-to-end acceptance check.

## Access and rollback

LibreChat requires an account. This instance allows local passwords and disables
self-registration and social login. Provision the first account with LibreChat's
create-user tool through SSH and supply a unique password via stdin. The first
account is the instance admin. The plain HTTP URL is for the trusted LAN and
offers no transport encryption. Keep local passwords separate from directory
credentials.

## Optional Authentik sign-in

OpenID Connect is disabled by default. To enable it on rebuilt Eddie:

1. Set up a trusted LAN HTTPS URL for LibreChat, such as
   `https://eddie.local.deepthot.org`. An HTTPS reverse proxy on Eddie should
   forward to `http://127.0.0.1:3080`, preserving the host and forwarding
   protocol headers and chat streaming. Enabling this mode moves the Docker
   listener from Eddie's LAN port 80 to localhost port 3080.
2. In Authentik at `https://auth.deepthot.org`, create an Eddie application
   with a confidential OAuth2/OpenID Connect provider. Register the exact
   redirect URI, for example
   `https://eddie.local.deepthot.org/oauth/openid/callback`. Grant the
   application to the household group or explicitly selected users.
3. Pass the following variables in an Ansible Vault-encrypted extra-vars file
   using `--extra-vars @/path/to/eddie-auth.vault.yml --ask-vault-pass`.
   Generate a distinct, persistent random session secret of at least 32
   characters. Copy the discovery URL from the provider page.

   ```yaml
   librechat_oidc_enabled: true
   librechat_url: https://eddie.local.deepthot.org
   librechat_oidc_discovery_url: https://auth.deepthot.org/application/o/eddie/.well-known/openid-configuration
   librechat_oidc_client_id: REPLACE_WITH_CLIENT_ID
   librechat_oidc_client_secret: REPLACE_WITH_CLIENT_SECRET
   librechat_oidc_session_secret: REPLACE_WITH_RANDOM_SESSION_SECRET
   librechat_oidc_allow_registration: true
   ```

   Set `librechat_oidc_allow_registration` only after restricting Eddie in
   Authentik. It permits account creation on first successful Authentik login.
   Regular LibreChat self-registration stays disabled, and local sign-in is
   available for the administrator.
4. In fresh browser sessions, verify a household user can sign in and chat,
   an Authentik user outside the Eddie policy is denied, and the local admin
   can still sign in. Authentik owns the two-factor and FreeIPA policy.

To return to the original local-only pilot, rerun without the OIDC extra-vars
file. The old LAN HTTP listener returns, the managed OIDC environment file is
removed after Compose converges, and the database is retained.

From the project directory on Eddie, use
`docker compose --project-name librechat-eddie stop` to stop the two services.
The volumes persist. To bring them back, rerun the playbook. For an image
rollback, restore the prior image references and rerun, restoring the compatible
database backup if the newer release applied incompatible migrations.
