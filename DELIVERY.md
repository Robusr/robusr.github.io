# 交付报告

> 2026-10-21 更新：仓库配置已切换到 https://robusr.cn，canonical、hreflang、Open Graph、JSON-LD、sitemap 与 robots 均已更新，部署后生效；GitHub Actions 部署工作流已移除；GitHub Pages 站点设置仍需在仓库后台关闭。以下为 2026-10-20 的原始交付记录。

日期：2026-10-20
工作分支：`feat/homepage`
状态：站点可构建、可本地预览；未推送、未合并、未部署。

## 1. 完成内容

- 依据信息库 01–07、`sources.md` 与 `data/*.json`，完成事实审计、三语文案、结构化数据、设计与实现。
- 生成三个静态页面：英文 `/`（默认）、中文 `/zh/`、法文 `/fr/`，以及 `404.html`。
- 设计为单列编辑式布局，最大宽度 880 px，强调色只有一个深青 `#0f6b5f`；无卡片阴影、无渐变、无装饰插画。
- 页面结构固定为 8 个区块：Header、Hero、Selected Work、Journey、Awards & Media、More Work、About、Footer / Contact。
- 5 个主项目严格按 Vulcan → Hsiwu → DustArrow X → OnesArm → Sencillo 排列；Journey 6 行、Awards 3 条、More Work 6 条。
- 所有文案由 `src/data/*.json` 驱动，模板中没有硬编码项目文案。
- 技术栈：Astro 7 静态输出、零前端框架；自托管 Inter 可变字体；少量原生 JS 只负责滚动边线、语言切换保留锚点、语言提示条。

## 2. 设计与实现要点

- 英文为唯一事实源，中文与法文逐节对应；法文使用不换行空格、弯撇号与法式小数逗号。
- 首屏肖像使用 512 px（4:5 竖版）裁切，桌面 260 px、移动不超过 200 px；不加边框、阴影或滤镜；背景以暖白纸感渐变铺底，页边叠加极淡的制图点阵，并使用两幅手绘个人 IP 线稿（右下角拼贴形象、左下角全身站姿）作为低透明度装饰。
- 项目缩略图统一 16:9，输出 480/960 两档 WebP，并提供 JPEG 回退与 `width`/`height`。
- 首屏肖像预加载；项目图懒加载；背景插画按视口加载（移动 46 KB、1200–1439 px 154 KB、1440 px 以上 213 KB），首屏资源本地实测约 146 KiB（移动）/ 269 KiB（笔记本）/ 329 KiB（桌面）。
- 深色模式未实现（brief 中为可选项）；未加入任何统计、追踪、Cookie 弹窗或第三方字体 CDN。
- 站点根目录直接作为 Astro 应用，而不是 brief 示例中的 `site/` 子目录：本仓库是 GitHub Pages 用户站点，根目录构建可保持 `base: /`，`dist/` 可直接发布。

## 3. 事实来源与快照

- 身份、学校、家乡、方向、团队定位：`01-identity-and-bio.md`、`data/profile.json`。
- 项目事实、技术栈、证据点：`02-project-cards.md`、`data/projects.json`、各项目 README。
- 时间线与奖项：`03-timeline.md`、`04-awards-and-media.md`、`sources.md`。
- 图片与 alt：`07-asset-manifest.md`；原图保留在信息库，站点只使用转换后的副本。
- 星标数字为 2026-10-20 快照：Vulcan 23、Hsiwu 8；页面显示 `Oct 2026` / `2026 年 10 月` / `oct. 2026`。
- Sencillo 的所有性能数字都标注为“设计目标，非实测”，并保留“原型前阶段”状态。

## 4. 三语一致性

- 每页 6 个 section、5 个项目、6 行 Journey、3 条 Awards、6 条 More Work，顺序与链接完全一致。
- 关键数字在三语中全部出现且一致：23、8、40、10、9、32、24、450、5052、0.8、30、8/8、2²、3!。
- 三语图片路径、srcset、项目链接一致；`aria-current` 正确标记当前语言。
- 每页有独立 canonical 与 4 条 hreflang（en / zh-Hans / fr / x-default）。
- 语言切换保留锚点，例如 `/zh/#about` → `/#about` 或 `/fr/#about`。
- 详细机器检查见 `qa/consistency.json`。

## 5. 验证结果

| 语言 | Performance | Accessibility | Best Practices | SEO | LCP | CLS | 传输 |
|---|---|---|---|---|---|---|---|
| EN | 100 | 100 | 100 | 100 | 1.6 s | 0.001 | 179 KiB |
| ZH | 100 | 100 | 100 | 100 | 1.7 s | 0 | 197 KiB |
| FR | 100 | 100 | 100 | 100 | 1.4 s | 0.001 | 179 KiB |

- 1440 / 1024 / 768 / 390 px 均无横向溢出、无文字截断、无控制台错误。
- 200% 缩放代理（720 px 视口）无横向溢出。
- 关闭 JavaScript 后正文完整可读。
- 键盘走查：Skip to content 为第一个焦点；品牌、导航、语言切换、Hero 链接均有可见焦点环。
- 所有站外链接在 2026-10-20 返回 200；`robusr.cn` 无 DNS 响应，未使用。
- 移动端独立链接与按钮均达到 44 × 44 px；Awards 段落中的行内媒体链接属于 WCAG 2.5.8 行内豁免。
- 完整记录见 `QA.md`，截图见 `screenshots/`。

## 6. 内容缺口与冲突摘要

- `robusr.cn` 未验证，当前 canonical、hreflang、sitemap、JSON-LD 全部使用 `https://robusr.github.io`。
- 第 37 届全国青少年科技创新大赛二等奖的证据等级为中等：DustArrow README 确认参赛与电视报道，但未写奖项等级。
- Hsiwu 的“六段翼、三台电机”与资料库中“六段独立驱动”存在措辞冲突；页面采用与电机数量一致的说法，未写“六台独立驱动”。
- 中文与法文文案需要母语技术审校；More Work 的中法文描述由英文仓库简介翻译而来。
- 其余缺口见 `CONTENT_GAPS.md`，冲突与处理见 `CONTENT_CONFLICTS.md`。

## 7. 部署与待确认

当前未推送、未合并、未部署，符合 brief 的停止条件。

建议步骤：

1. 审阅 `screenshots/`、`QA.md`、`CONTENT_GAPS.md` 与三语文案。
2. `git push -u origin feat/homepage`，创建 PR。
3. 合并到 `main` 后，在仓库 Settings → Pages 选择 **GitHub Actions** 作为来源。
4. `.github/workflows/deploy.yml` 会自动构建并发布到 `https://robusr.github.io/`。
5. 如确认 `robusr.cn` 可用，再添加 `public/CNAME` 与 DNS 记录；具体步骤见 `DEPLOY.md`。DNS、HTTPS 与正式发布均未执行。

待确认事项：

- 是否发布到 `main` 并启用 Pages。
- 是否绑定 `robusr.cn`。
- 是否同步 `Robusr/Robusr` 的 Profile README（本仓库未修改）。
- 中文、法文是否交母语审校。
- 第 37 届二等奖是否需要更严格的证据表述。

## 8. 交付物

- 站点源码：`src/`、`public/`、`astro.config.mjs`、`package.json`、`tsconfig.json`
- 构建产物：`dist/`（本地生成，已在 `.gitignore` 中排除，由 CI 重建）
- 文案：`content/copy-en.md`、`copy-zh.md`、`copy-fr.md`、`glossary.md`
- 审计：`content-inventory.md`、`CONTENT_GAPS.md`、`CONTENT_CONFLICTS.md`
- 验证：`QA.md`、`qa/`、`screenshots/`
- 部署：`DEPLOY.md`、`.github/workflows/deploy.yml`
- 本报告：`DELIVERY.md`
