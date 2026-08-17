import os
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
files = sorted(f for f in os.listdir(DEMO_DIR) if f.lower().endswith(".dem"))

for f in files:
    path = os.path.join(DEMO_DIR, f)
    try:
        h = DemoParser(path).parse_header()
        server = h.get("server_name", "?") or "?"
        flag = "国服" if ("tencent" in server.lower() or "tgd" in server.lower()) else "国际"
        print(f"[{flag}] {h.get('patch_version','?'):<6} {f}")
    except Exception as e:
        print(f"[ERR] {f}: {str(e)[:50]}")
