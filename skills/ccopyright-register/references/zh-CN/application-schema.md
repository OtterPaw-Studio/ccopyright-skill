# 申请事实数据结构（中文）

`facts/application.json` 是可人工编辑的唯一事实源。当前结构版本为 `schema_version: 2`；`init` 和 `status` 会把版本 1 原地补全到版本 2，保留已有事实，不自动确认新增字段，也不另外维护一份“影子事实”。

## `software`

### 门户基础字段

- `full_name`：必填，与申请表完全一致的软件全称。
- `short_name`：可选；没有简称时保留空字符串，不填写“无”。
- `version`：必填，精确保留 `V` 前缀、标点和大小写。
- `category`：`application`、`embedded`、`middleware` 或 `operating-system`。
- `description.type`：`original` 或 `modified`。选择修改软件时，补充 50 字内的 `modification_summary`，并用 `modification_basis` 记录“该软件已登记”或“已取得原权利人授权”等依据状态。
- `development_type`：`independent`、`cooperative`、`commissioned` 或 `assigned-task`。
- `rights_acquisition`：`original` 或 `successor`；后者必须另行确认取得依据。
- `rights_scope`：`all` 或 `partial`；部分权利必须记录范围并准备对应证明。
- `completion_date`：申请人确认的开发完成日期，不能用最后一次 Git 提交日期替代。

### 发表与著作权人

- `publication.status`：`unpublished` 或 `published`。已发表时补充 `date`、`country` 和 `region`。
- `rights_holders`：申请人确认、顺序固定的著作权人名称列表。
- `joint_rights_holders`：是否存在多个著作权人共同享有权利；其值必须与著作权人列表一致。
- 著作权人的证件类型、证件号码、扫描件、签名等个人敏感数据不属于该 JSON，只能在门户中由申请人处理。

### 环境、语言与功能

- `environment` 包含六个独立字段：`development_hardware`、`runtime_hardware`、`development_os`、`development_tools`、`runtime_platform`、`supporting_software`。当前截图中每项可见上限为 50 字。
- `programming_languages`：门户枚举中选择的语言列表；`other_programming_languages` 只记录枚举外语言，当前可见上限为 120 字。
- `purpose`、`industry`：当前可见上限各为 50 字。
- `technical_features`：门户提供的技术特点标签；`other_technical_features` 当前可见上限为 100 字。
- `main_functions`：面向申请表的连续说明文字。当前截图显示计数器 `500~1300`，本地按最少 500、最多 1300 字检查，但最终提交前仍需在当前门户确认。
- `competitive_advantages`、`commercial_value`：内部辅助字段，不是这组截图中可见的门户字段，不应混入复制底稿。

所有描述都必须以仓库事实为依据，并经申请人认可。

## `dates` 与 `snapshot`

以下概念必须分开：

- `software.completion_date`：申请人确认的申请事实。
- `software.publication.date`：适用时的首次发表事实。
- `dates.code_snapshot_date`：所选源码快照对应的日期。
- `dates.material_preparation_date`：材料编制日期。
- `snapshot.commit`：用于追溯的 Git 提交，不是完成时间或权属证明。
- `snapshot.include_uncommitted`：是否有意包含工作区未提交修改。

当 Git 快照模式为 `head`/`commit` 且 `include_uncommitted: false` 时，最终生成会验证每个所选源码都存在于配置的十六进制提交中并与其一致。非 Git 仓库或有意使用未提交内容时，应使用 `working-tree` 模式（或明确包含未提交内容）。

## `requirements`

这是带日期、可配置的规则快照，不是永远不变的门户说明。

- `captured_at`、`source_urls`：规则来源与采集日期；未复核当前门户时保持空值且不得确认 `requirements.current`。
- `portal_evidence`：证据基线标识、接收/采集日期、覆盖范围，以及是否保留原图或个人数据。两项隐私标志必须为 `false`。
- `portal_field_limits`：从门户证据读取到的字段字数上下限。
- `portal_unknowns`：截图没有证明、提交前仍需人工确认的格式、大小、枚举或帮助文本。
- `paper`：普通流程基线通常为 A4。
- `program_lines_per_page`、`document_lines_per_page`：每页编号行目标。
- `front_pages`、`back_pages`：前后选择窗口。
- `allow_short_final_page_for_complete_material`：完整材料最后不足一页时的处理。
- `max_pdf_bytes`：当前上传大小限制；`null` 表示本地不主张具体限制。

最终生成前，必须用当前门户要求更新这些字段，并将 `captured_at` 写成实际复核日期。

## `source`

- `files`：相对仓库根目录、顺序明确的第一方源码路径。
- `suggested_files`：只属于扫描建议；最终模式不会用它替代 `files`。
- `mode`：`auto`、`whole` 或 `front-back`。
- `deposit_type`：本 Skill 仅支持 `general`；`exceptional` 会停止并转入专业流程。
- `program_line_count`：申请表中的源码量。应以所选源码物理行数复核并确认；生成器会把它和实际选择结果比对。
- `program_line_count_basis`：行数口径说明，普通流程建议为 `selected-source-physical-lines`。
- `ordering`：说明如何组成有序源码流。
- `exclude_globs`：预留给申请人记录排除说明；权威选择仍是显式 `files`。

建议采用功能阅读顺序：入口、核心领域逻辑、编排、存储/集成、界面。除非确有必要，不选择依赖、生成代码、测试或夹具；不得选择秘密信息或申请人无权披露的代码。

## `document`

- `kind`：例如 `user-manual` 或 `design-description`。
- `title`：可选的明确标题。
- `deposit_type`：本 Skill 仅支持 `general`；`exceptional` 会停止。
- `max_display_units_per_line`：确定性换行宽度。
- `sections`：有序章节，每项包含 `title`、`paragraphs` 和仓库相对路径 `evidence`。
- `screenshots`：包含 `path`、`page`、`title`、`caption`。
- `additional_documents`：门户“增加其他文档”的准备记录，不替代主要文档鉴别材料。

文案是经确认的输入，不代表可以凭空编写功能。证据缺失只产生 `WARNING`。

## `confirmations`

最终模式要求模板中全部确认键为 `true`，覆盖：

- 软件名称、版本、分类、权利、著作权人、完成日期、开发方式、发表状态；
- 开发/运行环境、用途、行业、技术特点与主要功能；
- 源码选择、源码量和普通交存方式；
- 文档内容与当前规则快照。

“已确认”只表示申请人复核了该值，不代表工具给出了法律结论。条件分支仍会单独检查，例如已发表软件的日期/地点、修改软件说明、继受取得依据、部分权利范围，以及合作/委托/下达任务开发的证明材料。

## `proof_checklist` 与 `review`

这里只记录证明材料是否已准备及非敏感备注。清单会根据开发方式、修改软件、继受取得、部分权利或多著作权人等分支动态增加项目。不得写入证件号码、证件扫描件、签名、账号凭据、门户会话信息或用户截图中的个人数据。
