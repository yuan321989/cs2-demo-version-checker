import os
import re
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

rows = []
for f in sorted(os.listdir(DEMO_DIR)):
    if not f.lower().endswith(".dem"):
        continue
    try:
        h = DemoParser(os.path.join(DEMO_DIR, f)).parse_header()
        patch = h.get("patch_version", "?")
        gdir = h.get("game_directory", "?") or "?"
        m = re.search(r"csgo_v(\d+)", gdir)
        build = m.group(1) if m else "?"
        rows.append((f, patch, build, gdir))
    except Exception as e:
        rows.append((f, "ERR", "?", str(e)[:40]))

print(f"{'demo':<58} {'patch':<7} {'server build':<13}")
print("-" * 90)
for f, patch, build, gdir in sorted(rows, key=lambda r: int(r[2]) if r[2].isdigit() else 0):
    print(f"{f:<58} {patch:<7} {build:<13}")

print()
print("== 构建号范围 ==")
builds = sorted({int(r[2]) for r in rows if r[2].isdigit()})
print(f"从 {builds[0]} 到 {builds[-1]}，共 {len(builds)} 个不同构建号")
print(builds)
