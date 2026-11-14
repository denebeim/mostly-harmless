#!/usr/bin/env python3
"""Append sanitized, live command output to the shared private session log."""
import datetime
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
from zoneinfo import ZoneInfo

SECRET_NAMES = re.compile(r"password|passwd|token|secret|private.?key|api.?key", re.I)
ASSIGNMENT = re.compile(
    r'''(?ix)(["']?(?:password|passwd|api[_-]?key|(?:access[_-]?|refresh[_-]?)?token|(?:client[_-]?)?secret|authorization)["']?\s*[:=]\s*)(?:"[^"\n]*"|'[^'\n]*'|[^\s,}]+)'''
)


class Redactor:
    def __init__(self):
        self.values = sorted(
            {v for k, v in os.environ.items() if SECRET_NAMES.search(k) and v},
            key=len, reverse=True,
        )
        self.pem = False

    def clean(self, line):
        if self.pem:
            if '-----END ' in line:
                self.pem = False
            return ''
        if '-----BEGIN ' in line and any(
            name in line for name in ('PRIVATE KEY', 'CERTIFICATE')
        ):
            self.pem = '-----END ' not in line
            return '[REDACTED PEM MATERIAL]\n'
        for value in self.values:
            line = line.replace(value, '[REDACTED]')
        line = re.sub(r'(?i)(bearer\s+)\S+', r'\1[REDACTED]', line)
        return ASSIGNMENT.sub(r'\1[REDACTED]', line)


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 ai-twiddles/log-session.py COMMAND [ARG ...]', file=sys.stderr)
        return 2
    log = os.environ.get('DEEPTHOT_SESSION_LOG', str(
        Path(__file__).resolve().parents[1] / 'chat.log'))
    # Open before launching: a logging failure must never run an unlogged command.
    fd = os.open(log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.fchmod(fd, 0o600)
    redactor = Redactor()
    run = uuid.uuid4().hex[:12]
    with os.fdopen(fd, 'a', encoding='utf-8') as out:
        def emit(text):
            text = redactor.clean(text)
            out.write(text)
            out.flush()
            sys.stdout.write(text)
            sys.stdout.flush()

        def marker(text):
            # Metadata must survive even when a child ends inside a PEM block.
            out.write(text)
            out.flush()
            sys.stdout.write(text)
            sys.stdout.flush()

        marker('\nBEGIN ' + datetime.datetime.now(ZoneInfo('America/Phoenix')).isoformat()
               + ' run=' + run + '\n')
        # Do not log argv or cwd: either may contain credentials. Output is sanitized.
        try:
            child = subprocess.Popen(sys.argv[1:], stdin=None, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True,
                                     encoding='utf-8', errors='replace', bufsize=1)
        except OSError as exc:
            emit('Unable to start command: ' + str(exc) + '\n')
            status = 127 if isinstance(exc, FileNotFoundError) else 126
        else:
            try:
                for line in child.stdout:
                    emit(line)
            except KeyboardInterrupt:
                child.send_signal(2)
            finally:
                child.stdout.close()
            status = child.wait()
            if status < 0:
                status = 128 - status
        marker('\nEND run=' + run + ' exit=' + str(status) + '\n')
        return status


if __name__ == '__main__':
    sys.exit(main())
