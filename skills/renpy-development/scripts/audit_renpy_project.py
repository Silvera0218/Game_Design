#!/usr/bin/env python3
"""Static structural audit for a Ren'Py project.

This is intentionally conservative. It complements, but never replaces,
Ren'Py's own lint command and an actual project launch.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


SOURCE_ENCODINGS = ("utf-8-sig", "utf-8")
ASSET_EXTENSIONS = (
    "png",
    "jpg",
    "jpeg",
    "webp",
    "avif",
    "gif",
    "svg",
    "ogg",
    "opus",
    "mp3",
    "wav",
    "flac",
    "webm",
    "mp4",
    "mkv",
    "ttf",
    "otf",
    "woff",
    "woff2",
)

DEFINITION_PATTERNS = {
    "labels": re.compile(
        r"(?m)^[ ]*label[ \t]+([A-Za-z_][\w.]*)"
        r"(?:[ \t]*\([^:\n]*\))?[ \t]*:"
    ),
    "screens": re.compile(
        r"(?m)^[ ]*screen[ \t]+([A-Za-z_][\w.]*)"
        r"(?:[ \t]*\([^:\n]*\))?[ \t]*:"
    ),
    "transforms": re.compile(
        r"(?m)^[ ]*transform[ \t]+([A-Za-z_][\w.]*)"
        r"(?:[ \t]*\([^:\n]*\))?[ \t]*:"
    ),
    "images": re.compile(
        r"(?m)^[ ]*image[ \t]+([A-Za-z_][\w]*(?:[ \t]+[\w]+)*)[ \t]*="
    ),
}


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in SOURCE_ENCODINGS:
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def find_game_dir(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    if path.is_file():
        path = path.parent
    if path.name.lower() == "game":
        return path
    candidate = path / "game"
    if candidate.is_dir():
        return candidate
    if any(path.glob("*.rpy")):
        return path
    raise FileNotFoundError(
        f"Could not find a Ren'Py game directory at or below: {path}"
    )


def find_scalar(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1) if match else None


def audit(game_dir: Path) -> dict:
    all_rpy = sorted(game_dir.rglob("*.rpy"))
    source_files = [
        path
        for path in all_rpy
        if "tl" not in {part.lower() for part in path.relative_to(game_dir).parts}
        and "cache" not in {part.lower() for part in path.relative_to(game_dir).parts}
    ]
    translation_files = [path for path in all_rpy if path not in source_files]

    findings = {"failures": [], "concerns": [], "notes": []}
    definitions: dict[str, list[tuple[str, str]]] = {
        key: [] for key in DEFINITION_PATTERNS
    }
    referenced_assets: set[str] = set()
    options_text = ""
    total_lines = 0

    asset_pattern = re.compile(
        r"""(?ix)
        ["']
        (
            (?!https?://)
            [^"'\r\n]+
            \.(?:%s)
        )
        ["']
        """
        % "|".join(ASSET_EXTENSIONS)
    )

    mutable_define = re.compile(
        r"(?m)^[ ]*define[ \t]+([A-Za-z_][\w.]*)[ \t]*=[ \t]*"
        r"(\[|\{|list\s*\(|dict\s*\(|set\s*\()"
    )

    for path in source_files:
        relative = path.relative_to(game_dir).as_posix()
        text = read_text(path)
        total_lines += text.count("\n") + 1

        if path.name.lower() == "options.rpy":
            options_text += "\n" + text

        for line_number, line in enumerate(text.splitlines(), 1):
            if "\t" in line[: len(line) - len(line.lstrip())]:
                findings["failures"].append(
                    f"{relative}:{line_number}: tab used in indentation"
                )

        for kind, pattern in DEFINITION_PATTERNS.items():
            for match in pattern.finditer(text):
                definitions[kind].append((match.group(1), relative))

        for match in mutable_define.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings["concerns"].append(
                f"{relative}:{line}: mutable value '{match.group(1)}' "
                "is declared with define; game state usually needs default"
            )

        for match in re.finditer(
            r"(?im)^[ \t]*(?:\$[ \t]*)?.*\bopen[ \t]*\(", text
        ):
            line = text.count("\n", 0, match.start()) + 1
            findings["concerns"].append(
                f"{relative}:{line}: direct open() call; verify writable path, "
                "rollback boundary, and platform behavior"
            )

        for match in re.finditer(
            r"""(?ix)
            ["']
            (
                [A-Za-z]:[\\/][^"'\r\n]+
                |
                /(?:Users|home)/[^"'\r\n]+
            )
            ["']
            """,
            text,
        ):
            line = text.count("\n", 0, match.start()) + 1
            findings["failures"].append(
                f"{relative}:{line}: absolute OS path '{match.group(1)}'"
            )

        for match in asset_pattern.finditer(text):
            referenced_assets.add(match.group(1).replace("\\", "/"))

        if re.search(
            r"(?m)^[ ]*(?:define[ \t]+)?config\.developer[ \t]*=[ \t]*True\b",
            text,
        ):
            findings["concerns"].append(
                f"{relative}: config.developer is explicitly True; "
                "review before distribution"
            )

    for kind, values in definitions.items():
        counts = Counter(name for name, _ in values)
        for name, count in sorted(counts.items()):
            if count > 1:
                locations = sorted(path for found, path in values if found == name)
                findings["failures"].append(
                    f"duplicate {kind[:-1]} '{name}' in {', '.join(locations)}"
                )

    label_names = {name for name, _ in definitions["labels"]}
    if "start" not in label_names:
        findings["failures"].append("missing required entry label 'start'")

    if not (game_dir / "options.rpy").is_file():
        findings["concerns"].append("options.rpy was not found")
    if not (game_dir / "screens.rpy").is_file():
        findings["concerns"].append("screens.rpy was not found")

    missing_assets = []
    for reference in sorted(referenced_assets):
        if "[" in reference or "{" in reference or "%" in reference:
            continue
        if not (game_dir / reference).is_file():
            missing_assets.append(reference)
    for reference in missing_assets:
        findings["concerns"].append(
            f"literal asset reference was not found under game/: {reference}"
        )

    orphaned_rpyc = []
    for compiled in game_dir.glob("*.rpyc"):
        source = compiled.with_suffix(".rpy")
        if not source.exists():
            orphaned_rpyc.append(compiled.name)
    if orphaned_rpyc:
        findings["concerns"].append(
            "orphaned top-level .rpyc files may keep removed scripts active: "
            + ", ".join(sorted(orphaned_rpyc))
        )

    metadata = {
        "name": find_scalar(
            r"^[ \t]*(?:define[ \t]+)?config\.name[ \t]*=[ \t]*[\"']([^\"']+)",
            options_text,
        ),
        "version": find_scalar(
            r"^[ \t]*(?:define[ \t]+)?config\.version[ \t]*=[ \t]*[\"']([^\"']+)",
            options_text,
        ),
        "build_name": find_scalar(
            r"^[ \t]*(?:define[ \t]+)?build\.name[ \t]*=[ \t]*[\"']([^\"']+)",
            options_text,
        ),
    }

    if findings["failures"]:
        verdict = "FAIL"
    elif findings["concerns"]:
        verdict = "CONCERNS"
    else:
        verdict = "PASS"

    return {
        "verdict": verdict,
        "game_dir": str(game_dir),
        "metadata": metadata,
        "counts": {
            "source_files": len(source_files),
            "translation_files": len(translation_files),
            "source_lines": total_lines,
            **{key: len(value) for key, value in definitions.items()},
            "literal_asset_references": len(referenced_assets),
        },
        "findings": findings,
        "limitations": [
            "This audit does not parse full Ren'Py grammar.",
            "Run the target SDK's Lint and launch the game before release.",
        ],
    }


def print_human(report: dict) -> None:
    print(f"Ren'Py Project Audit: {report['verdict']}")
    print(f"Game directory: {report['game_dir']}")
    metadata = report["metadata"]
    if any(metadata.values()):
        print(
            "Metadata: "
            f"name={metadata['name']!r}, version={metadata['version']!r}, "
            f"build_name={metadata['build_name']!r}"
        )
    counts = report["counts"]
    print(
        "Counts: "
        + ", ".join(f"{key}={value}" for key, value in counts.items())
    )
    for section in ("failures", "concerns", "notes"):
        values = report["findings"][section]
        if values:
            print(f"\n{section.upper()}:")
            for value in values:
                print(f"- {value}")
    print("\nLimitations:")
    for value in report["limitations"]:
        print(f"- {value}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Ren'Py project root or game directory")
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON"
    )
    args = parser.parse_args()

    try:
        game_dir = find_game_dir(args.project)
        report = audit(game_dir)
    except (FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)

    return {"PASS": 0, "CONCERNS": 1, "FAIL": 2}[report["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
