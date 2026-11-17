# Setup: build the system on your computer and connect it to your AI

This page takes you from zero to your first translated file. No coding knowledge is needed. Allow about 30 minutes, plus the time to find one good sample file.

App menus change often. Where this page names a button or menu, check your app's current help pages if it looks different.

---

## What you need

| Item | Why |
|---|---|
| A computer (Mac, Windows or Linux) | The workspace folder lives here |
| An AI assistant that can read and write files in a folder | For example the Claude desktop app with folder access, or Claude Code. Others work if they can read and write your folder |
| Python 3 (free) | Runs the three scripts. Most Mac and Linux machines have it; on Windows, install it from python.org. The commands on this page use `python3`; on Windows use `py` or `python` instead |
| One approved SRT in each target language | Calibrates the style guide. Without it, the system works but is "uncalibrated" |

---

## Step 1. Download this repository

On the repository page, click **Code**, then **Download ZIP**, and unzip it somewhere you will find again, for example `Documents/ai-dubbing-translator`.

(If you use git: `git clone <repository URL>`.)

## Step 2. Create your workspace folder

The **workspace** is where your languages, files and lessons live. Keep it separate from the downloaded repository, so an update to the repository never touches your work.

Example: `Documents/Dubbing Workspace`

```
Dubbing Workspace/
├── _tools/
│   ├── srt_scaffold.py          reads the source: timings and character budgets
│   ├── srt_assemble.py          writes the target file with the source's timings
│   └── srt_structure_check.py   checks the finished file
├── Urdu Dubbing Translator/
└── Spanish Dubbing Translator/
```

**Create one language folder per language.** The easy way, in a terminal opened in the downloaded repository:

```
python3 tools/new_language.py Spanish --workspace "~/Documents/Dubbing Workspace"
```

It copies the template, fills in the language name and date, copies all three scripts into `_tools/`, and never overwrites an existing folder.

**Without a terminal:** copy `templates/language-role/` into your workspace yourself, rename it `Spanish Dubbing Translator`, and copy the three scripts from `tools/` into a `_tools` folder.

**Optional, for working from other devices:** put the workspace inside a synced folder (Google Drive, OneDrive, Dropbox, iCloud). If your sync app offers it, set the workspace to **always keep files on this device**; otherwise the AI may find files that exist only in the cloud and cannot open them. See `STORAGE.md`.

## Step 3. Calibrate each language (the most important step)

In each language folder:

1. **REFERENCE/**: add one approved, human-checked SRT in that language, and any term list your team already uses.
2. **_brief.md**: fill in who the content is for, the delivery target (voice actor or text-to-speech), the reviewer, the reading-rate limit, and any module (for religious or quoted content, switch on `modules/sacred-and-quoted-texts.md`).
3. **style-guide.md** and **glossary.md**: fill in what you know. Or ask the AI: *"Read the sample in REFERENCE and draft the style guide and glossary for this language. Mark anything you are unsure of as [role rule]."* Then review its draft.

## Step 4. Install the skill

The skill is one file, `SKILL.md`. It teaches the AI the workflow.

**Claude desktop or web app:**
1. Make a folder named `ai-dubbing-translator` and put `SKILL.md` inside it.
2. Zip that folder.
3. Upload the zip in the app's skills settings (look under Settings for Skills or Capabilities).

**Claude Code:** copy `SKILL.md` to `~/.claude/skills/ai-dubbing-translator/SKILL.md` (on Windows: `%USERPROFILE%\.claude\skills\ai-dubbing-translator\SKILL.md`).

**Other AI assistants:** paste the contents of `SKILL.md` into the assistant's project or system instructions.

## Step 5. Connect the workspace folder to your AI

The AI must be able to **read and write** the workspace, or it cannot load your rules or save lessons.

**Claude desktop app:** give it access to your workspace folder (the app lets you add or connect a folder to a task or project). Approve the permission it asks for.

**Claude Code:** open a terminal in the workspace and start Claude Code there:
```
cd ~/Documents/"Dubbing Workspace"
claude
```
(On Windows PowerShell: `cd "$HOME\Documents\Dubbing Workspace"`, then `claude`.)

**Other assistants:** use their folder or file connector, or upload the language folder's files to a project. Without write access, the AI shows each new lesson in the chat and you save it yourself.

**Recommended:** add one line to your AI's custom or global instructions so it always knows where to look:

```
My dubbing workspace is <full path to the folder>. For any subtitle translation or dubbing task, use the ai-dubbing-translator skill and that workspace.
```

## Step 6. Your first file

1. Put the English SRT in the language's `INPUTS/` folder (or attach it in the chat).
2. Type the activation line:
   ```
   Spanish Dubbing Translator: ep12_ENG.srt - SRT for voice-over - interview - host male, guest female
   ```
3. Follow the steps in "How the skill works" below. Expect many corrections on the first files: that is the training.

---

## How the skill works

```
 You: activation line
        │
        ▼
 1. Load the language folder ── brief, style guide, glossary, lessons, modules
        │
        ▼
 2. Read the whole English SRT
        │
        ▼
 3. Speaker map ── AI proposes, YOU confirm (nothing is translated before this)
        │
        ▼
 4. Translate ── natural speech first, then cut into the original blocks
        │
        ▼
 5. QA ── script until 0 errors, then read back as continuous speech
        │
        ▼
 6. Deliver ── new dated SRT + QA notes in OUTPUTS/ (nothing overwritten)
        │
        ▼
 7. You review and correct ──► AI writes each correction into the glossary,
                                lessons log or style guide the same day
                                        │
                                        └──► the next file starts smarter
```

**Where things are saved:**

| What | Where |
|---|---|
| English source, confirmed speaker map | `INPUTS/YYYY-MM-DD <code> ...` |
| Translated SRT, QA notes | `OUTPUTS/YYYY-MM-DD <code> ...` |
| New fixed word choices | `glossary.md` |
| Mistakes and the checks that prevent them | `_LESSONS - <Language>.md` |
| Changes to how the language works | `_brief.md` or `style-guide.md`, plus `CHANGELOG.md` |

**What you decide, always:** the speaker map, any flagged line, new glossary terms, and the final approval. The AI never sends or publishes anything.

---

## Troubleshooting

These apply on Mac, Windows and Linux alike.

| Problem | Likely cause | Fix |
|---|---|---|
| The AI says it cannot find the language folder | Folder not connected, or a different name | Connect the workspace (Step 5) and keep the name `<Language> Dubbing Translator` |
| The AI cannot write lessons or save outputs | The AI has read-only access to the folder | Give it read and write access, or save the lessons it shows in the chat yourself |
| A file is listed but will not open | The workspace is in a synced folder (Google Drive, OneDrive, Dropbox, iCloud) and the file is stored only online | Open the file once so it downloads, or set the workspace to always keep files on this device. See `STORAGE.md` |
| Two copies of a file with "conflict" in the name | The same file was changed on two devices before syncing | Keep both, compare them, merge by hand. Never delete a lessons file |
| The AI repeats an old mistake | The correction was given in chat only | Ask it to write the lesson into the lessons file; check the entry has a concrete "check that prevents it" |
| The translation sounds like English in another language | It was cut on the English blocks before composing | Point the AI to Step 4 of the skill: compose first, then cut |
| QA script error: block count differs | A block was merged, split or dropped | The script names the first place the timestamps stop matching |
| `srt_assemble.py` says REFUSED and writes nothing | A structure rule was broken, so the file was not written at all | Read the list it printed, fix those blocks in the translations file, run it again. Nothing was damaged |
| REFUSED: "already in its own script ... not present exactly" | A word that should have been copied from the source was retyped, and differs invisibly | Copy that string from the worksheet's `preserve` column instead of typing it |
| `python3` not found | Python not installed, or on Windows the command has a different name | Install Python 3 from python.org. On Windows, try `py` or `python` instead of `python3` |
| Letters show as boxes or question marks | The SRT was saved in the wrong text encoding | Save it as UTF-8 in your text editor, then run the QA script again |
| A path with spaces fails in the terminal | The path was not in quotes | Put the whole path in double quotes, as in the examples |
