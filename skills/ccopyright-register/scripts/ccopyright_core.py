from __future__ import annotations

import copy
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path
from typing import Any, Iterable


TOOL_VERSION = "0.2.0"
APPLICATION_SCHEMA_VERSION = 2
ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"

SOFTWARE_CATEGORY_LABELS = {
    "application": "应用软件",
    "embedded": "嵌入式软件",
    "middleware": "中间件",
    "operating-system": "操作系统",
}
SOFTWARE_DESCRIPTION_LABELS = {
    "original": "原创",
    "modified": "修改（含翻译软件、合成软件）",
}
MODIFICATION_BASIS_LABELS = {
    "not-applicable": "不适用",
    "registered": "该软件已登记",
    "authorization-required": "修改、翻译或合成他人软件，需要原权利人授权",
    "unconfirmed": "待确认",
}
DEVELOPMENT_TYPE_LABELS = {
    "independent": "单独开发",
    "cooperative": "合作开发",
    "commissioned": "委托开发",
    "assigned-task": "下达任务开发",
}
RIGHTS_ACQUISITION_LABELS = {
    "original": "原始取得",
    "successor": "继受取得",
}
RIGHTS_SCOPE_LABELS = {"all": "全部权利", "partial": "部分权利"}
PUBLICATION_STATUS_LABELS = {"unpublished": "未发表", "published": "已发表"}
DEPOSIT_TYPE_LABELS = {"general": "一般交存", "exceptional": "例外交存"}
SOURCE_LINE_COUNT_BASES = {
    "selected-source-physical-lines",
    "applicant-confirmed-total",
}
ENVIRONMENT_FIELDS = (
    "development_hardware",
    "runtime_hardware",
    "development_os",
    "development_tools",
    "runtime_platform",
    "supporting_software",
)


class CcopyrightError(RuntimeError):
    pass


SOURCE_EXTENSIONS = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".gd": "GDScript",
    ".go": "Go",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript JSX",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".lua": "Lua",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    ".php": "PHP",
    ".pl": "Perl",
    ".py": "Python",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scala": "Scala",
    ".sh": "Shell",
    ".sol": "Solidity",
    ".sql": "SQL",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript TSX",
    ".vue": "Vue",
    ".zig": "Zig",
}

SCREENSHOT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
MAX_SCREENSHOT_BYTES = 20_000_000
DOCUMENT_EXTENSIONS = {".md", ".mdx", ".rst", ".txt", ".adoc"}
SENSITIVE_TEXT_EXTENSIONS = {
    ".adoc",
    ".conf",
    ".env",
    ".ini",
    ".json",
    ".md",
    ".mdx",
    ".properties",
    ".rst",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
MANIFEST_NAMES = {
    "package.json",
    "pyproject.toml",
    "cargo.toml",
    "go.mod",
    "pubspec.yaml",
    "project.godot",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "package.swift",
}
LICENSE_NAMES = {
    "license",
    "license.md",
    "license.txt",
    "copying",
    "copying.md",
    "notice",
    "notice.txt",
}
SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".ccopyright",
    ".idea",
    ".vscode",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "vendors",
    "third_party",
    "third-party",
    "external",
    "externals",
    "pods",
    ".gradle",
    ".dart_tool",
    "deriveddata",
    "target",
    "dist",
    "build",
    "coverage",
}
THIRD_PARTY_DIRECTORIES = {
    "node_modules",
    "vendor",
    "vendors",
    "third_party",
    "third-party",
    "external",
    "externals",
    "pods",
}
GENERATED_PARTS = {"generated", "gen", "dist", "build", "target", "deriveddata"}
TEST_PARTS = {"test", "tests", "spec", "specs", "__tests__", "fixtures"}

SECRET_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("openai-style-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    (
        "credential-assignment",
        re.compile(
            r"(?i)['\"]?\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|password)\b['\"]?"
            r"\s*[:=]\s*['\"][^'\"]{8,}['\"]"
        ),
    ),
]
PRIVATE_NETWORK_PATTERN = re.compile(
    r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|"
    r"192\.168\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)(?::\d+)?"
)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def today_iso() -> str:
    return dt.date.today().isoformat()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CcopyrightError(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CcopyrightError(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def stable_hash(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return sha256_bytes(encoded)


def _merge_missing(target: dict[str, Any], defaults: dict[str, Any]) -> None:
    for key, default in defaults.items():
        if key not in target:
            target[key] = copy.deepcopy(default)
        elif isinstance(target[key], dict) and isinstance(default, dict):
            _merge_missing(target[key], default)


def upgrade_application(application: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Upgrade an application in memory without replacing user-provided facts."""
    if not isinstance(application, dict):
        return application, False
    upgraded = copy.deepcopy(application)
    original = copy.deepcopy(application)
    software = upgraded.setdefault("software", {})
    if isinstance(software, dict):
        publication = software.get("publication")
        if isinstance(publication, dict) and "location" in publication:
            if not publication.get("region"):
                publication["region"] = publication.get("location", "")
            publication.pop("location", None)
        environment = software.setdefault("environment", {})
        if isinstance(environment, dict):
            legacy_development = software.pop("development_environment", "")
            legacy_runtime = software.pop("runtime_environment", "")
            if legacy_development and not environment.get("development_tools"):
                environment["development_tools"] = legacy_development
            if legacy_runtime and not environment.get("runtime_platform"):
                environment["runtime_platform"] = legacy_runtime
        main_functions = software.get("main_functions")
        if isinstance(main_functions, list):
            software["main_functions"] = "\n".join(
                str(value).strip() for value in main_functions if str(value).strip()
            )
    proof_codes = {
        "Applicant identity document": "applicant-identity",
        "Application confirmation/signature page required by the current portal": "portal-confirmation",
        "Ownership or development agreement when applicable": "other-ownership-proof",
    }
    proof_items = upgraded.get("proof_checklist")
    if isinstance(proof_items, list):
        for item in proof_items:
            if isinstance(item, dict) and not item.get("code"):
                code = proof_codes.get(str(item.get("item", "")))
                if code:
                    item["code"] = code
    defaults = load_json(ASSET_DIR / "application.template.json")
    _merge_missing(upgraded, defaults)
    version = upgraded.get("schema_version", 1)
    if isinstance(version, int) and not isinstance(version, bool) and version <= APPLICATION_SCHEMA_VERSION:
        upgraded["schema_version"] = APPLICATION_SCHEMA_VERSION
    return upgraded, upgraded != original


def application_fingerprint(application: dict[str, Any]) -> str:
    """Hash material-driving facts while ignoring lifecycle bookkeeping."""
    normalized = copy.deepcopy(application)
    normalized.pop("state", None)
    review = normalized.get("review")
    if isinstance(review, dict):
        review.pop("human_reviewed_at", None)
    return stable_hash(normalized)


def finding(
    level: str,
    code: str,
    message: str,
    *,
    path: str = "",
    line: int | None = None,
) -> dict[str, Any]:
    if level not in {"INFO", "WARNING"}:
        raise ValueError("precheck findings may only be INFO or WARNING")
    item: dict[str, Any] = {"level": level, "code": code, "message": message}
    if path:
        item["path"] = path
    if line is not None:
        item["line"] = line
    return item


def is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def safe_relative_path(raw: str, root: Path) -> Path:
    root = root.resolve()
    candidate = Path(raw).expanduser()
    lexical = candidate if candidate.is_absolute() else root / candidate
    lexical = Path(os.path.abspath(lexical))
    try:
        relative = lexical.relative_to(root)
    except ValueError as exc:
        raise CcopyrightError(f"Path escapes repository: {raw}") from exc
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise CcopyrightError(f"Symlink inputs are not accepted: {raw}")
    resolved = lexical.resolve()
    if not is_within(resolved, root):
        raise CcopyrightError(f"Path escapes repository: {raw}")
    return resolved


def relative_posix(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def decode_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8-sig"), False
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), True


def command_output(args: list[str], *, cwd: Path | None = None) -> str:
    try:
        process = subprocess.run(
            args,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""
    return process.stdout.strip()


def command_version(command: str, *version_args: str) -> dict[str, Any]:
    executable = shutil.which(command)
    if not executable:
        return {"available": False, "path": "", "version": ""}
    try:
        process = subprocess.run(
            [executable, *(version_args or ("--version",))],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = (process.stdout or process.stderr).strip()
    except OSError:
        output = ""
    return {"available": True, "path": executable, "version": output.splitlines()[0] if output else "unknown"}


def preflight(chrome: str | None = None) -> dict[str, Any]:
    chrome_path = find_chromium(chrome)
    chrome_version = ""
    if chrome_path:
        chrome_version = command_output([chrome_path, "--version"])
    return {
        "tool_version": TOOL_VERSION,
        "python": {
            "available": True,
            "path": sys.executable,
            "version": sys.version.split()[0],
        },
        "chromium": {
            "available": bool(chrome_path),
            "path": chrome_path or "",
            "version": chrome_version,
        },
        "pdfinfo": command_version("pdfinfo", "-v"),
        "pdftotext": command_version("pdftotext", "-v"),
        "pdftoppm": command_version("pdftoppm", "-v"),
        "git": command_version("git", "--version"),
    }


def scan_sensitive_text(text: str, path: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for line_number, line_text in enumerate(text.splitlines(), start=1):
        for kind, pattern in SECRET_PATTERNS:
            if pattern.search(line_text):
                results.append(
                    finding(
                        "WARNING",
                        "sensitive-value",
                        f"Potential {kind} detected; the value is intentionally omitted.",
                        path=path,
                        line=line_number,
                    )
                )
        if PRIVATE_NETWORK_PATTERN.search(line_text):
            results.append(
                finding(
                    "WARNING",
                    "private-network-reference",
                    "Potential private-network URL detected; review before source disclosure.",
                    path=path,
                    line=line_number,
                )
            )
    return results


def git_inventory(repo: Path) -> dict[str, Any]:
    inside = command_output(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo)
    if inside != "true":
        return {"is_repository": False}
    head = command_output(["git", "rev-parse", "HEAD"], cwd=repo)
    branch = command_output(["git", "branch", "--show-current"], cwd=repo)
    status = command_output(["git", "status", "--porcelain=v1"], cwd=repo)
    commit_date = command_output(
        ["git", "show", "-s", "--format=%cI", "HEAD"], cwd=repo
    )
    submodules_raw = command_output(["git", "submodule", "status", "--recursive"], cwd=repo)
    submodules = []
    for row in submodules_raw.splitlines():
        parts = row.strip().split()
        if len(parts) >= 2:
            submodules.append({"commit": parts[0].lstrip("-+U"), "path": parts[1]})
    return {
        "is_repository": True,
        "head": head,
        "branch": branch,
        "commit_date": commit_date,
        "dirty": bool(status),
        "dirty_entry_count": len(status.splitlines()) if status else 0,
        "submodules": submodules,
    }


def _manifest_suggestions(repo: Path, manifest_paths: Iterable[Path]) -> tuple[list[dict[str, str]], list[str]]:
    suggestions: list[dict[str, str]] = []
    frameworks: set[str] = set()
    for path in manifest_paths:
        lower = path.name.lower()
        try:
            if lower == "package.json":
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data.get("name"), str):
                    suggestions.append({"field": "name", "value": data["name"], "source": relative_posix(path, repo)})
                if isinstance(data.get("version"), str):
                    suggestions.append({"field": "version", "value": data["version"], "source": relative_posix(path, repo)})
                frameworks.add("Node.js")
                dependencies = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                for package, label in {
                    "next": "Next.js",
                    "react": "React",
                    "vue": "Vue",
                    "svelte": "Svelte",
                    "electron": "Electron",
                }.items():
                    if package in dependencies:
                        frameworks.add(label)
            elif lower in {"pyproject.toml", "cargo.toml"}:
                import tomllib

                data = tomllib.loads(path.read_text(encoding="utf-8"))
                section = data.get("project", {}) if lower == "pyproject.toml" else data.get("package", {})
                for field in ("name", "version"):
                    if isinstance(section.get(field), str):
                        suggestions.append({"field": field, "value": section[field], "source": relative_posix(path, repo)})
                frameworks.add("Python" if lower == "pyproject.toml" else "Rust/Cargo")
            elif lower == "go.mod":
                first = path.read_text(encoding="utf-8").splitlines()[0].strip()
                if first.startswith("module "):
                    suggestions.append({"field": "name", "value": first[7:].strip(), "source": relative_posix(path, repo)})
                frameworks.add("Go modules")
            elif lower == "pubspec.yaml":
                text = path.read_text(encoding="utf-8")
                for field in ("name", "version"):
                    match = re.search(rf"(?m)^{field}:\s*['\"]?([^'\"\s#]+)", text)
                    if match:
                        suggestions.append({"field": field, "value": match.group(1), "source": relative_posix(path, repo)})
                frameworks.add("Flutter/Dart")
            elif lower == "project.godot":
                text = path.read_text(encoding="utf-8")
                for config_key, field in (("config/name", "name"), ("config/version", "version")):
                    match = re.search(rf'(?m)^{re.escape(config_key)}\s*=\s*"([^"]+)"', text)
                    if match:
                        suggestions.append({"field": field, "value": match.group(1), "source": relative_posix(path, repo)})
                frameworks.add("Godot")
            elif lower == "pom.xml":
                text = path.read_text(encoding="utf-8")
                artifact = re.search(r"<artifactId>([^<]+)</artifactId>", text)
                version = re.search(r"<version>([^<]+)</version>", text)
                if artifact:
                    suggestions.append({"field": "name", "value": artifact.group(1), "source": relative_posix(path, repo)})
                if version:
                    suggestions.append({"field": "version", "value": version.group(1), "source": relative_posix(path, repo)})
                frameworks.add("Java/Maven")
            elif lower in {"build.gradle", "build.gradle.kts"}:
                frameworks.add("Gradle")
            elif lower == "package.swift":
                frameworks.add("Swift Package Manager")
        except (OSError, UnicodeError, ValueError, IndexError):
            continue
    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in suggestions:
        key = (item["field"], item["value"], item["source"])
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    return deduped, sorted(frameworks)


def scan_repository(
    repo: Path,
    *,
    max_file_bytes: int = 2_000_000,
    excluded_roots: Iterable[Path] = (),
) -> dict[str, Any]:
    repo = repo.resolve()
    if not repo.is_dir():
        raise CcopyrightError(f"Repository directory does not exist: {repo}")
    excluded_root_paths = {path.resolve() for path in excluded_roots}

    sources: list[dict[str, Any]] = []
    documents: list[str] = []
    screenshots: list[str] = []
    manifests: list[str] = []
    manifest_paths: list[Path] = []
    licenses: list[str] = []
    excluded: list[dict[str, str]] = []
    findings: list[dict[str, Any]] = []
    language_totals: dict[str, dict[str, int]] = {}

    for current, directories, files in os.walk(repo, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_directories: list[str] = []
        for directory in sorted(directories):
            child = current_path / directory
            relative = child.relative_to(repo).as_posix()
            if child.is_symlink():
                findings.append(finding("WARNING", "symlink-skipped", "Symlink directory was not traversed.", path=relative))
                excluded.append({"path": relative, "reason": "symlink"})
            elif child.resolve() in excluded_root_paths:
                findings.append(finding("INFO", "workspace-skipped", "Preparation workspace was excluded from repository scanning.", path=relative))
                excluded.append({"path": relative, "reason": "preparation-workspace"})
            elif directory.lower() in SKIP_DIRECTORIES:
                reason = "third-party" if directory.lower() in THIRD_PARTY_DIRECTORIES else "generated-or-cache"
                level = "WARNING" if reason == "third-party" else "INFO"
                findings.append(finding(level, "directory-skipped", f"Directory skipped as {reason} content.", path=relative))
                excluded.append({"path": relative, "reason": reason})
            else:
                kept_directories.append(directory)
        directories[:] = kept_directories

        for filename in sorted(files):
            path = current_path / filename
            relative = path.relative_to(repo).as_posix()
            if path.is_symlink():
                target_inside = is_within(path.resolve(), repo)
                findings.append(
                    finding(
                        "WARNING",
                        "symlink-skipped",
                        "Symlink file was skipped" + ("." if target_inside else " because it resolves outside the repository."),
                        path=relative,
                    )
                )
                excluded.append({"path": relative, "reason": "symlink"})
                continue
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size > max_file_bytes:
                excluded.append({"path": relative, "reason": "file-too-large"})
                findings.append(finding("INFO", "large-file-skipped", f"File exceeds scan limit ({size} bytes).", path=relative))
                continue

            lower_name = filename.lower()
            suffix = path.suffix.lower()
            parts_lower = {part.lower() for part in path.relative_to(repo).parts}
            if lower_name in MANIFEST_NAMES:
                manifests.append(relative)
                manifest_paths.append(path)
            if lower_name in LICENSE_NAMES or lower_name.startswith("license."):
                licenses.append(relative)
            if suffix in SCREENSHOT_EXTENSIONS:
                screenshots.append(relative)
            if suffix in DOCUMENT_EXTENSIONS and (
                lower_name.startswith(("readme", "manual", "guide", "design", "architecture", "spec"))
                or parts_lower & {"doc", "docs", "documentation"}
            ):
                documents.append(relative)

            language = SOURCE_EXTENSIONS.get(suffix)
            additional_sensitive_text = (
                suffix in SENSITIVE_TEXT_EXTENSIONS
                or lower_name == ".env"
                or lower_name.startswith(".env.")
                or lower_name in MANIFEST_NAMES
            )
            if not language and not additional_sensitive_text:
                continue
            try:
                text, replacement_decode = decode_text(path)
            except OSError:
                continue
            if not language:
                findings.extend(scan_sensitive_text(text, relative))
                if replacement_decode:
                    findings.append(finding("WARNING", "encoding-replacement", "Text file was not valid UTF-8 and was decoded with replacement characters.", path=relative))
                continue
            rows = text.splitlines()
            physical = len(rows)
            nonempty = sum(1 for row in rows if row.strip())
            generated = bool(parts_lower & GENERATED_PARTS) or bool(
                re.search(r"(?i)(generated file|auto-generated|do not edit)", "\n".join(rows[:8]))
            )
            test_file = bool(parts_lower & TEST_PARTS) or bool(
                re.search(r"(?i)(?:^|[_\-.])(test|spec)(?:[_\-.]|$)", filename)
            )
            third_party = bool(parts_lower & THIRD_PARTY_DIRECTORIES)
            candidate = not generated and not test_file and not third_party
            entry = {
                "path": relative,
                "language": language,
                "bytes": size,
                "physical_lines": physical,
                "nonempty_lines": nonempty,
                "sha256": sha256_file(path),
                "candidate": candidate,
                "generated": generated,
                "test": test_file,
                "third_party": third_party,
                "decode_replacement": replacement_decode,
            }
            sources.append(entry)
            totals = language_totals.setdefault(language, {"files": 0, "physical_lines": 0, "nonempty_lines": 0})
            totals["files"] += 1
            totals["physical_lines"] += physical
            totals["nonempty_lines"] += nonempty
            if replacement_decode:
                findings.append(finding("WARNING", "encoding-replacement", "Source was not valid UTF-8 and was decoded with replacement characters.", path=relative))
            if generated:
                findings.append(finding("INFO", "generated-source", "Generated-looking source is not proposed as first-party material.", path=relative))
            if test_file:
                findings.append(finding("INFO", "test-source", "Test or fixture source is not proposed by default.", path=relative))
            if candidate:
                findings.extend(scan_sensitive_text(text, relative))

    git = git_inventory(repo)
    if git.get("dirty"):
        findings.append(finding("WARNING", "dirty-worktree", "The Git working tree has uncommitted changes; choose the snapshot mode explicitly."))
    if git.get("submodules"):
        findings.append(finding("INFO", "git-submodules", "Git submodules were detected and are not proposed as first-party source automatically."))
    for license_path in licenses:
        findings.append(finding("INFO", "license-file", "A license or notice file was detected; review third-party and first-party boundaries.", path=license_path))

    suggestions, frameworks = _manifest_suggestions(repo, manifest_paths)
    candidate_sources = [item for item in sources if item["candidate"]]
    findings.sort(key=lambda item: (0 if item["level"] == "WARNING" else 1, item.get("path", ""), item.get("line", 0), item["code"]))
    return {
        "schema_version": 1,
        "generated_at": utc_now(),
        "repository": str(repo),
        "git": git,
        "frameworks": frameworks,
        "manifests": sorted(manifests),
        "version_suggestions": suggestions,
        "languages": dict(sorted(language_totals.items())),
        "sources": sources,
        "candidate_sources": candidate_sources,
        "candidate_totals": {
            "files": len(candidate_sources),
            "physical_lines": sum(item["physical_lines"] for item in candidate_sources),
            "nonempty_lines": sum(item["nonempty_lines"] for item in candidate_sources),
        },
        "documents": sorted(set(documents)),
        "screenshots": sorted(set(screenshots)),
        "licenses": sorted(set(licenses)),
        "excluded": excluded,
        "findings": findings,
        "finding_counts": {
            "INFO": sum(1 for item in findings if item["level"] == "INFO"),
            "WARNING": sum(1 for item in findings if item["level"] == "WARNING"),
        },
    }


def precheck_markdown(inventory: dict[str, Any]) -> str:
    lines = [
        "# Repository precheck",
        "",
        f"Generated: `{inventory['generated_at']}`",
        "",
        "This report contains only INFO and WARNING observations. It is not a legal conclusion and never blocks material generation.",
        "",
        "## Summary",
        "",
        f"- Candidate source files: {inventory['candidate_totals']['files']}",
        f"- Candidate physical lines: {inventory['candidate_totals']['physical_lines']}",
        f"- Candidate non-empty lines: {inventory['candidate_totals']['nonempty_lines']}",
        f"- INFO findings: {inventory['finding_counts']['INFO']}",
        f"- WARNING findings: {inventory['finding_counts']['WARNING']}",
        "",
        "## Findings",
        "",
    ]
    if not inventory["findings"]:
        lines.append("No observations were produced.")
    for item in inventory["findings"]:
        location = item.get("path", "")
        if item.get("line") is not None:
            location += f":{item['line']}"
        suffix = f" — `{location}`" if location else ""
        lines.append(f"- **{item['level']} / {item['code']}**: {item['message']}{suffix}")
    lines.extend(["", "## Candidate source files", ""])
    for item in inventory["candidate_sources"]:
        lines.append(
            f"- `{item['path']}` — {item['language']}, {item['physical_lines']} physical / {item['nonempty_lines']} non-empty lines"
        )
    return "\n".join(lines) + "\n"


def default_application(inventory: dict[str, Any]) -> dict[str, Any]:
    template = load_json(ASSET_DIR / "application.template.json")
    app = copy.deepcopy(template)
    name_suggestion = next((item for item in inventory["version_suggestions"] if item["field"] == "name"), None)
    version_suggestion = next((item for item in inventory["version_suggestions"] if item["field"] == "version"), None)
    if name_suggestion:
        app["software"]["short_name"] = name_suggestion["value"]
    if version_suggestion:
        app["software"]["version"] = version_suggestion["value"]
    app["software"]["programming_languages"] = list(inventory["languages"].keys())
    app["dates"]["material_preparation_date"] = today_iso()
    app["source"]["suggested_files"] = [item["path"] for item in inventory["candidate_sources"]]
    app["source"]["suggested_program_line_count"] = int(
        inventory.get("candidate_totals", {}).get("physical_lines", 0)
    )
    git = inventory.get("git", {})
    if git.get("is_repository"):
        app["snapshot"]["commit"] = git.get("head", "")
        commit_date = git.get("commit_date", "")
        app["dates"]["code_snapshot_date"] = commit_date[:10] if commit_date else ""
    else:
        app["snapshot"]["mode"] = "working-tree"
        app["snapshot"]["include_uncommitted"] = True
    return app


def workspace_paths(workspace: Path) -> dict[str, Path]:
    workspace = workspace.resolve()
    return {
        "root": workspace,
        "facts": workspace / "facts",
        "application": workspace / "facts" / "application.json",
        "requirements": workspace / "facts" / "requirements-snapshot.md",
        "reports": workspace / "reports",
        "inventory": workspace / "reports" / "repository-inventory.json",
        "precheck": workspace / "reports" / "precheck.md",
        "drafts": workspace / "drafts",
        "work": workspace / "work",
        "qa": workspace / "qa",
        "ready": workspace / "ready-to-submit",
    }


def requirements_snapshot_markdown(application: dict[str, Any]) -> str:
    requirements = application.get("requirements", {})
    confirmations = application.get("confirmations", {})
    evidence = requirements.get("portal_evidence", {})
    captured_at = requirements.get("captured_at") or "not confirmed"
    current = isinstance(confirmations, dict) and confirmations.get("requirements.current") is True
    lines = [
        "# Requirements snapshot",
        "",
        f"Current portal captured: `{captured_at}`",
        f"Current portal confirmed by applicant: `{'yes' if current else 'no'}`",
        "",
        "The maintained baseline is not a substitute for the current portal. User-provided current text or redacted screenshots take precedence.",
        "",
        "## Maintained portal-form evidence",
        "",
        f"- Baseline ID: `{evidence.get('baseline_id', '')}`",
        f"- Evidence received: `{evidence.get('received_at', '') or 'unknown'}`",
        f"- Original capture date: `{evidence.get('captured_at', '') or 'unknown'}`",
        f"- Coverage: `{evidence.get('scope', 'unknown')}`",
        f"- Original screenshots retained: `{'yes' if evidence.get('originals_retained') else 'no'}`",
        f"- Personal identity data retained: `{'yes' if evidence.get('personal_data_retained') else 'no'}`",
        "",
        "One supplied screenshot contained applicant identity data. The skill records only the privacy-safe field analysis; it does not retain the image, name, or identity number.",
        "",
        "## Sources",
        "",
    ]
    lines.extend(f"- {url}" for url in requirements.get("source_urls", []))
    lines.extend(
        [
            "",
            "## Configured material rules",
            "",
            f"- Paper: {requirements.get('paper', '')}",
            f"- Program rows per page: {requirements.get('program_lines_per_page', '')}",
            f"- Document rows per page: {requirements.get('document_lines_per_page', '')}",
            f"- Front pages: {requirements.get('front_pages', '')}",
            f"- Back pages: {requirements.get('back_pages', '')}",
            f"- Accepted visible upload formats: {', '.join(requirements.get('accepted_upload_formats', [])) or 'not confirmed'}",
            f"- Maximum PDF bytes: {requirements.get('max_pdf_bytes') or 'not confirmed'}",
            "",
            "## Visible portal field limits",
            "",
            "| Field path | Minimum characters | Maximum characters |",
            "|---|---:|---:|",
        ]
    )
    maximums = requirements.get("portal_field_limits", {})
    minimums = requirements.get("portal_field_minimums", {})
    if isinstance(maximums, dict):
        for field in sorted(maximums):
            lines.append(f"| `{field}` | {minimums.get(field, '') if isinstance(minimums, dict) else ''} | {maximums[field]} |")
    lines.extend(["", "## Unresolved portal constraints", ""])
    unknowns = requirements.get("portal_unknowns", [])
    if isinstance(unknowns, list):
        lines.extend(f"- {value}" for value in unknowns)
    lines.extend(
        [
            "",
            "Do not set `confirmations.requirements.current` to true until these values have been checked against the current portal for this application.",
            "",
        ]
    )
    return "\n".join(lines)


def initialize_workspace(repo: Path, workspace: Path, *, force: bool = False) -> dict[str, Any]:
    repo = repo.resolve()
    workspace = workspace.resolve()
    if repo == workspace:
        raise CcopyrightError("The preparation workspace must not be the repository root.")
    paths = workspace_paths(workspace)
    inventory = scan_repository(repo, excluded_roots=(workspace,))
    for key in ("facts", "reports", "drafts", "work", "qa", "ready"):
        paths[key].mkdir(parents=True, exist_ok=True)
    write_json(paths["inventory"], inventory)
    paths["precheck"].write_text(precheck_markdown(inventory), encoding="utf-8")
    if paths["application"].exists() and not force:
        application, changed = upgrade_application(load_json(paths["application"]))
        if changed:
            write_json(paths["application"], application)
    else:
        application = default_application(inventory)
        write_json(paths["application"], application)
    paths["requirements"].write_text(requirements_snapshot_markdown(application), encoding="utf-8")
    return {"paths": {key: str(value) for key, value in paths.items()}, "inventory": inventory, "application": application}


def nested_value(value: dict[str, Any], dotted: str) -> Any:
    current: Any = value
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


FINAL_REQUIRED_VALUES = [
    "software.full_name",
    "software.version",
    "software.category",
    "software.description.type",
    "software.rights_holders",
    "software.joint_rights_holders",
    "software.completion_date",
    "software.publication.status",
    "software.development_type",
    "software.rights_acquisition",
    "software.rights_scope",
    "software.environment.development_hardware",
    "software.environment.runtime_hardware",
    "software.environment.development_os",
    "software.environment.development_tools",
    "software.environment.runtime_platform",
    "software.environment.supporting_software",
    "software.purpose",
    "software.industry",
    "software.main_functions",
    "requirements.captured_at",
    "source.files",
    "source.program_line_count",
    "source.deposit_type",
    "document.deposit_type",
    "document.sections",
]
FINAL_REQUIRED_CONFIRMATIONS = [
    "software.full_name",
    "software.version",
    "software.classification",
    "software.rights",
    "software.rights_holders",
    "software.completion_date",
    "software.development",
    "software.publication",
    "software.environment",
    "software.functionality",
    "source.selection",
    "source.program_line_count",
    "materials.deposit",
    "document.content",
    "requirements.current",
]


def _relative_config_path(value: str) -> bool:
    try:
        path = Path(value)
        return bool(value) and not path.is_absolute() and not re.match(r"^[A-Za-z]:[\\/]", value) and ".." not in path.parts and "\x00" not in value
    except (OSError, ValueError):
        return False


def application_validation_errors(application: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    schema_version = application.get("schema_version")
    if schema_version != APPLICATION_SCHEMA_VERSION:
        errors.append(f"schema_version must be {APPLICATION_SCHEMA_VERSION}.")
    software = application.get("software")
    if not isinstance(software, dict):
        return ["software must be an object."]
    for field in ("full_name", "short_name", "version", "completion_date"):
        value = software.get(field)
        if value not in (None, "") and not isinstance(value, str):
            errors.append(f"software.{field} must be a string.")
        if isinstance(value, str) and ("\n" in value or "\r" in value):
            errors.append(f"software.{field} must be a single line.")
    completion_date = software.get("completion_date")
    if isinstance(completion_date, str) and completion_date:
        try:
            parsed_completion = dt.date.fromisoformat(completion_date)
            if parsed_completion.isoformat() != completion_date:
                raise ValueError
            if parsed_completion > dt.date.today():
                errors.append("software.completion_date must not be in the future.")
        except ValueError:
            errors.append("software.completion_date must use YYYY-MM-DD.")
    holders = software.get("rights_holders")
    if holders not in (None, []) and not isinstance(holders, list):
        errors.append("software.rights_holders must be a list.")
    elif isinstance(holders, list):
        normalized_holders = [str(value).strip() for value in holders]
        if any(not isinstance(value, str) or not value.strip() for value in holders):
            errors.append("software.rights_holders entries must be non-empty strings.")
        if len(normalized_holders) != len(set(normalized_holders)):
            errors.append("software.rights_holders must not contain duplicates.")
    joint_holders = software.get("joint_rights_holders")
    if joint_holders is not None and not isinstance(joint_holders, bool):
        errors.append("software.joint_rights_holders must be null or boolean.")
    enum_fields = {
        "category": set(SOFTWARE_CATEGORY_LABELS),
        "development_type": set(DEVELOPMENT_TYPE_LABELS),
        "rights_acquisition": set(RIGHTS_ACQUISITION_LABELS),
        "rights_scope": set(RIGHTS_SCOPE_LABELS),
    }
    for field, allowed in enum_fields.items():
        value = software.get(field)
        if value not in allowed | {"unconfirmed"}:
            errors.append(f"software.{field} must be one of: {', '.join(sorted(allowed))}, or unconfirmed.")
    description = software.get("description")
    if not isinstance(description, dict):
        errors.append("software.description must be an object.")
    else:
        description_type = description.get("type")
        if description_type not in set(SOFTWARE_DESCRIPTION_LABELS) | {"unconfirmed"}:
            errors.append("software.description.type must be original, modified, or unconfirmed.")
        modification_basis = description.get("modification_basis")
        if modification_basis not in MODIFICATION_BASIS_LABELS:
            errors.append(
                "software.description.modification_basis must be not-applicable, registered, authorization-required, or unconfirmed."
            )
        if not isinstance(description.get("modification_summary", ""), str):
            errors.append("software.description.modification_summary must be a string.")
    publication = software.get("publication", {})
    if not isinstance(publication, dict):
        errors.append("software.publication must be an object.")
    else:
        if publication.get("status") not in set(PUBLICATION_STATUS_LABELS) | {"unconfirmed"}:
            errors.append("software.publication.status must be published, unpublished, or unconfirmed.")
        if publication.get("date"):
            try:
                value = str(publication["date"])
                if dt.date.fromisoformat(value).isoformat() != value:
                    raise ValueError
            except ValueError:
                errors.append("software.publication.date must use YYYY-MM-DD when supplied.")
        for field in ("country", "region"):
            if not isinstance(publication.get(field, ""), str):
                errors.append(f"software.publication.{field} must be a string.")
    environment = software.get("environment")
    if not isinstance(environment, dict):
        errors.append("software.environment must be an object.")
    else:
        for field in ENVIRONMENT_FIELDS:
            if not isinstance(environment.get(field, ""), str):
                errors.append(f"software.environment.{field} must be a string.")
    for field in (
        "other_programming_languages",
        "rights_acquisition_details",
        "rights_scope_details",
        "purpose",
        "industry",
        "other_technical_features",
        "main_functions",
        "competitive_advantages",
        "commercial_value",
    ):
        if not isinstance(software.get(field, ""), str):
            errors.append(f"software.{field} must be a string.")
    for field in ("programming_languages", "technical_features"):
        values = software.get(field)
        if not isinstance(values, list) or any(not isinstance(value, str) or not value.strip() for value in values):
            errors.append(f"software.{field} must be a list of non-empty strings.")
        elif len(values) != len(set(values)):
            errors.append(f"software.{field} must not contain duplicates.")

    dates = application.get("dates", {})
    if not isinstance(dates, dict):
        errors.append("dates must be an object.")
    else:
        for field in ("code_snapshot_date", "material_preparation_date"):
            value = dates.get(field)
            if value:
                try:
                    text = str(value)
                    if dt.date.fromisoformat(text).isoformat() != text:
                        raise ValueError
                except ValueError:
                    errors.append(f"dates.{field} must use YYYY-MM-DD when supplied.")

    snapshot = application.get("snapshot", {})
    if not isinstance(snapshot, dict):
        errors.append("snapshot must be an object.")
    else:
        mode = str(snapshot.get("mode", "")).lower().replace("_", "-")
        if mode not in {"head", "commit", "working-tree", "worktree"}:
            errors.append("snapshot.mode must be head, commit, or working-tree.")
        if not isinstance(snapshot.get("include_uncommitted", False), bool):
            errors.append("snapshot.include_uncommitted must be boolean.")

    requirements = application.get("requirements")
    if not isinstance(requirements, dict):
        errors.append("requirements must be an object.")
    else:
        if requirements.get("paper") != "A4":
            errors.append("requirements.paper must be A4; the current renderer supports A4 only.")
        for field in ("program_lines_per_page", "document_lines_per_page", "front_pages", "back_pages"):
            value = requirements.get(field)
            minimum = 1 if field in {"program_lines_per_page", "document_lines_per_page"} else 0
            if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
                errors.append(f"requirements.{field} must be an integer >= {minimum}.")
        front_pages = requirements.get("front_pages")
        back_pages = requirements.get("back_pages")
        if (
            isinstance(front_pages, int)
            and not isinstance(front_pages, bool)
            and isinstance(back_pages, int)
            and not isinstance(back_pages, bool)
            and front_pages + back_pages <= 0
        ):
            errors.append("requirements.front_pages and back_pages must provide positive total capacity.")
        captured_at = requirements.get("captured_at")
        if captured_at:
            try:
                text = str(captured_at)
                if dt.date.fromisoformat(text).isoformat() != text:
                    raise ValueError
            except ValueError:
                errors.append("requirements.captured_at must use YYYY-MM-DD when supplied.")
        source_urls = requirements.get("source_urls", [])
        if not isinstance(source_urls, list) or any(not isinstance(value, str) for value in source_urls):
            errors.append("requirements.source_urls must be a list of strings.")
        max_bytes = requirements.get("max_pdf_bytes")
        if max_bytes is not None and (not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes <= 0):
            errors.append("requirements.max_pdf_bytes must be null or a positive integer.")
        accepted_formats = requirements.get("accepted_upload_formats", [])
        if not isinstance(accepted_formats, list) or any(not isinstance(value, str) or not value for value in accepted_formats):
            errors.append("requirements.accepted_upload_formats must be a list of non-empty strings.")
        for field in ("portal_field_limits", "portal_field_minimums"):
            limits = requirements.get(field, {})
            if not isinstance(limits, dict) or any(
                not isinstance(key, str)
                or not isinstance(value, int)
                or isinstance(value, bool)
                or value < 0
                for key, value in limits.items()
            ):
                errors.append(f"requirements.{field} must map field paths to non-negative integers.")
        evidence = requirements.get("portal_evidence", {})
        if not isinstance(evidence, dict):
            errors.append("requirements.portal_evidence must be an object.")
        else:
            if evidence.get("originals_retained") is not False:
                errors.append("requirements.portal_evidence.originals_retained must remain false.")
            if evidence.get("personal_data_retained") is not False:
                errors.append("requirements.portal_evidence.personal_data_retained must remain false.")

    source = application.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object.")
    else:
        mode = str(source.get("mode", "")).lower().replace("_", "-")
        if mode not in {"auto", "whole", "front-back"}:
            errors.append("source.mode must be auto, whole, or front-back.")
        files = source.get("files")
        if files not in (None, []) and not isinstance(files, list):
            errors.append("source.files must be a list.")
        elif isinstance(files, list):
            if any(not isinstance(value, str) or not _relative_config_path(value) for value in files):
                errors.append("source.files entries must be non-empty repository-relative paths without '..'.")
            if len(files) != len(set(files)):
                errors.append("source.files must not contain duplicates.")
        if source.get("deposit_type") not in DEPOSIT_TYPE_LABELS:
            errors.append("source.deposit_type must be general or exceptional.")
        program_line_count = source.get("program_line_count")
        if program_line_count is not None and (
            not isinstance(program_line_count, int)
            or isinstance(program_line_count, bool)
            or program_line_count <= 0
        ):
            errors.append("source.program_line_count must be null or a positive integer.")
        if source.get("program_line_count_basis") not in SOURCE_LINE_COUNT_BASES:
            errors.append(
                "source.program_line_count_basis must be selected-source-physical-lines or applicant-confirmed-total."
            )

    document = application.get("document")
    if not isinstance(document, dict):
        errors.append("document must be an object.")
    else:
        if document.get("deposit_type") not in DEPOSIT_TYPE_LABELS:
            errors.append("document.deposit_type must be general or exceptional.")
        max_units = document.get("max_display_units_per_line", 72)
        if not isinstance(max_units, int) or isinstance(max_units, bool) or max_units < 20:
            errors.append("document.max_display_units_per_line must be an integer >= 20.")
        sections = document.get("sections")
        if sections not in (None, []) and not isinstance(sections, list):
            errors.append("document.sections must be a list.")
        elif isinstance(sections, list):
            for index, section in enumerate(sections):
                if not isinstance(section, dict):
                    errors.append(f"document.sections[{index}] must be an object.")
                    continue
                if not isinstance(section.get("paragraphs", []), list) or any(not isinstance(value, str) for value in section.get("paragraphs", [])):
                    errors.append(f"document.sections[{index}].paragraphs must be a list of strings.")
                evidence = section.get("evidence", [])
                if not isinstance(evidence, list) or any(not isinstance(value, str) or not _relative_config_path(value) for value in evidence):
                    errors.append(f"document.sections[{index}].evidence must contain repository-relative paths.")
        screenshots = document.get("screenshots", [])
        if not isinstance(screenshots, list):
            errors.append("document.screenshots must be a list.")
        else:
            for index, screenshot in enumerate(screenshots):
                if not isinstance(screenshot, dict):
                    errors.append(f"document.screenshots[{index}] must be an object.")
                    continue
                raw_path = screenshot.get("path")
                if not isinstance(raw_path, str) or not _relative_config_path(raw_path):
                    errors.append(f"document.screenshots[{index}].path must be repository-relative.")
                page = screenshot.get("page", index + 1)
                if not isinstance(page, int) or isinstance(page, bool) or page < 1:
                    errors.append(f"document.screenshots[{index}].page must be a positive integer.")
        additional_documents = document.get("additional_documents", [])
        if not isinstance(additional_documents, list) or any(not isinstance(value, dict) for value in additional_documents):
            errors.append("document.additional_documents must be a list of objects.")

    confirmations = application.get("confirmations")
    if confirmations is not None and not isinstance(confirmations, dict):
        errors.append("confirmations must be an object.")
    elif isinstance(confirmations, dict):
        for key, value in confirmations.items():
            if not isinstance(value, bool):
                errors.append(f"confirmations.{key} must be boolean.")
    return list(dict.fromkeys(errors))


def _missing_portal_values(application: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for dotted in FINAL_REQUIRED_VALUES:
        value = nested_value(application, dotted)
        if value is None or value == "" or value == [] or value == "unconfirmed":
            missing.append(dotted)
    software = application.get("software", {})
    publication = software.get("publication", {}) if isinstance(software, dict) else {}
    if isinstance(publication, dict) and publication.get("status") == "published":
        for field in ("date", "country", "region"):
            if not publication.get(field):
                missing.append(f"software.publication.{field}")
    description = software.get("description", {}) if isinstance(software, dict) else {}
    if isinstance(description, dict) and description.get("type") == "modified":
        if not description.get("modification_summary"):
            missing.append("software.description.modification_summary")
        if description.get("modification_basis") in {None, "", "unconfirmed", "not-applicable"}:
            missing.append("software.description.modification_basis")
    if isinstance(software, dict):
        languages = software.get("programming_languages", [])
        if not languages and not str(software.get("other_programming_languages", "")).strip():
            missing.append("software.programming_languages")
        features = software.get("technical_features", [])
        if not features and not str(software.get("other_technical_features", "")).strip():
            missing.append("software.technical_features")
        if software.get("rights_acquisition") == "successor" and not str(
            software.get("rights_acquisition_details", "")
        ).strip():
            missing.append("software.rights_acquisition_details")
        if software.get("rights_scope") == "partial" and not str(
            software.get("rights_scope_details", "")
        ).strip():
            missing.append("software.rights_scope_details")
    return list(dict.fromkeys(missing))


def portal_constraint_violations(application: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    software = application.get("software", {})
    requirements = application.get("requirements", {})
    if isinstance(requirements, dict):
        maximums = requirements.get("portal_field_limits", {})
        minimums = requirements.get("portal_field_minimums", {})
        if isinstance(maximums, dict):
            for field, maximum in maximums.items():
                value = nested_value(application, field)
                if isinstance(value, str) and isinstance(maximum, int) and len(value) > maximum:
                    violations.append(f"{field} has {len(value)} characters; visible portal maximum is {maximum}.")
        if isinstance(minimums, dict):
            for field, minimum in minimums.items():
                value = nested_value(application, field)
                if isinstance(value, str) and value and isinstance(minimum, int) and len(value) < minimum:
                    violations.append(f"{field} has {len(value)} characters; visible portal minimum is {minimum}.")
    if isinstance(software, dict):
        holders = software.get("rights_holders", [])
        joint = software.get("joint_rights_holders")
        if isinstance(holders, list) and holders:
            if len(holders) > 1 and joint is not True:
                violations.append("software.joint_rights_holders must be true when more than one rights holder is listed.")
            if len(holders) == 1 and joint is True:
                violations.append("software.joint_rights_holders must be false when exactly one rights holder is listed.")
    source = application.get("source", {})
    document = application.get("document", {})
    if isinstance(source, dict) and source.get("deposit_type") == "exceptional":
        violations.append("Exceptional program deposit is outside this ordinary-deposit workflow.")
    if isinstance(document, dict) and document.get("deposit_type") == "exceptional":
        violations.append("Exceptional document deposit is outside this ordinary-deposit workflow.")
    return list(dict.fromkeys(violations))


def application_status(application: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(application, dict):
        return {
            "state": "draft",
            "missing_required_values": ["application"],
            "unconfirmed_required_facts": list(FINAL_REQUIRED_CONFIRMATIONS),
            "invalid_required_values": ["Application JSON root must be an object."],
            "portal_constraint_violations": [],
            "final_complete": False,
        }
    application, upgraded = upgrade_application(application)
    missing = _missing_portal_values(application)
    confirmations = application.get("confirmations", {})
    unconfirmed = [key for key in FINAL_REQUIRED_CONFIRMATIONS if not isinstance(confirmations, dict) or confirmations.get(key) is not True]
    invalid = application_validation_errors(application)
    portal_violations = portal_constraint_violations(application)
    return {
        "state": application.get("state", "draft"),
        "schema_version": application.get("schema_version"),
        "schema_upgraded_in_memory": upgraded,
        "missing_required_values": missing,
        "unconfirmed_required_facts": unconfirmed,
        "invalid_required_values": invalid,
        "portal_constraint_violations": portal_violations,
        "final_complete": not missing and not unconfirmed and not invalid and not portal_violations,
    }


def canonical_identity(application: dict[str, Any], *, final: bool) -> dict[str, str]:
    software = application.get("software", {})
    full_name = str(software.get("full_name", "")).strip()
    version = str(software.get("version", "")).strip()
    rights_holders = software.get("rights_holders", [])
    if not isinstance(rights_holders, list):
        rights_holders = []
    holder = "、".join(str(value).strip() for value in rights_holders if str(value).strip())
    if not final:
        full_name = full_name or "[UNCONFIRMED SOFTWARE NAME]"
        version = version or "[UNCONFIRMED VERSION]"
        holder = holder or "[UNCONFIRMED RIGHTS HOLDER]"
    return {"full_name": full_name, "version": version, "rights_holder": holder}


def safe_filename(value: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", value).strip(" .")
    return cleaned or "software"


def display_width(value: str) -> int:
    units = 0
    for char in value:
        if char == "\t":
            units += 4 - (units % 4)
        else:
            units += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
    return units


def markdown_fence(rows: Iterable[dict[str, Any]]) -> str:
    longest = 0
    for row in rows:
        for match in re.finditer(r"`+", str(row.get("text", ""))):
            longest = max(longest, len(match.group(0)))
    return "`" * max(3, longest + 1)


def wrap_display(value: str, max_units: int) -> list[str]:
    value = value.strip()
    if not value:
        return []
    rows: list[str] = []
    current: list[str] = []
    units = 0
    for char in value:
        width = 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
        if current and units + width > max_units:
            rows.append("".join(current).rstrip())
            current = []
            units = 0
            if char.isspace():
                continue
        current.append(char)
        units += width
    if current:
        rows.append("".join(current).rstrip())
    return rows


def read_selected_source(repo: Path, files: list[str]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    stream: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    stream_index = 1
    for raw_path in files:
        path = safe_relative_path(raw_path, repo)
        if not path.is_file():
            raise CcopyrightError(f"Selected source file does not exist: {raw_path}")
        text, replacement_decode = decode_text(path)
        relative = relative_posix(path, repo)
        if replacement_decode:
            warnings.append(finding("WARNING", "encoding-replacement", "Selected source was decoded with replacement characters.", path=relative))
        warnings.extend(scan_sensitive_text(text, relative))
        for original_line, row in enumerate(text.splitlines(), start=1):
            stream.append(
                {
                    "stream_index": stream_index,
                    "path": relative,
                    "original_line": original_line,
                    "text": row,
                    "row_sha256": sha256_bytes(f"{relative}\0{original_line}\0{row}".encode("utf-8")),
                }
            )
            stream_index += 1
    return stream, warnings


def source_snapshot_status(
    repo: Path,
    files: list[str],
    snapshot: dict[str, Any],
) -> dict[str, Any]:
    normalized_files = [relative_posix(safe_relative_path(raw, repo), repo) for raw in files]
    mode = str(snapshot.get("mode", "working-tree")).lower().replace("_", "-")
    commit = str(snapshot.get("commit", "")).strip()
    include_uncommitted = bool(snapshot.get("include_uncommitted", False))
    problems: list[str] = []
    if mode in {"working-tree", "worktree"} or include_uncommitted:
        return {
            "basis": "working-tree",
            "commit": commit,
            "include_uncommitted": include_uncommitted,
            "consistent": True,
            "problems": [],
        }
    if mode not in {"head", "commit"}:
        problems.append(f"Unsupported snapshot mode: {mode}")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", commit):
        problems.append("Snapshot commit must be a 7-64 character hexadecimal commit ID.")
    if command_output(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo) != "true":
        problems.append("Repository is not a Git working tree; use working-tree snapshot mode.")
    if problems:
        return {
            "basis": "git-commit",
            "commit": commit,
            "include_uncommitted": False,
            "consistent": False,
            "problems": problems,
        }
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=repo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if commit_check.returncode != 0:
        problems.append("Snapshot commit does not resolve in this repository.")
    else:
        for relative in normalized_files:
            tracked = subprocess.run(
                ["git", "cat-file", "-e", f"{commit}:{relative}"],
                cwd=repo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if tracked.returncode != 0:
                problems.append(f"Selected source is not present at the snapshot commit: {relative}")
                continue
            compared = subprocess.run(
                ["git", "diff", "--quiet", commit, "--", relative],
                cwd=repo,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if compared.returncode == 1:
                problems.append(f"Selected source differs from the snapshot commit: {relative}")
            elif compared.returncode != 0:
                problems.append(f"Git could not compare selected source with the snapshot: {relative}")
    return {
        "basis": "git-commit",
        "commit": commit,
        "include_uncommitted": False,
        "consistent": not problems,
        "problems": problems,
    }


def select_source_rows(stream: list[dict[str, Any]], requirements: dict[str, Any], mode: str) -> tuple[list[dict[str, Any]], str]:
    lines_per_page = int(requirements["program_lines_per_page"])
    front_rows = int(requirements["front_pages"]) * lines_per_page
    back_rows = int(requirements["back_pages"]) * lines_per_page
    capacity = front_rows + back_rows
    if capacity <= 0:
        raise CcopyrightError("Configured front/back source capacity must be greater than zero.")
    normalized_mode = mode.lower().replace("_", "-")
    if normalized_mode == "auto":
        normalized_mode = "whole" if len(stream) <= capacity else "front-back"
    if normalized_mode == "whole":
        return list(stream), "whole"
    if normalized_mode != "front-back":
        raise CcopyrightError(f"Unsupported source selection mode: {mode}")
    if len(stream) <= capacity:
        return list(stream), "whole"
    tail = list(stream[-back_rows:]) if back_rows else []
    return list(stream[:front_rows]) + tail, "front-back"


def _css() -> str:
    return (ASSET_DIR / "material.css").read_text(encoding="utf-8")


def _html_document(title: str, pages: list[str]) -> str:
    return (
        "<!doctype html><html lang=\"zh-CN\"><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(title)}</title><style>{_css()}</style></head><body>"
        + "".join(pages)
        + "</body></html>"
    )


def _header(identity: dict[str, str]) -> str:
    return (
        '<header class="header"><div class="identity">'
        f"{html.escape(identity['full_name'])}　{html.escape(identity['version'])}"
        '</div><div class="holder">著作权人：'
        f"{html.escape(identity['rights_holder'])}</div></header>"
    )


def _footer(label: str, current: int, total: int) -> str:
    return (
        '<footer class="footer"><span>'
        f"{html.escape(label)}</span><span>第 {current:02d} / {total:02d} 页</span></footer>"
    )


def _draft_mark(final: bool) -> str:
    return "" if final else '<div class="draft-mark">DRAFT</div>'


def _page_chunks(rows: list[Any], size: int) -> list[list[Any]]:
    return [rows[index : index + size] for index in range(0, len(rows), size)] or [[]]


def build_program_material(
    repo: Path,
    application: dict[str, Any],
    work_dir: Path,
    *,
    final: bool,
) -> dict[str, Any]:
    source_config = application["source"]
    files = source_config.get("files", [])
    if not files:
        files = source_config.get("suggested_files", []) if not final else []
    if not files:
        raise CcopyrightError("No source files selected. Add ordered paths to source.files.")
    normalized_files = [relative_posix(safe_relative_path(str(raw), repo), repo) for raw in files]
    if len(normalized_files) != len(set(normalized_files)):
        raise CcopyrightError("source.files contains duplicate paths; each selected file must appear once.")
    stream, warnings = read_selected_source(repo, normalized_files)
    reported_line_count = source_config.get("program_line_count")
    line_count_basis = source_config.get(
        "program_line_count_basis", "selected-source-physical-lines"
    )
    if (
        line_count_basis == "selected-source-physical-lines"
        and isinstance(reported_line_count, int)
        and not isinstance(reported_line_count, bool)
        and reported_line_count != len(stream)
    ):
        message = (
            f"Reported source-program line count is {reported_line_count}, but the selected "
            f"source stream contains {len(stream)} physical lines."
        )
        if final:
            raise CcopyrightError(message)
        warnings.append(finding("WARNING", "source-line-count-mismatch", message))
    snapshot_status = source_snapshot_status(
        repo,
        normalized_files,
        application.get("snapshot", {}),
    )
    if snapshot_status["problems"]:
        if final:
            raise CcopyrightError(
                "Selected source does not match the configured snapshot: "
                + "; ".join(snapshot_status["problems"])
            )
        warnings.extend(
            finding("WARNING", "snapshot-mismatch", problem)
            for problem in snapshot_status["problems"]
        )
    selected, selection_mode = select_source_rows(stream, application["requirements"], source_config.get("mode", "auto"))
    if not selected:
        raise CcopyrightError("Selected source files contain no printable lines.")
    lines_per_page = int(application["requirements"]["program_lines_per_page"])
    pages_data = _page_chunks(selected, lines_per_page)
    identity = canonical_identity(application, final=final)
    snapshot = application.get("snapshot", {})
    snapshot_date = application.get("dates", {}).get("code_snapshot_date", "")
    manifest_rows: list[dict[str, Any]] = []
    markdown = [
        f"# {identity['full_name']} {identity['version']} 程序鉴别材料",
        "",
        f"- 著作权人：{identity['rights_holder']}",
        f"- 代码快照：{snapshot.get('commit', '')}",
        f"- 快照日期：{snapshot_date}",
        f"- 选择方式：{selection_mode}",
        f"- 每页源程序行：{lines_per_page}",
        "",
    ]
    pages_html: list[str] = []
    total_pages = len(pages_data)
    fence = markdown_fence(selected)
    selected_sequence = 1
    for page_index, page_rows in enumerate(pages_data, start=1):
        files_on_page: list[str] = []
        html_rows: list[str] = []
        markdown.extend([f"## 第 {page_index:02d}/{total_pages:02d} 页", "", f"{fence}text"])
        nonempty = 0
        for row in page_rows:
            if not files_on_page or files_on_page[-1] != row["path"]:
                files_on_page.append(row["path"])
            material_id = f"P{selected_sequence:06d}"
            text = row["text"]
            if text.strip():
                nonempty += 1
            units = max(display_width(text), 1)
            font_size = min(5.4, max(3.0, 5.4 * 136 / units))
            if font_size <= 3.0 and units > 245:
                warnings.append(finding("WARNING", "very-long-source-line", "A selected source line may require visual review at the minimum font size.", path=row["path"], line=row["original_line"]))
            html_rows.append(
                '<li class="row"><span class="row-id">'
                f"{material_id}</span><span class=\"code\" style=\"font-size:{font_size:.2f}pt\">"
                f"{html.escape(text, quote=False)}</span></li>"
            )
            markdown.append(f"{material_id}  {text}")
            manifest_rows.append(
                {
                    "material_id": material_id,
                    "page": page_index,
                    "stream_index": row["stream_index"],
                    "path": row["path"],
                    "original_line": row["original_line"],
                    "row_sha256": row["row_sha256"],
                    "nonempty": bool(text.strip()),
                }
            )
            selected_sequence += 1
        markdown.extend([fence, ""])
        meta = (
            f"{selection_mode}｜材料第{page_index:02d}/{total_pages:02d}页｜"
            f"打印行{len(page_rows)}｜非空行{nonempty}｜{' → '.join(files_on_page)}"
        )
        row_height = 241.5 / max(lines_per_page, 1)
        pages_html.append(
            '<section class="page program">'
            + _draft_mark(final)
            + _header(identity)
            + '<main class="content"><div class="meta">'
            + html.escape(meta)
            + '</div><ol class="rows">'
            + "".join(row.replace('class="row"', f'class="row" style="height:{row_height:.3f}mm;line-height:{row_height:.3f}mm"', 1) for row in html_rows)
            + "</ol></main>"
            + _footer("程序鉴别材料", page_index, total_pages)
            + "</section>"
        )
    work_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_filename(f"{identity['full_name']}{identity['version']}程序鉴别材料")
    md_path = work_dir / f"{stem}.md"
    html_path = work_dir / f"{stem}.html"
    manifest_path = work_dir / "program-manifest.json"
    md_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    html_path.write_text(_html_document(stem, pages_html), encoding="utf-8")
    physical_lines_by_file: dict[str, int] = {}
    for row in stream:
        physical_lines_by_file[row["path"]] = physical_lines_by_file.get(row["path"], 0) + 1
    manifest = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "final": final,
        "identity": identity,
        "snapshot": snapshot,
        "snapshot_status": snapshot_status,
        "snapshot_date": snapshot_date,
        "selection_mode": selection_mode,
        "ordered_files": normalized_files,
        "source_files": [
            {
                "path": relative,
                "bytes": (repo / relative).stat().st_size,
                "sha256": sha256_file(repo / relative),
                "physical_lines": physical_lines_by_file.get(relative, 0),
            }
            for relative in normalized_files
        ],
        "source_stream_rows": len(stream),
        "reported_source_program_lines": reported_line_count,
        "source_program_line_count_basis": line_count_basis,
        "selected_rows": len(selected),
        "lines_per_page": lines_per_page,
        "pages": total_pages,
        "rows": manifest_rows,
        "warnings": warnings,
        "outputs": {"markdown": md_path.name, "html": html_path.name},
    }
    write_json(manifest_path, manifest)
    return {"markdown": md_path, "html": html_path, "manifest": manifest_path, "data": manifest}


def _choice_label(labels: dict[str, str], value: Any) -> str:
    text = str(value or "")
    return labels.get(text, text)


def build_worksheet(
    application: dict[str, Any],
    drafts_dir: Path,
    *,
    program_data: dict[str, Any] | None = None,
) -> Path:
    software = application["software"]
    publication = software.get("publication", {})
    description = software.get("description", {})
    environment = software.get("environment", {})
    source = application.get("source", {})
    document = application.get("document", {})
    requirements = application.get("requirements", {})
    confirmations = application.get("confirmations", {})
    limits = requirements.get("portal_field_limits", {})
    minimums = requirements.get("portal_field_minimums", {})
    languages = list(software.get("programming_languages", []))
    features = list(software.get("technical_features", []))
    rows: list[tuple[str, Any, str | None, str | None]] = [
        ("权利取得方式", _choice_label(RIGHTS_ACQUISITION_LABELS, software.get("rights_acquisition")), "software.rights", "software.rights_acquisition"),
        ("继受取得说明", software.get("rights_acquisition_details", ""), "software.rights", None),
        ("软件全称", software.get("full_name", ""), "software.full_name", "software.full_name"),
        ("软件简称（可选；无简称时留空）", software.get("short_name", ""), None, "software.short_name"),
        ("版本号", software.get("version", ""), "software.version", "software.version"),
        ("权利范围", _choice_label(RIGHTS_SCOPE_LABELS, software.get("rights_scope")), "software.rights", "software.rights_scope"),
        ("部分权利说明", software.get("rights_scope_details", ""), "software.rights", None),
        ("软件分类", _choice_label(SOFTWARE_CATEGORY_LABELS, software.get("category")), "software.classification", "software.category"),
        ("软件说明", _choice_label(SOFTWARE_DESCRIPTION_LABELS, description.get("type")), "software.classification", "software.description.type"),
        ("修改、合成或翻译说明", description.get("modification_summary", ""), "software.classification", "software.description.modification_summary"),
        ("修改软件依据", _choice_label(MODIFICATION_BASIS_LABELS, description.get("modification_basis")), "software.classification", "software.description.modification_basis"),
        ("开发方式", _choice_label(DEVELOPMENT_TYPE_LABELS, software.get("development_type")), "software.development", "software.development_type"),
        ("开发完成日期", software.get("completion_date", ""), "software.completion_date", "software.completion_date"),
        ("发表状态", _choice_label(PUBLICATION_STATUS_LABELS, publication.get("status")), "software.publication", "software.publication.status"),
        ("首次发表日期", publication.get("date", ""), "software.publication", "software.publication.date"),
        ("首次发表国家", publication.get("country", ""), "software.publication", "software.publication.country"),
        ("首次发表地区", publication.get("region", ""), "software.publication", "software.publication.region"),
        ("开发的硬件环境", environment.get("development_hardware", ""), "software.environment", "software.environment.development_hardware"),
        ("运行的硬件环境", environment.get("runtime_hardware", ""), "software.environment", "software.environment.runtime_hardware"),
        ("开发该软件的操作系统", environment.get("development_os", ""), "software.environment", "software.environment.development_os"),
        ("软件开发环境/开发工具", environment.get("development_tools", ""), "software.environment", "software.environment.development_tools"),
        ("软件运行平台/操作系统", environment.get("runtime_platform", ""), "software.environment", "software.environment.runtime_platform"),
        ("软件运行支持环境/支持软件", environment.get("supporting_software", ""), "software.environment", "software.environment.supporting_software"),
        ("编程语言（门户选项）", "、".join(languages), "software.environment", None),
        ("其他编程语言", software.get("other_programming_languages", ""), "software.environment", "software.other_programming_languages"),
        ("源程序量（行）", source.get("program_line_count", ""), "source.program_line_count", None),
        ("开发目的", software.get("purpose", ""), "software.functionality", "software.purpose"),
        ("面向领域/行业", software.get("industry", ""), "software.functionality", "software.industry"),
        ("软件技术特点（门户标签）", "、".join(features), "software.functionality", None),
        ("其他技术特点", software.get("other_technical_features", ""), "software.functionality", "software.other_technical_features"),
        ("程序鉴别材料交存方式", _choice_label(DEPOSIT_TYPE_LABELS, source.get("deposit_type")), "materials.deposit", None),
        ("文档鉴别材料交存方式", _choice_label(DEPOSIT_TYPE_LABELS, document.get("deposit_type")), "materials.deposit", None),
        ("著作权人", "、".join(software.get("rights_holders", [])), "software.rights_holders", None),
        ("多个著作权人共同享有", "是" if software.get("joint_rights_holders") is True else "否" if software.get("joint_rights_holders") is False else "待确认", "software.rights", None),
    ]
    lines = [
        "# 软件著作权登记申请表填写底稿",
        "",
        "本文件用于人工复制到当前门户，不执行浏览器填写。提交前必须逐项核对门户文字和选项。",
        "",
        "著作权人证件号码、证件扫描件和未脱敏门户截图不得写入本文件或仓库。",
        "",
        "| 门户字段 | 建议值 | 字符数 | 可见限制 | 状态 |",
        "|---|---|---:|---|---|",
    ]
    for label, value, confirmation_key, limit_key in rows:
        text = str(value if value is not None else "")
        escaped = text.replace("|", "\\|").replace("\n", "<br>")
        if limit_key and isinstance(limits, dict) and limit_key in limits:
            minimum = minimums.get(limit_key) if isinstance(minimums, dict) else None
            visible_limit = f"{minimum}–{limits[limit_key]}" if minimum else f"≤ {limits[limit_key]}"
        else:
            visible_limit = "未见/不适用"
        if confirmation_key is None:
            state = "optional/review"
        else:
            state = "confirmed" if confirmations.get(confirmation_key) is True else "review"
        lines.append(f"| {label} | {escaped} | {len(text)} | {visible_limit} | {state} |")
    reported = source.get("program_line_count")
    computed = program_data.get("source_stream_rows") if isinstance(program_data, dict) else None
    lines.extend(
        [
            "",
            "## 源程序量核对",
            "",
            f"- 申报值：`{reported if reported is not None else '待确认'}` 行",
            f"- 所选源码物理行数：`{computed if computed is not None else '尚未生成'}` 行",
            f"- 统计依据：`{source.get('program_line_count_basis', '')}`",
            "",
            "采用 `selected-source-physical-lines` 时，两者必须一致；采用申请人确认总量时，需由申请人解释仓库选择与申报总量的边界。",
            "",
            "## 软件的主要功能",
            "",
        ]
    )
    main_functions = str(software.get("main_functions", ""))
    minimum = minimums.get("software.main_functions", "") if isinstance(minimums, dict) else ""
    maximum = limits.get("software.main_functions", "") if isinstance(limits, dict) else ""
    lines.extend(
        [
            f"字符数：`{len(main_functions)}`；当前维护基线：`{minimum}–{maximum}`。",
            "",
            main_functions or "[REVIEW REQUIRED]",
            "",
            "## 内部可选说明（不是本批截图确认的门户字段）",
            "",
            f"- 竞争优势：{software.get('competitive_advantages', '') or '[未填写]'}",
            f"- 商业价值：{software.get('commercial_value', '') or '[未填写]'}",
            "",
        ]
    )
    path = drafts_dir / "form-worksheet.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_proof_checklist(application: dict[str, Any], drafts_dir: Path) -> Path:
    software = application.get("software", {})
    description = software.get("description", {}) if isinstance(software, dict) else {}
    configured = application.get("proof_checklist", [])
    configured_by_code = {
        str(item.get("code")): item
        for item in configured
        if isinstance(item, dict) and item.get("code")
    }
    items: list[dict[str, str]] = []

    def add(code: str, item: str, note: str, required: str = "yes") -> None:
        stored = configured_by_code.get(code, {})
        items.append(
            {
                "code": code,
                "item": item,
                "required": required,
                "status": str(stored.get("status", "not-recorded")),
                "note": str(stored.get("note", note)),
            }
        )

    add(
        "applicant-identity",
        "Applicant identity document",
        "Keep identity documents and identity numbers outside the code repository.",
    )
    add(
        "portal-confirmation",
        "Application confirmation/signature/declaration page",
        "Confirm whether a later portal step requires this; the supplied screenshots do not show it.",
        "current-portal-dependent",
    )
    development_type = software.get("development_type") if isinstance(software, dict) else None
    if development_type == "cooperative":
        add("cooperative-agreement", "Cooperative-development contract or agreement PDF", "Required by the visible cooperative-development branch; retain outside the repository.")
    elif development_type == "commissioned":
        add("commissioned-agreement", "Commissioned-development contract or agreement PDF", "Required by the visible commissioned-development branch; retain outside the repository.")
    elif development_type == "assigned-task":
        add("assigned-task-document", "Project task document or ownership contract PDF", "Required by the visible assigned-task branch; retain outside the repository.")
    if isinstance(description, dict) and description.get("type") == "modified":
        if description.get("modification_basis") == "authorization-required":
            add("original-holder-authorization", "Original rights-holder authorization PDF", "Confirm the current modified-software branch and retain the authorization outside the repository.")
        elif description.get("modification_basis") == "registered":
            add("previous-registration", "Previous software registration evidence", "The visible branch states that the software is already registered; confirm the exact current proof requirement.", "current-portal-dependent")
    if isinstance(software, dict) and software.get("rights_acquisition") == "successor":
        add("successor-proof", "Succession, transfer, inheritance, or assumption proof PDF", "Use the proof matching the confirmed successor-acquisition basis; retain outside the repository.")
    if isinstance(software, dict) and software.get("rights_scope") == "partial":
        add("partial-rights-proof", "Partial-rights basis or agreement", "The supplied screenshots do not show the partial-rights branch; confirm the current portal requirement.", "current-portal-dependent")
    known_codes = {item["code"] for item in items}
    for item in configured:
        if not isinstance(item, dict) or item.get("code") in known_codes:
            continue
        items.append(
            {
                "code": str(item.get("code", "custom")),
                "item": str(item.get("item", "")),
                "required": "application-dependent",
                "status": str(item.get("status", "not-recorded")),
                "note": str(item.get("note", "")),
            }
        )
    lines = [
        "# Proof-material checklist",
        "",
        "Keep identity and ownership proof documents outside the code repository. This checklist records readiness only.",
        "",
        "This file records readiness only. Upload controls visible in the supplied portal screenshots accept PDF; size and filename rules remain unconfirmed.",
        "",
        "| Item | Required | Status | Note |",
        "|---|---|---|---|",
    ]
    for item in items:
        lines.append(
            "| {item} | {required} | {status} | {note} |".format(
                item=str(item.get("item", "")).replace("|", "\\|"),
                required=str(item.get("required", "")).replace("|", "\\|"),
                status=str(item.get("status", "not-recorded")).replace("|", "\\|"),
                note=str(item.get("note", "")).replace("|", "\\|"),
            )
        )
    path = drafts_dir / "proof-checklist.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def build_document_material(
    repo: Path,
    application: dict[str, Any],
    work_dir: Path,
    reports_dir: Path,
    *,
    final: bool,
) -> dict[str, Any]:
    document = application["document"]
    identity = canonical_identity(application, final=final)
    max_units = int(document.get("max_display_units_per_line", 72))
    lines: list[dict[str, Any]] = []
    evidence_entries: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    line_number = 1
    sections = document.get("sections", [])
    if not sections:
        raise CcopyrightError("document.sections is empty; add approved material content.")
    for section_index, section in enumerate(sections, start=1):
        title = str(section.get("title", "")).strip()
        if title:
            lines.append({"id": f"D{line_number:05d}", "text": f"【{title}】", "heading": True, "section": section_index})
            line_number += 1
        for paragraph in section.get("paragraphs", []):
            for wrapped in wrap_display(str(paragraph), max_units):
                lines.append({"id": f"D{line_number:05d}", "text": wrapped, "heading": False, "section": section_index})
                line_number += 1
        evidence_paths = [str(value) for value in section.get("evidence", [])]
        for evidence_path in evidence_paths:
            exists = False
            digest = ""
            try:
                resolved = safe_relative_path(evidence_path, repo)
                exists = resolved.exists()
                digest = sha256_file(resolved) if resolved.is_file() else ""
            except CcopyrightError:
                resolved = None
            if not exists:
                warnings.append(finding("WARNING", "missing-evidence", "Referenced evidence path does not exist inside the repository.", path=evidence_path))
            evidence_entries.append({"section": title, "path": evidence_path, "exists": exists, "sha256": digest})

    lines_per_page = int(application["requirements"]["document_lines_per_page"])
    pages_data = _page_chunks(lines, lines_per_page)
    assets_dir = work_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    screenshot_by_page: dict[int, dict[str, Any]] = {}
    screenshot_manifest: list[dict[str, Any]] = []
    for index, screenshot in enumerate(document.get("screenshots", []), start=1):
        raw_path = str(screenshot.get("path", ""))
        if not raw_path:
            warnings.append(finding("WARNING", "missing-screenshot-path", "Screenshot entry has no path."))
            continue
        try:
            source = safe_relative_path(raw_path, repo)
        except CcopyrightError:
            warnings.append(finding("WARNING", "invalid-screenshot-path", "Screenshot path is outside the repository or is a symlink.", path=raw_path))
            continue
        if not source.is_file() or source.suffix.lower() not in SCREENSHOT_EXTENSIONS:
            warnings.append(finding("WARNING", "missing-screenshot", "Screenshot file is missing or has an unsupported extension.", path=raw_path))
            continue
        if source.stat().st_size > MAX_SCREENSHOT_BYTES:
            warnings.append(finding("WARNING", "large-screenshot-skipped", "Screenshot exceeds the 20 MB local safety limit and was not rendered.", path=raw_path))
            continue
        if source.suffix.lower() == ".svg":
            svg_text, _ = decode_text(source)
            active_svg = re.search(r"(?i)<\s*(?:script|foreignObject)\b", svg_text)
            external_svg = re.search(
                r'''(?i)(?:href|src)\s*=\s*["'](?!#|data:)[^"']+["']''',
                svg_text,
            )
            if active_svg or external_svg:
                warnings.append(finding("WARNING", "active-svg-skipped", "SVG contains active or external content and was not rendered; provide a flattened raster screenshot.", path=raw_path))
                continue
        target_page = int(screenshot.get("page", index + 1))
        if target_page < 1:
            target_page = 1
        if target_page > len(pages_data):
            warnings.append(finding("WARNING", "screenshot-page-adjusted", "Screenshot target page exceeded document length and was moved to the last page.", path=raw_path))
            target_page = len(pages_data)
        target_name = f"figure-{index:02d}{source.suffix.lower()}"
        target = assets_dir / target_name
        shutil.copy2(source, target)
        record = {
            "path": relative_posix(source, repo),
            "sha256": sha256_file(source),
            "output": f"assets/{target_name}",
            "page": target_page,
            "title": str(screenshot.get("title", f"Figure {index}")),
            "caption": str(screenshot.get("caption", "")),
        }
        if target_page in screenshot_by_page:
            warnings.append(finding("WARNING", "multiple-screenshots-one-page", "Only the first screenshot assigned to a page is rendered; review screenshot page assignments.", path=raw_path))
        else:
            screenshot_by_page[target_page] = record
        screenshot_manifest.append(record)

    title = document.get("title") or f"{identity['full_name']}{identity['version']}软件说明书"
    markdown = [
        f"# {title}",
        "",
        f"- 软件全称：{identity['full_name']}",
        f"- 版本号：{identity['version']}",
        f"- 著作权人：{identity['rights_holder']}",
        f"- 开发完成日期：{application['software'].get('completion_date', '')}",
        f"- 文档编制日期：{application.get('dates', {}).get('material_preparation_date', '')}",
        "",
    ]
    pages_html: list[str] = []
    total_pages = len(pages_data)
    for page_index, page_rows in enumerate(pages_data, start=1):
        markdown.extend([f"## 第 {page_index:02d}/{total_pages:02d} 页", ""])
        html_rows: list[str] = []
        for row in page_rows:
            markdown.append(f"{row['id']}  {row['text']}  ")
            row_class = "row heading" if row["heading"] else "row"
            row_height = 238.5 / max(lines_per_page, 1)
            html_rows.append(
                f'<li class="{row_class}" style="height:{row_height:.3f}mm;line-height:{row_height:.3f}mm">'
                f'<span class="row-id">{row["id"]}</span><span>{html.escape(row["text"], quote=False)}</span></li>'
            )
        screenshot = screenshot_by_page.get(page_index)
        if screenshot:
            markdown.extend([
                "",
                f"![{screenshot['title']}]({screenshot['output']})",
                "",
                f"*{screenshot['title']}：{screenshot['caption']}*",
            ])
        markdown.append("")
        meta = f"完整文档｜第{page_index:02d}/{total_pages:02d}页｜打印行{len(page_rows)}"
        text_panel = f'<div class="text-panel"><div class="meta">{html.escape(meta)}</div><ol class="rows">{"".join(html_rows)}</ol></div>'
        if screenshot:
            figure = (
                '<figure class="figure-card"><img src="'
                + html.escape(screenshot["output"])
                + '" alt="'
                + html.escape(screenshot["title"])
                + '"><figcaption>'
                + html.escape(screenshot["title"])
                + '</figcaption><div class="figure-note">'
                + html.escape(screenshot["caption"])
                + "</div></figure>"
            )
            page_class = "page document illustrated"
            body = text_panel + figure
        else:
            page_class = "page document"
            body = f'<div class="meta">{html.escape(meta)}</div><ol class="rows">{"".join(html_rows)}</ol>'
        pages_html.append(
            f'<section class="{page_class}">'
            + _draft_mark(final)
            + _header(identity)
            + f'<main class="content">{body}</main>'
            + _footer("文档鉴别材料", page_index, total_pages)
            + "</section>"
        )

    work_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_filename(f"{identity['full_name']}{identity['version']}文档鉴别材料")
    md_path = work_dir / f"{stem}.md"
    html_path = work_dir / f"{stem}.html"
    manifest_path = work_dir / "document-manifest.json"
    md_path.write_text("\n".join(markdown) + "\n", encoding="utf-8")
    html_path.write_text(_html_document(stem, pages_html), encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "final": final,
        "identity": identity,
        "title": title,
        "lines_per_page": lines_per_page,
        "pages": total_pages,
        "rows": lines,
        "screenshots": screenshot_manifest,
        "warnings": warnings,
        "outputs": {"markdown": md_path.name, "html": html_path.name},
    }
    write_json(manifest_path, manifest)
    evidence_path = reports_dir / "evidence-map.md"
    evidence_lines = [
        "# Evidence map",
        "",
        "Internal review aid; do not upload unless the current portal explicitly requests it.",
        "",
        "| Document section | Evidence path | Exists | SHA-256 |",
        "|---|---|---|---|",
    ]
    for item in evidence_entries:
        escaped_section = item["section"].replace("|", "\\|")
        evidence_lines.append(
            f"| {escaped_section} | `{item['path']}` | {'yes' if item['exists'] else 'no'} | `{item['sha256']}` |"
        )
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text("\n".join(evidence_lines) + "\n", encoding="utf-8")
    return {"markdown": md_path, "html": html_path, "manifest": manifest_path, "evidence": evidence_path, "data": manifest}


def build_review_checklist(application: dict[str, Any], drafts_dir: Path) -> Path:
    items = [
        "Software full name exactly matches the current application form.",
        "Version punctuation and optional V prefix exactly match the current application form.",
        "Software category, original/modified status, rights acquisition, rights scope, and development type match the current portal options.",
        "Every rights-holder name and ordering is correct.",
        "Joint-ownership selection agrees with the complete rights-holder list.",
        "Completion date was confirmed by the applicant and was not inferred from Git.",
        "Publication status and conditional date, country, and region were confirmed by the applicant.",
        "All six portal environment fields fit the visible 50-character limits.",
        "Main functions and other visible text fields satisfy the confirmed current portal limits.",
        "Reported source-program line count and its stated basis were reviewed.",
        "Program and document deposit types are both ordinary general deposit; exceptional deposit uses a separate specialist process.",
        "Every conditional cooperation, commission, assigned-task, modification, successor, or partial-rights proof is ready outside the repository.",
        "Selected source code may be disclosed and contains no unwanted secrets or personal information.",
        "Program rows preserve the original file content and order shown in the source manifest.",
        "Document claims describe implemented functions and evidence warnings were reviewed.",
        "Screenshots come from the registered version and contain no private or test information.",
        "No applicant identity number, identity scan, or unredacted portal screenshot is stored in the workspace.",
        "The current portal requirements match the requirements snapshot.",
        "The PDFs reviewed are the latest validated revision.",
    ]
    lines = ["# Final human-review checklist", "", "Publishing requires the applicant to check every item manually.", ""]
    lines.extend(f"- [ ] {item}" for item in items)
    lines.extend(["", "Warnings do not prevent publication, but they should remain visible to the applicant.", ""])
    path = drafts_dir / "final-review-checklist.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def build_all(repo: Path, workspace: Path, *, final: bool, render: bool = False, chrome: str | None = None) -> dict[str, Any]:
    paths = workspace_paths(workspace)
    repo = repo.resolve()
    inventory = load_json(paths["inventory"])
    inventory_repo = inventory.get("repository") if isinstance(inventory, dict) else None
    if not isinstance(inventory_repo, str) or Path(inventory_repo).resolve() != repo:
        raise CcopyrightError("Preparation workspace belongs to a different repository. Run init with the intended repository and workspace.")
    application, upgraded = upgrade_application(load_json(paths["application"]))
    if upgraded:
        write_json(paths["application"], application)
    status = application_status(application)
    if status["invalid_required_values"]:
        raise CcopyrightError(
            "Application configuration is invalid: "
            + "; ".join(status["invalid_required_values"])
        )
    if application.get("source", {}).get("deposit_type") == "exceptional" or application.get("document", {}).get("deposit_type") == "exceptional":
        raise CcopyrightError(
            "Exceptional deposit is outside this ordinary-deposit workflow. "
            "Stop generation and use the appropriate specialist process."
        )
    if final and not status["final_complete"]:
        raise CcopyrightError(
            "Final generation requires confirmed facts. "
            f"Missing values: {status['missing_required_values']}; "
            f"unconfirmed: {status['unconfirmed_required_facts']}; "
            f"invalid: {status['invalid_required_values']}; "
            f"portal constraints: {status['portal_constraint_violations']}"
        )
    program = build_program_material(repo, application, paths["work"], final=final)
    worksheet = build_worksheet(application, paths["drafts"], program_data=program["data"])
    proof = build_proof_checklist(application, paths["drafts"])
    review = build_review_checklist(application, paths["drafts"])
    document = build_document_material(repo, application, paths["work"], paths["reports"], final=final)
    paths["requirements"].write_text(requirements_snapshot_markdown(application), encoding="utf-8")
    application["state"] = "generated"
    write_json(paths["application"], application)
    result: dict[str, Any] = {
        "schema_version": APPLICATION_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "tool_version": TOOL_VERSION,
        "final": final,
        "application_sha256": sha256_file(paths["application"]),
        "application_fingerprint": application_fingerprint(application),
        "repository_inventory_sha256": sha256_file(paths["inventory"]) if paths["inventory"].exists() else "",
        "status": status,
        "worksheet": str(worksheet),
        "proof_checklist": str(proof),
        "review_checklist": str(review),
        "program": {key: str(value) for key, value in program.items() if key != "data"},
        "document": {key: str(value) for key, value in document.items() if key != "data"},
        "warnings": program["data"]["warnings"] + document["data"]["warnings"],
        "rendered": {},
    }
    if render:
        result["rendered"] = render_materials(paths["work"], chrome=chrome)
    build_report = paths["reports"] / "build-report.json"
    write_json(build_report, result)
    result["build_report"] = str(build_report)
    return result


def find_chromium(explicit: str | None = None) -> str | None:
    if explicit:
        path = Path(explicit).expanduser()
        if path.is_file():
            return str(path.resolve())
        located = shutil.which(explicit)
        if located:
            return located
        raise CcopyrightError(f"Chromium executable not found: {explicit}")
    candidates = [
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        shutil.which("chrome"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        os.path.expandvars(r"$PROGRAMFILES\Google\Chrome\Application\chrome.exe"),
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    return None


def render_html(html_path: Path, pdf_path: Path, *, chrome: str | None = None) -> dict[str, Any]:
    executable = find_chromium(chrome)
    if not executable:
        raise CcopyrightError("Chrome/Chromium was not found. Generate HTML now and render PDF on a supported machine.")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        pdf_path.unlink()
    with tempfile.TemporaryDirectory(prefix="ccopyright-chrome-") as profile:
        args = [
            executable,
            "--headless",
            "--allow-file-access-from-files",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-gpu",
            "--disable-sync",
            "--metrics-recording-only",
            "--no-default-browser-check",
            "--no-first-run",
            "--no-pdf-header-footer",
            "--timeout=10000",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={pdf_path.resolve()}",
            html_path.resolve().as_uri(),
        ]
        command = args
        detached_macos_launch = False
        executable_path = Path(executable)
        if sys.platform == "darwin" and ".app" in executable_path.as_posix():
            app_bundle = next(
                (parent for parent in executable_path.parents if parent.suffix == ".app"),
                None,
            )
            if app_bundle is not None:
                command = [
                    "/usr/bin/open",
                    "-n",
                    "-a",
                    str(app_bundle),
                    "--args",
                    *args[1:],
                ]
                detached_macos_launch = True
        try:
            process = subprocess.run(
                command,
                cwd=html_path.parent,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=45 if not detached_macos_launch else 15,
            )
        except subprocess.TimeoutExpired as exc:
            raise CcopyrightError(
                "Chromium PDF rendering exceeded 45 seconds and was terminated. "
                "Review local Chrome policies and retry with --chrome if needed."
            ) from exc
        pdf_complete = not detached_macos_launch
        if detached_macos_launch and process.returncode == 0:
            deadline = time.monotonic() + 45
            stable_size = -1
            stable_checks = 0
            while time.monotonic() < deadline:
                try:
                    size = pdf_path.stat().st_size
                    with pdf_path.open("rb") as handle:
                        handle.seek(max(0, size - 2048))
                        complete = b"%%EOF" in handle.read()
                except OSError:
                    size = 0
                    complete = False
                if complete and size > 0 and size == stable_size:
                    stable_checks += 1
                    if stable_checks >= 2:
                        pdf_complete = True
                        break
                else:
                    stable_checks = 0
                stable_size = size
                time.sleep(0.2)
    if process.returncode != 0 or not pdf_complete or not pdf_path.is_file() or pdf_path.stat().st_size == 0:
        detail = process.stderr.strip() or process.stdout.strip() or "no diagnostic output"
        raise CcopyrightError(f"Chromium PDF rendering failed with exit code {process.returncode}: {detail}")
    return {
        "html": str(html_path),
        "pdf": str(pdf_path),
        "pdf_sha256": sha256_file(pdf_path),
        "renderer": executable,
        "renderer_version": command_output([executable, "--version"]),
    }


def render_materials(work_dir: Path, *, chrome: str | None = None) -> dict[str, Any]:
    program_manifest = load_json(work_dir / "program-manifest.json")
    document_manifest = load_json(work_dir / "document-manifest.json")
    outputs: dict[str, Any] = {}
    for label, manifest in (("program", program_manifest), ("document", document_manifest)):
        html_path = work_dir / manifest["outputs"]["html"]
        pdf_path = html_path.with_suffix(".pdf")
        outputs[label] = render_html(html_path, pdf_path, chrome=chrome)
        manifest["outputs"]["pdf"] = pdf_path.name
        write_json(work_dir / f"{label}-manifest.json", manifest)
    render_report = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "tool_version": TOOL_VERSION,
        "outputs": outputs,
    }
    reports_dir = work_dir.parent / "reports"
    write_json(reports_dir / "render-report.json", render_report)
    build_report_path = reports_dir / "build-report.json"
    if build_report_path.is_file():
        build_report = load_json(build_report_path)
        build_report["rendered"] = outputs
        write_json(build_report_path, build_report)
    return outputs


def _parse_pdfinfo(path: Path) -> dict[str, Any]:
    executable = shutil.which("pdfinfo")
    if not executable:
        raise CcopyrightError("pdfinfo is required for PDF validation.")
    process = subprocess.run([executable, str(path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result: dict[str, Any] = {"raw": process.stdout}
    pages = re.search(r"(?m)^Pages:\s+(\d+)", process.stdout)
    size = re.search(r"(?m)^Page size:\s+([\d.]+) x ([\d.]+) pts", process.stdout)
    result["pages"] = int(pages.group(1)) if pages else 0
    if size:
        result["page_width_points"] = float(size.group(1))
        result["page_height_points"] = float(size.group(2))
    for key in ("Title", "Author", "Creator", "Producer"):
        match = re.search(rf"(?m)^{key}:\s*(.*)$", process.stdout)
        result[key.lower()] = match.group(1).strip() if match else ""
    return result


def _extract_pdf_pages(path: Path) -> list[str]:
    executable = shutil.which("pdftotext")
    if not executable:
        raise CcopyrightError("pdftotext is required for PDF validation.")
    process = subprocess.run([executable, "-layout", str(path), "-"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pages = process.stdout.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def _validate_one_pdf(
    pdf: Path,
    manifest: dict[str, Any],
    *,
    kind: str,
    application: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not pdf.is_file():
        return {"kind": kind, "path": str(pdf), "passed": False, "errors": ["PDF file is missing."], "warnings": []}
    try:
        info = _parse_pdfinfo(pdf)
        pages = _extract_pdf_pages(pdf)
    except (CcopyrightError, subprocess.CalledProcessError) as exc:
        return {"kind": kind, "path": str(pdf), "passed": False, "errors": [str(exc)], "warnings": []}
    if info.get("pages") != manifest.get("pages") or len(pages) != manifest.get("pages"):
        errors.append(f"Page count differs from manifest: pdfinfo={info.get('pages')}, extracted={len(pages)}, manifest={manifest.get('pages')}.")
    width = info.get("page_width_points", 0)
    height = info.get("page_height_points", 0)
    if abs(width - 595.0) > 5 or abs(height - 842.0) > 5:
        errors.append(f"Page size is not A4 within tolerance: {width} x {height} points.")
    prefix = "P" if kind == "program" else "D"
    digits = 6 if kind == "program" else 5
    pattern = re.compile(rf"^\s*({prefix}\d{{{digits}}})\b")
    extracted_ids: list[str] = []
    page_counts: list[int] = []
    for page in pages:
        ids = [match.group(1) for row in page.splitlines() if (match := pattern.match(row))]
        extracted_ids.extend(ids)
        page_counts.append(len(ids))
    expected_ids = [row["material_id"] for row in manifest["rows"]] if kind == "program" else [row["id"] for row in manifest["rows"]]
    if extracted_ids != expected_ids:
        errors.append(f"Extracted numbered rows do not match the {kind} manifest.")
    configured_rows = int(manifest["lines_per_page"])
    for index, count in enumerate(page_counts, start=1):
        expected_count = configured_rows
        if index == len(page_counts):
            expected_count = len(expected_ids) - configured_rows * (len(page_counts) - 1)
        if count != expected_count:
            errors.append(f"Page {index} has {count} extracted rows; expected {expected_count}.")
    allow_short = bool(application["requirements"].get("allow_short_final_page_for_complete_material", True))
    if page_counts and page_counts[-1] < configured_rows:
        if allow_short:
            warnings.append(f"The final complete-material page has {page_counts[-1]} rows, fewer than the configured {configured_rows}; confirm current portal treatment.")
        else:
            errors.append("The final page is shorter than the configured row requirement.")
    identity = manifest["identity"]
    all_text = "\n".join(pages)
    for label, value in identity.items():
        if not value or value not in all_text:
            errors.append(f"Canonical {label} is missing from extracted PDF text.")
    if manifest.get("final") and re.search(r"UNCONFIRMED|REVIEW REQUIRED|\bDRAFT\b|待确认", all_text, flags=re.I):
        errors.append("Final PDF contains an unresolved placeholder or draft marker.")
    max_bytes = application["requirements"].get("max_pdf_bytes")
    if max_bytes is not None and pdf.stat().st_size > int(max_bytes):
        errors.append(f"PDF size {pdf.stat().st_size} exceeds configured maximum {max_bytes}.")
    metadata_text = " ".join(str(info.get(key, "")) for key in ("title", "author", "creator", "producer"))
    if re.search(r"(?:/Users/|/home/|[A-Za-z]:\\Users\\)", metadata_text):
        warnings.append("PDF metadata appears to contain a local user path.")
    return {
        "kind": kind,
        "path": str(pdf),
        "sha256": sha256_file(pdf),
        "bytes": pdf.stat().st_size,
        "pdfinfo": {key: value for key, value in info.items() if key != "raw"},
        "page_row_counts": page_counts,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def render_review_pages(pdf: Path, destination: Path) -> dict[str, Any]:
    executable = shutil.which("pdftoppm")
    if not executable:
        return {"available": False, "reason": "pdftoppm not found", "pages": [], "contact_sheet": ""}
    destination.mkdir(parents=True, exist_ok=True)
    prefix = destination / "page"
    subprocess.run([executable, "-png", "-r", "110", str(pdf), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    files = sorted(destination.glob("page-*.png"))
    cards = "".join(
        f'<figure><img src="{html.escape(path.name)}" alt="{html.escape(path.name)}"><figcaption>{html.escape(path.name)}</figcaption></figure>'
        for path in files
    )
    contact = destination / "contact-sheet.html"
    contact.write_text(
        "<!doctype html><meta charset=\"utf-8\"><title>PDF review</title>"
        "<style>body{font-family:sans-serif;background:#e5e9ef;margin:20px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}figure{margin:0;background:white;padding:8px;border-radius:8px}img{width:100%;height:auto}figcaption{font-size:12px;color:#596273;margin-top:6px}</style>"
        f"<main>{cards}</main>",
        encoding="utf-8",
    )
    return {"available": True, "pages": [str(path) for path in files], "contact_sheet": str(contact)}


def validate_workspace(workspace: Path, *, render_pages: bool = True) -> dict[str, Any]:
    paths = workspace_paths(workspace)
    application, upgraded = upgrade_application(load_json(paths["application"]))
    if upgraded:
        write_json(paths["application"], application)
    status = application_status(application)
    if status["invalid_required_values"]:
        raise CcopyrightError(
            "Application configuration is invalid: "
            + "; ".join(status["invalid_required_values"])
        )
    build_report = load_json(paths["reports"] / "build-report.json")
    program_manifest = load_json(paths["work"] / "program-manifest.json")
    document_manifest = load_json(paths["work"] / "document-manifest.json")
    current_fingerprint = application_fingerprint(application)
    consistency_errors: list[str] = []
    if build_report.get("application_fingerprint") != current_fingerprint:
        consistency_errors.append("Application facts changed after material generation; rebuild and render again.")
    for label, manifest in (("program", program_manifest), ("document", document_manifest)):
        expected_identity = canonical_identity(application, final=bool(manifest.get("final")))
        if manifest.get("identity") != expected_identity:
            consistency_errors.append(f"The {label} manifest identity does not match current application facts.")
        if bool(manifest.get("final")) != bool(build_report.get("final")):
            consistency_errors.append(f"The {label} manifest draft/final mode differs from the build report.")
    program_pdf_name = program_manifest.get("outputs", {}).get("pdf")
    document_pdf_name = document_manifest.get("outputs", {}).get("pdf")
    if not program_pdf_name or not document_pdf_name:
        raise CcopyrightError("PDF outputs are not recorded. Run build with --render or render the HTML files first.")
    program_pdf = paths["work"] / program_pdf_name
    document_pdf = paths["work"] / document_pdf_name
    program_result = _validate_one_pdf(program_pdf, program_manifest, kind="program", application=application)
    document_result = _validate_one_pdf(document_pdf, document_manifest, kind="document", application=application)
    review: dict[str, Any] = {}
    if render_pages:
        try:
            review["program"] = render_review_pages(program_pdf, paths["qa"] / "program-pages")
            review["document"] = render_review_pages(document_pdf, paths["qa"] / "document-pages")
        except subprocess.CalledProcessError as exc:
            review["error"] = str(exc)
    report = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "tool_version": TOOL_VERSION,
        "passed": program_result["passed"] and document_result["passed"] and not consistency_errors,
        "application_fingerprint": current_fingerprint,
        "consistency_errors": consistency_errors,
        "program": program_result,
        "document": document_result,
        "review_artifacts": review,
        "application_status": status,
    }
    paths["qa"].mkdir(parents=True, exist_ok=True)
    write_json(paths["qa"] / "validation-report.json", report)
    md_lines = [
        "# Validation report",
        "",
        f"Result: **{'PASS' if report['passed'] else 'FAIL'}**",
        "",
    ]
    md_lines.extend(f"- ERROR: {value}" for value in consistency_errors)
    if consistency_errors:
        md_lines.append("")
    for result in (program_result, document_result):
        md_lines.extend([f"## {result['kind'].title()}", "", f"- File: `{result['path']}`", f"- SHA-256: `{result.get('sha256', '')}`", f"- Passed: {result['passed']}", ""])
        md_lines.extend(f"- ERROR: {value}" for value in result["errors"])
        md_lines.extend(f"- WARNING: {value}" for value in result["warnings"])
        md_lines.append("")
    (paths["qa"] / "validation-report.md").write_text("\n".join(md_lines), encoding="utf-8")
    if report["passed"]:
        application["state"] = "validated"
        write_json(paths["application"], application)
    return report


def publish_workspace(workspace: Path, *, human_reviewed: bool) -> Path:
    if not human_reviewed:
        raise CcopyrightError("Publishing requires explicit human-review confirmation.")
    paths = workspace_paths(workspace)
    application, upgraded = upgrade_application(load_json(paths["application"]))
    if upgraded:
        write_json(paths["application"], application)
    status = application_status(application)
    if not status["final_complete"]:
        raise CcopyrightError(f"Application facts are not final-complete: {status}")
    validation_path = paths["qa"] / "validation-report.json"
    validation = load_json(validation_path)
    if validation.get("passed") is not True:
        raise CcopyrightError("Technical validation has not passed.")
    build_report = load_json(paths["reports"] / "build-report.json")
    if build_report.get("final") is not True:
        raise CcopyrightError("The validated build is a draft. Run final generation and validation first.")
    current_fingerprint = application_fingerprint(application)
    if build_report.get("application_fingerprint") != current_fingerprint:
        raise CcopyrightError("Application facts changed after the final build. Rebuild, render, and validate before publishing.")
    if validation.get("application_fingerprint") != current_fingerprint:
        raise CcopyrightError("Application facts changed after validation. Rebuild, render, and validate before publishing.")
    program_manifest = load_json(paths["work"] / "program-manifest.json")
    document_manifest = load_json(paths["work"] / "document-manifest.json")
    program_pdf_name = program_manifest.get("outputs", {}).get("pdf", "")
    document_pdf_name = document_manifest.get("outputs", {}).get("pdf", "")
    if not program_pdf_name or not document_pdf_name:
        raise CcopyrightError("Rendered PDF names are missing from the material manifests.")
    program_pdf = paths["work"] / program_pdf_name
    document_pdf = paths["work"] / document_pdf_name
    expected_hashes = {
        "program": validation.get("program", {}).get("sha256", ""),
        "document": validation.get("document", {}).get("sha256", ""),
    }
    for label, pdf in (("program", program_pdf), ("document", document_pdf)):
        if not pdf.is_file() or sha256_file(pdf) != expected_hashes[label]:
            raise CcopyrightError(f"The {label} PDF changed after validation. Render and validate again.")
    revision_name = "revision-" + dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = paths["ready"] / revision_name
    counter = 2
    while destination.exists():
        destination = paths["ready"] / f"{revision_name}-{counter}"
        counter += 1
    staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=paths["ready"]))
    try:
        identity = canonical_identity(application, final=True)
        program_name = safe_filename(f"{identity['full_name']}{identity['version']}程序鉴别材料.pdf")
        document_name = safe_filename(f"{identity['full_name']}{identity['version']}文档鉴别材料.pdf")
        copies = [
            (program_pdf, staging / program_name),
            (document_pdf, staging / document_name),
            (paths["drafts"] / "form-worksheet.md", staging / "申请表填写底稿.md"),
            (paths["drafts"] / "proof-checklist.md", staging / "证明材料清单.md"),
            (paths["drafts"] / "final-review-checklist.md", staging / "最终人工复核清单.md"),
            (paths["qa"] / "validation-report.md", staging / "技术校验报告.md"),
            (paths["application"], staging / "application-facts.json"),
        ]
        for source, target in copies:
            if not source.is_file():
                raise CcopyrightError(f"Required publication artifact is missing: {source}")
            shutil.copy2(source, target)
        generation_manifest = {
            "schema_version": 1,
            "published_at": utc_now(),
            "human_review_confirmed": True,
            "tool_version": TOOL_VERSION,
            "application_sha256": sha256_file(staging / "application-facts.json"),
            "application_fingerprint": current_fingerprint,
            "inventory_sha256": sha256_file(paths["inventory"]) if paths["inventory"].is_file() else "",
            "build_report_sha256": sha256_file(paths["reports"] / "build-report.json"),
            "validation_report_sha256": sha256_file(validation_path),
            "snapshot": application.get("snapshot", {}),
            "warnings": build_report.get("warnings", []),
        }
        write_json(staging / "generation-manifest.json", generation_manifest)
        checksum_rows = []
        for path in sorted(staging.iterdir(), key=lambda item: item.name):
            if path.is_file():
                checksum_rows.append(f"{sha256_file(path)}  {path.name}")
        (staging / "SHA256SUMS").write_text("\n".join(checksum_rows) + "\n", encoding="utf-8")
        staging.replace(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    application["state"] = "ready"
    application.setdefault("review", {})["human_reviewed_at"] = utc_now()
    write_json(paths["application"], application)
    return destination
