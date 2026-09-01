# 流程与命令（中文）

仓库与材料工作目录不在同一位置时，统一使用绝对路径。以下示例假设命令从已安装 Skill 的目录运行。

## 1. 检查本机能力

```bash
python scripts/ccopyright.py preflight
```

只安装 Python 就能扫描仓库和生成 HTML。渲染 PDF 需要 Chrome/Chromium；技术校验需要 `pdfinfo` 和 `pdftotext`；`pdftoppm` 用于生成逐页复核图片。

## 2. 只评估，不初始化

```bash
python scripts/ccopyright.py scan \
  --repo /仓库/绝对路径 \
  --output /输出/绝对路径/repository-review.json
```

命令会写出 JSON 和同名 Markdown 报告。发现项只有 `INFO` 和 `WARNING`。扫描器不判断权属，也不修改仓库内容。

## 3. 初始化材料工作目录

```bash
python scripts/ccopyright.py init \
  --repo /仓库/绝对路径 \
  --workspace /仓库/绝对路径/.ccopyright
```

申请人编辑过 `facts/application.json` 后，不要随意使用 `--force`。不带 `--force` 再次运行时，会刷新仓库清单并保留申请事实。

`init` 会创建 schema v2 事实模板和隐私安全的 `facts/requirements-snapshot.md`。已有 schema v1 工作区会原地迁移：保留现有事实，补充新增字段，并将新增确认项保持为 `false`。

## 4. 补全唯一事实源

编辑 `.ccopyright/facts/application.json`，再检查完整性：

```bash
python scripts/ccopyright.py status \
  --workspace /仓库/绝对路径/.ccopyright
```

推测值不能自动确认。先按 [门户表单证据基线](portal-form.md) 逐项检查：名称/版本、分类、原创或修改、开发方式、权利取得和范围、著作权人、完成与发表事实、六项环境、语言、用途、行业、主要功能、技术特点、源码量和交存方式。最终模式还要求有序源码文件、文档章节和全部必要确认。

`status` 会列出普通缺失项、条件分支缺失项和门户字段约束问题。条件分支包括已发表、修改软件、继受取得、部分权利，以及合作/委托/下达任务开发。著作权人的证件号码、证件扫描件和签名不进入工作区。

## 5. 生成草稿

```bash
python scripts/ccopyright.py build \
  --repo /仓库/绝对路径 \
  --workspace /仓库/绝对路径/.ccopyright
```

草稿可以带待确认标记，并会显示门户字段长度或分支问题；这些问题必须在最终模式前解决。进入最终模式前至少复核：

- `drafts/form-worksheet.md`
- `drafts/proof-checklist.md`
- `reports/precheck.md`
- `reports/evidence-map.md`
- `work/program-manifest.json`
- `work/document-manifest.json`
- `work/` 下生成的 Markdown 与 HTML

## 6. 最终生成与渲染

```bash
python scripts/ccopyright.py build \
  --repo /仓库/绝对路径 \
  --workspace /仓库/绝对路径/.ccopyright \
  --final \
  --render
```

无法自动发现 Chrome 时增加 `--chrome /Chrome/绝对路径`。也可以单独重复渲染：

```bash
python scripts/ccopyright.py render \
  --workspace /仓库/绝对路径/.ccopyright \
  --chrome /Chrome/绝对路径
```

`reports/render-report.json` 会记录渲染器身份和 PDF 哈希。

选择程序或文档“例外交存”时，本 Skill 会停止；它只生成普通交存材料。合作开发、委托开发、下达任务开发、修改软件、继受取得和部分权利会在证明清单中动态出现相应项目，但工具不会替申请人判断文件是否具有法律效力。

## 7. 校验

```bash
python scripts/ccopyright.py validate \
  --workspace /仓库/绝对路径/.ccopyright
```

阅读 `qa/validation-report.md`，并检查 `qa/` 下的逐页 PNG 与 `contact-sheet.html`。技术通过不等于完成人工复核。

## 8. 发布一个新版本

逐项检查 `drafts/final-review-checklist.md` 后运行：

```bash
python scripts/ccopyright.py publish \
  --workspace /仓库/绝对路径/.ccopyright \
  --human-reviewed
```

命令会在 `ready-to-submit/` 下创建带时间戳的新目录，绝不覆盖旧版本。目录包含两份 PDF、可复制填写的底稿与清单、申请事实快照、生成清单和校验和。实际上传哪些文件必须以当前门户为准；内部清单和 QA 产物默认不上传。

## 生命周期

```text
draft -> generated -> validated -> ready
```

- `draft`：事实可以不完整。
- `generated`：草稿或最终工作产物已经生成。
- `validated`：当前 PDF 已通过确定性校验。
- `ready`：人工复核后已发布不可覆盖的新版本。

校验后修改任何影响材料的事实，都必须重新生成、渲染和校验，才能再次发布。
