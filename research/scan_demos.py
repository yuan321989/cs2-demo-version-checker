import os
import sys
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

files = sorted(os.listdir(DEMO_DIR))
files = [f for f in files if f.lower().endswith(".dem")]

print(f"{'文件':<60} {'大小MB':<8} {'引擎':<8} {'地图':<20} {'tick率':<7} {'时长s':<7} 状态")
print("-" * 130)

for f in files:
    path = os.path.join(DEMO_DIR, f)
    size_mb = os.path.getsize(path) / 1024 / 1024
    try:
        parser = DemoParser(path)
        h = parser.parse_header()
        map_name = h.get("map_name", "?") or "?"
        tickrate = h.get("tick_rate", 0) or 0
        duration = round(h.get("duration", 0) or 0)
        print(f"{f:<60} {size_mb:<8.1f} CS2      {map_name:<20} {tickrate:<7} {duration:<7} OK")
    except Exception as e:
        err = str(e).splitlines()[0][:60] if str(e) else type(e).__name__
        print(f"{f:<60} {size_mb:<8.1f} ?         {'':<20} {'':<7} {'':<7} FAIL: {err}")
