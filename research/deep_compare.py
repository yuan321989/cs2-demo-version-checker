from demoparser2 import DemoParser
import os

wmpvp = r"C:\Users\mr.bread\Desktop\PROject\hermes project\cs游戏分析\tmp_wmpvp\9211728447651027212_0.dem"
valve = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\spirit-vs-9z-m3-dust2.dem"

print("=" * 70)
print("完美平台 vs Valve 官方 demo 的 header 对比")
print("=" * 70)
for label, path in [("完美平台", wmpvp), ("Valve官方", valve)]:
    p = DemoParser(path)
    h = p.parse_header()
    print(f"\n--- {label} ---")
    for k, v in h.items():
        print(f"  {k}: {v}")

print()
print("=" * 70)
print("事件类型对比")
print("=" * 70)
w_events = set(DemoParser(wmpvp).list_game_events())
v_events = set(DemoParser(valve).list_game_events())
print(f"完美平台事件数: {len(w_events)}, 官方事件数: {len(v_events)}")
print(f"完美平台独有: {sorted(w_events - v_events)}")
print(f"官方独有: {sorted(v_events - w_events)}")

print()
print("=" * 70)
print("实体字段对比")
print("=" * 70)
w_fields = set(DemoParser(wmpvp).list_updated_fields())
v_fields = set(DemoParser(valve).list_updated_fields())
print(f"完美平台字段数: {len(w_fields)}, 官方字段数: {len(v_fields)}")
print(f"完美平台独有字段(前15): {sorted(w_fields - v_fields)[:15]}")
print(f"官方独有字段(前15): {sorted(v_fields - w_fields)[:15]}")
