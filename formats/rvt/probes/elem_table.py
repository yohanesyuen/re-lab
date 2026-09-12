#!/usr/bin/env uv run
"""Locate and walk the element table inside an RVT's main stream."""
from __future__ import annotations

from pathlib import Path

import click


@click.command()
@click.argument("sample", type=click.Path(exists=True, path_type=Path))
def main(sample: Path) -> None:
    """Run this probe against SAMPLE and print findings."""
    raise NotImplementedError("stub")


if __name__ == "__main__":
    main()
