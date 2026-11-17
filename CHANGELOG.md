# Changelog

## 2.1.0 · 2026-11-17 · Lessons turned into mechanism

Rewritten against a 40-entry production lessons log. Each change below closes a
failure that happened in real use, three of them after the rule was already
written down. The theme is the same throughout: where a rule has been broken
repeatedly, replace the rule with a mechanism.

- **Triggering.** The skill description now says when to use the skill, not only
  what it does, including pasted lines and one-line requests with a file attached.
- **No quick jobs (Step 0).** The most repeated process failure was translating a
  short excerpt without loading the role files. It is now a gate at the top of the
  workflow rather than a sentence in the middle, with the two consequences spelled
  out: ask for the source file, and name a partial delivery as partial.
- **New `tools/srt_scaffold.py`.** Reads the source once for timings, a per-block
  character budget at the reading-rate ceiling, and any text already in its own
  script. Knowing the budget before composing replaces re-cutting lines at QA.
- **New `tools/srt_assemble.py`.** Writes the target SRT with timestamps and
  numbering copied from the source and the source's encoding reproduced, and
  refuses the file if a block is missing, empty, over two lines or has lost a
  string that was meant to be copied verbatim. "Never retype a timestamp" and
  "never retype vocalised Arabic" are now enforced instead of requested.
- **QA script.** Added timestamp sanity checks that work without a source (ends
  before it starts, runs backwards, overlaps), an optional `--particles-file` so
  blocks carrying no content word are caught, and `--json` so the fix-and-re-run
  loop reads data instead of prose. A block the source already carries in its own
  script is no longer flagged as untranslated.
- **One source of truth for cut rules.** `templates/language-role/particles.txt`
  is read by both the style guide and the QA script, because the two lists drifted
  apart in practice and the script was the one that was right.
- **A check that cannot fail is not evidence (Step 5).** Three ways a green check
  has passed a bad file, written out: nothing to find, a defect that manufactured
  the evidence, and a tool that can only pick from a list.
- **Verify the delivered copy (Step 6).** A write can report success and leave the
  old version in place. Read the file back from where you wrote it, on every
  write. Plus what to deliver when no workspace is reachable.
- **Escalation rule (Step 7).** At a third occurrence, stop writing the lesson and
  promote it to a step in the workflow or a refusal in a script.
- Speaker map: scan the whole file for turn-taking, never read one quote span as
  one speaker, and take context from the full telling rather than the montage clip
  beside it. Meaning: a back-translation pass for additions, a named pass for
  English sentence shape, and rewrite the whole line when a correction does not
  name the wrong word.
- `New language setup` now points to `docs/GUIDE.md` section 9 instead of
  duplicating it, which keeps the hot path shorter and the two copies from drifting.
- `tools/new_language.py` copies all three scripts and fills in `.txt` templates.
- **Excerpts are first-class.** `srt_scaffold.py` and `srt_structure_check.py` take
  `--partial`, so a few blocks pulled out of a larger file keep the numbers they
  have there instead of being renumbered from 1. Found by the test run below: the
  first version of the scaffold refused an excerpt, and the agent fell back to a
  hand-written script, which is the exact thing these tools exist to replace.
- An unconfirmed speaker map now has its own file name, so an assumption cannot be
  read later as a decision.
- `evals/` added: a sample English SRT fixture, a test role folder whose glossary
  and lessons log contain terms that appear in the fixture, three test cases, and
  `evals/grade.py` to score the mechanical ones. The three cases were run against
  both 2.0 and 2.1 with the same model; `_eval-workspace/benchmark.md` has the
  numbers and the honest caveats, the main one being that the translation-quality
  assertions pass in both versions and so do not measure the rewrite.

## 2.0.0 · 2026-11-09 · First public release

- Generic for any language and any organization (version 1 was internal to one team).
- New `templates/language-role/` folder to start a language in minutes.
- Optional `modules/`, starting with "Sacred and quoted texts".
- `docs/STORAGE.md`: local folder first, cloud copy as backup, and the replace-and-verify rule so lessons are never lost on a cloud drive.
- New `docs/SETUP.md`: build the workspace on your computer, connect it to your AI, and a diagram of how the skill works.
- New `tools/new_language.py`: creates a language folder from the template in one command, never overwriting.
- QA script unchanged in behaviour; moved to `tools/`.
- Setup and troubleshooting written for Mac, Windows and Linux alike.

## 1.0.0 · 2026-11-08 · Internal

- Workflow skill, QA script and team guide, built from a single-language role that has run since July 2026.
