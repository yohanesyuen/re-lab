# re-lab

A lab for reverse-engineering binary file formats. It separates the reusable
part — byte primitives, record inference, statistical analysis, container
unwrapping — from the format-specific part, which is a set of probes and notes
per format.

## Quick start

```
uv sync
uv run pytest
uv run scripts/scan.py path/to/sample.bin
```

Every module is currently a stub with a docstring describing what it will do.

## Layout

```
src/relab/          generic toolkit (binary, structure, analysis, containers)
formats/<fmt>/      per-format probes, notes, and local-only fixtures
research/           prior-art summaries and dated experiment logs
scripts/            click CLIs built on relab: scan, carve, strings, compare
tests/              mirrors src/relab
```

Formats under study: `rvt` (Revit, OLE2 container), `dwg` (AutoCAD), `evo`
(not yet characterised).

See `AGENTS.md` for the working conventions.
