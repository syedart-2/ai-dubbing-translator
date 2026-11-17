# <Language> Style Guide

Built from `REFERENCE/<approved sample>.srt` on YYYY-MM-DD. Add to it whenever a reviewer corrects something.

## Word order

- Natural order: <for example subject, object, verb>
- Where time, place and means go: <...>

## Where a line may be cut

Cut only at a natural phrase boundary.

**Never cut between:**
- <for example a noun and its postposition>
- <for example the parts of a compound verb>
- <...>

**Never leave alone in a block:** the words listed in `particles.txt`, which is the single
source of truth for this rule. The QA script reads that same file with `--particles-file`,
so the guide and the script cannot drift apart. Add a word there, not here.

Every block must carry at least one content word: a lone particle is ambiguous read aloud.

## Sentence frames to rewrite, not translate

English frames that sound foreign when copied:
| English frame | Write instead |
|---|---|
| <...> | <...> |

## Punctuation, numerals, quotes

- Full stop, comma, question mark: <which characters>
- Numerals: <Western / local digits; when to write numbers as words>
- Quotation marks: <...>
- Spacing rules: <...>

## Line length and reading rate

- Typical line: <n> characters; maximum: <n>
- Reading rate ceiling for voice-over: <n> characters per second

## Register

| Format | Register |
|---|---|
| Interview | <...> |
| Documentary | <...> |
| Promo | <...> |
