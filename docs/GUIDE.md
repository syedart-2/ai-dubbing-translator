# Guide: building an AI dubbing translation system that learns

## 1. The idea

An AI assistant does not "remember" how your team translates. Every time it starts a job, it reads a small set of files. Those files hold your rules, your word choices and every mistake you have already corrected. That is the whole trick.

**Training the AI = keeping these files up to date.** Each correction goes into a file. The next job reads that file, so the same mistake does not come back.

| Part | What it means |
|---|---|
| **Rules** | Fixed instructions: structure, style, content rules. Written once, changed rarely. |
| **Memory** | The glossary and the lessons log. They grow after every file. |
| **Checks** | A speaker map before translating, a QA script and a read-aloud after translating. |

The goal is a target-language SRT that a **voice actor** can read in the booth, with the original timing kept exactly.

## 2. One folder per language

Copy `templates/language-role/` once per language. The skill (`SKILL.md`) is shared; the folders are not. This keeps one source of truth per language and lets each language grow its own rules.

| File | Job |
|---|---|
| `_brief.md` | How this language role works: client, delivery target, reviewer, modules |
| `style-guide.md` | Word order, where a line may be cut, punctuation, numerals, register |
| `glossary.md` | Fixed term choices. Binding |
| `speaker-map-template.md` | Filled before every SRT translation |
| `qa-notes-template.md` | Flags saved with every delivery |
| `_LESSONS - <Language>.md` | Every mistake and the check that prevents it |
| `REFERENCE/` | Approved samples and team term lists. Read only |

## 3. The workflow for every file

1. Load the role files (brief, style guide, glossary, lessons, modules).
2. Read the activation line: file, job type, format, speakers.
3. Read the whole English file.
4. Propose a speaker map and **wait** for a person to confirm it.
5. Compose natural target-language speech, then cut it at phrase boundaries.
6. Keep the structure exact (blocks, numbering, timestamps, encoding).
7. Run the QA script until errors are zero.
8. Read the whole file back as continuous speech.
9. Save the SRT and the QA notes as new dated files.
10. Send it to a native reviewer if the manager does not read the language.
11. Write every correction into the right file the same day.

## 4. Why the speaker map comes first

Many languages encode things English hides: verb gender (Urdu, Hindi, Arabic, Hebrew), politeness level and first-person word (Japanese, Korean), formal or informal "you" (Spanish, German, French, Turkish). "I went" in English says nothing about who is speaking. In Urdu it is `میں گیا` from a man and `میں گئی` from a woman.

Get it wrong and the fix is not find-and-replace: the agreement runs through every verb and adjective in the file. So the AI proposes a map with its evidence, marks anything it cannot tell as UNKNOWN, and waits for a person.

## 5. Compose first, then cut

The most common failure is a file that passes every mechanical check and still reads like English wearing another language's words. It happens when the translation is cut on the English block boundaries.

So: write each sentence as natural speech with the grid out of sight, in the language's own word order. Only then place the cuts, at phrase boundaries the style guide allows. A short block holding one slow word is correct: it is a breath for the voice actor.

## 6. Lessons from real reviews (Urdu examples)

These came from production reviews. The pattern applies to every language; the examples are Urdu.

**Everyday words over book words.**

| Too bookish | Everyday |
|---|---|
| مسلمہ | پکی بات |
| تصادم | ٹکراؤ |
| محض | صرف |

A well-known classical term still beats a clumsy plain phrase. Once a key term is chosen, keep it through the whole argument.

**Never translate an idiom word for word.**

| English | Word for word (wrong) | Natural |
|---|---|---|
| at your own pace | اپنی رفتار سے | اپنی سہولت سے |
| you know (filler) | آپ جانتے ہیں | drop it, or use a natural filler |

This mistake came back three times before it got its own rule. That is what a lessons log is for.

**Other rules that came from reviews:**
- Number must match the real count: one person takes a singular noun.
- No explanations the speaker did not say.
- Keep the speaker's hesitations and restarts. Do not "clean them up".
- Modern words stay transliterated when that is what people say (ویڈیو، چینل).
- Grammatical gender is not biological sex. Mixing the two terms once broke the logic of a whole video.

## 7. A clean script is not a finished file

The QA script checks structure. It cannot tell whether the language sounds natural. A rejected file once passed the script twice. So two human-style checks are always required:

1. Read the whole file as continuous speech, blocks ignored.
2. Do not trust a clean result from a check that had nothing to check (for example a gender check on a file with no first-person speech).

## 8. The lessons loop: how the AI actually "learns"

**A correction given only in chat is lost when the chat ends.** It must go into a file the same day.

| Kind of correction | Where it goes |
|---|---|
| A word choice to use every time | Glossary |
| A rule for one series only | Series brief |
| A mistake that could happen again | Lessons log |
| A change to how the role works | Brief or style guide, plus a changelog line |

Every lessons entry has four parts: date and video code, what went wrong, how it was caught, and **the check that prevents it next time** (the most important part).

Add new entries at the end and never delete old ones. If a mistake repeats, write "repeat of <code>" in the title. A repeat means the check was not strong enough: make it stronger.

## 9. Building a new language

**Carries over unchanged:** the folder shape, the workflow, the structure rules, compose-then-cut, the lessons loop, "flag, do not guess", and any modules.

**Rebuilt for each language:**

| Item | Why it changes |
|---|---|
| Style guide | Word order, punctuation, numerals and cut rules differ |
| Glossary | Terms are written differently in each language and community |
| Speaker map column | Gender, politeness, formal "you" or first-person word |
| QA checks | Keep the structure checks; add checks for the language's own common errors |
| Reading-speed limit | Scripts read at different speeds |
| Reviewer | If the manager does not read the language, a native reviewer checks every file |

**Steps:**
1. Get one approved sample SRT in the language. Without it, the AI is guessing; say so in the brief.
2. Add any existing team term list to `REFERENCE/`.
3. Copy the template folder and adapt each file. Mark rules not yet confirmed by a reviewer as `[role rule]`.
4. Decide the speaker-map column.
5. Run the first file and expect many corrections. **Log every one.** The first five files do most of the training.
6. When the first file is approved, keep it in `REFERENCE/` and re-check the style guide against it.

## 10. Checklist for every file

- [ ] Role files loaded (brief, style guide, glossary, lessons, modules)
- [ ] Whole English file read
- [ ] Speaker map confirmed by a person
- [ ] Composed in the target language, then cut
- [ ] Block count, numbering and timestamps identical
- [ ] QA script: 0 errors, advisories read
- [ ] Read back as continuous speech
- [ ] SRT and QA notes saved as new dated files
- [ ] Native review if needed
- [ ] Every correction written into the right file today
