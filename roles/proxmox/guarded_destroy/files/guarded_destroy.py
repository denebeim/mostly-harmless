#!/usr/bin/python3
"""Delete a reviewed guest while a digest-acquired Proxmox lock blocks writers.

Only this operation bypasses its own logical lock. Normal Proxmox operations
remain blocked from acquisition through deletion. Root's explicit skiplock or
out-of-band file edits are administrative overrides, not cooperating writers.
"""
import argparse
import json
import re
import subprocess
import sys


class GuardError(RuntimeError):
    pass


def destroy(vmid, node, reviewed, run=subprocess.run):
    digest = reviewed.get('digest', '')
    if not re.fullmatch(r'[0-9a-f]{40}', digest) or reviewed.get('lock'):
        raise GuardError('A reviewed digest and an unlocked guest are required')

    def command(*args):
        result = run(list(args), check=True, capture_output=True, text=True)
        return result.stdout

    def config():
        return json.loads(command('pvesh', 'get',
                                  f'/nodes/{node}/qemu/{vmid}/config',
                                  '--output-format', 'json'))

    # Proxmox compares the digest and sets the logical lock under its config
    # mutex. This must NOT use --skiplock: a competing operation wins or fails.
    command('qm', 'set', str(vmid), '--lock', 'create', '--digest', digest)
    locked = None
    try:
        locked = config()
        expected = {k: v for k, v in reviewed.items() if k != 'digest'}
        expected['lock'] = 'create'
        if {k: v for k, v in locked.items() if k != 'digest'} != expected:
            locked = None  # cannot prove ownership; leave the lock for review
            raise GuardError('Configuration changed while acquiring the deletion lock')
        command('qm', 'shutdown', str(vmid), '--skiplock', '1', '--timeout', '180')
        current = config()
        if current.get('digest') != locked['digest'] or current.get('lock') != 'create':
            raise GuardError('Configuration changed despite the deletion lock')
        command('qm', 'destroy', str(vmid), '--skiplock', '1')
    except Exception as original:
        if locked is None:
            raise GuardError('Deletion aborted; acquired lock requires manual review') from original
        try:
            current = config()
            if current.get('digest') != locked['digest'] or current.get('lock') != 'create':
                raise GuardError('Lock ownership changed')
            # Digest-checked cleanup cannot clear another operation's lock.
            command('qm', 'set', str(vmid), '--delete', 'lock', '--skiplock', '1',
                    '--digest', locked['digest'])
        except Exception:
            raise GuardError('Deletion aborted; changed/missing configuration left for manual review') from original
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vmid', type=int, required=True)
    parser.add_argument('--node', required=True)
    args = parser.parse_args()
    if args.vmid <= 0 or not re.fullmatch(r'[A-Za-z0-9_-]+', args.node):
        parser.error('Invalid VM ID or node')
    destroy(args.vmid, args.node, json.load(sys.stdin))
    print(f'Destroyed reviewed VM {args.vmid}')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        # stdin includes the private VM config; never echo it or subprocess output.
        print('Guarded deletion failed. Inspect the target and any retained Proxmox lock before retrying.', file=sys.stderr)
        sys.exit(1)
