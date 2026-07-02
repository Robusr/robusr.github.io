# Robusr's Utopia

[ [English](./README.md) ]

一个模拟 macOS 终端交互的个人主页。访客可以输入命令或直接用自然语言
提问，了解我的个人信息、浏览 GitHub 项目、查看实时统计数据 --
一切都在一个毛玻璃终端窗口中完成。

![终端截屏](./assets/img/example.png)

## 功能特性

- **macOS 风格终端窗口** -- 红黄绿交通灯标题栏、圆角、毛玻璃背景模糊
  效果（backdrop-filter），覆盖全屏背景图
- **Oh My Zsh 风格提示符**（`$ ~`），支持上下箭头浏览历史命令
- **打字机效果输出** -- 回复内容逐字打印，模拟真实终端体验
- **ASCII 像素风 Logo** -- 斜体 "Robusr" 文字，逐字母彩虹配色
  （通过 Pillow 离线生成）
- **中英双语 i18n** -- 默认英文，输入 `lang` 命令可切换为中文
- **实时 GitHub 集成** -- 页面加载时自动获取公开仓库列表和个人资料统计
- **自然语言匹配** -- 可用中英文直接提问，如 "你是谁？"、"你会什么？"、
  "看看你的项目"
- **响应式布局** -- 移动端自适应，字体和边距自动缩小
- **纯静态站点** -- 无框架、无打包工具、无运行时外部依赖

## 可用命令

| 命令 | 别名 | 说明 |
|---|---|---|
| `help` | `h`, `?` | 显示完整命令列表 |
| `about` | `whoami` | 显示个人简介 |
| `skills` | `skill` | 列出技能 |
| `contact` | -- | 显示联系方式 |
| `projects` | `project`, `portfolio` | 列出 GitHub 公开仓库（实时） |
| `stats` | `status` | 显示 GitHub 个人资料概览（实时） |
| `lang` | `zh`, `en` | 切换中 / 英文 |
| `clear` | `cls` | 清屏 |

也可以直接自然语言提问，例如 "你会什么？"、"你是谁？"、
"怎么联系你？"。

## 项目结构

```
.
├── index.html              # HTML 骨架（38 行）
├── css/
│   └── style.css           # 全部样式（221 行）
├── js/
│   └── main.js             # 终端引擎、i18n、命令逻辑（677 行）
├── assets/
│   └── img/
│       ├── Street.jpg      # 全屏背景图
│       ├── Robusr.jpeg     # 网站图标
│       └── example.png     # README 截屏
├── scripts/
│   └── ascii_gen.py        # ASCII Logo 离线生成工具（Pillow）
├── .gitignore
├── README.md
└── README.zh-CN.md
```

## 自定义配置

### 个人信息

编辑 [js/main.js](js/main.js) 顶部的 `personalInfo` 对象：

```javascript
const personalInfo = {
  name:    'YourName',
  tagline: { en: "...", zh: "..." },
  bio:     { en: "...", zh: "..." },
  skills:  { en: [...], zh: [...] },
  contact: { email: '...', github: '...', wechat: '...' },
};
```

### ASCII Logo

Logo 像素图已预计算并存储为 `LOGO_UP` 常量。
如需修改文字后重新生成，运行：

```bash
python3 scripts/ascii_gen.py "你的名字"
```

然后将打印的 `LOGO_UP` / `LOGO_UP_SPLITS` / `LOGO_COLORS`
代码块复制到 [js/main.js](js/main.js) 中。

依赖：Python 3 + [Pillow](https://python-pillow.org/)
（`pip install Pillow`）。

### 背景图

将 `assets/img/Street.jpg` 替换为你自己的图片。
如更改文件名，需同步更新 [css/style.css](css/style.css) 中
`.bg` 规则的 URL。

## 部署

本项目专为 **GitHub Pages** 设计。将仓库推送到
`<username>.github.io`，在仓库设置中启用 Pages
（根目录、main 分支）即可，无需构建步骤。

其他静态托管平台（Netlify、Vercel、Cloudflare Pages）
只需将部署目录指向仓库根目录。

## 技术栈

| 层级 | 技术 |
|---|---|
| 标记 | HTML5 |
| 样式 | CSS3（Flexbox、backdrop-filter、自定义滚动条） |
| 逻辑 | 原生 JavaScript（ES2020+） |
| 字体 | Fira Code / Menlo / Consolas / SF Mono（系统字体栈） |
| API | GitHub REST API（未认证，仅公开数据） |
| Logo 生成 | Python 3 + Pillow（离线） |

## 许可证

本项目仅供个人使用。欢迎自行修改用于你的个人主页。
