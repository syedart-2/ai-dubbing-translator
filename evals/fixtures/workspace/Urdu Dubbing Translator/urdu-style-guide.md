# Urdu Style Guide

Built from `REFERENCE/approved-sample.srt`. Add to it whenever a reviewer corrects something.

## Word order

- Natural order: subject, object, verb.
- Time, place and means go **before** the verb, never trailing after it as English does.

## Where a line may be cut

Cut only at a natural phrase boundary.

**Never cut between:**
- a noun and its postposition (کو، سے، میں، پر، کا/کے/کی)
- the parts of a compound verb (استعمال کرنا، ذکر کرنا)
- the ergative نے and its subject
- an اضافت pair

**Never leave alone in a block:** the words listed in `particles.txt`, which is the single source of truth for this rule. The QA script reads that same file with `--particles-file`.

## Punctuation, numerals, quotes

- Full stop: ۔  Question mark: ؟  Comma: ،
- Numerals: Western digits.

## Line length and reading rate

- Maximum 50 characters per line; ceiling 25 characters per second.

## Register

| Format | Register |
|---|---|
| Interview | plain spoken Urdu, the way a person talks |
| Documentary | neutral narration, no literary flourish |
