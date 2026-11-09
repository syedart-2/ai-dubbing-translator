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

## Run the QA script

```
python3 tools/srt_structure_check.py "translated.srt" --source "english.srt" --cps 25 --maxlen 50
```

It reports only and never edits. Exit code 1 means there are errors to fix.

Checks: block count, numbering, timestamps against the source, empty blocks, blocks with 3 or more lines, extra or double spaces, invisible direction characters, line length, reading speed, untranslated blocks, BOM and line endings, and vocalised Arabic copied exactly from the source.

It checks **structure only**. A clean run does not mean the translation is good: always read the whole file back as continuous speech, and use a native reviewer for any language you do not read.

## Principles

- **Timing is sacred.** Same blocks, same numbers, byte-identical timestamps.
- **Compose, then cut.** Write natural speech first, then split it at the language's own phrase boundaries.
- **Ask, do not guess.** Speakers, genders and doubtful terms are confirmed by a person.
- **Write every lesson down the same day,** with the check that prevents it.
- **Never overwrite.** New versions only.

## License

MIT. See `LICENSE`. You may use, change and share it, including commercially, as long as the license and credit stay with it.
