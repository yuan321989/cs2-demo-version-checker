# CS2 Demo Version Checker 🎮

**自动检测 CS2 demo 需要哪个游戏版本**，告别"Demo is incompatible with this game version"。

```
丢进一个 .dem 文件 → 自动读取协议版本 → 告诉你要切换哪个 Steam 历史版本
```

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 这是什么？

CS2 的 demo（回放文件）**绑定录制时的游戏协议版本**。游戏更新后，旧 demo 会报
`Demo is incompatible with this game version` / `解析消息失败` 无法播放。

这个工具读取 demo 文件头里的 `patch_version`，自动算出需要切换到的 Steam 历史版本。

> 只读文件头（毫秒级），不需要解析整个 demo。

## 快速开始

```bash
# 1. 安装依赖
pip install demoparser2

# 2. 检测单个 demo
python demo_version_checker.py path/to/match.dem

# 3. 扫描整个 demo 目录（默认扫描 CS2 安装目录）
python demo_version_checker.py

# 4. 告诉工具你当前装的版本，标出哪些能看、哪些需要切
python demo_version_checker.py --current 1.41.6.7
```

### 输出示例

```
文件                                                      patch   推荐版本
spirit-vs-9z-m3-dust2.dem                                 14165   1.41.6.7   ✅ 可直接看
falcons-vs-spirit-m1-dust2.dem                            14141   1.41.4.1   ❌ 需切 1.41.4.1
```

## 核心原理

```
demo 头部 patch_version = 录制服务器协议号 = 游戏版本号去小数点
   例: 1.41.6.8 → 14168,  1.41.4.1 → 14141
```

**格式周期模型**（大量实测归纳）：

- Valve 有 3 个 **demo 格式断裂点**：`14088` / `14152` / `14168`
  （对应 Animation、Animgraph 2、2026-07 更新）
- 跨断裂点的 demo 无法在新版本播放，必须切换到录制时所在周期的版本
- 断裂点之间的小更新不改变 demo 格式，跨小版本可正常播放

| 推荐版本 | 协议号 | 兼容 patch 范围 |
|---|---|---|
| 1.41.2.9 | 14129 | 14088 ~ 14129 |
| 1.41.4.1 | 14141 | 14088 ~ 14141 |
| 1.41.6.7 | 14167 | 14152 ~ 14167 |
| 1.41.7.2+ | 14172+ | 14168 ~ 最新 |

## 如何切换游戏版本

Steam 官方支持直接切换历史版本：

```
Steam 库 → CS2 → 右键属性 → Beta/游戏版本 → 选择对应版本 → 等待下载
```

不需要下载任何第三方工具。

## 支持的 demo 来源

实测覆盖（100+ demo 验证）：

- ✅ Valve 官方比赛 demo（GOTV / ESL）
- ✅ 完美世界竞技平台（WMPVP）demo
- ✅ 5E 平台 demo
- ✅ 腾讯国服 demo（国际服客户端可播）

## 项目结构

```
cs2-demo-version-checker/
├── demo_version_checker.py    # 核心工具（单文件，零配置）
├── README.md                  # 本文档
├── 经验汇总.md                 # 完整研究文档 + 全部实测数据
└── research/                  # 调研脚本（版本映射/平台对比/数据深度验证）
```

## 常见问题

**Q: demo 报"解析消息失败"怎么办？**
A: 用本工具检测 patch_version → 切换对应版本 → 即可播放。

**Q: 为什么官方不兼容旧 demo？**
A: CS2 动画系统更新会改变 demo 格式（官方已确认），Valve 不为历史 demo 做向后兼容，
只能切换历史版本播放。

**Q: 第三方平台的 demo 和官方有区别吗？**
A: 底层协议完全一样（`valve_demo_2`），只是第三方平台多录制了语音和微观动作事件。

## 相关项目

- [demoparser2](https://github.com/LaihoE/demoparser) - 本项目依赖的 CS2 demo 解析器（Rust 核心）
- [CS Demo Manager](https://cs-demo-manager.com) - demo 管理工具（版本切换的参考数据源）

## License

MIT
