#!/usr/bin/env python3
"""Write the target SRT from translated lines, taking the structure from the source.

Part of ai-dubbing-translator. MIT License, (c) 2026 Muhammad Ali Nasir Ud Din.

Why this exists: the structure rules (same block count, same numbering, timestamps
byte-identical, same encoding) are mechanical, so a machine should keep them. This
script copies every timestamp straight from the worksheet that was read out of the
source, so no timestamp is ever typed. It reproduces the source's BOM and line
endings. And it refuses to write a file that breaks a structure rule, which is
cheaper than finding the break at QA.

The refusal that matters most: if the source block held text already in its own
script (Arabic in an English SRT, say), that exact string must appear in the
translated block. A retyped copy can differ in its combining marks and render
identically, so the eye cannot catch it and neither can a spellcheck. The check can.

Usage:
  python3 tools/srt_assemble.py --worksheet work.json --translations trans.json \\
                                --out TARGET.srt

--translations takes either:
  a .json file   {"1": ["line one"], "2": ["line one", "line two"]}
  or a .txt file in numbered-block form:

      1
      line one

      2
      line one
      line two

Exit codes: 0 written, 2 refused and nothing written, 1 bad arguments.
"""
import argparse
import json
import re
import sys
from pathlib import Path

BIDI = re.compile("[‎‏؜‪-‮⁦-⁩﻿]")


def read_translations(path):
    p = Path(path)
    if p.suffix.lower() == ".json":
        raw = json.loads(p.read_text(encoding="utf-8-sig"))
        if isinstance(raw, list):
            return {i: [l for l in v] for i, v in enumerate(raw, 1)}
        return {int(k): (v if isinstance(v, list) else str(v).split("\n")) for k, v in raw.items()}
    text = p.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    out = {}
    for chunk in re.split(r"\n\s*\n", text.strip("\n")):
        lines = [l for l in chunk.split("\n")]
        if not lines:
            continue
        head = lines[0].strip()
        if not head.isdigit():
            raise SystemExit(f"Refused: a block in {path} does not start with its number: {head!r}")
        out[int(head)] = lines[1:]
    return out


def normalise(lines):
    """Tidy whitespace only. Never changes words.

    Leading and trailing spaces and doubled spaces are typing artefacts, not
    translation choices, so fixing them here saves a round trip. Anything that
    could change meaning is refused instead, below.
    """
    fixed, notes = [], []
    for l in lines:
        s = re.sub(r" {2,}", " ", l.strip())
        if s != l:
            notes.append(s)
        fixed.append(s)
    return [l for l in fixed if l != ""], notes


def main():
    ap = argparse.ArgumentParser(description="Assemble the target SRT from the source structure.")
    ap.add_argument("--worksheet", required=True, help="JSON from srt_scaffold.py")
    ap.add_argument("--translations", required=True, help=".json or .txt of translated lines")
    ap.add_argument("--out", required=True, help="target .srt to write")
    ap.add_argument("--max-lines", type=int, default=2, help="maximum lines per block (default 2)")
    a = ap.parse_args()

    work = json.loads(Path(a.worksheet).read_text(encoding="utf-8"))
    trans = read_translations(a.translations)
    blocks = work["blocks"]
    refusals, tidied = [], []

    expected = {b["n"] for b in blocks}
    got = set(trans)
    for n in sorted(expected - got):
        refusals.append(f"b{n}: no translation given")
    for n in sorted(got - expected):
        refusals.append(f"b{n}: translation given for a block that is not in the source")

    out_blocks = []
    for b in blocks:
        lines, notes = normalise(trans.get(b["n"], []))
        if notes:
            tidied.append(b["n"])
        if not lines:
            refusals.append(f"b{b['n']}: empty after tidying whitespace")
        if len(lines) > a.max_lines:
            refusals.append(f"b{b['n']}: {len(lines)} lines (max {a.max_lines})")
        joined = " ".join(lines)
        for l in lines:
            if BIDI.search(l):
                refusals.append(f"b{b['n']}: invisible bidi or BOM character in the text")
        for span in b.get("preserve", []):
            if span not in joined:
                refusals.append(
                    f"b{b['n']}: text that is already in its own script in the source is not "
                    f"present exactly: {span!r}. Copy it from the worksheet, do not retype it."
                )
        if not b["ts"]:
            refusals.append(f"b{b['n']}: the source has no timestamp for this block")
        out_blocks.append((b["n"], b["ts"], lines))

    if refusals:
        print(f"REFUSED ({len(refusals)}). Nothing was written to {a.out}.")
        for r in refusals:
            print("  " + r)
        sys.exit(2)

    body = "\n\n".join(f"{n}\n{ts}\n" + "\n".join(lines) for n, ts, lines in out_blocks) + "\n"
    nl = "\r\n" if work["encoding"]["crlf"] else "\n"
    data = body.replace("\n", nl).encode("utf-8")
    if work["encoding"]["bom"]:
        data = b"\xef\xbb\xbf" + data
    Path(a.out).write_bytes(data)

    print(f"Written: {a.out}")
    print(f"blocks: {len(out_blocks)} · timestamps copied from the source, none typed")
    print(f"encoding reproduced: BOM={work['encoding']['bom']}, CRLF={work['encoding']['crlf']}")
    if tidied:
        print(f"whitespace tidied in blocks: {', '.join(str(n) for n in tidied)}")
    print("Next: run srt_structure_check.py against the source, then read the whole file aloud.")


if __name__ == "__main__":
    main()
