<div align="center">

# ccopyright-register

> **从软件代码仓库出发，准备一套可复核的普通计算机软件著作权登记材料。**

**仓库评估** · **事实确认** · **材料生成** · **PDF 校验** · **人工复核**

[English](README.en.md) · [什么时候用它](#什么时候用它) · [开始使用](#开始使用) · [产物目录](#产物目录) · [安全与限制](#安全与限制)

</div>

---

`ccopyright-register` 用来把一个真实的软件仓库整理成软著登记材料。它会先看源码、文档和仓库状态，再把你确认过的申请信息写入底稿，生成程序和文档鉴别材料。

它只负责向[中国版权保护中心](https://www.ccopyright.com.cn/)提交前的准备工作：不填写或提交门户，不操作申请人账号，也不跟踪申请或解析补正通知。

本仓库还提供只读的 `ccopyright-qa`。如果你还在了解规则、判断是否需要代理或
拆解服务报价，可以先安装答疑 Skill；本指南只介绍材料准备 Skill。

## 什么时候用它

| 你想做什么 | 它会怎么处理 |
|---|---|
| “先看看这个仓库能不能做” | 只读检查源码、文档、Git、许可证和敏感模式，列出候选边界及 **INFO/WARNING** |
| “先做一份草稿” | 说明写入位置后创建 `.ccopyright/`，整理事实并生成底稿和鉴别材料 |
| “看看材料还差什么” | 渲染 A4 PDF，检查分页、哈希、字段限制和待确认项，再生成逐页接触表 |
| “留一份已经人工复核的版本” | 得到明确确认后，发布带时间戳的 `ready-to-submit` 版本，不覆盖旧稿 |

规则、代理和服务报价方面的问题交给 `ccopyright-qa`。登录门户、自动提交、缴费、跟踪申请和解析补正通知不在这个 Skill 的范围内。

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

用 Agent 打开准备登记的软件仓库，可以先只做评估：

~~~text
使用 $ccopyright-register 评估这个仓库是否适合准备普通软著登记。
先不要生成材料，请列出候选源码边界、缺失的申请事实和全部警告。
~~~

已经确定要自己准备，也可以直接从草稿开始：

~~~text
使用 $ccopyright-register 为这个仓库准备软著登记草稿。
创建 .ccopyright 工作区，不修改业务源码，只询问仓库无法安全确定的事实。
~~~

草稿确认完以后，再进入最终生成：

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

仓库里能找到的信息只能作为线索。下面这些内容必须由申请人自己确认：

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

1. **评估**：只读盘点仓库，给出 **INFO**/**WARNING** 预检。
2. **初始化**：创建 **.ccopyright/** 和唯一事实文件；已有工作区会保留原来的事实并完成迁移。
3. **草稿**：生成填写底稿、条件证明清单、源码/文档材料和追溯记录。
4. **确认**：补全申请事实，核对当前门户要求、源码顺序和文档证据。
5. **渲染与校验**：生成 A4 PDF，检查尺寸、源码行映射、字段、哈希和待确认标记。
6. **复核与发布**：逐页看完接触表，再明确发布一个不覆盖旧内容的新版本。

仓库、权属和知识产权预检里的 **WARNING** 是提醒，不会单独挡住草稿生成。真正会挡住最终生成的，是没有解决的门户字段限制、条件证明、必填事实、例外交存选择或 PDF 校验失败。

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

按门户顺序整理中文填写内容，同时记录字符数、确认状态和条件分支。内置配置会在草稿里提示字数冲突、缺少的条件字段和证明准备状态，并在最终生成时拦住未解决的问题。这个配置只是兼容性检查，当前门户始终优先。

### 程序鉴别材料

只使用明确选中的第一方源码，并保留原始内容、空行、注释和制表符。材料中的每一行都能查回原文件、原行号、源码流位置和哈希。

### 文档鉴别材料

只使用申请人确认的文档和真实产品截图，重要描述尽量对应到仓库证据。找不到证据时会给出警告，不会替产品编功能。

### 证明材料清单

根据合作开发、委托开发、下达任务、修改软件、继受取得、部分权利等情况，列出需要在仓库外准备的证明，但不会把证明文件复制进来。状态只有 `not-recorded`、`ready` 和 `not-required`；当前申请涉及的分支必须达到允许的就绪状态，才能最终生成。

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
- 仓库和知识产权预检结果只使用 **INFO** 与 **WARNING** 两级。

最后仍要以当前门户为准，并由申请人逐页检查渲染后的材料。
