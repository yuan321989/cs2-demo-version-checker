from demoparser2 import DemoParser
import os

# 5E 天梯 demo vs Valve 官方
fife = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\5E_g161-20260521222034088604101_de_dust2.dem"
valve = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\spirit-vs-9z-m3-dust2.dem"

print("=" * 70)
print("5E 天梯 vs Valve 官方 header 对比")
print("=" * 70)
for label, path in [("5E天梯", fife), ("Valve官方", valve)]:
    h = DemoParser(path).parse_header()
    print(f"\n--- {label} ---")
    for k, v in h.items():
        print(f"  {k}: {v}")

print()
print("=" * 70)
print("事件对比")
print("=" * 70)
f_ev = set(DemoParser(fife).list_game_events())
v_ev = set(DemoParser(valve).list_game_events())
print(f"5E事件数: {len(f_ev)}, 官方事件数: {len(v_ev)}")
print(f"5E独有: {sorted(f_ev - v_ev)}")
print(f"官方独有: {sorted(v_ev - f_ev)}")

print()
print("=" * 70)
print("实体字段对比")
print("=" * 70)
f_fd = set(DemoParser(fife).list_updated_fields())
v_fd = set(DemoParser(valve).list_updated_fields())
print(f"5E字段数: {len(f_fd)}, 官方字段数: {len(v_fd)}")
print(f"5E独有(前10): {sorted(f_fd - v_fd)[:10]}")
print(f"官方独有(前10): {sorted(v_fd - f_fd)[:10]}")

print()
print("=" * 70)
print("语音对比")
print("=" * 70)
for label, path in [("5E天梯", fife), ("Valve官方", valve)]:
    v = DemoParser(path).parse_voice()
    print(f"  {label}: {len(v)} 条语音")

print()
print("=" * 70)
print("击杀事件样本 (验证数据完整性)")
print("=" * 70)
k = DemoParser(fife).parse_event("player_death")
print(f"  击杀数: {len(k)}")
print(f"  武器分布: {k['weapon'].value_counts().head(5).to_dict()}")
