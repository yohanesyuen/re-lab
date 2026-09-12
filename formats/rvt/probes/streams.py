#!/usr/bin/env uv run
"""List the OLE streams in an RVT and summarise each one's size and entropy."""
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
