from __future__ import annotations

import hashlib
import json
import os
import re
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
                "captured_at": "2026-09-01",
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
        self.assertEqual(upgraded["schema_version"], 3)
        self.assertEqual(upgraded["software"]["full_name"], "保留的软件名称")
        self.assertEqual(upgraded["software"]["environment"]["development_tools"], "旧开发环境")
        self.assertEqual(upgraded["software"]["environment"]["runtime_platform"], "旧运行环境")
        self.assertEqual(upgraded["software"]["main_functions"], "功能一\n功能二")
        self.assertEqual(upgraded["software"]["publication"]["region"], "旧发表地点")
        self.assertFalse(upgraded["confirmations"]["software.classification"])

    def test_init_upgrades_schema_v2_portal_evidence_to_validation_profile(self) -> None:
        workspace = self.repo / ".ccopyright"
        initialized = core.initialize_workspace(self.repo, workspace)
        application_path = Path(initialized["paths"]["application"])
        application = core.load_json(application_path)
        application["schema_version"] = 2
        application["software"]["full_name"] = "保留的申请事实"
        application["requirements"]["portal_evidence"] = {
            "baseline_id": "legacy-value",
            "originals_retained": False,
            "personal_data_retained": False,
        }
        application["requirements"].pop("portal_validation_profile", None)
        application["requirements"]["portal_field_limits"]["software.purpose"] = 48
        application["requirements"]["portal_unknowns"].append("申请人自定义待核对项")
        core.write_json(application_path, application)

        core.initialize_workspace(self.repo, workspace)
        upgraded = core.load_json(application_path)
        self.assertEqual(upgraded["schema_version"], 3)
        self.assertEqual(upgraded["software"]["full_name"], "保留的申请事实")
        self.assertNotIn("portal_evidence", upgraded["requirements"])
        self.assertEqual(
            upgraded["requirements"]["portal_validation_profile"],
            "ccpc-form-profile-v1",
        )
        self.assertEqual(upgraded["requirements"]["portal_field_limits"]["software.purpose"], 48)
        self.assertIn("申请人自定义待核对项", upgraded["requirements"]["portal_unknowns"])

    def test_schema_v3_removes_residual_legacy_portal_evidence(self) -> None:
        application = core.load_json(
            ROOT
            / "skills"
            / "ccopyright-register"
            / "assets"
            / "application.template.json"
        )
        application["requirements"]["portal_evidence"] = {
            "attachment_path": "/private/tmp/unredacted-portal.png",
            "personal_data_retained": True,
        }

        upgraded, changed = core.upgrade_application(application)

        self.assertTrue(changed)
        self.assertNotIn("portal_evidence", upgraded["requirements"])
        self.assertIn("portal_evidence", application["requirements"])

    def test_reopening_workspace_preserves_removed_portal_gate(self) -> None:
        workspace = self.repo / ".ccopyright"
        initialized = core.initialize_workspace(self.repo, workspace)
        application_path = Path(initialized["paths"]["application"])
        application = core.load_json(application_path)
        application["requirements"]["portal_field_limits"].pop("software.purpose")
        core.write_json(application_path, application)

        core.initialize_workspace(self.repo, workspace)
        core.initialize_workspace(self.repo, workspace)
        reopened = core.load_json(application_path)
        self.assertNotIn(
            "software.purpose",
            reopened["requirements"]["portal_field_limits"],
        )

    def test_future_schema_is_rejected_before_migration(self) -> None:
        application = core.load_json(
            ROOT
            / "skills"
            / "ccopyright-register"
            / "assets"
            / "application.template.json"
        )
        application["schema_version"] = core.APPLICATION_SCHEMA_VERSION + 1
        application["requirements"]["portal_evidence"] = {"legacy": True}
        original = json.loads(json.dumps(application, ensure_ascii=False))

        with self.assertRaisesRegex(core.CcopyrightError, "newer than supported"):
            core.upgrade_application(application)
        self.assertEqual(application, original)


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
        application["proof_checklist"][0]["status"] = "done"
        status = core.application_status(application)
        self.assertFalse(status["final_complete"])
        joined = "\n".join(status["invalid_required_values"])
        self.assertIn("YYYY-MM-DD", joined)
        self.assertIn("duplicates", joined)
        self.assertIn("A4", joined)
        self.assertIn("repository-relative", joined)
        self.assertIn("proof_checklist[0].status", joined)

    def test_cli_status_reports_malformed_requirements_without_crashing(self) -> None:
        workspace = self.initialized_workspace()
        paths = core.workspace_paths(workspace)
        snapshot_before = paths["requirements"].read_bytes()
        application = core.load_json(paths["application"])
        application["requirements"]["accepted_upload_formats"] = ["pdf", 7]
        core.write_json(paths["application"], application)

        process = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "skills"
                    / "ccopyright-register"
                    / "scripts"
                    / "ccopyright.py"
                ),
                "status",
                "--workspace",
                str(workspace),
            ],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        self.assertEqual(process.returncode, 0, process.stderr)
        status = json.loads(process.stdout)
        self.assertTrue(
            any(
                "accepted_upload_formats" in error
                for error in status["invalid_required_values"]
            )
        )
        self.assertFalse(status["final_complete"])
        self.assertEqual(snapshot_before, paths["requirements"].read_bytes())

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
        self.assertTrue(any("portal validation profile maximum is 50" in value for value in status["portal_constraint_violations"]))
        self.assertFalse(status["final_complete"])

        core.write_json(core.workspace_paths(workspace)["application"], application)
        draft = core.build_all(self.repo, workspace, final=False)
        self.assertTrue(
            any(
                item["level"] == "WARNING"
                and item["code"] == "portal-validation-profile"
                and "maximum is 50" in item["message"]
                for item in draft["warnings"]
            )
        )
        with self.assertRaisesRegex(core.CcopyrightError, "portal constraints"):
            core.build_all(self.repo, workspace, final=True)

    def test_conditional_branch_gaps_are_draft_warnings_and_final_blocks(self) -> None:
        workspace = self.initialized_workspace()
        paths = core.workspace_paths(workspace)
        application = core.load_json(paths["application"])
        application["software"]["publication"] = {
            "status": "published",
            "date": "",
            "country": "",
            "region": "",
        }
        application["software"]["description"] = {
            "type": "modified",
            "modification_summary": "",
            "modification_basis": "not-applicable",
        }
        application["software"]["rights_acquisition"] = "successor"
        application["software"]["rights_acquisition_details"] = ""
        application["software"]["rights_scope"] = "partial"
        application["software"]["rights_scope_details"] = ""
        core.write_json(paths["application"], application)

        draft = core.build_all(self.repo, workspace, final=False)
        conditional_warnings = [
            item["message"]
            for item in draft["warnings"]
            if item["level"] == "WARNING" and item["code"] == "portal-conditional"
        ]
        joined = "\n".join(conditional_warnings)
        self.assertIn("publication status is published", joined)
        self.assertIn("modified software", joined)
        self.assertIn("successor acquisition", joined)
        self.assertIn("rights scope is partial", joined)
        with self.assertRaisesRegex(core.CcopyrightError, "portal conditionals"):
            core.build_all(self.repo, workspace, final=True)

    def test_portal_gate_profile_supports_minimum_only_and_validates_paths(self) -> None:
        workspace = self.initialized_workspace()
        application = core.load_json(core.workspace_paths(workspace)["application"])
        minimums = application["requirements"]["portal_field_minimums"]
        maximums = application["requirements"]["portal_field_limits"]
        maximums.pop("software.commercial_value", None)
        minimums["software.commercial_value"] = 20

        application["software"]["commercial_value"] = ""
        self.assertFalse(
            any(
                "software.commercial_value" in item
                for item in core.portal_constraint_violations(application)
            )
        )
        application["software"]["commercial_value"] = "简短说明"
        self.assertTrue(
            any(
                "software.commercial_value" in item and "minimum is 20" in item
                for item in core.portal_constraint_violations(application)
            )
        )
        snapshot = core.requirements_snapshot_markdown(application)
        self.assertIn("| `software.commercial_value` | 20 |  |", snapshot)

        core.write_json(core.workspace_paths(workspace)["application"], application)
        draft = core.build_all(self.repo, workspace, final=False)
        self.assertTrue(
            any(
                item["code"] == "portal-validation-profile"
                and "software.commercial_value" in item["message"]
                and "minimum is 20" in item["message"]
                for item in draft["warnings"]
            )
        )
        with self.assertRaisesRegex(core.CcopyrightError, "portal constraints"):
            core.build_all(self.repo, workspace, final=True)

        maximums["invalid-path"] = 10
        maximums["software.not_a_field"] = 10
        minimums["software.purpose"] = 51
        errors = "\n".join(core.application_validation_errors(application))
        self.assertIn("dotted application field paths", errors)
        self.assertIn("does not resolve to an application field", errors)
        self.assertIn("minimum 51 greater than maximum 50", errors)

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
        draft = core.build_all(self.repo, workspace, final=False)

        conditional_warnings = [
            item["message"]
            for item in draft["warnings"]
            if item["code"] == "portal-conditional"
        ]
        self.assertTrue(
            any("cooperative-agreement" in message for message in conditional_warnings)
        )
        self.assertTrue(
            any(
                "original-holder-authorization" in message
                for message in conditional_warnings
            )
        )
        with self.assertRaisesRegex(core.CcopyrightError, "portal conditionals"):
            core.build_all(self.repo, workspace, final=True)

        application = core.load_json(paths["application"])
        application["proof_checklist"].extend(
            [
                {
                    "code": "cooperative-agreement",
                    "item": "Cooperative-development contract or agreement PDF",
                    "status": "ready",
                    "note": "Prepared outside the repository.",
                },
                {
                    "code": "original-holder-authorization",
                    "item": "Original rights-holder authorization PDF",
                    "status": "ready",
                    "note": "Prepared outside the repository.",
                },
            ]
        )
        core.write_json(paths["application"], application)
        result = core.build_all(self.repo, workspace, final=True)
        self.assertTrue(result["final"])

        proof = (paths["drafts"] / "proof-checklist.md").read_text(encoding="utf-8")
        self.assertIn("Cooperative-development contract or agreement PDF", proof)
        self.assertIn("Original rights-holder authorization PDF", proof)
        worksheet = (paths["drafts"] / "form-worksheet.md").read_text(encoding="utf-8")
        self.assertIn("软件著作权登记申请表填写底稿", worksheet)
        self.assertIn("开发的硬件环境", worksheet)
        self.assertIn("源程序量核对", worksheet)
        self.assertIn("500–1300", worksheet)
        snapshot = paths["requirements"].read_text(encoding="utf-8")
        self.assertIn("Current portal reviewed: `2026-09-01`", snapshot)
        self.assertIn("Profile ID: `ccpc-form-profile-v1`", snapshot)
        self.assertIn("Authority: `portal compatibility only`", snapshot)
        self.assertNotIn("portal-form evidence", snapshot.lower())
        self.assertNotIn("screenshots retained", snapshot.lower())

    def test_every_conditional_proof_branch_has_a_readiness_gate(self) -> None:
        workspace = self.initialized_workspace()
        base = core.load_json(core.workspace_paths(workspace)["application"])
        cases = {
            "cooperative-agreement": {
                "software": {"development_type": "cooperative"},
                "ready_status": "ready",
            },
            "commissioned-agreement": {
                "software": {"development_type": "commissioned"},
                "ready_status": "ready",
            },
            "assigned-task-document": {
                "software": {"development_type": "assigned-task"},
                "ready_status": "ready",
            },
            "original-holder-authorization": {
                "description": {
                    "type": "modified",
                    "modification_summary": "经授权修改",
                    "modification_basis": "authorization-required",
                },
                "ready_status": "ready",
            },
            "previous-registration": {
                "description": {
                    "type": "modified",
                    "modification_summary": "在已登记软件基础上修改",
                    "modification_basis": "registered",
                },
                "ready_status": "not-required",
            },
            "successor-proof": {
                "software": {
                    "rights_acquisition": "successor",
                    "rights_acquisition_details": "受让取得",
                },
                "ready_status": "ready",
            },
            "partial-rights-proof": {
                "software": {
                    "rights_scope": "partial",
                    "rights_scope_details": "仅享有复制权和信息网络传播权",
                },
                "ready_status": "not-required",
            },
        }

        for code, changes in cases.items():
            with self.subTest(code=code):
                application = json.loads(json.dumps(base, ensure_ascii=False))
                for field, value in changes.get("software", {}).items():
                    application["software"][field] = value
                if "description" in changes:
                    application["software"]["description"] = changes["description"]

                unresolved = core.portal_conditional_violations(application)
                self.assertTrue(any(code in message for message in unresolved))

                application["proof_checklist"].append(
                    {
                        "code": code,
                        "item": code,
                        "status": changes["ready_status"],
                        "note": "Current portal reviewed; proof remains outside the repository.",
                    }
                )
                resolved = core.portal_conditional_violations(application)
                self.assertFalse(any(code in message for message in resolved))

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
            self.assertEqual(
                ["ccopyright-qa.skill", "ccopyright-register.skill"],
                sorted(first_bytes),
            )
            self.assertFalse((output / "ccopyright.skill").exists())
            self.assertFalse((output / "软著.skill").exists())

            for name in ("ccopyright-qa", "ccopyright-register"):
                with zipfile.ZipFile(output / f"{name}.skill") as archive:
                    self.assertIsNone(archive.testzip())
                    names = set(archive.namelist())
                    self.assertNotIn("package.json", names)
                    self.assertFalse(
                        any(path.startswith("/") or ".." in Path(path).parts for path in names)
                    )
                    manifest = json.loads(archive.read("PACKAGE-MANIFEST.json"))
                    self.assertEqual(manifest["skill"], name)
                    self.assertEqual(manifest["locales"], ["en", "zh-CN"])

            with zipfile.ZipFile(output / "ccopyright-register.skill") as archive:
                self.assertIsNone(archive.testzip())
                names = set(archive.namelist())
                required = {
                    "SKILL.md",
                    "README.md",
                    "README.en.md",
                    "agents/openai.yaml",
                    "references/en/application-schema.md",
                    "references/en/material-preparation.md",
                    "references/en/official-sources.md",
                    "scripts/ccopyright_core.py",
                    "references/en/workflow.md",
                    "references/en/portal-form.md",
                    "references/en/quality-checks.md",
                    "references/zh-CN/application-schema.md",
                    "references/zh-CN/material-preparation.md",
                    "references/zh-CN/official-sources.md",
                    "references/zh-CN/workflow.md",
                    "references/zh-CN/portal-form.md",
                    "references/zh-CN/quality-checks.md",
                }
                self.assertTrue(required.issubset(names))
                self.assertIn(b"name: ccopyright-register", archive.read("SKILL.md"))
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

            with zipfile.ZipFile(output / "ccopyright-qa.skill") as archive:
                names = set(archive.namelist())
                required = {
                    "SKILL.md",
                    "README.md",
                    "README.en.md",
                    "agents/openai.yaml",
                    "references/en/answering-guide.md",
                    "references/en/official-sources.md",
                    "references/en/registration-baseline.md",
                    "references/en/source-policy.md",
                    "references/en/topic-map.md",
                    "references/zh-CN/answering-guide.md",
                    "references/zh-CN/official-sources.md",
                    "references/zh-CN/registration-baseline.md",
                    "references/zh-CN/source-policy.md",
                    "references/zh-CN/topic-map.md",
                }
                self.assertTrue(required.issubset(names))
                self.assertIn(b"name: ccopyright-qa", archive.read("SKILL.md"))
                self.assertIn(b"$ccopyright-qa", archive.read("agents/openai.yaml"))
                self.assertIn("[English](README.en.md)", archive.read("README.md").decode())
                self.assertIn("[简体中文](README.md)", archive.read("README.en.md").decode())
                self.assertFalse(any(name.startswith("scripts/") for name in names))

    def test_repository_documents_exactly_two_independent_skills(self) -> None:
        skills_root = ROOT / "skills"
        names = sorted(
            path.parent.name
            for path in skills_root.glob("*/SKILL.md")
            if path.is_file()
        )
        self.assertEqual(["ccopyright-qa", "ccopyright-register"], names)

        for readme_name in ("README.md", "README.en.md"):
            readme = (ROOT / readme_name).read_text(encoding="utf-8")
            self.assertIn("ccopyright-qa", readme)
            self.assertIn("ccopyright-register", readme)

        qa_root = skills_root / "ccopyright-qa"
        register_root = skills_root / "ccopyright-register"
        self.assertFalse((qa_root / "scripts").exists())
        self.assertTrue((register_root / "scripts" / "ccopyright.py").is_file())

    def test_skill_descriptions_route_qa_and_preparation_intents(self) -> None:
        qa_root = ROOT / "skills" / "ccopyright-qa"
        register_root = ROOT / "skills" / "ccopyright-register"
        qa_frontmatter = (qa_root / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
        register_frontmatter = (
            (register_root / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
        )

        self.assertIn("Do not scan repositories", qa_frontmatter)
        self.assertIn("use ccopyright-register", qa_frontmatter)
        self.assertIn("Use when the user explicitly asks", register_frontmatter)
        self.assertIn("Do not use for general registration Q&A", register_frontmatter)
        self.assertIn("use ccopyright-qa", register_frontmatter)
        self.assertNotIn("Use for 软件著作权, 软著", register_frontmatter)

    def test_qa_official_source_catalog_and_portal_profile_boundary(self) -> None:
        qa_root = ROOT / "skills" / "ccopyright-qa"
        expected_urls = {
            "https://www.ccopyright.com.cn/index.php?optionid=1057",
            "https://www.ccopyright.com.cn/index.php?optionid=1080",
            "https://www.ccopyright.com.cn/index.php?optionid=1081",
            "https://www.ccopyright.com.cn/index.php?optionid=1087&page=1",
            "https://www.ccopyright.com.cn/index.php?optionid=1571",
            "https://www.ncac.gov.cn/xxfb/flfg/bmgz/202410/t20241015_869486.html",
            "https://xzfg.moj.gov.cn/mobile/law/detail?LawID=581",
            "https://www.npc.gov.cn/c2/c30834/202011/t20201119_308796.html",
        }
        catalog_url_sets = []
        catalog_paths = [
            ROOT / "skills" / skill / "references" / locale / "official-sources.md"
            for skill in ("ccopyright-qa", "ccopyright-register")
            for locale in ("zh-CN", "en")
        ]
        for catalog_path in catalog_paths:
            catalog = catalog_path.read_text(encoding="utf-8")
            for url in expected_urls:
                self.assertIn(url, catalog)
            self.assertIn("2026-09-01", catalog)
            catalog_url_sets.append(set(re.findall(r"https://[^)\s]+", catalog)))
        self.assertTrue(all(urls == catalog_url_sets[0] for urls in catalog_url_sets[1:]))

        template = json.loads(
            (ROOT / "skills" / "ccopyright-register" / "assets" / "application.template.json").read_text(
                encoding="utf-8"
            )
        )
        profile_id = template["requirements"]["portal_validation_profile"]
        profile_docs = [
            qa_root / "references" / locale / "registration-baseline.md"
            for locale in ("zh-CN", "en")
        ] + [
            ROOT / "skills" / "ccopyright-register" / "references" / locale / "portal-form.md"
            for locale in ("zh-CN", "en")
        ]
        for profile_doc in profile_docs:
            content = profile_doc.read_text(encoding="utf-8").replace(",", "")
            self.assertIn(profile_id, content)
            for configured_value in (50, 100, 120, 500, 1300):
                self.assertIn(str(configured_value), content)

        qa_docs = [qa_root / "SKILL.md", *qa_root.rglob("*.md")]
        forbidden_history = (
            "2026-08-31",
            "12 张",
            "twelve user-provided",
            "received partial form screenshots",
            "screenshot baseline",
            "截图基线",
        )
        for path in dict.fromkeys(qa_docs):
            content = path.read_text(encoding="utf-8").lower()
            for phrase in forbidden_history:
                self.assertNotIn(phrase.lower(), content, f"Legacy screenshot history in {path}")

    def test_skill_markdown_local_links_resolve(self) -> None:
        readmes = {
            ROOT / "README.md",
            ROOT / "README.en.md",
            ROOT / "skills" / "ccopyright-qa" / "README.md",
            ROOT / "skills" / "ccopyright-qa" / "README.en.md",
            ROOT / "skills" / "ccopyright-register" / "README.md",
            ROOT / "skills" / "ccopyright-register" / "README.en.md",
            *list((ROOT / "skills" / "ccopyright-qa").rglob("*.md")),
            *list((ROOT / "skills" / "ccopyright-register").rglob("*.md")),
        }
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for readme in sorted(readmes):
            content = readme.read_text(encoding="utf-8")
            for destination in link_pattern.findall(content):
                if destination.startswith(("http://", "https://", "#")):
                    continue
                target = destination.split("#", 1)[0]
                self.assertTrue(
                    (readme.parent / target).is_file(),
                    f"Broken local link in {readme.relative_to(ROOT)}: {destination}",
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
