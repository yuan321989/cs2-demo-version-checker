# CS2 Demo 版本适配经验

解决 CS2 历史 demo "Demo is incompatible with this game version" / "解析消息失败" 问题。
自动检测 demo 需要的游戏版本，给出 Steam 版本切换方案。

## 核心原理

```
demo 文件头 patch_version 字段 = 录制服务器的协议版本号
= 游戏 PatchVersion 去掉小数点（1.41.6.8 -> 14168）
```

- demo 文件是明文二进制，用 demoparser2 可直接读头部（无需逆向）
- 兼容规则（2026-08-16 实测归纳，**格式周期模型**）：
  - 真正的 demo 格式断裂点：**14088 / 14152 / 14168**
    （Animation / Animgraph 2 / 2026-07-09 更新，跨断裂点则不能播）
  - 中间小版本（14094/14103/14112）不改变格式，跨它们可播
  - 客户端协议号 P 能播 [format_epoch(P), P] 内所有 patch
  - 关键实测：1.41.2.9(14129) 播 patch 14107 差 22 成功（推翻早期"差值<=16"模型）；
    1.41.6.7(14167) 播 patch 14141 失败（跨 14152 断裂点）
- 选版本策略 = **"协议号 >= demo patch 的最小可用版本"**

## demo 库现状（2026-08-16 共 56 个）

来源分布：
- **Valve 官方/比赛 demo**：34 个（spirit-vs-9z、spirit-vs-falcons、spirit-vs-mouz、5E 等）
- **完美世界竞技平台（WMPVP）**：22 个（`WMPVP_` 前缀，zip 内解压）
- **腾讯国服**：2 个（YU、mi1，patch 14164/14167，国际服可播）

## 已实测验证（2026-08-15）

| Steam 版本 | 协议号 | 实测结果 |
|---|---|---|
| 1.41.6.7 | 14167 | ✅ spirit-vs-9z-m3-dust2（patch 14165）、YU.dem（patch 14164，腾讯国服）|
| 1.41.6.7 | 14167 | ✅ spirit-vs-falcons-m1-nuke/m2-dust2（patch 14126）|
| 1.41.6.7 | 14167 | ❌ spirit-vs-mouz-m1-dust2（patch 14141）、spirit-vs-falcons-m1-nuke（patch 14126）|
| 1.41.4.1 | 14141 | ⏳ 待验证（patch 14141 的 14 个 demo）|
| 1.41.2.9 | 14129 | ⏳ 待验证（patch 14126 的 2 个 demo）|

> 注意：表格中有冲突项（1.41.6.7 对 14126 有 ✅ 和 ❌），需复核。

## 完整映射（56 个 demo）

| 推荐版本 | 协议号 | 覆盖 demo | 数量 |
|---|---|---|---|
| **1.41.6.7** | 14167 | spirit-vs-9z 三场、spirit-vs-falcons(14160/14165) 三场、666/777/888/999/b/t、YU、mi1、9.dem、003815794996129301013、g181×2、WMPVP_* (14160~14165) 18 个 | 40 |
| **1.41.4.1** | 14141 | 0038 开头×5、1~4.dem、falcons-vs-spirit×2、spirit-vs-mouz×2、9215456684820760588、5e_aim_springfestival、WMPVP_9207926766762418572 (14135) | 15 |
| **1.41.2.9** | 14129 | spirit-vs-falcons-m1-nuke、m2-dust2 | 2 |
| **1.41.7.2** | 14172 | WMPVP_9211728447651027212、WMPVP_9218906059285477644、WMPVP_9222143021300860940 (patch 14171) | 3 |

## 关键经验

1. **Steam 属性 -> Beta/游戏版本 可直接切换历史版本**（CS2 已支持，无需 download_depot 手动下载）
2. **demo 的 patch_version 决定兼容版本**，服务器归属（腾讯国服/国际服）不影响播放
   （实测 YU.dem 是腾讯广州服务器，国际服 1.41.6.7 客户端可正常播放）
3. **1.41.7.x（latest）播不了所有历史 demo**——必须切到录制时点的版本
4. 腾讯国服 demo（server_name 含 tencent/tgd）同样按 patch_version 匹配即可
5. 每个版本切换需重新下载几 GB 客户端文件，建议按版本批量播放
6. **第三方平台 demo 的已知问题**（2026-08-16 实测）：
   - 完美世界竞技平台 demo（server_name 含"完美世界"）：视角数据正常（demoparser2 验证
     yaw/pitch/坐标全范围正常），但官方客户端回放视角与录制时不同步（歪视角）——
     第三方服务器视角同步策略与 Valve GOTV 不同，官方客户端渲染无解，只能走数据层
   - 自定义地图/练枪图 demo（如 5E 平台 g181-*）：旧版本客户端播放可能闪退，
     属播放器级兼容问题，数据层解析不受影响
   - 播 demo 闪退前先确认版本匹配：patch 14153 的 demo 在 1.41.4.1 下必闪退
     （协议号不匹配），必须用对应推荐版本

## 完美平台 demo 存储位置

```
C:\Users\mr.bread\AppData\Roaming\Wmpvp\demo\   <- 完美平台下载的 zip 包
```

- 格式：`<steamid>_0.zip`，内含同名 .dem
- 播放方式：完美平台客户端内置播放器可直接播 zip；解压出的 .dem 可用
  Steam 版本切换方案在 CS2 内播放
- 注意：部分 zip 可能下载损坏（0 字节），需在平台内重新下载

## 工具用法

```bash
pip install demoparser2
python demo_version_checker.py                          # 扫描默认目录全部 demo
python demo_version_checker.py --current 1.41.6.7       # 标出当前版本能看的
python demo_version_checker.py path/a.dem               # 检测单个 demo
```

## 相关数据源

- CS Demo Manager 源码 `cs2-plugin-version.ts`：协议版本区间划分
  （14030 Armory / 14088 Animation / 14094 / 14103 / 14112 / 14152 Animgraph2 / 14168 / latest）
- Swiftly-Tracker/CS2-Dumps：构建号 -> PatchVersion 映射
- SteamDB depot 2347770/2347771：manifest 记录（download_depot 备用方案）

## 版本对应关系备忘

| 游戏版本 | 协议号 | 备注 |
|---|---|---|
| 1.40.8.8 | 14088 | |
| 1.41.2.9 | 14129 | |
| 1.41.4.1 | 14141 | |
| 1.41.6.7 | 14167 | Animgraph 2 前最后版本 |
| 1.41.6.8 | 14168 | Animgraph 2 后 |
| 1.41.6.9 | 14169 | |
| 1.41.7.2~7.4 | 14172~14174 | latest 区间 |
