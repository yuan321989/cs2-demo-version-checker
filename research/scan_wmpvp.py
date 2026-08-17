import os
import glob
import zipfile
import tempfile
from demoparser2 import DemoParser

DEMO_DIR = r"C:\Users\mr.bread\AppData\Roaming\Wmpvp\demo"
STEAM_VERSIONS = {
    "1.40.8.8": 14088, "1.41.2.9": 14129, "1.41.4.1": 14141,
    "1.41.6.7": 14167, "1.41.6.8": 14168, "1.41.6.9": 14169,
    "1.41.7.2": 14172, "1.41.7.3": 14173, "1.41.7.4": 14174,
}

def recommend_version(patch: int) -> str:
    candidates = [(v, p) for v, p in STEAM_VERSIONS.items() if p >= patch]
    if not candidates:
        return "?"
    return min(candidates, key=lambda x: x[1])[0]

print(f"{'zip文件':<26} {'patch':<7} {'推荐版本':<10} {'地图':<20} 服务器")
print("-" * 100)

with tempfile.TemporaryDirectory() as tmp:
    for zf in sorted(glob.glob(os.path.join(DEMO_DIR, "*.zip"))):
        name = os.path.basename(zf)
        try:
            with zipfile.ZipFile(zf) as z:
                inner = z.namelist()[0]
                z.extract(inner, tmp)
                dem_path = os.path.join(tmp, inner)
                h = DemoParser(dem_path).parse_header()
                patch = h.get("patch_version", "?")
                if patch.isdigit():
                    ver = recommend_version(int(patch))
                else:
                    ver = "?"
                print(f"{name:<26} {patch:<7} {ver:<10} {str(h.get('map_name','?')):<20} {h.get('server_name','?')}")
        except Exception as e:
            print(f"{name:<26} ERROR: {str(e)[:60]}")
        finally:
            for f in os.listdir(tmp):
                try:
                    os.remove(os.path.join(tmp, f))
                except:
                    pass
