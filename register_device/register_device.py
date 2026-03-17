import os
import re
import sys
import time
import json
import random
import binascii
import platform
import subprocess
import urllib.request
from pathlib import Path


if getattr(sys, "frozen", False):
    root_dir = Path(sys.executable).parent.absolute()
else:
    root_dir = Path(__file__).parent.absolute()


def getsystem() -> str:
    system = platform.system()
    if system.startswith("Win"):
        return "win"+platform.machine()[-2:]
    elif system.startswith("Lin"):
        return "linux" + platform.machine()[-2:]
    else:
        return "osx64"
    

JAVA_DIR: str = os.path.join(root_dir, 'java')
JNI_PATH: str = os.path.join(os.path.join(JAVA_DIR, "prebuilt"), getsystem())


def get_random_mc() -> str:
    mcrandom = ["a","1","2","3","4","5","6","7","8","9"]
    mc = '{}:{}:{}:{}:{}:{}'.format("".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)),"".join(random.choices(mcrandom,k=2)))
    return mc


def get_payload(java_path: str, jni_path: str, message: str):
    os.chdir(java_path)

    command = r"java -jar -Djna.library.path={} -Djava.library.path={} unidbg.jar {}".format(jni_path, jni_path, message)
    stdout, _ = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).communicate()

    res = re.search(r'hex=([\s\S]*?)\nsize', stdout.decode())
    if not res:
        return
    
    hex_str = res.group(1)
    hexadecimal = hex_str.encode('utf-8')
    return binascii.unhexlify(hexadecimal)


def register_device(java_dir: str, jni_path: str, gentime: str = str(int(time.time() * 1000)), udid: str = str(random.randint(221480502743165, 821480502743165)), openudid: str = str(binascii.hexlify(os.urandom(8)).decode())) -> tuple[str, str] | None:
    mc = get_random_mc()
    message = " ".join([gentime, udid, openudid, mc])
    res = get_payload(java_dir, jni_path, message)
    headers = {
        'user-agent': 'com.zhiliaoapp.musically.go/420903 (Linux; U; Android 7.1.2; ru_RU; SM-A805N; Build/PPR1.180610.011;tt-ok/3.12.13.45.lite-ul)',
        'content-type': 'application/octet-stream;tt-data=a',
    }
    try:
        request = urllib.request.Request(url='https://log-boot.tiktokv.com/service/2/device_register/', data=res, headers=headers)
        response = urllib.request.urlopen(request)
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return
    else:
        if response.getcode() != 200:
            print(f"Bad status code: {response.status_code}")
            print(f"Full response: {response.text}")
            return
        
        response_text = response.read().decode("utf-8", errors="ignore")

        try:
            response_data = json.loads(response_text)
        except Exception as e:
            print(f"Failed to unmarshal JSON: {str(e)}")
            print(f"Full response: {response.text}")
            return
                        
        if not response_data:
            print(f"No response from server: {response.text}")
            return
        
        if not isinstance(response_data, dict):
            print(f"Bad type of response: {type(response_data)}")
            return 
        
        server_time: int | None = response_data.get("server_time")
        if not server_time:
            print(f"Failed to find [server_time] in [response_data]")
            print(f"Full response: {response_data}")
            return
        
        device_id: str | None = response_data.get("device_id_str")
        if not device_id:
            print(f"Failed to find [device_id] in [response_data]")
            print(f"Full response: {response_data}")
            return
        
        install_id: str | None = response_data.get("install_id_str")
        if not install_id:
            print(f"Failed to find [install_id] in [response_data]")
            print(f"Full response: {response_data}")
            return
        
        print(f'Successfully registered device | device_id={device_id} | install_id={install_id}')
        return device_id, install_id
    
if __name__ == "__main__":
    register_device(JAVA_DIR, JNI_PATH)