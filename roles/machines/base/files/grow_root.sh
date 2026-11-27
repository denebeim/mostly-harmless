#!/bin/bash
set -euo pipefail
export LC_ALL=C

exec 9>/run/deepthot-grow-root.lock
flock -x 9

read -r root_device filesystem < <(findmnt --noheadings --evaluate --output SOURCE,FSTYPE --target /)
if [[ $filesystem != ext4 ]]; then
    printf 'Expected an ext4 root filesystem, got %s\n' "$filesystem" >&2
    exit 1
fi

read -r device_type parent partition < <(lsblk --nodeps --noheadings --raw --output TYPE,PKNAME,PARTN "$root_device")
if [[ $device_type != part || -z $parent || ! $partition =~ ^[1-9][0-9]*$ ]]; then
    printf 'Expected an ext4 root on a direct disk partition, got %s\n' "$root_device" >&2
    exit 1
fi

disk="/dev/$parent"
expected_bytes=$(numfmt --from=iec "$1")
disk_bytes=$(blockdev --getsize64 "$disk")
if (( disk_bytes < expected_bytes )); then
    printf 'Guest sees %s bytes on %s, expected at least %s\n' "$disk_bytes" "$disk" "$expected_bytes" >&2
    exit 1
fi

partition_changed=false
if output=$(growpart "$disk" "$partition" 2>&1); then
    partition_changed=true
else
    status=$?
    if [[ $status != 1 || $output != NOCHANGE:* ]]; then
        printf '%s\n' "$output" >&2
        exit "$status"
    fi
fi
printf '%s\n' "$output"

# Retry filesystem growth even if an earlier run already grew the partition.
output=$(resize2fs "$root_device" 2>&1) || { printf '%s\n' "$output" >&2; exit 1; }
printf '%s\n' "$output"
if [[ $partition_changed == true || $output != *'Nothing to do!'* ]]; then
    printf 'ROOT_RESIZED\n'
fi
