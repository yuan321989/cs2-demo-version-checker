import os
import glob
import zipfile
import shutil

DEMO_DIR = r"C:\Users\mr.bread\AppData\Roaming\Wmpvp\demo"
TARGET = r"D:\steam\steam\steamapps\common\Counter-Strike Global Offensive\game\csgo"

ok, skip, exist = 0, 0, 0
for zf in sorted(glob.glob(os.path.join(DEMO_DIR, "*.zip"))):
    name = os.path.basename(zf)
    try:
        with zipfile.ZipFile(zf) as z:
            inner = z.namelist()[0]
            dest = os.path.join(TARGET, "WMPVP_" + inner)
            if os.path.exists(dest):
                exist += 1
                continue
            with z.open(inner) as src, open(dest, "wb") as out:
                shutil.copyfileobj(src, out)
            ok += 1
            print(f"OK  {name} -> WMPVP_{inner}")
    except Exception as e:
        skip += 1
        print(f"SKIP {name}: {str(e)[:50]}")

print(f"\n解压成功: {ok}, 已存在: {exist}, 跳过: {skip}")
