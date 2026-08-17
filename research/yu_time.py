from demoparser2 import DemoParser
import os

path = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\9215456684820760588_0.dem"
print("文件修改时间:", os.path.getmtime(path))

import datetime
print("文件修改时间(本地):", datetime.datetime.fromtimestamp(os.path.getmtime(path)))
print("文件大小:", round(os.path.getsize(path)/1024/1024, 1), "MB")

p = DemoParser(path)
h = p.parse_header()
print("\nHeader:")
for k, v in h.items():
    print(f"  {k}: {v}")

# 提取比赛事件线索：回合、击杀时间轴
try:
    kills = p.parse_event("player_death")
    print(f"\n击杀数: {len(kills)}")
    print("首个击杀 tick:", kills['tick'].min() if len(kills) else "N/A")
    print("最后击杀 tick:", kills['tick'].max() if len(kills) else "N/A")
except Exception as e:
    print("击杀解析失败:", str(e)[:80])
