#!/usr/bin/python3
"""Copy quiesced native user state, preserving originals for rollback."""
import shutil,sys
from pathlib import Path
source,dest=map(Path,sys.argv[1:])
exclude={'hermes-agent','installs','runtime','terminal-sessions','logs','cache','image_cache','audio_cache','telemetry','gateway_state.json','gateway-starts.log','config.yaml','profiles'}
for item in source.iterdir():
    if item.name in exclude or item.is_symlink() or item.name.endswith(('.lock','.sock','.pid','-wal','-shm')):continue
    target=dest/item.name
    if item.is_dir():shutil.copytree(item,target,dirs_exist_ok=True,symlinks=True)
    elif item.is_file():shutil.copy2(item,target)
print('Native user state copied; source retained.')
