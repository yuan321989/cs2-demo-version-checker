import os
import re
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

# ============ 锚点验证（来自 CS Demo Manager 源码注释） ============
# CS2PluginVersion: '14030' = "up to the 1.40.3.0 version"
#                    '14168' = "... 09/07/2026 update (1.41.6.8)"
# => 规则：协议版本号 = PatchVersion 去小数点（1.41.6.8 -> 14168）
ANCHORS = [
    ("1.40.3.0", 14030, "CSDM 注释 14030"),
    ("1.41.6.8", 14168, "CSDM 注释 14168"),
]

print("=== 规则验证：PatchVersion 去点 ===")
for ver, proto, src in ANCHORS:
    calc = int(ver.replace(".", ""))
    status = "OK" if calc == proto else f"MISMATCH (calc={calc})"
    print(f"  {ver} -> {proto} ({src}): {status}")

# ============ Steam 官方可切换版本（用户提供） ============
STEAM_VERSIONS = [
    ("1.40.8.8", 14088), ("1.41.2.9", 14129), ("1.41.4.1", 14141),
    ("1.41.6.7", 14167), ("1.41.6.8", 14168), ("1.41.6.9", 14169),
    ("1.41.7.2", 14172), ("1.41.7.3", 14173), ("1.41.7.4", 14174),
]

print()
print("=== Steam 可选版本 -> 协议号 ===")
for v, p in STEAM_VERSIONS:
    print(f"  {v:<10} -> {p}")

# 选版本规则：客户端协议号 >= demo patch，且为可选项中最接近的
def pick_version(demo_patch: int):
    candidates = [(v, p) for v, p in STEAM_VERSIONS if p >= demo_patch]
    if not candidates:
        return "无可用版本"
    return min(candidates, key=lambda x: x[1])

print()
print(f"{'demo':<55} {'patch':<7} {'build':<9} {'推荐Steam版本':<12} 说明")
print("-" * 105)

rows = []
for f in sorted(os.listdir(DEMO_DIR)):
    if not f.lower().endswith(".dem"):
        continue
    try:
        h = DemoParser(os.path.join(DEMO_DIR, f)).parse_header()
        patch_s = h.get("patch_version", "?")
        gdir = h.get("game_directory", "?") or "?"
        m = re.search(r"csgo_v(\d+)", gdir)
        build = m.group(1) if m else "?"
        if patch_s.isdigit():
            patch = int(patch_s)
            ver, _ = pick_version(patch)
            note = "GOTV比赛" if build == "?" else f"服务器v{build}"
            rows.append((f, patch_s, build, ver, note))
        else:
            rows.append((f, patch_s, build, "?", "解析失败"))
    except Exception as e:
        rows.append((f, "?", "?", "?", str(e)[:30]))

for f, patch, build, ver, note in sorted(rows, key=lambda r: int(r[1]) if r[1].isdigit() else 999999):
    print(f"{f:<55} {patch:<7} {build:<9} {ver:<12} {note}")
