from demoparser2 import DemoParser
import os

path = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\YU.dem"
print("文件大小:", round(os.path.getsize(path) / 1024 / 1024, 1), "MB")

p = DemoParser(path)
h = p.parse_header()
for k, v in h.items():
    print(f"  {k}: {v}")

print("\n可用事件:", p.list_game_events()[:20])
print("\n击杀事件数:", len(p.parse_event("player_death")))
