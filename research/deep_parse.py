from demoparser2 import DemoParser
import os

path = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\spirit-vs-9z-m3-dust2.dem"
p = DemoParser(path)

print("=" * 70)
print("1. header - 文件头")
print("=" * 70)
h = p.parse_header()
for k, v in h.items():
    print(f"  {k}: {v}")

print()
print("=" * 70)
print("2. parse_player_info - 玩家档案")
print("=" * 70)
try:
    df = p.parse_player_info()
    print(f"  玩家数: {len(df)}, 字段: {list(df.columns)}")
    print(df.head(3).to_string())
except Exception as e:
    print(f"  ERR: {str(e)[:80]}")

print()
print("=" * 70)
print("3. parse_grenades - 投掷物完整弹道")
print("=" * 70)
try:
    g = p.parse_grenades()
    print(f"  投掷物记录: {len(g)}, 字段: {list(g.columns)}")
    print(g.head(3).to_string())
except Exception as e:
    print(f"  ERR: {str(e)[:80]}")

print()
print("=" * 70)
print("4. parse_item_drops - 道具掉落")
print("=" * 70)
try:
    d = p.parse_item_drops()
    print(f"  掉落记录: {len(d)}, 字段: {list(d.columns)}")
    if len(d):
        print(d.head(3).to_string())
except Exception as e:
    print(f"  ERR: {str(e)[:80]}")

print()
print("=" * 70)
print("5. parse_skins - 皮肤数据")
print("=" * 70)
try:
    s = p.parse_skins()
    print(f"  皮肤记录: {len(s)}, 字段: {list(s.columns)}")
    if len(s):
        print(s.head(3).to_string())
except Exception as e:
    print(f"  ERR: {str(e)[:80]}")
