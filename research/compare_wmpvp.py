import zipfile
import os
import struct

DEMO_DIR = r"C:\Users\mr.bread\AppData\Roaming\Wmpvp\demo"
sample = os.path.join(DEMO_DIR, "9211728447651027212_0.zip")

print("=" * 60)
print("1. ZIP 结构分析")
print("=" * 60)
with zipfile.ZipFile(sample) as z:
    for info in z.infolist():
        print(f"  文件名: {info.filename}")
        print(f"  大小: {info.file_size} bytes (压缩后 {info.compress_size})")
        print(f"  压缩方式: {info.compress_type} (0=存储, 8=deflate)")
        print(f"  注释: {info.comment!r}")
        print(f"  创建时间: {info.date_time}")

# 看 zip 中央目录的额外字段（完美平台可能塞了元数据）
print()
print("原始字节头 64 字节:")
with open(sample, "rb") as f:
    head = f.read(64)
    print(" ", head[:32].hex(" "), "|", head[:32])

# 解压出来对比文件头
print()
print("=" * 60)
print("2. DEM 文件头对比 (完美平台 vs Valve 官方)")
print("=" * 60)
with zipfile.ZipFile(sample) as z:
    z.extract("9211728447651027212_0.dem", r"C:\Users\mr.bread\Desktop\PROject\hermes project\cs游戏分析\tmp_wmpvp")

wmpvp_dem = r"C:\Users\mr.bread\Desktop\PROject\hermes project\cs游戏分析\tmp_wmpvp\9211728447651027212_0.dem"
valve_dem = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\spirit-vs-9z-m3-dust2.dem"

for label, path in [("完美平台", wmpvp_dem), ("Valve官方", valve_dem)]:
    print(f"\n--- {label} ({os.path.basename(path)}) ---")
    with open(path, "rb") as f:
        magic = f.read(16)
        print(f"  文件头魔数: {magic}")
        # Source 2 demo: PBDEMS2 开头
        rest = f.read(128)
        print(f"  头 128 字节: {rest[:64].hex(' ')}")
