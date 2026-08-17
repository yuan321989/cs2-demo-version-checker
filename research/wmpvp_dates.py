import os
import glob
from demoparser2 import DemoParser
import datetime

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

rows = []
for f in sorted(glob.glob(os.path.join(DEMO_DIR, "WMPVP_*.dem"))):
    try:
        h = DemoParser(f).parse_header()
        patch = h.get("patch_version", "?")
        srv = h.get("server_name", "?")
        mt = os.path.getmtime(f)
        mtime = datetime.datetime.fromtimestamp(mt).strftime("%Y-%m-%d %H:%M")
        rows.append((os.path.basename(f), patch, srv, mtime))
    except Exception as e:
        rows.append((os.path.basename(f), "ERR", str(e)[:40], ""))

print(f"{'文件':<45} {'patch':<7} {'修改时间':<17} 服务器")
print("-" * 110)
for f, patch, srv, mt in sorted(rows, key=lambda r: r[1] if str(r[1]).isdigit() else 0):
    print(f"{f:<45} {patch:<7} {mt:<17} {srv}")

print()
dates = [r[3][:10] for r in rows if r[3]]
print(f"共 {len(rows)} 个, 时间范围: {min(dates)} ~ {max(dates)}")
