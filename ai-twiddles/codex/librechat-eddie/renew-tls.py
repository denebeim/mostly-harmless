#!/usr/bin/env python3
"""Issue or renew Eddie's certificate without moving either host's secrets."""

import argparse
import shlex
import subprocess

SSH = ["ssh", "-F", "/dev/null", "-o", "BatchMode=yes", "-o",
       "StrictHostKeyChecking=yes", "-o", "ConnectTimeout=6"]
EDDIE = "ansible@192.168.42.132"
DMZ = "ansible@192.168.42.15"

PREPARE = """
set -eu
umask 077
install -d -m 0700 /etc/librechat-eddie/tls
cd /etc/librechat-eddie/tls
if [ -s key.pem ] && openssl x509 -in fullchain.pem -checkend 2592000 -noout >/dev/null 2>&1; then
    exit 10
fi
if [ ! -s key.pem ]; then
    openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out key.pem
fi
openssl req -new -key key.pem -subj /CN=eddie.local.deepthot.org \\
    -addext subjectAltName=DNS:eddie.local.deepthot.org
"""

ISSUE = '''set -eu
umask 077
base=$HOME/deployments/eddie-cert
mkdir -p "$base/account"
cd "$base"
attempt=$(mktemp -d "$base/issue.XXXXXXXX")
cat > "$attempt/eddie.csr"
cred=$(mktemp "$base/.cloudflare.XXXXXXXX")
trap 'rm -f "$cred" "$attempt/eddie.csr" "$attempt/leaf.pem" "$attempt/chain.pem" "$attempt/fullchain.pem"; rmdir "$attempt"' EXIT
printf 'dns_cloudflare_api_token = %s\n' "$(cat "$HOME/deployments/traefik/cf-token")" > "$cred"
sudo -n docker run --rm --user "$(id -u):$(id -g)" -v "$base:/work" -v "$cred:/cloudflare.ini:ro" certbot/dns-cloudflare:v5.10.0@sha256:6d5e1e84f687ce81786c97cbeccb9dda94d86bbb29a81dbb85527bd68008d77d certonly --non-interactive --agree-tos --register-unsafely-without-email --config-dir /work/account --work-dir /work/tmp --logs-dir /work/logs --dns-cloudflare --dns-cloudflare-credentials /cloudflare.ini --dns-cloudflare-propagation-seconds 30 --csr "/work/${attempt##*/}/eddie.csr" --cert-path "/work/${attempt##*/}/leaf.pem" --chain-path "/work/${attempt##*/}/chain.pem" --fullchain-path "/work/${attempt##*/}/fullchain.pem" >&2
cat "$attempt/fullchain.pem"'''

INSTALL = """
set -eu
cd /etc/librechat-eddie/tls
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT
cat > "$tmp"
openssl verify -verify_hostname eddie.local.deepthot.org -untrusted "$tmp" "$tmp"
test "$(openssl x509 -in "$tmp" -noout -pubkey)" = "$(openssl pkey -in key.pem -pubout)"
install -m 0644 "$tmp" fullchain.pem.next
mv fullchain.pem.next fullchain.pem
if [ "$(docker inspect -f '{{.State.Running}}' librechat-eddie-https-1 2>/dev/null)" = true ]; then
    docker exec librechat-eddie-https-1 nginx -s reload
fi
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eddie-known-hosts", help="Verified host-key file for this Eddie VM")
    args = parser.parse_args()
    eddie_ssh = SSH.copy()
    if args.eddie_known_hosts:
        eddie_ssh.extend(["-o", f"UserKnownHostsFile={args.eddie_known_hosts}"])

    request = subprocess.run(
        eddie_ssh + [EDDIE, "sudo -n bash -c " + shlex.quote(PREPARE)],
        stdout=subprocess.PIPE, timeout=30)
    if request.returncode == 10:
        print("Eddie's certificate has more than 30 days left.")
        return
    request.check_returncode()
    result = subprocess.run(
        SSH + [DMZ, "bash -c " + shlex.quote(ISSUE)],
        input=request.stdout, stdout=subprocess.PIPE, timeout=180, check=True)
    subprocess.run(
        eddie_ssh + [EDDIE, "sudo -n bash -c " + shlex.quote(INSTALL)],
        input=result.stdout, timeout=30, check=True)
    print("Installed Eddie's verified certificate chain.")


if __name__ == "__main__":
    main()
