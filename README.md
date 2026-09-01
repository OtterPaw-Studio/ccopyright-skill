# 软件著作权自助工具集

**先把规则问明白，再把材料做扎实。**

> 把公开却分散、难懂、容易过时的软著登记信息，整理成有来源的回答和可复核的材料准备流程。

[English](README.en.md) · [选择 Skill](#两个-skill怎么选) · [快速安装](#一分钟安装) · [第一次使用](#第一次使用) · [完整流程](#从问题到可提交材料) · [安全边界](#安全与边界)

**普通交存** · **人工提交** · **隐私优先** · **不提供法律结论**

---

## 这个项目解决什么问题

很多软著信息并不神秘，只是散落在法规、办事指南、FAQ 和登录后的登记门户里。这个项目提供两个可以独立安装的 Agent Skill，帮助你先理解，再动手：

| 找得到依据 | 看得懂服务 | 做得出材料 |
|---|---|---|
| 区分法规、办事指南、当前门户和第三方说法 | 拆解服务费买到的工作，不把代理包装成官方必需 | 从代码仓库生成可追溯、可校验、可人工复核的登记材料 |

目标是减少信息差，而不是宣称所有第三方服务都没有价值。材料整理、文案、排版、代录入和人工沟通都可能产生真实成本；你应该先看清官方事项、自己能完成的工作、付费服务的实际交付，以及仍需专业判断的复杂问题，再自主选择。

两个 Skill 都服务于向[中国版权保护中心](https://www.ccopyright.com.cn/)人工办理前的理解与准备阶段。它们不登录账号、不自动填写或提交网页、不跟踪申请，也不解析补正通知。

## 两个 Skill，怎么选

| | **ccopyright-qa** | **ccopyright-register** |
|---|---|---|
| 适合 | 先问规则、字段、材料、自助可行性或服务报价 | 已决定处理代码仓库、生成或校验登记材料 |
| 默认行为 | 只读答疑，说明来源、日期、适用条件和未知项 | 先评估仓库，再在 `.ccopyright/` 内准备材料 |
| 会写文件吗 | 不会 | 只有用户同意后才写入材料工作区 |
| 本地依赖 | 普通使用无需 Python、Chrome 或 Poppler | Python 必需；PDF 流程需要 Chrome 与 Poppler |
| 典型请求 | “软件简称可以不填吗？”“我一定要找代理吗？” | “评估这个仓库”“生成源码、说明书和 PDF” |

最短选择方式：

- **只想把问题问明白**：使用 **ccopyright-qa**。
- **已经要处理代码仓库**：使用 **ccopyright-register**。
- **还不确定从哪里开始**：两个一起安装，先问 QA。

```text
提出问题 → ccopyright-qa → 自助或付费决策 → ccopyright-register → 人工复核 → 当前门户提交
```

## 一分钟安装

### 推荐：一次安装两个 Skill

```bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
```

### 只安装一个

答疑：

```bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-qa
```

材料准备：

```bash
npx skills add OtterPaw-Studio/ccopyright-skill --skill ccopyright-register
```

### 全局安装到 Codex

```bash
npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register \
  --agent codex \
  --global
```

已经克隆本仓库时，可以从当前目录安装：

```bash
npx skills add . --skill ccopyright-qa ccopyright-register
```

**skills** CLI 可以直接通过 **npx** 运行，无需预先全局安装。安装、更新、卸载和匿名遥测说明见 [skills.sh CLI 文档](https://www.skills.sh/docs/cli)。如需关闭某次安装的遥测：

```bash
DISABLE_TELEMETRY=1 npx skills add OtterPaw-Studio/ccopyright-skill \
  --skill ccopyright-qa ccopyright-register
```

## 第一次使用

复制一段最符合当前需求的提示词即可。

### 先问需要什么

```text
使用 $ccopyright-qa 告诉我申请普通软件著作权通常需要哪些材料。
请区分官方法规基线、当前门户仍需核对的事项，以及我可以自行完成的工作。
```

### 先评估仓库，不生成材料

```text
使用 $ccopyright-register 评估这个仓库是否适合准备普通软著登记。
先不要生成材料，请列出建议的软件身份、源码边界、缺失事实和全部警告。
```

### 直接开始草稿

```text
使用 $ccopyright-register 为这个仓库准备软著登记材料。
先说明写入范围，再创建 .ccopyright 工作区并生成草稿；
只询问代码无法安全确定的事实。
```

### 拆解一份服务报价

```text
使用 $ccopyright-qa 拆解下面这份已经删除身份、订单和支付信息的服务报价。
告诉我每项交付物、我仍需完成的工作，以及需要向服务商问清楚的问题。
```

面向登记提交的填写底稿和鉴别材料默认使用中文。

## 前置依赖

| 依赖 | **ccopyright-qa** | **ccopyright-register** |
|---|:---:|:---:|
| 支持 Agent Skills 的 AI Agent | 必须 | 必须 |
| 带 **npx** 的 Node.js | 仅安装时 | 仅安装时 |
| 访问当前官方页面 | 涉及时效问题时 | 确认当前门户要求时 |
| Python 3.10+，命令名为 **python** | 不需要 | 必须 |
| Chrome 或 Chromium | 不需要 | 生成 PDF 时 |
| Poppler | 不需要 | 校验 PDF、生成接触表时 |
| Git | 不需要 | 推荐但非必须 |

答疑 Skill 不要求代码仓库、门户账号或本地生成工具。材料准备 Skill 缺少 PDF 工具时，仍能扫描仓库并生成事实底稿、Markdown 和 HTML。

可以让 **ccopyright-register** 执行环境预检，也可以在它的安装目录运行：

```bash
python scripts/ccopyright.py preflight
```

本地生成器不额外需要 LLM API Key、门户密码、身份证明或签名证书。

---

## 从问题到可提交材料

| 阶段 | 使用者要做什么 | Skill 会做什么 | 结果 |
|---|---|---|---|
| 1. 理解 | 提出规则、材料或服务问题 | **ccopyright-qa** 区分来源、日期、条件和未知项 | 能判断下一步是否自助 |
| 2. 评估 | 指定要处理的代码仓库 | **ccopyright-register** 只读盘点源码、Git、文档、许可证和敏感模式 | 候选登记边界与预检报告 |
| 3. 确认 | 补充代码无法证明的申请事实 | 用 schema v3 的 `facts/application.json` 维护唯一事实 | 可追溯的申请底稿 |
| 4. 生成 | 确认源码顺序和文档内容 | 生成填写底稿、程序与文档鉴别材料、证明清单和追溯记录 | 草稿材料与内部复核文件 |
| 5. 校验 | 处理必填事实和当前门户约束 | 渲染 A4 PDF，检查分页、哈希、字段约束和待确认项 | 技术校验结果与逐页接触表 |
| 6. 复核 | 逐页检查并明确确认 | 创建不覆盖旧内容的时间戳修订 | `ready-to-submit` 人工复核版本 |

### 回答依据如何区分

**ccopyright-qa** 会把依据分成四类：

1. 官方法律、条例或规章；
2. 中国版权保护中心的具体办事指南或 FAQ，并标明访问日期；
3. 本次申请中明确核对的当前门户脱敏文字；
4. 只能证明第三方自身说法的材料，或明确标注的推断与实践建议。

涉及当前费用、入口、字段、上传限制、办理时限和服务商价格时，不能凭记忆回答。无法取得支持结论的当前来源时，Skill 会明确标记为未核验。

材料 Skill 内置的字段、条件分支和字数门禁是可更新的门户兼容性配置，不是答疑证据，也不是永久不变的官方规则。

### 仓库预检如何理解

仓库、权属和知识产权预检只输出 **INFO** 与 **WARNING**，用于提示人工复核，不作法律结论，也不会单独阻断材料生成。Git 和配置文件只能产生未确认建议，不能证明著作权人、开发完成日期、发表事实或源码披露权限。

## 会生成什么

**ccopyright-register** 默认在目标软件仓库中创建：

```text
.ccopyright/
├── facts/                 唯一申请事实和规则快照
├── reports/               仓库清单、预检、证据、构建和渲染报告
├── drafts/                可复制填写底稿与人工清单
├── work/                  Markdown、HTML、PDF、图片和追溯清单
├── qa/                    校验报告、逐页图片与接触表
└── ready-to-submit/       不覆盖旧内容的时间戳复核版本
```

主要产物包括：

- 按当前门户顺序组织的申请表填写底稿；
- 保留原始空行、注释、制表符和顺序的程序鉴别材料；
- 基于真实文档、仓库证据和产品截图的文档鉴别材料；
- 合作、委托、下达任务、修改、继受取得等条件证明准备清单；
- 源码追溯清单、证据映射、哈希和人工检查表；
- 本地工具可用时的 A4 PDF、逐页图片和接触表。

通常的上传候选是程序/文档鉴别材料 PDF，以及当前门户要求的表单或证明文件。追溯清单、证据映射、哈希和接触表默认只用于内部复核。

完整指南：[材料准备](skills/ccopyright-register/README.md) · [答疑](skills/ccopyright-qa/README.md)

## 如何理解第三方服务

项目不会脱离服务范围和证据，直接给某个价格贴上“合理”“不合理”或“骗局”标签。答疑 Skill 会拆分：

- 法规或当前门户要求申请人完成的事项；
- 申请人可以自行完成的事实核对、材料整理和门户操作；
- 服务商提供的文案、排版、材料制作、代录入、沟通或提醒；
- “加急”“包过”“不成功退款”等承诺的起算点、范围和条件；
- 权属争议、复杂合同、例外交存或涉密等确实需要专业判断的情形。

用户看到的报价可以作为待分析个案，但不会被写成当前市场价。服务商网页也只能证明该服务商在访问日期展示了某项内容，不能证明官方必要性或行业通行价格。

---

## 安全与边界

两个 Skill 都不会：

- 自动填写或提交浏览器表单；
- 登录、签字、缴费或操作申请人账号；
- 跟踪申请或解析补正通知；
- 判断权属、合同效力或保证登记通过；
- 保存证件号码、证件扫描件、签名、账号凭据、支付信息或会话数据；
- 自动处理例外交存、封存、涉密或军用流程。

**ccopyright-qa** 默认只读，不扫描仓库、不生成文件；**ccopyright-register** 只在说明写入范围后使用 `.ccopyright/` 工作区，不静默修改业务源码。所有回答和产物属于信息与材料准备辅助，不构成法律意见。

## 管理已安装的 Skill

```bash
# 查看
npx skills list
npx skills list --global

# 更新
npx skills update ccopyright-qa ccopyright-register

# 卸载
npx skills remove ccopyright-qa ccopyright-register
```

## 常见问题

### 我应该先安装哪个 Skill？

只想了解规则或判断是否需要服务，安装 **ccopyright-qa**；已经要处理代码仓库，安装 **ccopyright-register**；不确定时两个一起安装。

### 答疑结果一定是最新的吗？

不一定。法规可能修订，办事页面和登录后的门户也会变化。涉及当前费用、表单、入口、时限或上传限制时，需要重新核对具体官方页面和本次门户；内置校验配置不能替代这一步。

### 答疑 Skill 会判断某个服务费值不值吗？

不会替你做价值选择。它会说明这笔费用对应哪些工作、哪些事项你仍需完成、哪些承诺需要问清楚，以及哪些项目并非官方要求。

### 没有 Chrome 或 Poppler 能生成材料吗？

可以生成仓库评估、事实底稿、追溯清单、Markdown 和 HTML；PDF 渲染与技术校验需要相应工具。

### 每个 WARNING 都必须消除吗？

不需要，但要区分来源：

- 仓库、权属和知识产权**预检警告**只用于复核，不阻断生成；
- 门户字数冲突、条件字段缺失和活动分支的证明准备状态未解决时，会在草稿中显示为 **WARNING**，并阻断最终生成；
- 例外交存、必填事实缺失或未确认、PDF 校验失败等也会阻断相应的最终阶段。

## 官方参考

- [QA 官方页面来源目录](skills/ccopyright-qa/references/zh-CN/official-sources.md)
- [中国版权保护中心软件登记指南](https://www.ccopyright.com.cn/index.php?optionid=1030)
- [《计算机软件著作权登记办法》](https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html)
- [《计算机软件保护条例》现行整合文本](https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581)
- [skills.sh 文档](https://www.skills.sh/docs)

维护者与贡献者命令见 [AGENTS.md](AGENTS.md)。
