#!/usr/bin/python3
"""Register an enrolled Docker host in the central, command-scoped IPA rule."""
import re
import sys


def register(api, hostname):
    rule_name = "docker-admin-access"
    rule = api.Command.sudorule_show(rule_name)["result"]
    if (not rule.get("ipaenabledflag", (False,))[0]
            or tuple(rule.get("memberuser_group", ())) != ("docker-admins",)
            or tuple(rule.get("memberallowcmd_sudocmd", ())) != ("/usr/bin/docker",)
            or any(rule.get(key) for key in ("usercategory", "hostcategory", "cmdcategory", "memberuser_user", "memberhost_hostgroup"))):
        raise RuntimeError("Unexpected Docker sudo rule scope")
    if not api.Command.host_show(hostname)["result"].get("has_keytab"):
        raise RuntimeError("Host has no enrolled IPA keytab")
    if hostname in rule.get("memberhost_host", ()):
        return False
    result = api.Command.sudorule_add_host(rule_name, host=[hostname])
    if hostname not in result["result"].get("memberhost_host", ()):
        raise RuntimeError("IPA did not add the host to the Docker rule")
    return bool(result.get("completed"))


def main():
    if len(sys.argv) != 2 or not re.fullmatch(
        r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.local\.deepthot\.org", sys.argv[1]
    ):
        raise SystemExit("Expected an enrolled LAN host FQDN")
    from ipalib import api
    api.bootstrap(context="cli")
    api.finalize()
    api.Backend.rpcclient.connect()
    try:
        print("registered" if register(api, sys.argv[1]) else "already registered")
    finally:
        api.Backend.rpcclient.disconnect()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit("Docker IPA registration failed; check kinit admin, host enrollment and docker-admin-access scope.")
