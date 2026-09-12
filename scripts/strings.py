#!/usr/bin/env uv run
"""Dump strings with offsets from INPUT_PATH."""
from __future__ import annotations

from pathlib import Path

import click


@click.command()
@click.argument("input_path", type=click.Path(exists=True, path_type=Path))
@click.option(
    "-o", "--output",
    type=click.Path(path_type=Path),
    help="Path to save output.",
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Enable verbose output.",
)
def main(input_path: Path, output: Path | None, verbose: bool) -> None:
    """List strings (ASCII and UTF-16) found in INPUT_PATH."""
    if verbose:
        click.echo(f"Processing: {input_path}")

    raise NotImplementedError("stub")


if __name__ == "__main__":
    main()
