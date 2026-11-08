#!/usr/bin/python3
"""Run on the controller: exchange its existing Kerberos ticket for a host OTP.

Stdout is a credential: the calling Ansible task MUST use no_log. No ticket or
administrator password is copied to the guest. Called only for a fresh client.
"""
import re
import sys


def main():
    if len(sys.argv) != 2 or not re.fullmatch(
        r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.local\.deepthot\.org", sys.argv[1]
    ):
        raise SystemExit("Expected a LAN host FQDN")
    from ipalib import api, errors

    hostname = sys.argv[1]
    api.bootstrap(context="cli")
    api.finalize()
    api.Backend.rpcclient.connect()
    try:
        try:
            host = api.Command.host_show(hostname)["result"]
        except errors.NotFound:
            result = api.Command.host_add(hostname, random=True, force=True)
        else:
            # The newly built guest has no IPA configuration. Retire a stale
            # enrollment key on its existing host entry without deleting it.
            if host.get("has_keytab"):
                api.Command.host_disable(hostname)
            result = api.Command.host_mod(hostname, random=True)
        otp = result.get("result", {}).get("randompassword")
        if not otp:
            raise RuntimeError("IPA did not return a host enrollment password")
        print(otp)
    finally:
        api.Backend.rpcclient.disconnect()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Avoid accidentally including RPC credential values in diagnostics.
        print("IPA host enrollment preparation failed; verify kinit admin and controller IPA connectivity.", file=sys.stderr)
        sys.exit(1)
