"""
Category definitions and extension mapping for file formats.

This module provides the formal notion of "category" for file types and handles
extension normalization and category resolution.
"""

from enum import Enum
from pathlib import Path
from typing import Optional


class Category(Enum):
    """File format categories for conversion."""

    AUDIO = "audio"
    IMAGE = "image"
    VIDEO = "video"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    DOCUMENT = "document"


# Extension to category mapping
# Keys are normalized (lowercase) extensions without the dot
EXTENSION_TO_CATEGORY: dict[str, Category] = {
    # Audio
    "mp3": Category.AUDIO,
    "wav": Category.AUDIO,
    "m4a": Category.AUDIO,
    # Image
    "heic": Category.IMAGE,
    "jpg": Category.IMAGE,
    "jpeg": Category.IMAGE,
    "gif": Category.IMAGE,
    "icns": Category.IMAGE,
    "webp": Category.IMAGE,
    "avif": Category.IMAGE,
    # Video
    "mov": Category.VIDEO,
    "mp4": Category.VIDEO,
    # Spreadsheet
    "csv": Category.SPREADSHEET,
    "ods": Category.SPREADSHEET,
    "xlsx": Category.SPREADSHEET,
    "xls": Category.SPREADSHEET,
    "xlsm": Category.SPREADSHEET,
    # Presentation
    "odp": Category.PRESENTATION,
    "ppt": Category.PRESENTATION,
    "pptx": Category.PRESENTATION,
    # Document
    "docx": Category.DOCUMENT,
    "doc": Category.DOCUMENT,
    "odt": Category.DOCUMENT,
    "txt": Category.DOCUMENT,
    "rtf": Category.DOCUMENT,
}

# Alias mapping for extensions that should be treated identically
# (e.g., jpeg -> jpg)
EXTENSION_ALIASES: dict[str, str] = {
    "jpeg": "jpg",
}


def normalize_extension(ext: str) -> str:
    """
    Normalize a file extension.

    Args:
        ext: Extension string (with or without leading dot).

    Returns:
        Normalized extension (lowercase, without leading dot).

    Examples:
        >>> normalize_extension(".JPG")
        'jpg'
        >>> normalize_extension("jpeg")
        'jpg'
    """
    # Remove leading dot if present
    ext = ext.lstrip(".")
    # Convert to lowercase
    ext = ext.lower()
    # Resolve aliases
    ext = EXTENSION_ALIASES.get(ext, ext)
    return ext


def get_extension(path: str | Path) -> str:
    """
    Extract and normalize the extension from a file path.

    Args:
        path: File path as string or Path object.

    Returns:
        Normalized extension (without leading dot).

    Examples:
        >>> get_extension("photo.JPEG")
        'jpg'
        >>> get_extension(Path("document.docx"))
        'docx'
    """
    path_obj = Path(path)
    ext = path_obj.suffix
    return normalize_extension(ext)


def get_category(path: str | Path) -> Category:
    """
    Determine the category of a file based on its extension.

    Args:
        path: File path as string or Path object.

    Returns:
        Category enum value.

    Raises:
        ValueError: If the file extension is not supported.
    """
    ext = get_extension(path)
    category = EXTENSION_TO_CATEGORY.get(ext)

    if category is None:
        ext_with_dot = f".{ext}" if ext else "(no extension)"
        raise ValueError(
            f"Unsupported file format: {ext_with_dot}\n"
            f"Supported formats: {', '.join(sorted(set(EXTENSION_TO_CATEGORY.keys())))}"
        )

    return category


def get_supported_extensions(category: Optional[Category] = None) -> list[str]:
    """
    Get list of supported extensions, optionally filtered by category.

    Args:
        category: Optional category to filter by.

    Returns:
        List of supported extensions (normalized, without leading dot).
    """
    if category is None:
        return sorted(set(EXTENSION_TO_CATEGORY.keys()))
    return sorted(
        ext for ext, cat in EXTENSION_TO_CATEGORY.items() if cat == category
    )

