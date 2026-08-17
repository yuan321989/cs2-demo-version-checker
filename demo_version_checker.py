"""
CS2 Demo 版本适配器 - 自动检测 demo 需要的游戏版本
=================================================
用法:
    python demo_version_checker.py                 # 扫描默认目录全部 demo
    python demo_version_checker.py path/to/a.dem   # 检测单个 demo
    python demo_version_checker.py --watch         # 监控模式(后续)

原理:
    demo 文件头的 patch_version 字段 = 录制服务器的协议版本号
    = 游戏 PatchVersion 去掉小数点 (1.41.6.8 -> 14168)
    客户端协议号 >= demo patch 时兼容 (已实测验证: 1.41.6.7 可播 patch 14165/14164)
"""

import os
import re
import sys
import json
from pathlib import Path

try:
    from demoparser2 import DemoParser
except ImportError:
    print("需要安装 demoparser2: pip install demoparser2")
    sys.exit(1)

# Steam 官方可切换版本表 (CS2 属性 -> Beta/游戏版本)
# 格式: "版本名" -> 协议号
# 来源: 用户实测 + CS Demo Manager 源码注释 + SteamDB
# NOTE: Valve 会增删可选版本, 此表需定期更新
STEAM_VERSIONS = {
    "1.40.8.8": 14088,
    "1.41.2.9": 14129,
    "1.41.4.1": 14141,
    "1.41.6.7": 14167,
    "1.41.6.8": 14168,
    "1.41.6.9": 14169,
    "1.41.7.2": 14172,
    "1.41.7.3": 14173,
    "1.41.7.4": 14174,
}

# Valve 协议大版本变更点 (来自 CSDM cs2-plugin-version.ts 注释)
# 格式变更导致旧 demo 不兼容新客户端, 需要匹配的旧版本
PROTOCOL_BREAKS = [
    ("14030", "2023-beta ~ 2024-10-03 (Armory)"),
    ("14088", "2024-10-03 ~ 2025-07-28 (Animation)"),
    ("14094", "2025-07-28 ~ 2025-08-14"),
    ("14103", "2025-08-14 ~ 2025-09-17"),
    ("14112", "2025-09-17 ~ 2025-10-15"),
    ("14152", "2025-10-15 ~ 2026-04-08 (Animgraph 2)"),
    ("14168", "2026-04-08 ~ 2026-07-09 (1.41.6.8)"),
    ("latest", "2026-07-09 ~ 现在 (1.41.7.x)"),
]

# 真正的 demo 格式断裂点 (实测归纳, 2026-08-16):
# 跨这些点 demo 格式变化, 客户端播不了格式断裂前的 demo。
# 中间的 14094/14103/14112 只是小更新, 不改变 demo 格式
# (实测: 1.41.2.9=14129 能播 patch 14107, 跨了 14112/14103/14094 三个小版本)。
# 实测数据:
#   - 14129 客户端: 可播 14107/14126/14129 (周期起点 14088)
#   - 14141 客户端: 可播 14126/14135/14141 (周期起点 14088)
#   - 14167 客户端: 可播 14153~14167, 不可播 14141/14126 (周期起点 14152)
#   - 14172 客户端: 可播 14171 (周期起点 14168)
FORMAT_BREAKS = [14088, 14152, 14168]

DEFAULT_DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"


def read_demo_info(path: str) -> dict:
    """读取 demo 头部信息"""
    p = DemoParser(path)
    h = p.parse_header()
    patch_s = h.get("patch_version", "?") or "?"
    gdir = h.get("game_directory", "") or ""
    srv = h.get("server_name", "") or ""
    m = re.search(r"csgo_v(\d+)", gdir)
    build = m.group(1) if m else None
    return {
        "patch": int(patch_s) if patch_s.isdigit() else None,
        "patch_raw": patch_s,
        "server_build": build,
        "server_name": srv,
        "map": h.get("map_name", "?"),
    }


def protocol_band(patch: int) -> str:
    """判断 patch 属于哪个协议大版本区间"""
    if patch is None:
        return "?"
    for ver, desc in PROTOCOL_BREAKS:
        if ver == "latest":
            if patch > 14168:
                return desc
        elif ver == "14030":
            if patch <= 14030:
                return desc
        else:
            if patch == int(ver):
                return desc
    # 落在两个 break 之间: 归入上一个区间
    for ver, desc in reversed(PROTOCOL_BREAKS[:-1]):
        if patch > int(ver):
            return desc
    return "?"


def recommend_version(patch: int) -> str:
    """推荐 Steam 版本: 协议号 >= patch 的最小可用版本

    实测验证: 1.41.6.7(14167) 可播 patch 14153~14167 的 demo,
    但播不了 patch 14141/14126 (跨格式断裂点)。
    实测验证: 1.41.4.1(14141) 可播 patch 14126~14141 的 demo。
    因此取 '协议号>=patch 的最小版本' 即最接近的版本, 与实测一致。
    """
    if patch is None:
        return "?"
    candidates = [(v, p) for v, p in STEAM_VERSIONS.items() if p >= patch]
    if not candidates:
        return f"无可用版本 (patch {patch} 太新)"
    return min(candidates, key=lambda x: x[1])[0]


def format_epoch(proto: int) -> int:
    """返回客户端协议号所属格式周期的起点

    格式断裂点: FORMAT_BREAKS = [14088, 14152, 14168]
    客户端协议号 P 属于周期 [break_k, break_{k+1}), 周期起点 = 最大的 break <= P
    周期内的所有 demo patch 都兼容 (patch <= 客户端协议号即可)
    """
    start = 0
    for b in FORMAT_BREAKS:
        if proto < b:
            break
        start = b
    return start


def can_play_with(current_proto: int, patch: int) -> bool:
    """判断当前已装客户端(协议号)能否播放该 demo

    格式周期模型 (2026-08-16 实测归纳):
      客户端协议号 P 能播 [format_epoch(P), P] 范围内所有 patch。
      跨格式断裂点(14088/14152/14168)则不能播。

    实测验证:
      - 1.41.2.9(14129): 可播 14107/14126/14129 (起点14088, 差22也OK)
      - 1.41.4.1(14141): 可播 14126/14135/14141 (起点14088)
      - 1.41.6.7(14167): 可播 14153~14167, 不可播 14141/14126 (起点14152)
      - 1.41.7.2(14172): 可播 14171 (起点14168)
    反例(旧差值模型失效): 14129 播 14107 差 22 成功, 而差值<=16 模型会误判
    """
    if patch is None:
        return False
    start = format_epoch(current_proto)
    return start <= patch <= current_proto


def check_demo(path: str) -> dict:
    """检测单个 demo"""
    info = read_demo_info(path)
    if info["patch"] is None:
        info.update({"version": "?", "band": "?", "ok": False, "reason": f"无法读取 patch: {info['patch_raw']}"})
        return info
    ver = recommend_version(info["patch"])
    band = protocol_band(info["patch"])
    info.update({"version": ver, "band": band, "ok": True, "reason": ""})
    return info


def main():
    args = sys.argv[1:]
    current_ver = None
    current_proto = None

    if args and args[0] == "--current":
        if len(args) < 2:
            print("用法: python demo_version_checker.py --current 1.41.6.7")
            return
        current_ver = args[1]
        current_proto = STEAM_VERSIONS.get(current_ver)
        if current_proto is None:
            print(f"未知版本 {current_ver}, 可用: {list(STEAM_VERSIONS)}")
            return
        args = args[2:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        if not args:
            args = []
        else:
            return

    if args and args[0] == "--watch":
        print("监控模式暂未实现, 当前为一次性扫描")
        args = args[1:]

    targets = []
    if args:
        for a in args:
            p = Path(a)
            if p.is_file() and p.suffix.lower() == ".dem":
                targets.append(str(p))
            elif p.is_dir():
                targets += [str(x) for x in p.glob("*.dem")]
            else:
                print(f"跳过无效路径: {a}")
    else:
        targets = [str(x) for x in Path(DEFAULT_DEMO_DIR).glob("*.dem")]
        print(f"扫描默认目录: {DEFAULT_DEMO_DIR}")

    if not targets:
        print("没有找到 .dem 文件")
        return

    if current_ver:
        print(f"\n当前客户端版本: {current_ver} (协议 {current_proto})")
    print(f"\n{'文件':<55} {'patch':<7} {'推荐版本':<10} {'当前版本'}")
    print("-" * 105)

    summary = {}
    playable_now = 0
    for t in sorted(targets):
        name = os.path.basename(t)
        try:
            info = check_demo(t)
            if info["ok"]:
                if current_proto is not None:
                    can = can_play_with(current_proto, info["patch"])
                    mark = "✅ 可直接看" if can else f"❌ 需切 {info['version']}"
                    if can:
                        playable_now += 1
                else:
                    mark = f"需切 {info['version']}"
                print(f"{name:<55} {info['patch']:<7} {info['version']:<10} {mark}")
                summary[info["version"]] = summary.get(info["version"], 0) + 1
            else:
                print(f"{name:<55} {'?':<7} {'?':<10} FAIL: {info['reason']}")
        except Exception as e:
            print(f"{name:<55} {'?':<7} {'?':<10} ERR: {str(e)[:40]}")

    if current_proto is not None:
        print(f"\n当前版本可看: {playable_now} 个")
    if summary:
        print("\n== 切换计划 ==")
        for ver, cnt in sorted(summary.items(), key=lambda x: x[1], reverse=True):
            print(f"  切到 {ver:<10} 可播 {cnt} 个 demo")
        print("\n操作: Steam 库 -> CS2 属性 -> Beta/游戏版本 -> 选对应版本 -> 等下载完成")


if __name__ == "__main__":
    main()
