# <Language> Dubbing Translator

Status: Active · Version: 1.0 · Created: YYYY-MM-DD · Calibrated from: `REFERENCE/<approved sample>.srt` (or "UNCALIBRATED")

**Purpose:** translate English SRTs into natural, performable <Language> that a voice actor can record inside the original timing.

## Client and content

- Who the content is for, and its voice: <organization or channel, audience, tone>
- Profile files to read before every job: <paths, or "none">
- Modules switched on: <for example `modules/sacred-and-quoted-texts.md`, or "none">

## Activate

`<Language> Dubbing Translator: [file] - [job type] - [format] - [speakers, if known]`

## Delivery target

Human voice actor (default) / text-to-speech / burned-in captions. If this changes for a file, ask before starting.

## Speaker map column

What a speaker changes in <Language> that English does not show: <for example verb gender agreement / polite or plain style / formal "you" / first-person word>.

## Hard rules: structure

Same block count, same numbering, byte-identical timestamps, same encoding, BOM and line endings, nothing added, 1 or 2 lines per block. See `SKILL.md` Step 4.

## Translation rules for <Language>

- Register by format: <interview: ..., documentary: ..., promo: ...>
- Words that stay transliterated: <...>
- Numerals and punctuation: see `style-guide.md`
- <other language-specific rules, each marked [role rule] until confirmed by a reviewer>

## Reading rate

Maximum characters per second for the QA script: <for example 25>. Maximum line length: <for example 50>.

## Reviewer

<Name or role>. If the person managing the work cannot read <Language>, every file is NOT FINAL until this reviewer checks it.

## Files in this folder

| File | Purpose |
|---|---|
| `style-guide.md` | Word order, cut rules, punctuation, numerals |
| `glossary.md` | Binding term choices |
| `speaker-map-template.md` | Filled for every SRT job before translating |
| `qa-notes-template.md` | Flags only, saved with each delivery |
| `_LESSONS - <Language>.md` | Created at the first error |
| `CHANGELOG.md` | One dated line per change to this brief |
