# 中文文案

快照：2026-11-26。以 `content/copy-en.md` 为唯一事实源翻译。来源：`01-identity-and-bio.md`、`02-project-cards.md`、`03-timeline.md`、`04-awards-and-media.md`、`data/profile.json`、`data/projects.json`。

## Meta

- 标题：`郭沫晗 Robusr Guo — AI × 工程建造者`
- 描述：`郭沫晗（Robusr Guo），华中科技大学机器人工程科创实验班本科生，做 AI × 工程：CAD 智能体、仿生机器人、探空火箭与桌面 PCB 制造。`

## Header

- 站点名：Robusr Guo
- 导航：项目 · 经历 · 关于 · 联系
- 语言：English · 中文（当前）· Français

## Hero

- 小标签：华中科技大学 · 机器人工程
- 姓名：郭沫晗（旁注 Robusr Guo）
- 定位句：AI × 工程建造者。把真实问题做成能运行的硬件，再用 AI 压缩从想法到零件的距离。
- 简介：郭沫晗，十年卧室极客，华中科技大学机器人工程科创实验班本科生。13岁把卧室改造成机械电子工作室。
- 状态行：当前：Vulcan · Sencillo · HUST Robotics。
- 链接：GitHub · 邮箱 · Anteportal Labs
- 肖像 alt：郭沫晗在秋天的银杏树下
- 肖像图注：肖像

<!-- 来源：01-identity-and-bio.md 短版中文；5.1 定位句。 -->

## 迷你实验室

- 标题：迷你实验室
- 图注编号：图 00
- 说明：卧室工作台：白板上的推导、模块化机械臂、电子工作台，以及跑模型的笔记本电脑。
- alt：摆满设备的卧室工作台：写满公式的白板、机械臂、打开的笔记本电脑、电路板、工具和书架。
- 图片：`/assets/lab/minilab-1440.jpg`；480/960/1440 WebP，1440 JPEG 回退。

<!-- 来源：Robusr 提供的 minilab.jpeg；发布资源已去除 EXIF。 -->

## 代表项目

<!-- GitHub stars、forks、最近推送与最新 Release 由 src/data/github.json 渲染，并通过 /api/github 刷新；本稿不固定 stars 数。 -->

### 01 · Vulcan — AI × CAD — 活跃

- 一句话：一句话输入，可编辑的 SolidWorks 特征树输出。
- 正文：一款 SolidWorks AI 插件，把一句工程需求变成原生、可编辑的特征。模型返回受类型约束的 JSON 特征树，C# 客户端通过 SolidWorks COM API 执行。没有 exec()，没有代码生成面。
- 技术：C# · WPF · .NET 4.8 · Python · Flask · SolidWorks COM API · LLM
- 证据：GPL-3.0 · 类型化 JSON 契约
- 版本：v1.3.0
- 出口：仓库 → `https://github.com/Robusr/Vulcan`

### 02 · Hsiwu — 仿生机器人 — 完成

- 一句话：六段翼、三台电机、零行代码。
- 正文：仿生蝙蝠扑翼机器人，每侧三段、共六段翼面。3 片 NE555、1 片 74HC04 与 3 片 L293D 构成完整的控制逻辑。无 MCU、无固件。
- 技术：SolidWorks · Altium · NE555 · 74HC04 · L293D · FDM
- 证据：MIT · 含 Gerber、BOM 与 STEP
- 出口：仓库 → `https://github.com/Robusr/Hsiwu`

### 03 · DustArrow X — 航空航天 / 嵌入式 — 归档

- 一句话：为家乡的沙尘天气，造一支探空火箭。
- 正文：40 mm 模块化气象探空火箭，10 个功能舱段、9 块 PCB 模块。RP2040 传感栈、LoRa 下行与 PyQt5 地面站，用来测量沙尘天气中大气垂直结构。
- 技术：RP2040 · LoRa · PyQt5 · SolidWorks · EasyEDA · CFD
- 证据：第 37 届全国青少年科技创新大赛二等奖 · 32 项测试通过 · 2023 年戈壁试飞
- 出口：仓库 → `https://github.com/Robusr/DustArrow`

### 04 · OnesArm — 模块化机器人 — v2 现行

- 一句话：一台机械臂，二十四种构型。
- 正文：模块化串联机械臂，采用 T/N 榫卯接口。三个可互换模块得到 3! × 2² = 24 种布局；v2 平台使用步进/CAN 关节、5 mm 5052 铝板与碳纤维管。
- 技术：SolidWorks · STM32 · CAN · MATLAB · FEA
- 证据：第 38 届全国青少年科技创新大赛一等奖 · 24 种布局已建模 · 工作空间约 450 mm
- 出口：仓库 → `https://github.com/Robusr/OnesArm`

### 05 · Anteportal Labs · Sencillo — AI × 制造 — 原型前

- 一句话：从 vibe coding 到 vibe making。
- 正文：Anteportal Labs 是一支学生创立的团队，正在开发 Sencillo 桌面 PCB 加工中心。它把干法隔离铣削与机内铜铆钉过孔结合在一起。所有性能数字都是设计目标；截至 2026 年 10 月处于原型前阶段。
- 技术：CAM · CNC isolation milling · Copper rivet vias · Constrained generation · Offline
- 证据标记：设计目标，非实测
- 证据：8/8 mil 线宽线距 · 0.8 mm 铜铆钉过孔 · 单板 ≤30 分钟
- 出口：组织主页 → `https://github.com/Anteportal`

<!-- 来源：02-project-cards.md 第 1–5 张卡片；projects.json。Sencillo 的数字全部标注为设计目标，未写成实测。 -->

## 经历

- 2018 — 13岁把卧室改造成机械电子工作室。
- 2019–2022 — 做了超声波测距仪、写字机器人、RFID 柜锁、室内环境监测仪和树莓派个人网站。
- 2023 — DustArrow：从固体火箭推力采集器，到完整探空火箭、航电、遥测与戈壁试飞。
- 2023 — 第 37 届全国青少年科技创新大赛二等奖。
- 2024 — 第 38 届全国青少年科技创新大赛一等奖（OnesArm）；登上上海电视台《少年爱迪生》。
- 2026 — 进入华中科技大学机器人工程科创实验班。

<!-- 来源：03-timeline.md 一页版；04-awards-and-media.md。 -->

## 奖项与报道

- 2024 — 第 38 届全国青少年科技创新大赛一等奖 — OnesArm
- 2023 — 第 37 届全国青少年科技创新大赛二等奖 — DustArrow X
- 2024 — 上海电视台《少年爱迪生》第八季（2024）— 观看节目：`https://www.kankanews.com/detail/LMwVGm9WB2z`

<!-- 来源：04-awards-and-media.md。不使用奖状照片、节目截图或竞赛 logo。 -->

## 其他项目

- Huginn — 自动化数据统计与分析的 AI agent — Python — `https://github.com/Robusr/Huginn`
- Robusr-skill — 从个人记忆与人格中提炼的数字分身技能 — Agent skills — `https://github.com/Robusr/Robusr-skill`
- Lynx — 面向低速自动驾驶的感知融合 SDK — Python — `https://github.com/Robusr/Lynx`
- Gungnir — 商业模拟对抗的 AI copilot：确定性现金流引擎加 LLM 策略层 — Python · LLM — `https://github.com/Robusr/Gungnir`

<!-- 来源：02-project-cards.md「More work」；projects.json secondary；2026-11-26 的 GitHub 主页。由作者选定 4 项。 -->

## 关于

17 岁的那个冬天，喜欢高能燃料发动机的同学委托我，帮他们搭建简易的推力采集测试台和远程点火装置。按下按钮，硝糖燃料被点燃喷出的一瞬间，像极了《十月的天空》打破煤林镇传统与安稳的霍默，在那座小得只剩下名字的城市里，我决定开始造火箭。父亲是美术老师，他用来画山水长卷的落地台灯被我搬进了卧室。

从 Matlab 中冯卡门曲线的定量计算和理想模型的 CFD 定性分析，到模块化箭体 PCB 的装配拓扑和 LoRa 数据帧的丢包测试，系统工程中每一处加强筋和运放器，都是抽象理论工程化落地的具体节点。

由意到形，就像父亲笔下墨色的焦、浓、重、淡、清，山水写意一气呵成，为我的探索赋予意义。

<!-- 来源：作者于 2026-11-26 提供的中文原文；英文与法文为译本。 -->

<!-- 来源：01-identity-and-bio.md 长版；未重复 Hero 句子。 -->

## Footer

- 联系：Robusr@outlook.com · github.com/Robusr · github.com/Anteportal
- 地点：中国，武汉
- 最后更新：2026 年 11 月
- 语言：English · 中文（当前）· Français
- 签名：Why not?
