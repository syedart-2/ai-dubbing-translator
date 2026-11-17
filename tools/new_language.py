#!/usr/bin/env python3
"""Create a new language role folder from the template.

Part of ai-dubbing-translator. MIT License, (c) 2026 Muhammad Ali Nasir Ud Din.

Usage:
  python3 tools/new_language.py <Language> [--workspace PATH]

Example:
  python3 tools/new_language.py Spanish --workspace "~/Documents/Dubbing Workspace"

It copies templates/language-role/ to "<workspace>/<Language> Dubbing Translator/",
fills in the language name and today's date, and never overwrites an existing folder.
"""
import argparse
import datetime
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE = REPO / "templates" / "language-role"


def main():
    ap = argparse.ArgumentParser(description="Create a new language role folder from the template.")
    ap.add_argument("language", help="Language name, for example Spanish")
    ap.add_argument("--workspace", default=".", help="Workspace folder that holds one folder per language (default: current folder)")
    a = ap.parse_args()

    lang = a.language.strip()
    if not lang:
        sys.exit("Give a language name, for example: python3 tools/new_language.py Spanish")
    ws = Path(a.workspace).expanduser().resolve()
    ws.mkdir(parents=True, exist_ok=True)
    dest = ws / f"{lang} Dubbing Translator"
    if dest.exists():
        sys.exit(f"Stopped: '{dest}' already exists. Nothing was changed.")
    if not TEMPLATE.exists():
        sys.exit(f"Template not found at {TEMPLATE}. Run this script from inside the repository.")

    shutil.copytree(TEMPLATE, dest)
    today = datetime.date.today().isoformat()
    for pattern in ("*.md", "*.txt"):
        for f in dest.rglob(pattern):
            t = f.read_text(encoding="utf-8")
            t = t.replace("<Language>", lang)
            if f.name in ("_brief.md", "CHANGELOG.md"):
                t = t.replace("YYYY-MM-DD", today, 1)
            f.write_text(t, encoding="utf-8")
    lessons = dest / "_LESSONS template.md"
    if lessons.exists():
        lessons.rename(dest / f"_LESSONS - {lang} (template, rename at first entry).md")

    tools = ws / "_tools"
    tools.mkdir(exist_ok=True)
    copied = []
    for script in ("srt_structure_check.py", "srt_scaffold.py", "srt_assemble.py"):
        target = tools / script
        if not target.exists():
            shutil.copy2(REPO / "tools" / script, target)
        copied.append(target.name)

    print(f"Created: {dest}")
    print(f"Scripts in {tools}: {', '.join(copied)}")
    print("Next: put one approved sample SRT in REFERENCE/, then fill _brief.md and style-guide.md.")


if __name__ == "__main__":
    main()
