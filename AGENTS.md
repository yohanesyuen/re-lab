# re-lab — agent guide

Reverse-engineering lab for binary file formats. Generic tooling lives in the
`relab` package; everything format-specific lives under `formats/<name>/` and
never leaks back into `src/`. Inherits the rules in `~/projects/CLAUDE.md` and
`~/.claude/CLAUDE.md` (uv for every Python invocation, click for every CLI,
feature branches, explicit `git add <file>`).

## Layout

| Path | What goes there |
|---|---|
| `src/relab/binary/` | Byte-level primitives: carve, search, dump, entropy, codec. No knowledge of any format. |
| `src/relab/structure/` | Record/field/relation inference over a region of bytes. |
| `src/relab/analysis/` | Frequency, strings, deltas, and multi-sample comparison. |
| `src/relab/containers/` | Outer wrappers (OLE2 via `olefile`, ZIP, embedded compression) that yield inner streams. |
| `formats/<fmt>/probes/` | One click script per hypothesis; takes a sample path, prints findings. |
| `formats/<fmt>/notes/` | What each probe established. One note per topic, named after its probe. |
| `formats/<fmt>/fixtures/` | Local sample files. **Gitignored** — samples are proprietary or large; only `.gitkeep` is tracked. |
| `research/prior-art/` | One note per existing project we learn from; what it parses, what it leaves opaque. |
| `research/experiments/` | Dated `YYYY-MM-DD-<topic>.md` lab notebook entries: question, method, result, next. |
| `scripts/` | User-facing click CLIs composed from `relab`; `scan.py` is the first thing to run on a new sample. |
| `tests/` | Mirrors `src/relab/`. Currently import smoke tests only. |

## Status

Every `.py` is a stub: a module docstring stating its intended responsibility,
and CLIs that raise `NotImplementedError`. Implement behind the docstring's
contract; if the contract is wrong, change the docstring in the same commit.

## Running

```
uv sync                                  # creates .venv, installs relab editable + dev deps
uv run pytest                            # import smoke tests
uv run scripts/scan.py <sample>          # any script or probe; they are uv-run shebang'd
uv run formats/rvt/probes/streams.py <sample>
```

Scripts and probes import `relab`, so they run inside the project env rather
than as standalone PEP 723 scripts — no inline metadata block.

## Conventions

- Format knowledge flows one way: a probe may import anything in `relab`;
  `relab` never imports from `formats/`.
- When a probe's finding is stable, write it to the matching `notes/` file in
  the same change. A probe without a note is an open question, not a result.
- New experiments start with a question. Name the file with today's date.
- Don't commit fixtures. If a sample must be shared, describe how to obtain it
  in the format's `README.md`.
- Keep this file and `README.md` current with any change that makes them stale.
