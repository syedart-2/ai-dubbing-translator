# Module: Sacred and quoted texts

Switch this on in a role's `_brief.md` when the content quotes scripture, religious sources, legal texts, or any words attributed to a real person. It applies on top of the workflow in `SKILL.md`.

Developed for religious content (Quran and hadith), and written so it works for any tradition or any quoted source.

## Rules (binding when switched on)

1. **Never translate a sacred or quoted text from memory.** Use the established published translation the brief names for that language, and flag the line in the QA notes.
2. **If the established text cannot be fetched,** leave a clearly marked placeholder (for example `[QUOTE: source, reference, needs established translation]`) and flag it. Never fill it from memory.
3. **Text already in the original script** (for example Arabic in an English SRT) is **extracted and copied**, never retyped. A retyped word can look identical while its marks are in the wrong order. The QA script checks vocalised Arabic for this.
4. **Honorifics** (titles and blessings attached to names): carry exactly what the source has. Do not add them where the source has none, and do not drop them where it does, unless the brief sets another rule.
5. **More than one defensible rendering with different meaning or weight:** flag it; do not decide. The translator makes no religious or legal rulings.
6. **Any doubt about a sacred or sensitive line:** ask before delivering.

## QA notes

Add a flag of type "quoted or sacred text" for every line this module touches, with the source and reference.

## Brief line to add

```
Modules switched on: modules/sacred-and-quoted-texts.md (established translation for <Language>: <name of the published translation>)
```
