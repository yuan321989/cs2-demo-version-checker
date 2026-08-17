import os
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

# CS2 网络协议版本兼容区间（来源: CS Demo Manager 源码 cs2-plugin-version.ts）
# 插件版本 = 该区间客户端支持的最高协议版本
BANDS = [
    ("14030", "2023-beta ~ 2024-10-03 (Armory)"),
    ("14088", "2024-10-03 ~ 2025-07-28 (Animation)"),
    ("14094", "2025-07-28 ~ 2025-08-14"),
    ("14103", "2025-08-14 ~ 2025-09-17"),
    ("14112", "2025-09-17 ~ 2025-10-15"),
    ("14152", "2025-10-15 ~ 2026-04-08 (Animgraph 2)"),
    ("14168", "2026-04-08 ~ 2026-07-09 (1.41.6.8)"),
    ("latest", "2026-07-09 ~ 现在 (1.41.7.x)"),
]

def band_of(patch: str) -> int:
    if patch == "latest":
        return 14168
    return int(patch or 0)

rows = []
for f in sorted(os.listdir(DEMO_DIR)):
    if not f.lower().endswith(".dem"):
        continue
    try:
        h = DemoParser(os.path.join(DEMO_DIR, f)).parse_header()
        patch = h.get("patch_version", "?")
        srv = (h.get("server_name", "") or "").lower()
        src = "TENCENT" if ("tencent" in srv or "tgd" in srv) else "INTL"
        rows.append((f, patch, src))
    except Exception as e:
        rows.append((f, "ERR", str(e)[:30]))

print("demo 协议版本分布（按 patch_version）：")
from collections import Counter
cnt = Counter(r[1] for r in rows)
for p in sorted(cnt, key=lambda x: int(x) if x.isdigit() else 0):
    print(f"  patch {p:<6} x{cnt[p]}")
print()

# 找出每个 demo 落在哪个兼容区间
print("每个 demo 需要的引擎版本区间：")
for f, patch, src in sorted(rows, key=lambda r: int(r[1]) if r[1].isdigit() else 999999):
    if not patch.isdigit():
        print(f"  {f:<55} {patch}")
        continue
    pv = int(patch)
    band = None
    for v, desc in BANDS:
        upper = 14168 if v == "latest" else int(v)
        if v == "14030":
            if pv <= 14030:
                band = (v, desc)
                break
        elif v == "latest":
            if pv > 14168:
                band = (v, desc)
                break
        else:
            if pv == upper:
                band = (v, desc)
                break
    if band is None:
        # 找小于等于 patch 的最大区间
        for v, desc in reversed(BANDS[:-1]):
            if int(v) <= pv:
                band = (v, desc)
                break
    print(f"  {f:<55} patch {patch:<6} {src:<8} -> {band[0]} 区 ({band[1]})")
