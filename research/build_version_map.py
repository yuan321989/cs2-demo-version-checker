import os
import re
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

# 锚点：构建号 -> (PatchVersion, 客户端版本号)
# 来源：Swiftly-Tracker/CS2-Dumps manifest 文件 + 本机 steam.inf
# 2000880 -> 1.41.7.4,  2000884 -> 1.41.7.5
# 规律：构建号最后两位 = 1.41.7.x 的 x？2000880 vs 1.41.7.4  => 880 -> 7.4 需要验证更多点

# Steam 官方可切换版本列表（用户提供）
STEAM_VERSIONS = ["1.40.8.8", "1.41.2.9", "1.41.4.1", "1.41.6.7", "1.41.6.8", "1.41.6.9", "1.41.7.2", "1.41.7.3", "1.41.7.4"]

# 已知锚点（构建号 -> PatchVersion 字符串）
ANCHORS = {
    2000880: "1.41.7.4",
    2000884: "1.41.7.5",
}

def build_to_patch(build):
    """根据锚点插值：构建号差 4 = 1.41.7.4 -> 1.41.7.5 (x +1)
    所以 1.41.x.y 的构建号最后 2 位 = y*4 + 偏移？验证：
    2000880 -> 1.41.7.4: 末位80
    2000884 -> 1.41.7.5: 末位84
    构建号末两位 / 4 = y: 80/4=20? 不对。84/4=21?
    换个思路：构建号 2000xxx, x=880 -> 1.41.7.4, x=884 -> 1.41.7.5
    差 4 -> 版本小版本 +1。所以 1.41.7.4 = 880, 1.41.7.3 = 876, ... 1.41.6.7 = 840?
    840/4 = 210。hmm 尝试线性：小版本号 y = (x - 836) / 4? 880: (880-836)/4 = 11 不对。
    直接看：7.4->880, 7.5->884。即版本 (a.b.c.d) -> 构建号尾 = d*4 + offset。
    若 offset=852: 7.4 -> 28+852=880 ✓, 7.5 -> 32+852=884 ✓
    则 1.41.2.9 -> 36+852=888? 那比 880 还大, 不合理。
    """
    # 用插值：每版本小步进 4 构建号。以 1.41.7.4=880 为基准
    # 1.41.x.y: 构建尾 = 880 - (7.4 到 x.y 的版本差)*4
    def version_num(s):
        parts = [int(p) for p in s.split(".")]
        return ((parts[0] * 1000 + parts[1]) * 100 + parts[2]) * 10 + parts[3]

    def from_build(build):
        # 构建尾数 -> 版本尾数：b = 880 + (v - 74) * 4
        # v = 74 + (b - 880) / 4
        delta = (build - 2000880) / 4.0
        base = version_num("1.41.7.4")
        v = base + delta
        maj = v // 1000
        rem = v % 1000
        mid = rem // 100
        rem2 = rem % 100
        minor = rem2 // 10
        patch = rem2 % 10
        return f"{maj}.{mid}.{minor}.{patch}"

    return from_build(build)

print("构建号 -> 推算版本（锚点校验）：")
for b in [2000760, 2000776, 2000795, 2000809, 2000832, 2000837, 2000860, 2000880, 2000884]:
    print(f"  build {b} -> {build_to_patch(b)}")

print()
print("== demo 需要的版本（按服务器构建号推算）==")
print(f"{'demo':<55} {'patch':<7} {'build':<9} {'推算版本':<10} {'Steam可选':<10}")
print("-" * 100)

results = []
for f in sorted(os.listdir(DEMO_DIR)):
    if not f.lower().endswith(".dem"):
        continue
    try:
        h = DemoParser(os.path.join(DEMO_DIR, f)).parse_header()
        patch = h.get("patch_version", "?")
        gdir = h.get("game_directory", "?") or "?"
        m = re.search(r"csgo_v(\d+)", gdir)
        build = int(m.group(1)) if m else None
        if build is None:
            results.append((f, patch, "?", "?", "无构建号(比赛demo)"))
            continue
        est = build_to_patch(build)
        # 找到 >= 推算版本的最小可选 Steam 版本
        import re as _re
        def vnum(s):
            return tuple(int(x) for x in s.split("."))
        candidates = [v for v in STEAM_VERSIONS if vnum(v) >= vnum(est)]
        pick = min(candidates, key=vnum) if candidates else "无匹配(太旧)"
        results.append((f, patch, str(build), est, pick))
    except Exception as e:
        results.append((f, "ERR", "?", "?", str(e)[:30]))

for f, patch, build, est, pick in results:
    print(f"{f:<55} {patch:<7} {build:<9} {est:<10} {pick:<10}")
