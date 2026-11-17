# AI Dubbing Translator

A ready-made system for turning English SRT subtitles into **dubbing-ready translations in any language** with an AI assistant (built for Claude, usable with others). It keeps the timing intact for voice actors, and it **learns from every correction** you make.

Created by Muhammad Ali Nasir Ud Din. Built from a production workflow that has translated video for multilingual YouTube and social channels since July 2026.

## How it works in one line

The **skill** holds the workflow. Each language's **role folder** (brief, style guide, glossary, lessons log, QA script) holds the knowledge. Every correction is written back into the role folder, so the AI does better on the next file.

```
your-workspace/
├── Urdu Dubbing Translator/        <- one folder per language
│   ├── _brief.md                   how this language role works
│   ├── style-guide.md              word order, where lines may be cut, punctuation
│   ├── glossary.md                 fixed term choices (binding)
│   ├── speaker-map-template.md     who speaks, gender, who they address
│   ├── _LESSONS - Urdu.md          every mistake + the check that prevents it
│   ├── CHANGELOG.md
│   ├── INPUTS/  OUTPUTS/  REFERENCE/
└── Spanish Dubbing Translator/
```

## What is in this repo

| Path | What it is |
|---|---|
| `SKILL.md` | The AI skill: the step-by-step workflow for every file |
| `templates/language-role/` | Copy this folder to start a new language |
| `tools/srt_scaffold.py` | Reads the source once: timings, a character budget per block, and any text already in its own script |
| `tools/srt_assemble.py` | Writes the target SRT with the source's timestamps and encoding, and refuses a file that breaks a structure rule |
| `tools/srt_structure_check.py` | Language-neutral QA script (Python 3, no installs) |
| `modules/` | Optional rule sets you switch on per language, such as sacred and quoted texts |
| `docs/SETUP.md` | **Start here:** create the workspace on your computer, connect it to your AI, and how the skill works |
| `tools/new_language.py` | Creates a new language folder from the template in one command |
| `docs/GUIDE.md` | Full guide: why each rule exists and how to build a new language |
| `docs/STORAGE.md` | Working from a local folder or a cloud drive without losing lessons |

## Quick start (about 10 minutes)

Full step-by-step instructions, with the folder layout and a diagram of how the skill works, are in **`docs/SETUP.md`**.

Works on Mac, Windows and Linux. On Windows, type `py` or `python` where the commands say `python3`.

1. **Create a language folder:** `python3 tools/new_language.py Spanish --workspace "~/Documents/Dubbing Workspace"` (or copy `templates/language-role/` and rename it `Spanish Dubbing Translator`).
2. **Add a sample:** put one approved, human-checked SRT in that language into `REFERENCE/`. It calibrates the style guide.
3. **Fill the brief:** language, delivery target (voice actor or text-to-speech), reviewer, and any module you need.
4. **Install the skill** (below) and **connect the workspace folder** to your AI so it can read and write it.
5. **Run it:** `Spanish Dubbing Translator: episode12.srt - SRT for voice-over - interview - host male, guest female`

The AI first proposes a speaker map and waits for your confirmation, then translates, runs the QA script, and saves the translation and a short QA notes file.

## Install the skill

**Claude app:** create a folder named `ai-dubbing-translator`, put `SKILL.md` in it, zip the folder, and upload it in the app's skills settings. Menu names change between versions; check Claude's current help pages if they do not match.

**Claude Code:** copy `SKILL.md` to `~/.claude/skills/ai-dubbing-translator/SKILL.md` (on Windows: `%USERPROFILE%\.claude\skills\ai-dubbing-translator\SKILL.md`).

**Other AI assistants:** paste `SKILL.md` as the system or project instructions and give the assistant access to your workspace folder.

## Run the scripts

All three are plain Python 3 with no installs. They report or refuse; none of them edits your source.

An excerpt of a larger file is a normal job: add `--partial` to the first and third
commands and the blocks keep the numbers they have in the full file.

**1. Read the source** (before translating):

```
python3 tools/srt_scaffold.py "english.srt" --cps 25 --maxlen 50 --json work.json --md worksheet.md
```

Gives every block its real duration, a **character budget** at your reading-rate ceiling, and any
text already in its own script (Arabic in an English SRT, say) pulled out so it can be copied
instead of retyped.

**2. Write the target file** (after translating):

```
python3 tools/srt_assemble.py --worksheet work.json --translations trans.json --out "translated.srt"
```

Timestamps and numbering come from the worksheet, so no timestamp is ever typed. The source's BOM
and line endings are reproduced. It **refuses to write** if a block is missing, empty, over two
lines, carries an invisible direction character, or has lost a string that was meant to be copied
verbatim. Exit code 2 means nothing was written.

**3. Check it** (before delivering):

```
python3 tools/srt_structure_check.py "translated.srt" --source "english.srt" --cps 25 --maxlen 50 \
        --particles-file particles.txt --json qa.json
```

It reports only and never edits. Exit code 1 means there are errors to fix.

Checks: block count, numbering, timestamps against the source, timestamps that end before they
start or run backwards, overlapping blocks, empty blocks, blocks with 3 or more lines, blocks that
carry no content word, extra or double spaces, invisible direction characters, line length, reading
speed, untranslated blocks, BOM and line endings, and vocalised Arabic copied exactly from the
source.

It checks **structure only**. A clean run does not mean the translation is good: always read the whole file back as continuous speech, and use a native reviewer for any language you do not read.

## Principles

- **Timing is sacred.** Same blocks, same numbers, byte-identical timestamps, copied by a script and never typed.
- **No quick jobs.** Six pasted lines get the same rules as a whole episode. Skipping them is how a corrected mistake comes back.
- **Compose, then cut.** Write natural speech first, then split it at the language's own phrase boundaries.
- **Ask, do not guess.** Speakers, genders and doubtful terms are confirmed by a person.
- **Write every lesson down the same day,** with the check that prevents it.
- **A check that cannot fail is not evidence.** A clean result from a check that had nothing to find proves nothing.
- **At the third repeat, stop writing the lesson and change the machine.** Every refusal in `tools/` started as a lesson that came back.
- **Never overwrite.** New versions only, and read the delivered copy back before calling it saved.

## License

MIT. See `LICENSE`. You may use, change and share it, including commercially, as long as the license and credit stay with it.
