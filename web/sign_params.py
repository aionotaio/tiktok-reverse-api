import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Any


if getattr(sys, "frozen", False):
    root_dir = Path(sys.executable).parent.absolute()
else:
    root_dir = Path(__file__).parent.absolute()
    

BROWSER_DIR: str = os.path.join(root_dir, 'js')
BROWSER_PATH: str = os.path.join(BROWSER_DIR, 'browser.js')


def parse_signatures(signatures: Any) -> dict[str, Any] | None:
    try:
        tt_output = json.loads(signatures)["data"]
    except (json.JSONDecodeError, KeyError) as e:
        return
        
    return tt_output

def get_signatures(js_path: str, url: str, user_agent: str) -> dict[str, Any] | None:                
    proc = subprocess.Popen(['node', js_path, url, user_agent], stdout=subprocess.PIPE)
    stdout = proc.stdout
    if not stdout:
        return
        
    return parse_signatures(stdout.read().decode('utf-8'))
        

def get_sign_params(js_path: str, url: str, user_agent: str) -> dict[str, Any] | None:    
    signatures = get_signatures(js_path, url, user_agent)
    if not signatures:
        return
    
    return {
        "browser_language": signatures.get("navigator", {}).get("browser_language"),
        "browser_name": signatures.get("navigator", {}).get("browser_name"),
        "browser_platform": signatures.get("navigator", {}).get("browser_platform"),
        "browser_version": signatures.get("navigator", {}).get("browser_version"),
        "verifyFp": signatures.get("verify_fp"),
        "X-Bogus": signatures.get("x-bogus")
    }