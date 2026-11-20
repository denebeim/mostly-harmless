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
offers no transport encryption. Deepthot sign-in and TLS are future work.

From the project directory on Eddie, use
`docker compose --project-name librechat-eddie stop` to stop the two services.
The volumes persist. To bring them back, rerun the playbook. For an image
rollback, restore the prior image references and rerun, restoring the compatible
database backup if the newer release applied incompatible migrations.
