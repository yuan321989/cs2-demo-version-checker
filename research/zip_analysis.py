import zipfile
import os

# 检查完美平台 zip 是否有额外的元数据文件或特殊结构
DEMO_DIR = r"C:\Users\mr.bread\AppData\Roaming\Wmpvp\demo"
files = os.listdir(DEMO_DIR)
print(f"完美平台 demo 目录文件数: {len(files)}")
print("全部是 .zip:", all(f.endswith(".zip") for f in files))

# 看 zip 尾部注释/额外字段
sample = os.path.join(DEMO_DIR, "9211728447651027212_0.zip")
with open(sample, "rb") as f:
    data = f.read()
# zip 末尾 EOCD 记录
eocd = data.rfind(b"PK\x05\x06")
print(f"\nEOCD 位置: {eocd}")
if eocd > 0:
    comment_len = int.from_bytes(data[eocd+20:eocd+22], "little")
    print(f"zip 注释长度: {comment_len}")
    if comment_len:
        print(f"注释内容: {data[eocd+22:eocd+22+comment_len]!r}")

# 检查中央目录是否有压缩前原始大小以外的特殊字段
print("\n=== zip 内部文件名对比 ===")
with zipfile.ZipFile(sample) as z:
    names = z.namelist()
    print("条目:", names)
    # 检查是否有 __MACOSX 或额外条目
    extras = [n for n in names if n.startswith("__MACOSX") or "/" in n]
    print("额外条目:", extras if extras else "无(纯单文件 zip)")

# 对比: 解压后的 dem 与完美平台客户端播放时是否只是"标准 dem"
print("\n=== 结论验证: 完美平台 zip 就是一个标准 deflate zip, 内含标准 .dem ===")
with zipfile.ZipFile(sample) as z:
    info = z.infolist()[0]
    print(f"压缩率: {info.compress_size/info.file_size*100:.1f}% (deflate 正常水平)")
