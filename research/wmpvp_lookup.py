import zipfile, os, glob
from demoparser2 import DemoParser

ZIP_DIR = r"C:\Users\mr.bread\AppData\Roaming\Wmpvp\demo"

rows = []
for zf in sorted(glob.glob(os.path.join(ZIP_DIR, "*.zip"))):
    name = os.path.basename(zf).replace("_0.zip", "")
    try:
        with zipfile.ZipFile(zf) as z:
            info = z.infolist()[0]
            t = info.date_time
            pack = f"{t[0]:04d}-{t[1]:02d}-{t[2]:02d} {t[3]:02d}:{t[4]:02d}"
        rows.append([name, pack, None, None, None])
    except Exception as e:
        rows.append([name, "损坏", None, None, str(e)[:20]])

# 用已解压的 dem 补地图信息
DEMO_DIR = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"
for r in rows:
    dem = os.path.join(DEMO_DIR, f"WMPVP_{r[0]}_0.dem")
    if os.path.exists(dem):
        try:
            h = DemoParser(dem).parse_header()
            r[2] = h.get("map_name", "?")
            r[3] = h.get("patch_version", "?")
            r[4] = h.get("server_name", "?")
        except Exception:
            pass

print(f"{'完美平台ID':<22} {'对局时间(估)':<18} {'patch':<7} {'地图':<12} 服务器")
print("-" * 100)
for r in sorted(rows, key=lambda r: r[1]):
    name, pack, map_, patch, srv = r
    if patch is None:
        print(f"{name:<22} {pack:<18} {'?':<7} {'?':<12} {srv or '未解压'}")
    else:
        print(f"{name:<22} {pack:<18} {patch:<7} {str(map_):<12} {srv}")

print()
print("注: 对局时间为 zip 打包时间(完美平台打包日), 对局一般发生在当天或前一晚")
