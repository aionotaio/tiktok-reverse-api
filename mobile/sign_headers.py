import time

from .XArgus import XArgus
from .XLadon import XLadon
from .XGorgon import XGorgon


def sign_headers(query_string: str, headers: dict = {}, sec_device_id: str = "", aid: int = 1340, license_id: int = 1611921764, sdk_version_str: str = "v04.04.05-ov-android", sdk_version: int = 134744640, platform: int = 0, timestamp: int = int(time.time())) -> dict[str, str]:
    x_ss_stub = None
    if "x-ss-stub" in headers:
        x_ss_stub = headers["x-ss-stub"]
    return {**headers,
            **XGorgon().calculate(query_string, headers),
            **{
                "x-ladon": XLadon.calculate(timestamp, license_id, aid),
                "x-argus": XArgus.calculate(query_string, x_ss_stub, timestamp, platform=platform, aid=aid, license_id=license_id, sec_device_id=sec_device_id, sdk_version=sdk_version_str, sdk_version_int=sdk_version),
            }
            }
