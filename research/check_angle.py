from demoparser2 import DemoParser

p = DemoParser(r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\9215456684820760588_0.dem")
df = p.parse_ticks(["CCSPlayerPawn.m_angEyeAngles", "CCSPlayerPawn.m_vecX", "CCSPlayerPawn.m_vecY"])
ang = df["CCSPlayerPawn.m_angEyeAngles"]

print(f"玩家数: {df['name'].nunique()}")
print(f"总行数: {len(df)}")
yaws = [a[1] for a in ang if a is not None and len(a) > 1]
pitches = [a[0] for a in ang if a is not None and len(a) > 0]
print(f"yaw 范围: {min(yaws):.1f} ~ {max(yaws):.1f} (正常应为 -180~180)")
print(f"pitch 范围: {min(pitches):.1f} ~ {max(pitches):.1f} (正常应为 -89~89)")

# 视角是否持续变化（不是死数值）
unique_yaw = len(set(round(y, 1) for y in yaws))
print(f"yaw 不同值数量: {unique_yaw} (数据量 {len(yaws)}，若很小说明视角数据缺失)")

# 坐标是否正常
x = df["CCSPlayerPawn.m_vecX"]
print(f"X 范围: {x.min():.0f} ~ {x.max():.0f} (de_dust2 约 -2000~3000)")
