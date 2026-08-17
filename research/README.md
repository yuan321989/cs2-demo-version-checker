# 调研脚本说明

本目录包含 CS2 demo 研究过程中的全部调研脚本，作为项目研究证据。
所有脚本基于 `demoparser2`（`pip install demoparser2`）。

## 工具核心

- `demo_version_checker.py`（项目根目录）：**核心交付工具**
  自动读取 demo 头部 patch_version → 推荐匹配的 Steam 历史版本。
  用法：
  ```bash
  python demo_version_checker.py                          # 扫描全部 demo
  python demo_version_checker.py --current 1.41.6.7       # 标出当前版本能看的
  python demo_version_checker.py path/to/x.dem            # 检测单个 demo
  ```

## 调研脚本分组

### 版本映射研究（核心方法论来源）

| 脚本 | 用途 | 结论 |
|---|---|---|
| `check_versions.py` | 全量扫描 demo 的 patch_version | 34 个 demo 跨 8 个补丁版本 |
| `check_servers.py` | 识别 demo 录制服务器（腾讯国服/国际服） | YU/mi1 是腾讯国服，国际服可播 |
| `extract_builds.py` | 提取 demo 内服务器构建号（csgo_vXXXX） | 6 个不同构建号 2000776~2000860 |
| `build_version_map.py` | 构建号→版本号插值（初版，有误） | 证明插值法不可靠 |
| `version_map.py` | patch → 协议大区间映射（初版） | 建立区间概念 |
| `final_map.py` | patch 去点规则验证 + 最终映射表 | **验证 PatchVersion 去点规则** |
| `scan_demos.py` | 全量扫描（header/事件/击杀验证） | 34/34 全部可解析 |

### 第三方平台对比研究

| 脚本 | 用途 | 结论 |
|---|---|---|
| `compare_wmpvp.py` | 完美平台 zip 结构 + demo 文件头对比 | zip 是标准 deflate 单文件包 |
| `deep_compare.py` | 完美平台 vs 官方：事件/字段/header 全对比 | 底层协议相同，录制内容不同 |
| `zip_analysis.py` | zip 内部结构分析（EOCD/注释/条目） | 无特殊元数据，纯传输包装 |
| `compare_5e.py` | 5E 天梯 vs 官方：事件/字段/语音对比 | 5E 录语音（3.9 万条/局） |
| `scan_5e.py` | 5E 缓存目录全量扫描 | 5E demo 文件名自带日期 |
| `scan_wmpvp.py` | 完美平台 zip 全量解析 | 22 个 WMPVP demo 全部可解析 |
| `extract_wmpvp.py` | 解压完美平台 zip 到主目录 | 22 个成功 1 个损坏 |
| `wmpvp_lookup.py` | zip 内部时间 → 对局日期对照表 | 保留期与下载机制 |

### 数据深度验证

| 脚本 | 用途 | 结论 |
|---|---|---|
| `deep_parse.py` | 全 API 深度解析展示 | 投掷物 369 万条弹道记录 |
| `voice_test.py` | 语音提取验证 | 完美 10.2 万条/5E 3.9 万条，官方 0 |
| `check_angle.py` | 视角数据完整性验证 | 歪视角 demo 数据层完全正常 |
| `view_angle_demo.py` | 视角轨迹逐 tick 展示 | 拉枪视角完整可还原 |
| `match_info.py` | 对局玩家/击杀时间轴提取 | 用于完美平台查找封存 |

### 时间溯源

| 脚本 | 用途 |
|---|---|
| `yu_time.py` | 单 demo 时间信息提取 |
| `extract_time.py` | 从事件/消息挖时间戳（demo 无 Unix 时间） |
| `wmpvp_dates.py` | WMPVP demo 修改时间统计 |

### 其他

| 脚本 | 用途 |
|---|---|
| `analyze_yu.py` | YU.dem 深度分析（腾讯国服识别） |
| `check_g181.py` | 5E 练枪图 demo header 复核 |

## 关键研究结论（详见根目录 README.md 与 经验汇总.md）

1. **patch_version 去点规则**：demo 头 patch = 服务器协议号 = PatchVersion 去点
2. **格式周期模型**：断裂点 14088/14152/14168，周期内兼容
3. **三家平台**（完美/5E/官方）：底层协议相同，仅录制内容不同
4. **语音**：第三方平台 demo 含完整语音数据，可解析（解码待做）
