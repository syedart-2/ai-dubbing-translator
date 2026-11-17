# Urdu Dubbing Translator (test fixture)

Status: Active · Version: 1.0 · Created: 2026-11-17 · Calibrated from: `REFERENCE/approved-sample.srt`

**Purpose:** translate English SRTs into natural, performable Urdu that a voice actor can record inside the original timing.

## Client and content

- Who the content is for: a faith-based documentary channel, adult general audience, plain spoken register.
- Profile files to read before every job: none
- Modules switched on: `modules/sacred-and-quoted-texts.md` (established translation for Urdu: Fateh Muhammad Jalandhari)

## Activate

`Urdu Dubbing Translator: [file] - [job type] - [format] - [speakers, if known]`

## Delivery target

Human voice actor.

## Speaker map column

What a speaker changes in Urdu that English does not show: verb and adjective gender agreement.

## Hard rules: structure

Same block count, same numbering, byte-identical timestamps, same encoding, BOM and line endings, nothing added, 1 or 2 lines per block. See `SKILL.md` Step 4.

## Reading rate

Maximum characters per second for the QA script: 25. Maximum line length: 50.

## Reviewer

Native Urdu reviewer. The person managing the work does read Urdu.
