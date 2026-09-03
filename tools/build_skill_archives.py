#!/usr/bin/env python
"""Build deterministic, self-contained .skill archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
STABLE_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
PACKAGE_LOCALES = ("en", "zh-CN")
PACKAGE_SPECS = (
    {
        "name": "ccopyright-qa",
        "required": {
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
        },
    },
    {
        "name": "ccopyright-register",
        "required": {
            "SKILL.md",
            "README.md",
            "README.en.md",
            "agents/openai.yaml",
            "references/en/application-schema.md",
            "references/en/material-preparation.md",
            "references/en/official-sources.md",
            "references/en/workflow.md",
            "references/en/portal-form.md",
            "references/en/quality-checks.md",
            "references/zh-CN/application-schema.md",
            "references/zh-CN/material-preparation.md",
            "references/zh-CN/official-sources.md",
            "references/zh-CN/workflow.md",
            "references/zh-CN/portal-form.md",
            "references/zh-CN/quality-checks.md",
            "scripts/ccopyright.py",
            "scripts/ccopyright_core.py",
            "assets/application.template.json",
            "assets/material.css",
        },
    },
)
DEPRECATED_ARCHIVES = ("ccopyright.skill", "软著.skill")
IGNORED_PARTS = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def files_under(directory: Path) -> Iterable[Path]:
    if not directory.is_dir():
        raise RuntimeError(f"Missing package input directory: {directory}")
    for path in sorted(directory.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise RuntimeError(f"Symlinks are not accepted in packages: {path}")
        if not path.is_file():
            continue
        if set(path.parts) & IGNORED_PARTS or path.suffix in IGNORED_SUFFIXES:
            continue
        yield path


def collect_entries(
    package_root: Path,
    locales: tuple[str, ...],
    required: set[str],
) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    for path in files_under(package_root):
        entries[path.relative_to(package_root).as_posix()] = path.read_bytes()
    missing = sorted(required - entries.keys())
    if missing:
        raise RuntimeError(f"Package is missing required files: {missing}")
    manifest = {
        "format": "codex-skill-zip",
        "format_version": 1,
        "skill": package_root.name,
        "locales": list(locales),
        "files": [
            {"path": name, "bytes": len(data), "sha256": sha256(data)}
            for name, data in sorted(entries.items())
        ],
    }
    entries["PACKAGE-MANIFEST.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    return entries


def write_archive(destination: Path, entries: dict[str, bytes]) -> dict[str, object]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        destination,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(name, STABLE_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.flag_bits |= 0x800
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(destination) as archive:
        bad = archive.testzip()
        names = archive.namelist()
    if bad:
        raise RuntimeError(f"Archive integrity check failed at {bad}: {destination}")
    return {
        "path": str(destination),
        "bytes": destination.stat().st_size,
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "entries": len(names),
    }


def build(output_dir: Path) -> list[dict[str, object]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in DEPRECATED_ARCHIVES:
        deprecated = output_dir / filename
        if deprecated.is_file() or deprecated.is_symlink():
            deprecated.unlink()
    results = []
    for spec in PACKAGE_SPECS:
        name = str(spec["name"])
        package_root = ROOT / "skills" / name
        required = set(spec["required"])
        entries = collect_entries(package_root, PACKAGE_LOCALES, required)
        results.append(write_archive(output_dir / f"{name}.skill", entries))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "dist"),
        help="Destination directory (default: repository dist directory).",
    )
    args = parser.parse_args()
    results = build(Path(args.output_dir).expanduser().resolve())
    print(json.dumps({"archives": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
