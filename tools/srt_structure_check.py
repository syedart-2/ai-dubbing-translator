#!/usr/bin/env python3
"""Language-neutral SRT structure check. Reports only; never edits.
Part of ai-dubbing-translator. MIT License, (c) 2026 Muhammad Ali Nasir Ud Din.
Usage: python3 srt_structure_check.py TARGET.srt --source ENG.srt [--cps 25] [--maxlen 50]"""
import argparse, re, sys
TS = re.compile(r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}")
BIDI = re.compile("[\u200e\u200f\u061c\u202a-\u202e\u2066-\u2069\ufeff]")
ARABIC_VOCALISED = re.compile("[\u0600-\u06ff\u0750-\u077f]*[\u064b-\u0652\u0670][\u0600-\u06ff\u0750-\u077f\u064b-\u0652\u0670]*")

def load(path):
    raw = open(path, "rb").read()
    info = {"bom": raw.startswith(b"\xef\xbb\xbf"), "crlf": b"\r\n" in raw}
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    blocks = []
    for chunk in re.split(r"\n\s*\n", text.strip("\n")):
        lines = chunk.split("\n")
        if len(lines) < 2:
            blocks.append({"num": lines[0], "ts": "", "text": []}); continue
        blocks.append({"num": lines[0].strip(), "ts": lines[1].strip(), "text": lines[2:]})
    return blocks, info

def secs(t):
    h, m, rest = t.split(":"); s, ms = rest.split(",")
    return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000

def report(title, items, cap=12):
    """Group by message type so one missing block does not bury everything else."""
    print(f"{title} ({len(items)})")
    groups = {}
    for it in items:
        key = re.sub(r"^b\d+: ", "", it); key = re.sub(r"'[^']*'|\d+(\.\d+)?", "#", key)
        groups.setdefault(key, []).append(it)
    for key, its in groups.items():
        for it in its[:cap]: print("  " + it)
        if len(its) > cap: print(f"  ... and {len(its) - cap} more of this kind")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("--source")
    ap.add_argument("--cps", type=float, default=25.0)
    ap.add_argument("--maxlen", type=int, default=50)
    a = ap.parse_args()
    tgt, ti = load(a.target)
    err, adv = [], []
    for i, b in enumerate(tgt, 1):
        if b["num"] != str(i): err.append(f"b{i}: numbering reads '{b['num']}'")
        if not TS.match(b["ts"]): err.append(f"b{i}: bad timestamp line '{b['ts']}'")
        if not any(l.strip() for l in b["text"]): err.append(f"b{i}: empty text")
        if len(b["text"]) > 2: err.append(f"b{i}: {len(b['text'])} lines (max 2)")
        for l in b["text"]:
            if l != l.strip(): err.append(f"b{i}: leading/trailing space")
            if "  " in l: err.append(f"b{i}: double space")
            if BIDI.search(l): err.append(f"b{i}: invisible bidi/BOM character")
            if len(l) > a.maxlen: adv.append(f"b{i}: line {len(l)} chars (> {a.maxlen})")
        if TS.match(b["ts"]):
            st, en = b["ts"].split(" --> ")
            dur = secs(en[:12]) - secs(st)
            chars = sum(len(l) for l in b["text"])
            if dur > 0 and chars / dur > a.cps:
                adv.append(f"b{i}: {chars/dur:.1f} chars/sec (> {a.cps}), read it aloud")
    if a.source:
        src, si = load(a.source)
        if len(src) != len(tgt):
            err.append(f"block count {len(tgt)} vs source {len(src)}")
            for i, (s, t) in enumerate(zip(src, tgt), 1):
                if s["ts"] != t["ts"]:
                    err.append(f"first timestamp mismatch at b{i}: a block was probably merged, split or dropped here"); break
        for i, (s, t) in enumerate(zip(src, tgt), 1):
            if s["ts"] != t["ts"]: err.append(f"b{i}: timestamp differs from source")
            if [x.strip() for x in s["text"]] == [x.strip() for x in t["text"]] and any(s["text"]):
                adv.append(f"b{i}: identical to source (untranslated?)")
            for ar in ARABIC_VOCALISED.findall(" ".join(s["text"])):
                if ar and ar not in " ".join(t["text"]):
                    err.append(f"b{i}: vocalised Arabic from source not copied exactly: {ar}")
        if si["bom"] != ti["bom"]: adv.append(f"BOM: source={si['bom']} target={ti['bom']}")
        if si["crlf"] != ti["crlf"]: adv.append(f"line endings: source CRLF={si['crlf']} target CRLF={ti['crlf']}")
    report("ERRORS", err); report("ADVISORIES", adv)
    sys.exit(1 if err else 0)

if __name__ == "__main__":
    main()
