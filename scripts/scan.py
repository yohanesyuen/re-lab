#!/usr/bin/env uv run
"""Survey an unknown file: container type, entropy profile, string clusters, candidate record regions."""
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
    """One-shot survey of INPUT_PATH; the first thing to run on a new sample."""
    if verbose:
        click.echo(f"Processing: {input_path}")

    raise NotImplementedError("stub")


if __name__ == "__main__":
    main()
