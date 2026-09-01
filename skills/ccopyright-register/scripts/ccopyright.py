#!/usr/bin/env python
"""Command-line workflow for preparing Chinese software copyright materials."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from ccopyright_core import (
    CcopyrightError,
    application_status,
    build_all,
    initialize_workspace,
    load_json,
    precheck_markdown,
    preflight,
    publish_workspace,
    render_materials,
    requirements_snapshot_markdown,
    scan_repository,
    validate_workspace,
    workspace_paths,
    write_json,
    upgrade_application,
)


def emit(value: Any) -> None:
    if isinstance(value, Path):
        value = str(value)
    print(json.dumps(value, ensure_ascii=False, indent=2))


def path_value(raw: str) -> Path:
    return Path(raw).expanduser().resolve()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ccopyright",
        description=(
            "Prepare, render, validate, and package materials for Chinese "
            "computer-software copyright registration."
        ),
    )
    parser.add_argument("--version", action="version", version="ccopyright 0.3.0")
    commands = parser.add_subparsers(dest="command", required=True)

    preflight_parser = commands.add_parser("preflight", help="Report local tool availability.")
    preflight_parser.add_argument("--chrome", help="Explicit Chrome/Chromium executable.")

    scan_parser = commands.add_parser("scan", help="Inspect a repository without modifying it.")
    scan_parser.add_argument("--repo", default=".", help="Repository root (default: current directory).")
    scan_parser.add_argument(
        "--output",
        help="Optional JSON output path. A sibling .md precheck report is also written.",
    )
    scan_parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=2_000_000,
        help="Maximum bytes read from one candidate file.",
    )

    init_parser = commands.add_parser("init", help="Initialize a preparation workspace.")
    init_parser.add_argument("--repo", default=".", help="Repository root.")
    init_parser.add_argument("--workspace", default=".ccopyright", help="Preparation workspace.")
    init_parser.add_argument("--force", action="store_true", help="Replace application.json with a fresh template.")

    status_parser = commands.add_parser("status", help="Show final-mode completeness.")
    status_parser.add_argument("--workspace", default=".ccopyright", help="Preparation workspace.")

    build_command = commands.add_parser("build", help="Generate worksheets and identification materials.")
    build_command.add_argument("--repo", default=".", help="Repository root.")
    build_command.add_argument("--workspace", default=".ccopyright", help="Preparation workspace.")
    build_command.add_argument("--final", action="store_true", help="Require all final facts and confirmations.")
    build_command.add_argument("--render", action="store_true", help="Render generated HTML to PDF.")
    build_command.add_argument("--chrome", help="Explicit Chrome/Chromium executable.")

    render_parser = commands.add_parser("render", help="Render existing material HTML to PDF.")
    render_parser.add_argument("--workspace", default=".ccopyright", help="Preparation workspace.")
    render_parser.add_argument("--chrome", help="Explicit Chrome/Chromium executable.")

    validate_parser = commands.add_parser("validate", help="Validate rendered PDFs and manifests.")
    validate_parser.add_argument("--workspace", default=".ccopyright", help="Preparation workspace.")
    validate_parser.add_argument(
        "--no-render-pages",
        action="store_true",
        help="Skip PNG review-page and contact-sheet generation.",
    )

    publish_parser = commands.add_parser("publish", help="Create a new ready-to-submit revision.")
    publish_parser.add_argument("--workspace", default=".ccopyright", help="Preparation workspace.")
    publish_parser.add_argument(
        "--human-reviewed",
        action="store_true",
        help="Confirm the final human-review checklist was completed.",
    )
    return parser


def run(args: argparse.Namespace) -> Any:
    if args.command == "preflight":
        return preflight(args.chrome)

    if args.command == "scan":
        repo = path_value(args.repo)
        inventory = scan_repository(repo, max_file_bytes=args.max_file_bytes)
        if args.output:
            output = path_value(args.output)
            if output.suffix.lower() != ".json":
                raise CcopyrightError("--output must name a .json file.")
            write_json(output, inventory)
            markdown_path = output.with_suffix(".md")
            markdown_path.write_text(precheck_markdown(inventory), encoding="utf-8")
            return {
                "inventory": str(output),
                "precheck": str(markdown_path),
                "finding_counts": inventory["finding_counts"],
            }
        return inventory

    workspace = path_value(args.workspace)
    if args.command == "init":
        return initialize_workspace(path_value(args.repo), workspace, force=args.force)
    if args.command == "status":
        paths = workspace_paths(workspace)
        application_path = paths["application"]
        application, upgraded = upgrade_application(load_json(application_path))
        if upgraded:
            write_json(application_path, application)
        status = application_status(application)
        if not status["invalid_required_values"]:
            paths["requirements"].write_text(
                requirements_snapshot_markdown(application), encoding="utf-8"
            )
        return status
    if args.command == "build":
        return build_all(
            path_value(args.repo),
            workspace,
            final=args.final,
            render=args.render,
            chrome=args.chrome,
        )
    if args.command == "render":
        return render_materials(workspace_paths(workspace)["work"], chrome=args.chrome)
    if args.command == "validate":
        return validate_workspace(workspace, render_pages=not args.no_render_pages)
    if args.command == "publish":
        destination = publish_workspace(workspace, human_reviewed=args.human_reviewed)
        return {"ready_revision": str(destination)}
    raise CcopyrightError(f"Unsupported command: {args.command}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        emit(run(args))
    except (CcopyrightError, OSError, ValueError, KeyError) as exc:
        print(f"ccopyright: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
