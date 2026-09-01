from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests" / "fixtures" / "sample-app"
sys.path.insert(0, str(ROOT / "skills" / "ccopyright-register" / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

import build_skill_archives  # noqa: E402
import ccopyright_core as core  # noqa: E402


class RepositoryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="ccopyright-test-")
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        shutil.copytree(FIXTURE, self.repo)
        (self.repo / "src" / "tabs.py").write_text(
            "def tabbed() -> str:\n\treturn 'preserve-tab'\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def configure_application(self, workspace: Path) -> dict:
        paths = core.workspace_paths(workspace)
        application = core.load_json(paths["application"])
        main_functions = (
            "本软件面向需要生成规范问候语的用户，提供姓名输入、空值处理、字符规范化、"
            "确定性问候语生成、结果展示和异常输入提示等功能。用户输入姓名后，系统按照"
            "既定规则清理首尾空白并保留有效字符，再调用领域逻辑生成一致的中文问候结果。"
            "当输入为空时，系统使用访客名称生成可理解的默认结果。程序入口负责接收输入、"
            "调用核心逻辑并输出结果，领域模块负责输入规范化和文本生成，使功能边界清晰且"
            "便于测试。系统不依赖外部网络服务，不上传用户数据，能够在支持 Python 的桌面"
            "或服务器环境中运行。测试用例覆盖正常姓名、空输入和包含多余空格的输入，确保"
            "同一输入始终得到相同输出。生成结果可用于命令行演示、教学示例和自动化材料"
            "校验场景，并通过简明的操作说明帮助用户完成启动、输入和查看结果的完整流程。"
            "软件还提供清晰的模块组织和错误边界，方便维护人员定位输入处理与结果生成环节。"
            "在登记版本中，用户按照说明启动程序后输入姓名即可获得问候结果，无需配置账号、"
            "网络连接或第三方服务。系统在处理输入时不会修改源数据文件，也不会持久化姓名，"
            "程序结束后不保留用户输入。维护人员可以通过自动化测试验证核心规则，通过文档"
            "了解运行条件、启动方法、输入要求和输出含义，从而稳定地部署和复核登记版本。"
        )
        application["software"].update(
            {
                "full_name": "示例问候软件",
                "short_name": "示例软件",
                "version": "V1.2.3",
                "category": "application",
                "description": {
                    "type": "original",
                    "modification_summary": "",
                    "modification_basis": "not-applicable",
                },
                "rights_holders": ["示例申请人有限公司"],
                "joint_rights_holders": False,
                "completion_date": "2026-08-01",
                "publication": {
                    "status": "unpublished",
                    "date": "",
                    "country": "",
                    "region": "",
                },
                "development_type": "independent",
                "rights_acquisition": "original",
                "rights_scope": "all",
                "environment": {
                    "development_hardware": "通用个人计算机",
                    "runtime_hardware": "通用个人计算机或服务器",
                    "development_os": "macOS",
                    "development_tools": "Python 3.10、文本编辑器",
                    "runtime_platform": "macOS、Linux 或 Windows",
                    "supporting_software": "Python 3.10 或更高版本",
                },
                "purpose": "提供可复核的问候语生成能力。",
                "industry": "通用软件",
                "technical_features": ["APP"],
                "other_technical_features": "确定性文本处理",
                "main_functions": main_functions,
                "competitive_advantages": "结构简单，输出可预测。",
                "commercial_value": "用于演示材料生成与校验。",
            }
        )
        selected_files = ["src/main.py", "src/tabs.py"]
        selected_stream, _ = core.read_selected_source(self.repo, selected_files)
        application["source"].update(
            {
                "mode": "whole",
                "deposit_type": "general",
                "files": selected_files,
                "program_line_count": len(selected_stream),
                "program_line_count_basis": "selected-source-physical-lines",
                "ordering": "entry-point-then-support",
            }
        )
        application["requirements"].update(
            {
                "program_lines_per_page": 5,
                "document_lines_per_page": 4,
                "front_pages": 1,
                "back_pages": 1,
                "allow_short_final_page_for_complete_material": True,
                "max_pdf_bytes": None,
                "captured_at": "2026-08-31",
            }
        )
        application["document"].update(
            {
                "title": "示例问候软件使用说明书",
                "deposit_type": "general",
                "max_display_units_per_line": 64,
                "sections": [
                    {
                        "title": "软件概述",
                        "paragraphs": ["本软件接收用户输入的姓名，并返回规范化的问候语。"],
                        "evidence": ["src/main.py", "docs/missing-proof.md"],
                    },
                    {
                        "title": "操作流程",
                        "paragraphs": [
                            "用户启动程序并输入姓名。",
                            "软件清理输入后生成结果；空输入使用访客名称。",
                        ],
                        "evidence": ["src/main.py", "src/domain.py"],
                    },
                ],
                "screenshots": [
                    {
                        "path": "docs/screenshot.svg",
                        "page": 2,
                        "title": "问候结果",
                        "caption": "登记版本生成的示例问候语界面。",
                    }
                ],
            }
        )
        application["confirmations"] = {
            "software.full_name": True,
            "software.version": True,
            "software.classification": True,
            "software.rights": True,
            "software.rights_holders": True,
            "software.completion_date": True,
            "software.development": True,
            "software.publication": True,
            "software.environment": True,
            "software.functionality": True,
            "source.selection": True,
            "source.program_line_count": True,
            "materials.deposit": True,
            "document.content": True,
            "requirements.current": True,
        }
        core.write_json(paths["application"], application)
        return application

    def initialized_workspace(self) -> Path:
        workspace = self.repo / ".ccopyright"
        core.initialize_workspace(self.repo, workspace)
        self.configure_application(workspace)
        return workspace


class RepositoryScanTests(RepositoryTestCase):
    def test_scan_reports_only_info_warning_and_omits_secret_value(self) -> None:
        inventory = core.scan_repository(self.repo)
        levels = {item["level"] for item in inventory["findings"]}
        self.assertLessEqual(levels, {"INFO", "WARNING"})
        serialized = json.dumps(inventory, ensure_ascii=False)
        self.assertNotIn("fixture-secret-value", serialized)
        self.assertNotIn("fixture-config-secret", serialized)
        self.assertIn("sensitive-value", serialized)
        self.assertTrue(
            any(
                item["code"] == "sensitive-value" and item.get("path") == "config/settings.json"
                for item in inventory["findings"]
            )
        )
        self.assertEqual(
            next(item["value"] for item in inventory["version_suggestions"] if item["field"] == "version"),
            "1.2.3",
        )
        candidate_paths = {item["path"] for item in inventory["candidate_sources"]}
        self.assertIn("src/main.py", candidate_paths)
        self.assertNotIn("tests/test_domain.py", candidate_paths)

    def test_symlink_is_skipped_and_rejected_as_explicit_source(self) -> None:
        outside = self.root / "outside.py"
        outside.write_text("print('outside')\n", encoding="utf-8")
        link = self.repo / "src" / "linked.py"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks are unavailable on this platform")
        inventory = core.scan_repository(self.repo)
        linked = [item for item in inventory["findings"] if item.get("path") == "src/linked.py"]
        self.assertTrue(linked)
        self.assertTrue(all(item["level"] == "WARNING" for item in linked))
        with self.assertRaises(core.CcopyrightError):
            core.read_selected_source(self.repo, ["src/linked.py"])

    def test_init_preserves_existing_application_without_force(self) -> None:
        workspace = self.repo / ".ccopyright"
        first = core.initialize_workspace(self.repo, workspace)
        application_path = Path(first["paths"]["application"])
        application = core.load_json(application_path)
        self.assertEqual(application["software"]["short_name"], "sample-copyright-app")
        self.assertEqual(application["software"]["version"], "1.2.3")
        self.assertFalse(application["confirmations"]["software.version"])
        application["software"]["full_name"] = "Do not replace"
        core.write_json(application_path, application)
        core.initialize_workspace(self.repo, workspace)
        self.assertEqual(core.load_json(application_path)["software"]["full_name"], "Do not replace")
        inventory = core.load_json(core.workspace_paths(workspace)["inventory"])
        self.assertFalse(any(item["path"].startswith(".ccopyright/") for item in inventory["sources"]))

    def test_init_upgrades_schema_v1_without_replacing_existing_facts(self) -> None:
        workspace = self.repo / ".ccopyright"
        initialized = core.initialize_workspace(self.repo, workspace)
        application_path = Path(initialized["paths"]["application"])
        application = core.load_json(application_path)
        application["schema_version"] = 1
        application["software"]["full_name"] = "保留的软件名称"
        application["software"]["development_environment"] = "旧开发环境"
        application["software"]["runtime_environment"] = "旧运行环境"
        application["software"].pop("environment", None)
        application["software"]["main_functions"] = ["功能一", "功能二"]
        application["software"]["publication"] = {
            "status": "unpublished",
            "date": "",
            "location": "旧发表地点",
        }
        for key in (
            "category",
            "description",
            "joint_rights_holders",
            "other_programming_languages",
            "other_technical_features",
        ):
            application["software"].pop(key, None)
        core.write_json(application_path, application)

        core.initialize_workspace(self.repo, workspace)
        upgraded = core.load_json(application_path)
        self.assertEqual(upgraded["schema_version"], 2)
        self.assertEqual(upgraded["software"]["full_name"], "保留的软件名称")
        self.assertEqual(upgraded["software"]["environment"]["development_tools"], "旧开发环境")
        self.assertEqual(upgraded["software"]["environment"]["runtime_platform"], "旧运行环境")
        self.assertEqual(upgraded["software"]["main_functions"], "功能一\n功能二")
        self.assertEqual(upgraded["software"]["publication"]["region"], "旧发表地点")
        self.assertFalse(upgraded["confirmations"]["software.classification"])


class MaterialTests(RepositoryTestCase):
    def test_front_back_selection_has_expected_cut_points(self) -> None:
        stream = [{"stream_index": value} for value in range(1, 21)]
        selected, mode = core.select_source_rows(
            stream,
            {"program_lines_per_page": 5, "front_pages": 1, "back_pages": 1},
            "front-back",
        )
        self.assertEqual(mode, "front-back")
        self.assertEqual([item["stream_index"] for item in selected], [1, 2, 3, 4, 5, 16, 17, 18, 19, 20])

    def test_final_build_preserves_source_rows_and_maps_evidence(self) -> None:
        workspace = self.initialized_workspace()
        result = core.build_all(self.repo, workspace, final=True)
        self.assertTrue(result["final"])
        paths = core.workspace_paths(workspace)
        manifest = core.load_json(paths["work"] / "program-manifest.json")
        tab_row = next(
            item
            for item in manifest["rows"]
            if item["path"] == "src/tabs.py" and item["original_line"] == 2
        )
        expected_hash = hashlib.sha256("src/tabs.py\0".encode("utf-8") + b"2\0\treturn 'preserve-tab'").hexdigest()
        self.assertEqual(tab_row["row_sha256"], expected_hash)
        markdown = (paths["work"] / manifest["outputs"]["markdown"]).read_text(encoding="utf-8")
        self.assertIn("\treturn 'preserve-tab'", markdown)
        evidence = (paths["reports"] / "evidence-map.md").read_text(encoding="utf-8")
        self.assertIn("docs/missing-proof.md", evidence)
        self.assertIn("| no |", evidence)
        document_manifest = core.load_json(paths["work"] / "document-manifest.json")
        self.assertTrue(any(item["code"] == "missing-evidence" for item in document_manifest["warnings"]))
        status = core.application_status(core.load_json(paths["application"]))
        self.assertTrue(status["final_complete"])

    def test_final_build_blocks_incomplete_facts_but_draft_is_available(self) -> None:
        workspace = self.repo / ".ccopyright"
        core.initialize_workspace(self.repo, workspace)
        application_path = core.workspace_paths(workspace)["application"]
        application = core.load_json(application_path)
        application["document"]["sections"] = [{"title": "Draft", "paragraphs": ["Draft"], "evidence": []}]
        application["source"]["suggested_files"] = ["src/main.py"]
        core.write_json(application_path, application)
        draft = core.build_all(self.repo, workspace, final=False)
        self.assertFalse(draft["final"])
        with self.assertRaises(core.CcopyrightError):
            core.build_all(self.repo, workspace, final=True)

    def test_publish_requires_human_review_and_validation(self) -> None:
        workspace = self.initialized_workspace()
        core.build_all(self.repo, workspace, final=True)
        with self.assertRaises(core.CcopyrightError):
            core.publish_workspace(workspace, human_reviewed=False)
        with self.assertRaises(core.CcopyrightError):
            core.publish_workspace(workspace, human_reviewed=True)

    def test_status_reports_invalid_dates_types_and_paths(self) -> None:
        workspace = self.initialized_workspace()
        application_path = core.workspace_paths(workspace)["application"]
        application = core.load_json(application_path)
        application["software"]["completion_date"] = "2026-02-30"
        application["software"]["rights_holders"] = ["重复主体", "重复主体"]
        application["requirements"]["paper"] = "Letter"
        application["source"]["files"] = [str((self.repo / "src" / "main.py").resolve())]
        status = core.application_status(application)
        self.assertFalse(status["final_complete"])
        joined = "\n".join(status["invalid_required_values"])
        self.assertIn("YYYY-MM-DD", joined)
        self.assertIn("duplicates", joined)
        self.assertIn("A4", joined)
        self.assertIn("repository-relative", joined)

    def test_portal_conditionals_and_visible_character_limits_gate_final_mode(self) -> None:
        workspace = self.initialized_workspace()
        application = core.load_json(core.workspace_paths(workspace)["application"])
        self.assertTrue(core.application_status(application)["final_complete"])

        application["software"]["publication"] = {
            "status": "published",
            "date": "",
            "country": "",
            "region": "",
        }
        missing = core.application_status(application)["missing_required_values"]
        self.assertIn("software.publication.date", missing)
        self.assertIn("software.publication.country", missing)
        self.assertIn("software.publication.region", missing)

        application["software"]["publication"].update(
            {"date": "2026-08-15", "country": "中国", "region": "浙江省"}
        )
        application["software"]["description"] = {
            "type": "modified",
            "modification_summary": "",
            "modification_basis": "not-applicable",
        }
        missing = core.application_status(application)["missing_required_values"]
        self.assertIn("software.description.modification_summary", missing)
        self.assertIn("software.description.modification_basis", missing)

        application["software"]["description"].update(
            {"modification_summary": "在经授权的软件基础上修改", "modification_basis": "authorization-required"}
        )
        application["software"]["environment"]["development_hardware"] = "甲" * 51
        status = core.application_status(application)
        self.assertTrue(any("visible portal maximum is 50" in value for value in status["portal_constraint_violations"]))
        self.assertFalse(status["final_complete"])

    def test_conditional_proofs_and_portal_worksheet_are_generated(self) -> None:
        workspace = self.initialized_workspace()
        paths = core.workspace_paths(workspace)
        application = core.load_json(paths["application"])
        application["software"]["development_type"] = "cooperative"
        application["software"]["description"] = {
            "type": "modified",
            "modification_summary": "在经授权的软件基础上修改",
            "modification_basis": "authorization-required",
        }
        core.write_json(paths["application"], application)
        core.build_all(self.repo, workspace, final=True)

        proof = (paths["drafts"] / "proof-checklist.md").read_text(encoding="utf-8")
        self.assertIn("Cooperative-development contract or agreement PDF", proof)
        self.assertIn("Original rights-holder authorization PDF", proof)
        worksheet = (paths["drafts"] / "form-worksheet.md").read_text(encoding="utf-8")
        self.assertIn("软件著作权登记申请表填写底稿", worksheet)
        self.assertIn("开发的硬件环境", worksheet)
        self.assertIn("源程序量核对", worksheet)
        self.assertIn("500–1300", worksheet)
        snapshot = paths["requirements"].read_text(encoding="utf-8")
        self.assertIn("user-supplied-form-screenshots-received-2026-08-31", snapshot)
        self.assertIn("Personal identity data retained: `no`", snapshot)

    def test_exceptional_deposit_stops_the_ordinary_workflow(self) -> None:
        workspace = self.initialized_workspace()
        application_path = core.workspace_paths(workspace)["application"]
        application = core.load_json(application_path)
        application["source"]["deposit_type"] = "exceptional"
        core.write_json(application_path, application)
        with self.assertRaisesRegex(core.CcopyrightError, "Exceptional deposit"):
            core.build_all(self.repo, workspace, final=False)

    def test_selected_source_line_count_mismatch_blocks_final_generation(self) -> None:
        workspace = self.initialized_workspace()
        application_path = core.workspace_paths(workspace)["application"]
        application = core.load_json(application_path)
        application["source"]["program_line_count"] += 1
        core.write_json(application_path, application)
        with self.assertRaisesRegex(core.CcopyrightError, "Reported source-program line count"):
            core.build_all(self.repo, workspace, final=True)

    def test_applicant_confirmed_total_can_differ_from_selected_source_stream(self) -> None:
        workspace = self.initialized_workspace()
        paths = core.workspace_paths(workspace)
        application = core.load_json(paths["application"])
        application["source"]["program_line_count_basis"] = "applicant-confirmed-total"
        application["source"]["program_line_count"] += 100
        core.write_json(paths["application"], application)

        result = core.build_all(self.repo, workspace, final=True)
        manifest = core.load_json(paths["work"] / "program-manifest.json")
        self.assertTrue(result["final"])
        self.assertEqual(manifest["source_program_line_count_basis"], "applicant-confirmed-total")
        self.assertNotEqual(
            manifest["reported_source_program_lines"], manifest["source_stream_rows"]
        )

    def test_workspace_cannot_be_reused_for_another_repository(self) -> None:
        workspace = self.initialized_workspace()
        other_repo = self.root / "other-repo"
        shutil.copytree(FIXTURE, other_repo)
        with self.assertRaises(core.CcopyrightError):
            core.build_all(other_repo, workspace, final=True)

    def test_commit_snapshot_rejects_changed_selected_source(self) -> None:
        if not shutil.which("git"):
            self.skipTest("Git is not installed")
        commands = [
            ["git", "init", "-q"],
            ["git", "config", "user.name", "Fixture User"],
            ["git", "config", "user.email", "fixture@example.invalid"],
            ["git", "add", "."],
            ["git", "-c", "commit.gpgsign=false", "commit", "-qm", "fixture snapshot"],
        ]
        for command in commands:
            subprocess.run(
                command,
                cwd=self.repo,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        workspace = self.initialized_workspace()
        main_path = self.repo / "src" / "main.py"
        main_path.write_text(main_path.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")
        with self.assertRaises(core.CcopyrightError):
            core.build_all(self.repo, workspace, final=True)
        application_path = core.workspace_paths(workspace)["application"]
        application = core.load_json(application_path)
        application["snapshot"]["include_uncommitted"] = True
        changed_stream, _ = core.read_selected_source(self.repo, application["source"]["files"])
        application["source"]["program_line_count"] = len(changed_stream)
        core.write_json(application_path, application)
        result = core.build_all(self.repo, workspace, final=True)
        self.assertTrue(result["final"])


class CommandAndPackageTests(unittest.TestCase):
    def test_cli_preflight_returns_json(self) -> None:
        process = subprocess.run(
            [
                sys.executable,
                str(ROOT / "skills" / "ccopyright-register" / "scripts" / "ccopyright.py"),
                "preflight",
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = json.loads(process.stdout)
        self.assertIn("python", output)
        self.assertIn("chromium", output)

    def test_archive_is_deterministic_self_contained_and_localized(self) -> None:
        with tempfile.TemporaryDirectory(prefix="ccopyright-packages-") as temporary:
            output = Path(temporary)
            for deprecated in ("ccopyright.skill", "软著.skill"):
                (output / deprecated).write_bytes(b"obsolete")
            first = build_skill_archives.build(output)
            first_bytes = {Path(item["path"]).name: Path(item["path"]).read_bytes() for item in first}
            second = build_skill_archives.build(output)
            second_bytes = {Path(item["path"]).name: Path(item["path"]).read_bytes() for item in second}
            self.assertEqual(first_bytes, second_bytes)
            self.assertEqual(["ccopyright-register.skill"], sorted(first_bytes))
            self.assertFalse((output / "ccopyright.skill").exists())
            self.assertFalse((output / "软著.skill").exists())
            archive_path = output / "ccopyright-register.skill"
            with zipfile.ZipFile(archive_path) as archive:
                self.assertIsNone(archive.testzip())
                names = set(archive.namelist())
                required = {
                    "SKILL.md",
                    "package.json",
                    "README.md",
                    "README.en.md",
                    "agents/openai.yaml",
                    "scripts/ccopyright_core.py",
                    "references/en/workflow.md",
                    "references/en/portal-form.md",
                    "references/zh-CN/workflow.md",
                    "references/zh-CN/portal-form.md",
                }
                self.assertTrue(required.issubset(names))
                self.assertFalse(any(name.startswith("/") or ".." in Path(name).parts for name in names))
                self.assertIn(b"name: ccopyright-register", archive.read("SKILL.md"))
                package = json.loads(archive.read("package.json"))
                self.assertEqual(package["name"], "shuangchi-gsc-ccopyright-register")
                self.assertEqual(package["version"], "0.0.3")
                self.assertEqual(
                    set(package["files"]),
                    {
                        "SKILL.md",
                        "README.md",
                        "README.en.md",
                        "agents",
                        "assets",
                        "references",
                        "scripts",
                    },
                )
                self.assertIn(b"$ccopyright-register", archive.read("agents/openai.yaml"))
                zh_readme = archive.read("README.md").decode()
                en_readme = archive.read("README.en.md").decode()
                self.assertIn("[English](README.en.md)", zh_readme)
                self.assertIn("[简体中文](README.md)", en_readme)
                self.assertEqual(
                    (
                        ROOT
                        / "skills"
                        / "ccopyright-register"
                        / "scripts"
                        / "ccopyright_core.py"
                    ).read_bytes(),
                    archive.read("scripts/ccopyright_core.py"),
                )

    def test_contextlab_manifest_covers_every_skill_source_file(self) -> None:
        package_root = ROOT / "skills" / "ccopyright-register"
        package = json.loads((package_root / "package.json").read_text(encoding="utf-8"))
        declared = set(package["files"])
        for path in package_root.rglob("*"):
            if not path.is_file() or path.name == "package.json":
                continue
            relative = path.relative_to(package_root)
            self.assertTrue(
                relative.as_posix() in declared or relative.parts[0] in declared,
                f"Aone package manifest omits {relative.as_posix()}",
            )


class PdfIntegrationTests(RepositoryTestCase):
    def test_render_validate_and_revisioned_publish_when_tools_exist(self) -> None:
        if os.environ.get("CCOPYRIGHT_RUN_PDF_INTEGRATION") != "1":
            self.skipTest("Set CCOPYRIGHT_RUN_PDF_INTEGRATION=1 to launch local Chrome")
        capabilities = core.preflight()
        required = ("chromium", "pdfinfo", "pdftotext")
        if not all(capabilities[name]["available"] for name in required):
            self.skipTest("Chrome/Chromium and Poppler validation tools are not all installed")
        workspace = self.initialized_workspace()
        core.build_all(self.repo, workspace, final=True, render=True)
        report = core.validate_workspace(
            workspace,
            render_pages=capabilities["pdftoppm"]["available"],
        )
        self.assertTrue(report["passed"], json.dumps(report, ensure_ascii=False, indent=2))
        application_path = core.workspace_paths(workspace)["application"]
        application = core.load_json(application_path)
        original_purpose = application["software"]["purpose"]
        application["software"]["purpose"] = "Changed after rendering"
        core.write_json(application_path, application)
        stale_report = core.validate_workspace(workspace, render_pages=False)
        self.assertFalse(stale_report["passed"])
        self.assertTrue(stale_report["consistency_errors"])
        application["software"]["purpose"] = original_purpose
        core.write_json(application_path, application)
        refreshed_report = core.validate_workspace(workspace, render_pages=False)
        self.assertTrue(refreshed_report["passed"], json.dumps(refreshed_report, ensure_ascii=False, indent=2))
        first = core.publish_workspace(workspace, human_reviewed=True)
        second = core.publish_workspace(workspace, human_reviewed=True)
        self.assertNotEqual(first, second)
        self.assertTrue((first / "generation-manifest.json").is_file())
        self.assertTrue((first / "SHA256SUMS").is_file())


if __name__ == "__main__":
    unittest.main()
