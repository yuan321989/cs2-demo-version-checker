from demoparser2 import DemoParser
import datetime

path = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\9215456684820760588_0.dem"
p = DemoParser(path)

print("=" * 60)
print("对局标识参考信息")
print("=" * 60)

# 玩家信息
players = p.parse_player_info()
print(f"\n玩家数: {len(players)}")
print("玩家列表 (name / steamid / team):")
for _, row in players.iterrows():
    print(f"  {row['name']:<30} {row['steamid']}")

# 击杀时间轴概览
kills = p.parse_event("player_death")
print(f"\n击杀总数: {len(kills)}")
first_tick = kills['tick'].min()
last_tick = kills['tick'].max()
# CS2 64 tick 服务器, tick 换算秒
def tick_to_sec(t):
    return round((t - first_tick) / 64, 1)
print(f"对局时长: {tick_to_sec(last_tick)} 秒 ≈ {tick_to_sec(last_tick)/60:.1f} 分钟")

# 前 10 个击杀用于对照
print("\n前 10 次击杀 (时间轴起点 = 0):")
for _, k in kills.head(10).iterrows():
    t = tick_to_sec(int(k['tick']))
    print(f"  [{t:>7.1f}s] {k['attacker_name']} -> {k['user_name']} ({k['weapon']})")

# 回合信息
try:
    rounds = p.parse_rounds()
    print(f"\n回合数: {len(rounds)}")
except Exception as e:
    print(f"\n回合解析: {str(e)[:60]}")

# 服务器时间尝试: 有些 demo 带 server message
try:
    msgs = p.parse_event("server_message")
    if len(msgs):
        print("\n服务器消息 (可能含时间):")
        for _, m in msgs.head(5).iterrows():
            print(f"  {m.to_dict()}")
except Exception as e:
    print(f"\n服务器消息: {str(e)[:60]}")
