import os
import sys
import subprocess
from pathlib import Path


if getattr(sys, "frozen", False):
    root_dir = Path(sys.executable).parent.absolute()
else:
    root_dir = Path(__file__).parent.absolute()
    

ENCODER_PATH: str = os.path.join(root_dir, 'encoder.js')


def get_x_gnarly(js_path: str, query_string: str, body: str, user_agent: str) -> str | None:    
    proc = subprocess.Popen(['node', js_path, query_string, body, user_agent], stdout=subprocess.PIPE)
    stdout = proc.stdout
    if not stdout:
        return
        
    x_gnarly = stdout.read().decode('utf-8')
            
    return x_gnarly