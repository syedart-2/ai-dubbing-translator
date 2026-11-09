# Storage: local folder, cloud copy, and never losing a lesson

The system lives in ordinary files. The AI must be able to read them before it translates and write to them after a correction. This page covers the three situations it meets.

## 1. Local folder reachable (best)

Read and write the role folder directly. Append new lessons to the end of the lessons file. Save outputs as new dated files.

**Synced drives (iCloud, OneDrive, Google Drive for desktop):** a file can exist only as a cloud placeholder and fail to open, even though it is listed. Treat that as "not downloaded", not "missing". Download it (or set the folder to always keep files on the device) before concluding anything.

## 2. Only a cloud copy reachable

Many cloud connectors can create files but cannot edit a file's content in place. Use **replace-and-verify** to change an existing file such as the lessons log or the glossary:

1. **Read** the main file in full. Note its name, file ID and folder.
2. **Build** the new version: the old content exactly as it was, plus the new entries at the end (or in the right section). Do not reword old content.
3. **Create** it in the same folder as `<file name> NEW.md`, as plain text, not converted to a document format.
4. **Verify** by reading the new file back: the old content is present word for word, every new entry is present, and the format is unchanged.
5. **If the check passes:** move the old file into an `_archive/` folder next to it, renamed `<file name> (replaced YYYY-MM-DD).md`, then rename the new file to the original name. Moving keeps a safety copy; nothing is deleted.
6. **If the check fails:** change nothing. Save the new entries as `<file name> addendum YYYY-MM-DD.md` beside the main file, with the first line `Addendum to: <file name>. Status: NOT MERGED.`

Until an addendum is merged, any AI reading the main file must also read its addenda.

## 3. Nothing reachable

Say so in one line. Translate only from the universal rules in `SKILL.md`, label the output "uncalibrated", and show any new lesson in the chat so the user can save it.

## When the local folder is back

1. Let the sync finish, then check that replaced files show the new entries.
2. If a sync conflict produced two versions, keep both and ask the user.
3. Merge any addenda into their main file, oldest first, without rewording. Move the merged addenda into `_archive/merged-addenda/`.

## Rules that never change

- Never delete a user's file. Archive instead.
- Never overwrite an original. New versions only.
- Never create a second copy of a lessons file or glossary. One source of truth per language.
