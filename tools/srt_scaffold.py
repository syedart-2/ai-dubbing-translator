#!/usr/bin/env python3
"""Read an English SRT and write a translation worksheet.

Part of ai-dubbing-translator. MIT License, (c) 2026 Muhammad Ali Nasir Ud Din.

Why this exists: the two rules that are hardest to keep by hand are "never retype
a timestamp" and "never retype text that is already in its own script". Both have
failed in production even with the rules written down, because a timestamp typed
from memory looks right and a retyped Arabic word can be wrong at the codepoint
level while rendering identically. This script reads the timings and the foreign
script out of the source once, so nothing downstream has to be typed again.

It also gives each block a character budget, worked out from the block's real
duration and the reading-rate ceiling. Knowing the budget before composing is
much cheaper than discovering an overrun at QA and re-cutting the line.

Reports only. It never writes to the source.

Usage:
  python3 tools/srt_scaffold.py ENGLISH.srt [--cps 25] [--maxlen 50]
                                [--json work.json] [--md worksheet.md]

With no --json or --md it prints the worksheet to the screen.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

TS = re.compile(r"^(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})")


def is_foreign_letter(ch):
    """A letter or combining mark outside the Latin range.

    Used to find text that is already in its own script inside an English
    source, for example a Quranic word in Arabic. Combining marks matter most:
    they are what a retyped copy gets wrong.
    """
    if ord(ch) <= 0x02FF:
        return False
    return unicodedata.category(ch)[0] in ("L", "M")


def foreign_spans(text):
    """Maximal runs of foreign-script text, keeping internal spaces.

    A multi-word phrase stays one span so it can be substituted whole.
    """
    spans, run, pending = [], [], []
    for ch in text:
        if is_foreign_letter(ch):
            run.extend(pending)
            pending = []
            run.append(ch)
        elif run and (ch.isspace() or ch in "،؛؟ـ‍-'’"):
            pending.append(ch)
        else:
            if run:
                spans.append("".join(run))
            run, pending = [], []
    if run:
        spans.append("".join(run))
    return [s.strip() for s in spans if s.strip()]


def secs(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def load(path):
    raw = Path(path).read_bytes()
    info = {"bom": raw.startswith(b"\xef\xbb\xbf"), "crlf": b"\r\n" in raw}
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    blocks = []
    for chunk in re.split(r"\n\s*\n", text.strip("\n")):
        lines = chunk.split("\n")
        if len(lines) < 2:
            blocks.append({"num": lines[0].strip(), "ts": "", "text": []})
            continue
        blocks.append({"num": lines[0].strip(), "ts": lines[1].strip(), "text": lines[2:]})
    return blocks, info


def build(path, cps, maxlen, partial=False):
    """partial=True for an excerpt, whose numbering is the source's own, not 1..N.

    An excerpt of a real file is a normal job: a few blocks pasted into a chat, or
    a range the editor wants redone. Refusing it would push the work back to a
    hand-written script, which is the very thing these tools exist to replace.
    """
    blocks, info = load(path)
    out, problems = [], []
    prev_num = None
    for i, b in enumerate(blocks, 1):
        m = TS.match(b["ts"])
        if partial:
            if not b["num"].isdigit():
                problems.append(f"block {i}: numbering reads '{b['num']}', which is not a number")
            elif prev_num is not None and int(b["num"]) <= prev_num:
                problems.append(f"block {i}: number {b['num']} does not come after {prev_num}")
            if b["num"].isdigit():
                prev_num = int(b["num"])
        elif b["num"] != str(i):
            problems.append(f"b{i}: source numbering reads '{b['num']}'. "
                            f"If this is an excerpt rather than a whole file, pass --partial.")
        if not m:
            problems.append(f"b{i}: source has no readable timestamp line '{b['ts']}'")
            dur = None
        else:
            start, end = secs(m.group(1)), secs(m.group(2))
            dur = round(end - start, 3)
            if dur <= 0:
                problems.append(f"b{i}: source block ends at or before it starts")
        english = [l.rstrip() for l in b["text"]]
        joined = " ".join(english)
        out.append({
            "n": int(b["num"]) if b["num"].isdigit() else i,
            "position": i,
            "ts": b["ts"],
            "duration_s": dur,
            "char_budget": int(dur * cps) if dur and dur > 0 else None,
            "max_chars_per_line": maxlen,
            "english": english,
            "preserve": foreign_spans(joined),
        })
    return {
        "source": str(Path(path).resolve()),
        "partial": partial,
        "encoding": info,
        "cps": cps,
        "maxlen": maxlen,
        "block_count": len(out),
        "source_problems": problems,
        "blocks": out,
    }


def worksheet_md(data):
    lines = [
        f"# Translation worksheet",
        "",
        f"Source: `{data['source']}`",
        ("Excerpt: the block numbers below are the source's own, not 1..N.\n" if data.get("partial") else "") +
        f"Blocks: {data['block_count']} · reading-rate ceiling: {data['cps']} chars/sec "
        f"· max {data['maxlen']} chars per line",
        f"Encoding to reproduce: BOM={data['encoding']['bom']}, CRLF={data['encoding']['crlf']}",
        "",
        "`budget` is the character count this block's duration allows at the ceiling. "
        "It is a guide for composing, not a hard limit: a block over budget is an "
        "advisory to read aloud, not an error.",
        "",
        "`preserve` is text already in its own script in the source. Copy it from this "
        "file. Do not retype it: a retyped form can be wrong in its combining marks "
        "and still look identical.",
        "",
        "| # | duration | budget | English | preserve |",
        "|---|---|---|---|---|",
    ]
    for b in data["blocks"]:
        eng = " / ".join(b["english"]).replace("|", "\\|")
        pres = " · ".join(b["preserve"]).replace("|", "\\|")
        dur = f"{b['duration_s']:.2f}s" if b["duration_s"] is not None else "?"
        lines.append(f"| {b['n']} | {dur} | {b['char_budget'] or '?'} | {eng} | {pres} |")
    if data["source_problems"]:
        lines += ["", "## Problems in the source", ""]
        lines += [f"- {p}" for p in data["source_problems"]]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Write a translation worksheet from an English SRT.")
    ap.add_argument("source")
    ap.add_argument("--cps", type=float, default=25.0, help="reading-rate ceiling, characters per second")
    ap.add_argument("--maxlen", type=int, default=50, help="maximum characters per line")
    ap.add_argument("--json", help="write the machine-readable worksheet here (feeds srt_assemble.py)")
    ap.add_argument("--md", help="write the readable worksheet here")
    ap.add_argument("--partial", action="store_true",
                    help="the source is an excerpt, so keep its own block numbers instead of requiring 1..N")
    a = ap.parse_args()

    data = build(a.source, a.cps, a.maxlen, partial=a.partial)
    if a.json:
        Path(a.json).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"worksheet (json): {a.json}")
    if a.md:
        Path(a.md).write_text(worksheet_md(data), encoding="utf-8")
        print(f"worksheet (markdown): {a.md}")
    if not a.json and not a.md:
        print(worksheet_md(data))
    print(f"blocks: {data['block_count']}")
    n_pres = sum(1 for b in data["blocks"] if b["preserve"])
    if n_pres:
        print(f"blocks with text already in its own script (copy, never retype): {n_pres}")
    for p in data["source_problems"]:
        print("source problem: " + p)
    sys.exit(1 if data["source_problems"] else 0)


if __name__ == "__main__":
    main()
