"""Check the public repository without provider calls or third-party packages.

Run from any directory. Findings report file paths and issue types only, never
the contents of a suspected credential. This is a limited pattern scan, not a
replacement for provider revocation or a dedicated secret scanning service.
"""
from __future__ import annotations

import ast
import csv
import hashlib
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ("apps", "experiments", "data", "docs", "scripts")
TOP_LEVEL = (
    "README.md", "SECURITY.md", ".gitignore", ".gitattributes", ".env.example",
    "requirements.txt", "requirements-lock.txt",
)
SECRET_PATTERNS = (
    re.compile(rb"sk-[A-Za-z0-9_-]{15,}"),
    re.compile(rb"AIza[A-Za-z0-9_-]{20,}"),
    re.compile(rb"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(rb"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def public_files() -> list[Path]:
    paths = [ROOT / name for name in TOP_LEVEL]
    for directory in DIRECTORIES:
        paths.extend(p for p in (ROOT / directory).rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts)
    return sorted(paths)


def verify() -> int:
    errors = []
    files = public_files()
    python_count = 0
    link_count = 0
    for path in files:
        relative = path.relative_to(ROOT)
        if not path.is_file():
            errors.append(f"{relative}: required public file missing")
            continue
        raw = path.read_bytes()
        if any(pattern.search(raw) for pattern in SECRET_PATTERNS):
            errors.append(f"{relative}: potential credential pattern")
        if path.suffix == ".py":
            try:
                ast.parse(raw, filename=str(relative))
                python_count += 1
            except SyntaxError:
                errors.append(f"{relative}: Python syntax error")
        if path.suffix == ".md":
            text = raw.decode("utf-8")
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                url = urlsplit(target)
                if url.scheme or target.startswith("#"):
                    continue
                local = (path.parent / unquote(url.path)).resolve()
                if not local.is_relative_to(ROOT) or not local.exists():
                    errors.append(f"{relative}: invalid local link")
                link_count += 1

    with (ROOT / "data/manifest.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        path = (ROOT / "data" / row["file"]).resolve()
        if not path.is_relative_to(ROOT / "data") or not path.is_file():
            errors.append("data/manifest.csv: invalid snapshot path")
            continue
        raw = path.read_bytes()
        if len(raw) != int(row["bytes"]) or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            errors.append(f"{path.relative_to(ROOT)}: snapshot integrity mismatch")

    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {len(files)} public files, {python_count} Python files, "
          f"{link_count} local links, {len(rows)} filing hashes; {len(errors)} issues.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(verify())
