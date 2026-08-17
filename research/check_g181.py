from demoparser2 import DemoParser
import os

DEMO = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
for f in [
    "g181-20260508225614059342125_5e_aim_akm4.dem",
    "g181-20260508231721454987073_5e_aim_akm4.dem",
    "g181-20260325214750021892301_5e_aim_springfestival_2024.dem",
]:
    h = DemoParser(os.path.join(DEMO, f)).parse_header()
    print(f)
    print(f"  patch: {h.get('patch_version')} | map: {h.get('map_name')} | server: {h.get('server_name')}")
    print(f"  game_dir: {h.get('game_directory')}")
    print()
