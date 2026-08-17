import os
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
files = sorted(f for f in os.listdir(DEMO_DIR) if f.lower().endswith(".dem"))

ok, fail = [], []
for f in files:
    path = os.path.join(DEMO_DIR, f)
    try:
        h = DemoParser(path).parse_header()
        ok.append((f, h.get("patch_version", "?"), h.get("map_name", "?")))
    except Exception as e:
        err = str(e).splitlines()[0][:70] if str(e) else type(e).__name__
        fail.append((f, err))

print(f"=== 可解析 {len(ok)} 个 ===")
for f, ver, m in sorted(ok, key=lambda x: x[1]):
    print(f"  patch {ver:<8} {m:<22} {f}")
print(f"\n=== 解析失败 {len(fail)} 个 ===")
for f, err in fail:
    print(f"  {f}: {err}")
