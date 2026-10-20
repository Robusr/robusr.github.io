# 中文文案

快照：2026-10-20。以 `content/copy-en.md` 为唯一事实源翻译。来源：`01-identity-and-bio.md`、`02-project-cards.md`、`03-timeline.md`、`04-awards-and-media.md`、`data/profile.json`、`data/projects.json`。

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
- 简介：郭沫晗，华中科技大学机器人工程科创实验班本科生。六年级在宁夏固原从 Arduino 起步，做过探空火箭、模块化机械臂和仿生蝙蝠机器人。现在做 AI × 工程工具：Vulcan 把自然语言变成可编辑的 SolidWorks 特征，Sencillo 尝试把 PCB 制造放回桌面。
- 状态行：当前：Vulcan · Sencillo · HUST Robotics。
- 链接：GitHub · 邮箱 · Anteportal Labs
- 肖像 alt：郭沫晗在海边

<!-- 来源：01-identity-and-bio.md 短版中文；5.1 定位句。 -->

## 代表项目

### 01 · Vulcan — AI × CAD — 活跃

- 一句话：一句话输入，可编辑的 SolidWorks 特征树输出。
- 正文：一款 SolidWorks AI 插件，把一句工程需求变成原生、可编辑的特征。模型返回受类型约束的 JSON 特征树，C# 客户端通过 SolidWorks COM API 执行。没有 exec()，没有代码生成面。
- 技术：C# · WPF · .NET 4.8 · Python · Flask · SolidWorks COM API · LLM
- 证据：23 stars（2026 年 10 月）· GPL-3.0 · 类型化 JSON 契约
- 出口：仓库 → `https://github.com/Robusr/Vulcan`

### 02 · Hsiwu — 仿生机器人 — 完成

- 一句话：六段翼、三台电机、零行代码。
- 正文：仿生蝙蝠扑翼机器人，每侧三段、共六段翼面。3 片 NE555、1 片 74HC04 与 3 片 L293D 构成完整的控制逻辑。无 MCU、无固件。
- 技术：SolidWorks · Altium · NE555 · 74HC04 · L293D · FDM
- 证据：8 stars（2026 年 10 月）· MIT · 含 Gerber、BOM 与 STEP
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

- 2018 — 六年级接触 Arduino，把卧室改成电子工作室。
- 2019–2022 — 做了超声波测距仪、写字机器人、RFID 柜锁、室内环境监测仪和树莓派个人网站。
- 2023 — DustArrow：从固体火箭推力采集器，到完整探空火箭、航电、遥测与戈壁试飞。
- 2023 — 第 37 届全国青少年科技创新大赛二等奖。
- 2024 — 第 38 届全国青少年科技创新大赛一等奖（OnesArm）；登上上海电视台《少年爱迪生》。
- 2025–2026 — 进入华中科技大学机器人工程科创实验班；开源 Vulcan 与 Hsiwu；创立 Anteportal Labs，启动 Sencillo。

<!-- 来源：03-timeline.md 一页版；04-awards-and-media.md。 -->

## 奖项与报道

- 2024 — 第 38 届全国青少年科技创新大赛一等奖 — OnesArm
- 2023 — 第 37 届全国青少年科技创新大赛二等奖 — DustArrow X
- 2024 — 上海电视台《少年爱迪生》第八季（2024）— 观看节目：`https://www.kankanews.com/detail/LMwVGm9WB2z`

<!-- 来源：04-awards-and-media.md。不使用奖状照片、节目截图或竞赛 logo。 -->

## 其他项目

- Huginn — 自动化数据统计与分析的 AI agent — Python — `https://github.com/Robusr/Huginn`
- Robusr-skill — 从个人记忆与人格中提炼的数字分身技能 — Agent skills — `https://github.com/Robusr/Robusr-skill`
- Brokkr — 具备实时手部姿态识别与运动控制的灵巧手 — 硬件 / 视觉 — `https://github.com/Robusr/Brokkr`
- Tanngrisnir — 基于 STM32F103C8T6 的两轮自平衡车 — C / 嵌入式 — `https://github.com/Robusr/Tanngrisnir`
- Argo — 定量工程设计方法课程设计 — MATLAB — `https://github.com/Robusr/Argo`
- Lynx — 面向低速自动驾驶的感知融合 SDK — Python — `https://github.com/Robusr/Lynx`

## 关于

我成长在宁夏固原，沙尘暴来的时候，能见度会降到 5 米以下。所以我的第一个严肃项目是一支探空火箭，而不是一个网页：我想测量那片我看不透的大气。DustArrow 从一台推力采集器，长成了拥有 10 个舱段、9 块 PCB 模块和地面站的模块化火箭。问题始终是同一个：上面到底在发生什么？

到了华中科技大学，我开始往上游走。Vulcan 把一句话变成机械工程师可以继续修改的特征树；Sencillo 试着把 PCB 加工中心放到一张桌子上。线索没有变：找到一个我亲眼见过的问题，造出机器，再造就让下一个人做得更快的工具。工具，才是我希望留下的项目。

<!-- 来源：01-identity-and-bio.md 长版；未重复 Hero 句子。 -->

## Footer

- 联系：Robusr@outlook.com · github.com/Robusr · github.com/Anteportal
- 地点：中国，武汉
- 最后更新：2026 年 10 月
- 语言：English · 中文（当前）· Français
- 签名：Why not?
