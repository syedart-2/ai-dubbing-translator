#!/usr/bin/env python3
"""Grade the mechanically checkable assertions for one iteration.

Assertions that need judgement (did it gate on the speaker map, did it offer the
user a choice) are left with "passed": null for a person to fill in. Anything a
script can decide, a script decides: it is faster, repeatable across iterations,
and it cannot talk itself into a pass.

Usage: python3 evals/grade.py _eval-workspace/iteration-1
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "evals" / "fixtures" / "sample_ENG.srt"
CHECK = REPO / "tools" / "srt_structure_check.py"
PARTICLES = REPO / "evals" / "fixtures" / "workspace" / "Urdu Dubbing Translator" / "particles.txt"
SRT_BLOCK = re.compile(r"^\s*\d+\s*\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", re.M)


def source_blocks():
    text = SOURCE.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    out = {}
    for chunk in re.split(r"\n\s*\n", text.strip("\n")):
        lines = chunk.split("\n")
        if len(lines) >= 2 and lines[0].strip().isdigit():
            out[int(lines[0].strip())] = {"ts": lines[1].strip(), "text": lines[2:]}
    return out


SRC = source_blocks()
ARABIC_B10 = " ".join(SRC[10]["text"]).strip()


def find_srt(run: Path):
    """The delivered file, wherever the run put it, including inside a chat reply."""
    cands = sorted(run.rglob("*.srt"))
    cands = [c for c in cands if "_ENG" not in c.name and "approved-sample" not in c.name
             and "REFERENCE" not in c.parts and "INPUTS" not in c.parts]
    if cands:
        return cands[0].read_text(encoding="utf-8-sig"), str(cands[0].relative_to(run))
    for md in sorted(run.rglob("*.md")):
        body = md.read_text(encoding="utf-8", errors="replace")
        for fence in re.findall(r"```[a-z]*\n(.*?)```", body, re.S):
            if SRT_BLOCK.search(fence) and fence.count("-->") >= 3:
                return fence, f"{md.relative_to(run)} (code block)"
    return None, None


def all_prose(run: Path):
    parts = []
    for p in sorted(run.rglob("*.md")):
        parts.append(p.read_text(encoding="utf-8", errors="replace"))
    for p in sorted(run.rglob("*.txt")):
        if p.name != "particles.txt":
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def parse(text):
    out = {}
    for chunk in re.split(r"\n\s*\n", text.replace("\r\n", "\n").strip("\n")):
        lines = chunk.split("\n")
        if len(lines) >= 2 and lines[0].strip().isdigit():
            out[int(lines[0].strip())] = {"ts": lines[1].strip(), "text": lines[2:]}
    return out


def strip_marks(s):
    return "".join(c for c in s if not unicodedata.combining(c))


def grade(run: Path, assertions):
    srt, srt_where = find_srt(run)
    blocks = parse(srt) if srt else {}
    prose = all_prose(run)
    haystack = (srt or "") + "\n" + prose
    results = []

    for a in assertions:
        aid, text = a["id"], a["text"]
        passed, ev = None, ""

        if aid == "structure":
            if not srt:
                passed, ev = False, "no SRT found in the run output"
            else:
                tmp = run / "_graded.srt"
                tmp.write_text(srt if srt.endswith("\n") else srt + "\n", encoding="utf-8")
                r = subprocess.run([sys.executable, str(CHECK), str(tmp), "--source", str(SOURCE)],
                                   capture_output=True, text=True)
                tmp.unlink(missing_ok=True)
                errs = [l.strip() for l in r.stdout.splitlines()
                        if l.startswith("  ") and "ERRORS" not in l]
                nerr = int(re.search(r"ERRORS \((\d+)\)", r.stdout).group(1))
                passed = nerr == 0 and len(blocks) == len(SRC)
                ev = (f"{srt_where}: {len(blocks)} blocks, structure check errors={nerr}"
                      + ("" if passed else " :: " + "; ".join(errs[:4])))

        elif aid == "glossary-million":
            good = "ملین" in haystack
            bad = [w for w in ("کروڑ", "لاکھ") if w in haystack]
            passed = good and not bad
            ev = f"ملین present={good}; forbidden found={bad or 'none'}"

        elif aid == "lessons-idiom":
            good = "سہولت" in haystack
            bad = "رفتار" in haystack
            passed = good and not bad
            ev = f"سہولت present={good}; رفتار present={bad}"

        elif aid == "lessons-filler":
            bad = "جانتے ہیں" in haystack
            passed = not bad
            ev = f"آپ جانتے ہیں present={bad}"

        elif aid == "arabic-verbatim":
            got = " ".join(blocks.get(10, {}).get("text", [])).strip() if blocks else ""
            if not got:
                got_any = ARABIC_B10 in haystack
                passed = got_any
                ev = ("block 10 not located as a block; exact Arabic string found elsewhere in the "
                      f"output={got_any}")
            else:
                passed = got == ARABIC_B10
                ev = ("block 10 codepoint-identical to source" if passed else
                      f"block 10 differs; same letters ignoring marks="
                      f"{strip_marks(got) == strip_marks(ARABIC_B10)}")

        elif aid == "no-bare-particle":
            parts = {w.strip() for w in PARTICLES.read_text(encoding="utf-8-sig").splitlines()
                     if w.strip() and not w.startswith("#")}
            offenders = []
            for n, b in blocks.items():
                words = re.findall(r"[^\s،؟۔.,!?]+", " ".join(b["text"]))
                if words and all(w in parts for w in words):
                    offenders.append(n)
            passed = not offenders
            ev = f"blocks that are only function words: {offenders or 'none'}"

        elif aid == "timestamps-exact":
            found = re.findall(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", haystack)
            known = {b["ts"] for b in SRC.values()}
            wrong = sorted({t for t in found if t not in known})
            passed = not wrong
            ev = (f"{len(found)} timestamps reproduced, "
                  + ("all match the source exactly" if passed else f"not in source: {wrong[:3]}"))

        results.append({"id": aid, "text": text, "passed": passed, "evidence": ev,
                        "method": "script" if passed is not None else "needs judgement"})
    return {"run": run.name, "srt_found": srt_where, "expectations": results}


def main():
    it = Path(sys.argv[1])
    summary = {}
    for eval_dir in sorted(p for p in it.iterdir() if p.is_dir()):
        meta_path = eval_dir / "eval_metadata.json"
        if not meta_path.exists():
            continue
        assertions = json.loads(meta_path.read_text(encoding="utf-8"))["assertions"]
        for cfg in ("with_skill", "old_skill"):
            run = eval_dir / cfg
            if not run.exists():
                continue
            g = grade(run, assertions)
            (run / "grading.json").write_text(json.dumps(g, ensure_ascii=False, indent=1),
                                              encoding="utf-8")
            scored = [e for e in g["expectations"] if e["passed"] is not None]
            summary[f"{eval_dir.name}/{cfg}"] = (
                f"{sum(1 for e in scored if e['passed'])}/{len(scored)} scripted checks passed"
                f" ({len(g['expectations']) - len(scored)} need judgement)")
    for k, v in summary.items():
        print(f"{k:55s} {v}")


if __name__ == "__main__":
    main()
