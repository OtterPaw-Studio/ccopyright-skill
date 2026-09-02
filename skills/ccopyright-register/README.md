<div align="center">

# ccopyright-register

> **从软件代码仓库出发，准备一套可复核的普通计算机软件著作权登记材料。**

**仓库评估** · **事实确认** · **材料生成** · **PDF 校验** · **人工复核**

[English](README.en.md) · [适合什么目标](#适合什么目标) · [开始使用](#开始使用) · [产物目录](#产物目录) · [安全与限制](#安全与限制)

</div>

---

`ccopyright-register` 会分析软件仓库、整理申请人确认的登记事实，并准备申请表底稿及程序/文档鉴别材料。你可以直接在 AI 编程 Agent 中提出需求。

它服务于向[中国版权保护中心](https://www.ccopyright.com.cn/)人工提交之前的材料准备阶段，不填写或提交门户、不操作申请人账号、不跟踪申请，也不解析补正通知。

本仓库还提供只读的 `ccopyright-qa`。如果你还在了解规则、判断是否需要代理或
拆解服务报价，可以先安装答疑 Skill；本指南只介绍材料准备 Skill。

## 适合什么目标

| 你的目标 | Skill 会做什么 |
|---|---|
| “先看看这个仓库能不能做” | 只读盘点源码、文档、Git、许可证和敏感模式，给出候选边界及 **INFO/WARNING** |
| “开始准备一份草稿” | 说明写入范围后创建 `.ccopyright/`，整理事实并生成底稿与鉴别材料 |
| “检查材料能不能交” | 渲染 A4 PDF，检查分页、哈希、字段约束和待确认项，生成逐页接触表 |
| “保留一份人工复核版本” | 经明确确认后发布不覆盖旧内容的时间戳 `ready-to-submit` 版本 |

如果目标是规则答疑、是否需要代理或拆解服务报价，请使用 `ccopyright-qa`。如果目标是登录门户、自动提交、缴费、跟踪申请或解析补正通知，本 Skill 不支持。

## 安装

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-register
~~~

同时安装答疑和材料准备：

~~~bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
~~~

## 开始使用

用 Agent 打开要登记的软件仓库，先做评估：

~~~text
使用 $ccopyright-register 评估这个仓库是否适合准备普通软著登记。
先不要生成材料，请列出候选源码边界、缺失的申请事实和全部警告。
~~~

或者直接开始完整流程：

~~~text
使用 $ccopyright-register 为这个仓库准备软著登记草稿。
创建 .ccopyright 工作区，不修改业务源码，只询问仓库无法安全确定的事实。
~~~

最终阶段可以这样要求：

~~~text
使用 $ccopyright-register 执行最终生成，渲染并校验两份 PDF，生成逐页接触表，
然后列出人工复核清单。在我明确确认之前，不要发布 ready 版本。
~~~

面向登记提交的填写底稿和鉴别材料默认使用中文。

## 前置依赖

| 依赖 | 用途 | 是否必须 |
|---|---|---|
| Python 3.10+，命令名为 **python** | 扫描、事实、底稿、Markdown/HTML 和清单 | 必须 |
| Chrome 或 Chromium | 渲染鉴别材料 PDF | 渲染时需要 |
| Poppler 的 **pdfinfo** 与 **pdftotext** | PDF 技术校验 | 校验时需要 |
| Poppler 的 **pdftoppm** | 逐页图片与接触表 | 可选 |
| Git | 快照来源和未提交修改检查 | 推荐 |

检查本机环境：

~~~bash
python scripts/ccopyright.py preflight
~~~

本地生成器不要求 API Key、门户账号、身份证明或签名证书。

## 需要你确认的信息

仓库元数据只能作为建议。以下内容必须由你确认：

- 软件全称、可选简称和精确版本；
- 著作权人及顺序；
- 开发完成与发表事实；
- 软件分类、原创/修改、开发方式、权利取得与范围；
- 源码披露权限与源程序量；
- 程序和文档均采用普通交存；
- 文档内容与真实产品截图；
- 本次申请实际看到的当前门户要求。

证件号码、证件扫描件、签名、账号凭据、Cookie 和未脱敏门户截图必须保留在准备工作区之外。

## 使用流程

1. **评估** — 只读盘点仓库，并输出 **INFO**/**WARNING** 预检。
2. **初始化** — 创建 **.ccopyright/** 和 schema v3 唯一事实文件；旧工作区会保留事实并自动迁移。
3. **草稿** — 生成填写底稿、条件证明清单、源码/文档材料和追溯记录。
4. **确认** — 补全事实、当前门户规则、源码顺序并处理文档证据警告。
5. **渲染与校验** — 生成 A4 PDF，检查尺寸、行身份、规范字段、哈希和待确认标记。
6. **复核与发布** — 逐页检查接触表，再明确发布一个不覆盖旧内容的新版本。

仓库、权属和知识产权预检中的 **WARNING** 只用于复核，不会阻断生成。门户字数冲突、条件字段缺失和活动分支的证明准备状态未解决时，会在草稿中显示为 **WARNING**，并阻断最终生成；必填事实缺失、选择例外交存或 PDF 校验失败也会阻断相应阶段。

## 产物目录

~~~text
.ccopyright/
├── facts/                 唯一申请事实和规则快照
├── reports/               仓库清单、预检、证据、构建和渲染报告
├── drafts/                填写底稿与人工/证明清单
├── work/                  Markdown、HTML、PDF、截图和追溯清单
├── qa/                    校验报告、逐页图片和接触表
└── ready-to-submit/       带时间戳的人工复核版本
~~~

### 申请表填写底稿

按门户顺序组织中文填写值、字符数、确认状态和条件分支。内置门户校验配置会在
草稿中把字数冲突、未满足的条件字段和证明准备状态列为警告，并在最终模式执行门禁；它不是
官方依据，当前门户始终优先。

### 程序鉴别材料

由显式选择的第一方文件组成有序源码流，保留原始内容、空行、注释和制表符。每个打印行都能映射回原路径、原行号、源码流位置和哈希。

### 文档鉴别材料

基于申请人确认的文档与真实产品截图，重要描述尽量连接仓库证据。证据缺失只产生警告，不会虚构功能。

### 证明材料清单

根据合作开发、委托开发、下达任务、修改软件、继受取得、部分权利等分支列出仓库外的准备事项，不复制证明文件。状态只能是 `not-recorded`、`ready` 或 `not-required`；活动分支必须达到该分支允许的就绪状态才能最终生成。

## 可选：直接运行命令

通常由 Agent 代为执行：

~~~bash
python scripts/ccopyright.py init --repo /仓库/路径 --workspace /仓库/路径/.ccopyright
python scripts/ccopyright.py status --workspace /仓库/路径/.ccopyright
python scripts/ccopyright.py build --repo /仓库/路径 --workspace /仓库/路径/.ccopyright
python scripts/ccopyright.py build --repo /仓库/路径 --workspace /仓库/路径/.ccopyright --final --render
python scripts/ccopyright.py validate --workspace /仓库/路径/.ccopyright
python scripts/ccopyright.py publish --workspace /仓库/路径/.ccopyright --human-reviewed
~~~

完整命令见 [references/zh-CN/workflow.md](references/zh-CN/workflow.md)。官方直达页、
门户校验配置和事实结构分别见
[references/zh-CN/official-sources.md](references/zh-CN/official-sources.md)、
[references/zh-CN/portal-form.md](references/zh-CN/portal-form.md) 与
[references/zh-CN/application-schema.md](references/zh-CN/application-schema.md)。

## 安全与限制

- 只支持普通、非涉密交存；选择例外交存时停止。
- 不自动填写网页、提交、实名认证、签字、缴费、跟踪进度或解析补正通知。
- 不提供法律意见，不判断权属，也不保证登记通过。
- 不自动推断著作权人、完成日期、发表事实或源码披露权限。
- 不在工作区保存证件号码/扫描件、签名、账号凭据、会话数据或用户提供的门户截图。
- 仓库/知识产权预检严格只有 **INFO** 与 **WARNING** 两级。

正式提交前，必须复核当前门户要求并逐页检查渲染材料。
