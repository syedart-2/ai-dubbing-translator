In a real workspace this folder holds the scripts, put here by `tools/new_language.py`.

The fixture keeps it empty on purpose. A committed copy of a script here would be a
second source of truth that silently falls behind `tools/`, which is the same drift the
skill warns about for cut rules. Test runs should call the scripts in `tools/` directly,
or copy them in at the start of the run.
