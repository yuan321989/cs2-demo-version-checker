from demoparser2 import DemoParser
import os

# 测试完美平台带语音的 demo
wmpvp = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\WMPVP_9207646521171051020_0.dem"
# 对比官方 demo（应该没有语音）
valve = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\spirit-vs-9z-m3-dust2.dem"

for label, path in [("完美平台", wmpvp), ("Valve官方", valve)]:
    print(f"=== {label}: {os.path.basename(path)} ===")
    try:
        p = DemoParser(path)
        voice = p.parse_voice()
        print(f"  parse_voice() 返回类型: {type(voice)}")
        print(f"  shape/长度: {len(voice)}")
        if len(voice) > 0:
            print(f"  列: {list(voice.columns) if hasattr(voice, 'columns') else '?'}")
            print(voice.head(3).to_string() if hasattr(voice, 'head') else str(voice)[:500])
        else:
            print("  （无语音数据）")
    except Exception as e:
        print(f"  错误: {str(e)[:120]}")
    print()
