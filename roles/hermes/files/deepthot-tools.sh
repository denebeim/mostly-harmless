# SPDX-License-Identifier: GPL-3.0-only
# Managed by Ansible. VM tools are available to every shell user.
case ":${PATH-}:" in
    *:/usr/local/bin:*) ;;
    *) PATH="/usr/local/bin${PATH:+:$PATH}" ;;
esac
export PATH
