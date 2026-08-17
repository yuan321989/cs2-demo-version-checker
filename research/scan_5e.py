import os
import glob
from demoparser2 import DemoParser

DIR = r"D:\5EDemocache"
STEAM_VERSIONS = {
    "1.40.8.8": 14088, "1.41.2.9": 14129, "1.41.4.1": 14141,
    "1.41.6.7": 14167, "1.41.6.8": 14168, "1.41.6.9": 14169,
    "1.41.7.2": 14172, "1.41.7.3": 14173, "1.41.7.4": 14174,
}

def rec(patch):
    c = [(v, p) for v, p in STEAM_VERSIONS.items() if p >= patch]
    return min(c, key=lambda x: x[1])[0] if c else "?"

print(f"{'文件':<58} {'patch':<7} {'推荐版本':<10} {'地图':<20} 服务器")
print("-" * 115)
for f in sorted(glob.glob(os.path.join(DIR, "*.dem"))):
    name = os.path.basename(f)
    try:
        h = DemoParser(f).parse_header()
        patch = h.get("patch_version", "?")
        ver = rec(int(patch)) if patch.isdigit() else "?"
        print(f"{name:<58} {patch:<7} {ver:<10} {str(h.get('map_name','?')):<20} {h.get('server_name','?')}")
    except Exception as e:
        print(f"{name:<58} ERR: {str(e)[:50]}")
