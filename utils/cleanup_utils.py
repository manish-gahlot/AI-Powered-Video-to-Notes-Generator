# utils/cleanup_utils.py
import os
import shutil
from pathlib import Path
import time

def purge_old_temp_files(temp_dir: Path, older_than_hours: int = 24):
    now = time.time()
    threshold = older_than_hours * 3600
    for child in temp_dir.iterdir():
        try:
            mtime = child.stat().st_mtime
            if now - mtime > threshold:
                if child.is_dir():
                    shutil.rmtree(child, ignore_errors=True)
                else:
                    child.unlink(missing_ok=True)
        except Exception:
            pass

def safe_remove(path):
    path = Path(path)
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    else:
        path.unlink(missing_ok=True)
