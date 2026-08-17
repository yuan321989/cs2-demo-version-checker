from demoparser2 import DemoParser

p = DemoParser(r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\spirit-vs-9z-m3-dust2.dem")
fields = ["CCSPlayerPawn.m_angEyeAngles", "CCSPlayerPawn.m_vecX", "CCSPlayerPawn.m_vecY"]
df = p.parse_ticks(fields)

kills = p.parse_event("player_death")
k0 = kills[kills["user_name"] == "dgt"].iloc[0]
t0 = int(k0["tick"])
print(f"donk 首杀 dgt 发生在 tick {t0}，取前后 20 tick 视角轨迹：")
sub = df[(df["name"] == "donk") & (df["tick"] >= t0 - 20) & (df["tick"] <= t0 + 20)]
for _, r in sub.iterrows():
    ang = r["CCSPlayerPawn.m_angEyeAngles"]
    print(f"tick {int(r['tick']):>6}  yaw={ang[1]:>8.2f}  pitch={ang[0]:>7.2f}")
