import os
import glob
from demoparser2 import DemoParser

DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

# 尝试从 demo 内部提取时间线索
files = sorted(glob.glob(os.path.join(DEMO_DIR, "WMPVP_*.dem")))

# 检查事件里可能带时间的字段
for f in files[:3]:
    name = os.path.basename(f)
    p = DemoParser(f)
    print(f"=== {name} ===")
    try:
        # server_message / chat_message 可能带时间戳
        for ev in ["server_message", "chat_message"]:
            try:
                df = p.parse_event(ev)
                if len(df) > 0:
                    print(f"  {ev}: {len(df)} 条")
                    print(f"  字段: {list(df.columns)[:15]}")
                    if len(df):
                        print(f"  首条: {df.iloc[0].to_dict()}")
            except Exception as e:
                print(f"  {ev}: {str(e)[:50]}")
    except Exception as e:
        print(f"  ERR: {str(e)[:60]}")
    print()

# 尝试解析 hltv_versioninfo / 其他可能带时间的
print("=== 检查所有事件类型(前几个demo) ===")
seen = set()
for f in files:
    name = os.path.basename(f)
    p = DemoParser(f)
    evs = p.list_game_events()
    for ev in evs:
        if ev not in seen:
            seen.add(ev)
print("事件全集:", sorted(seen))
