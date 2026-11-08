"""Offline regression tests: no Proxmox, IPA, SSH or guest operations."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import unittest

import yaml
from jinja2 import Environment

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'guarded_destroy', ROOT / 'roles/proxmox/guarded_destroy/files/guarded_destroy.py')
GUARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GUARD)


class Proxmox:
    def __init__(self):
        self.conf = {'name': 'fixture', 'digest': 'a' * 40, 'scsi0': 'storage:314/root'}
        self.calls = []
        self.fail_shutdown = False
        self.fail_destroy = False
        self.bypass_lock_during_shutdown = False
        self.competing_write_blocked = False

    def run(self, args, **kwargs):
        self.calls.append(args)
        if args[:2] == ['pvesh', 'get']:
            if self.conf is None:
                raise subprocess.CalledProcessError(1, args)
            return subprocess.CompletedProcess(args, 0, json.dumps(self.conf), '')
        if args[:2] == ['qm', 'set']:
            if args[args.index('--digest') + 1] != self.conf['digest']:
                raise subprocess.CalledProcessError(1, args)
            if '--lock' in args:
                if self.conf.get('lock'):
                    raise subprocess.CalledProcessError(1, args)
                self.conf.update(lock='create', digest='b' * 40)
            else:
                self.conf.pop('lock')
                self.conf['digest'] = 'c' * 40
        elif args[:2] == ['qm', 'shutdown']:
            # A normal API writer sees the durable lock and cannot modify config.
            self.competing_write_blocked = self.conf.get('lock') == 'create'
            if self.bypass_lock_during_shutdown:
                self.conf.update(name='changed-by-root', digest='d' * 40)
            if self.fail_shutdown:
                raise subprocess.CalledProcessError(1, args)
        elif args[:2] == ['qm', 'destroy']:
            assert self.conf.get('lock') == 'create'
            assert '--skiplock' in args
            if self.fail_destroy:
                raise subprocess.CalledProcessError(1, args)
            self.conf = None
        else:
            raise AssertionError(args)
        return subprocess.CompletedProcess(args, 0, '', '')


class DeletionGuardTests(unittest.TestCase):
    def test_changed_guest_cannot_acquire_lock_or_reach_shutdown(self):
        p = Proxmox()
        reviewed = copy.deepcopy(p.conf)
        p.conf['digest'] = 'e' * 40
        with self.assertRaises(subprocess.CalledProcessError):
            GUARD.destroy(314, 'node', reviewed, p.run)
        self.assertEqual(len(p.calls), 1)

    def test_preexisting_lock_is_never_bypassed(self):
        p = Proxmox()
        reviewed = copy.deepcopy(p.conf)
        p.conf['lock'] = 'backup'
        with self.assertRaises(subprocess.CalledProcessError):
            GUARD.destroy(314, 'node', reviewed, p.run)
        self.assertEqual(p.conf['lock'], 'backup')
        self.assertEqual(len(p.calls), 1)

    def test_lock_remains_through_shutdown_and_delete(self):
        p = Proxmox()
        GUARD.destroy(314, 'node', copy.deepcopy(p.conf), p.run)
        self.assertTrue(p.competing_write_blocked)
        self.assertIsNone(p.conf)
        self.assertNotIn('--skiplock', p.calls[0])

    def test_shutdown_failure_unlocks_only_owned_digest(self):
        p = Proxmox()
        p.fail_shutdown = True
        with self.assertRaises(subprocess.CalledProcessError):
            GUARD.destroy(314, 'node', copy.deepcopy(p.conf), p.run)
        self.assertNotIn('lock', p.conf)
        self.assertFalse(any(c[:2] == ['qm', 'destroy'] for c in p.calls))
        self.assertEqual(p.calls[-1][-2:], ['--digest', 'b' * 40])

    def test_destroy_failure_cleans_up_owned_lock(self):
        p = Proxmox()
        p.fail_destroy = True
        with self.assertRaises(subprocess.CalledProcessError):
            GUARD.destroy(314, 'node', copy.deepcopy(p.conf), p.run)
        self.assertNotIn('lock', p.conf)

    def test_admin_override_aborts_without_clearing_changed_lock(self):
        p = Proxmox()
        p.bypass_lock_during_shutdown = True
        with self.assertRaises(GUARD.GuardError):
            GUARD.destroy(314, 'node', copy.deepcopy(p.conf), p.run)
        self.assertEqual(p.conf['name'], 'changed-by-root')
        self.assertEqual(p.conf['lock'], 'create')
        self.assertFalse(any(c[:2] == ['qm', 'destroy'] for c in p.calls))
        self.assertFalse(any('--delete' in c for c in p.calls))


class PlaybookGuardTests(unittest.TestCase):
    def test_both_destructive_entrypoints_check_efi_and_tpm(self):
        for name in ('roles/proxmox/rebuild_vm/tasks/preflight.yml',):
            text = (ROOT / name).read_text()
            patterns = re.findall(r"select\('match', '([^']+)'\)", text)
            disk_pattern = next(p for p in patterns if 'scsi' in p)
            for key in ('scsi0', 'ide2', 'efidisk0', 'tpmstate0'):
                self.assertRegex(key, disk_pattern)


    def test_retry_checks_both_streams_and_stops_on_other_failures(self):
        tasks = yaml.safe_load((ROOT / 'roles/hermes/tasks/verify.yml').read_text())
        task = next(t for t in tasks if 'until' in t)
        check = Environment().compile_expression(task['until'])
        error = 'Gateway did not answer session.create'
        for stdout, stderr in ((error, ''), ('', error), ('Gateway did not answer', 'session.create')):
            self.assertFalse(check(eddie_local_reply={'rc': 1, 'stdout': stdout, 'stderr': stderr}))
        self.assertTrue(check(eddie_local_reply={'rc': 1, 'stdout': '', 'stderr': 'other failure'}))
        self.assertTrue(check(eddie_local_reply={'rc': 0, 'stdout': 'Eddie is online.', 'stderr': ''}))


if __name__ == '__main__':
    unittest.main()
