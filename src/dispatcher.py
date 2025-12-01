"""
Conversion dispatcher that routes files to the appropriate converter.

This module handles the high-level logic of determining categories,
validating same-category conversions, and dispatching to the correct backend.
"""

from pathlib import Path

from src.categories import Category, get_category
from src.converters import (
    ConversionError,
    convert_audio,
    convert_image,
    convert_office,
    convert_video,
)


class CategoryMismatchError(ConversionError):
    """Raised when attempting to convert between different categories."""

    pass


def convert_file(
    input_path: Path,
    output_path: Path,
    verbose: bool = False,
) -> None:
    """
    Convert a file from one format to another within the same category.

    Args:
        input_path: Path to the input file.
        output_path: Path to the output file.
        verbose: If True, print diagnostic information.

    Raises:
        FileNotFoundError: If the input file does not exist.
        CategoryMismatchError: If input and output categories differ.
        ConversionError: If conversion fails.
        ValueError: If file format is unsupported.
    """
    # Validate input file exists
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Determine categories
    try:
        input_category = get_category(input_path)
    except ValueError as e:
        raise ValueError(f"Unsupported input format: {e}")

    try:
        output_category = get_category(output_path)
    except ValueError as e:
        raise ValueError(f"Unsupported output format: {e}")

    # Enforce same-category conversion
    if input_category != output_category:
        raise CategoryMismatchError(
            f"Cannot convert between different categories.\n"
            f"Input category: {input_category.value}\n"
            f"Output category: {output_category.value}\n"
            f"Only conversions within the same category are supported."
        )

    if verbose:
        print(f"Converting {input_category.value}: {input_path.name} -> {output_path.name}")

    # Dispatch to appropriate converter
    if input_category == Category.AUDIO:
        convert_audio(input_path, output_path, verbose=verbose)
    elif input_category == Category.VIDEO:
        convert_video(input_path, output_path, verbose=verbose)
    elif input_category == Category.IMAGE:
        convert_image(input_path, output_path, verbose=verbose)
    elif input_category in (Category.DOCUMENT, Category.SPREADSHEET, Category.PRESENTATION):
        convert_office(input_path, output_path, verbose=verbose)
    else:
        raise ConversionError(f"No converter available for category: {input_category.value}")

