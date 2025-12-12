#!/usr/bin/env python3
"""
anything2anything: A minimalist CLI tool for converting files between formats.

This module provides a command-line interface for converting files within the same
category using external tools (FFmpeg, ImageMagick, LibreOffice).
"""

import sys
from pathlib import Path

import typer
from rich.console import Console

from anything2anything.converters import ConversionError, ToolNotFoundError
from anything2anything.dispatcher import CategoryMismatchError, convert_file

app = typer.Typer(
    name="anything2anything",
    help="Convert files between formats within the same category (audio, video, image, document, spreadsheet, presentation).",
    add_completion=False,
)
console = Console()


@app.command()
def main(
    input_path: str = typer.Argument(..., help="Path to input file"),
    output_path: str = typer.Argument(..., help="Path to output file"),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite output file if it already exists",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Print detailed information about the conversion process",
    ),
) -> None:
    """
    Convert a file from one format to another.

    Only conversions within the same category are supported:
    - Audio: mp3, wav, m4a
    - Video: mov, mp4
    - Image: heic, jpg/jpeg, gif, icns, webp, avif
    - Spreadsheet: csv, ods, xlsx, xls, xlsm
    - Presentation: odp, ppt, pptx
    - Document: docx, doc, odt, txt, rtf, pdf

    Examples:
        # Convert HEIC image to JPG
        anything2anything photo.heic photo.jpg

        # Convert M4A audio to MP3
        anything2anything audio.m4a audio.mp3

        # Convert DOCX document to ODT
        anything2anything document.docx document.odt --verbose

        # Convert with force overwrite
        anything2anything input.mp4 output.mov --force
    """
    input_file = Path(input_path).resolve()
    output_file = Path(output_path).resolve()

    # Check if output file already exists
    if output_file.exists() and not force:
        console.print(
            f"[red]Error:[/red] Output file already exists: {output_file}\n"
            f"Use --force to overwrite it.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        convert_file(input_file, output_file, verbose=verbose)
        console.print(f"[green]Success:[/green] Converted {input_file.name} -> {output_file.name}")
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)
    except CategoryMismatchError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)
    except ToolNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)
    except ConversionError as e:
        console.print(f"[red]Error:[/red] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        console.print(
            f"[red]Unexpected error:[/red] {e}",
            file=sys.stderr,
        )
        if verbose:
            import traceback

            console.print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)


def cli() -> None:
    """Entry point for the console script."""
    app()


if __name__ == "__main__":
    cli()

