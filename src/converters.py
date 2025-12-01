"""
Backend conversion functions for each category.

This module contains the actual conversion logic that invokes external tools
(FFmpeg, ImageMagick, LibreOffice) to perform file conversions.
"""

import shutil
import subprocess
from pathlib import Path
from typing import Optional


class ConversionError(Exception):
    """Base exception for conversion errors."""

    pass


class ToolNotFoundError(ConversionError):
    """Raised when a required external tool is not found in PATH."""

    pass


def check_tool_available(tool_name: str) -> bool:
    """
    Check if an external tool is available in PATH.

    Args:
        tool_name: Name of the tool to check (e.g., "ffmpeg", "magick", "soffice").

    Returns:
        True if the tool is available, False otherwise.
    """
    return shutil.which(tool_name) is not None


def run_command(
    cmd: list[str],
    verbose: bool = False,
    tool_name: str = "external tool",
) -> None:
    """
    Run a shell command and handle errors.

    Args:
        cmd: Command and arguments as a list.
        verbose: If True, print the command and its output.
        tool_name: Name of the tool for error messages.

    Raises:
        ToolNotFoundError: If the tool is not found in PATH.
        ConversionError: If the command fails.
    """
    if verbose:
        print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        raise ToolNotFoundError(
            f"{tool_name} not found in PATH. Please install it and ensure it's available."
        )

    if result.returncode != 0:
        error_msg = f"{tool_name} failed with exit code {result.returncode}"
        if verbose or result.stderr:
            error_msg += f"\nError output:\n{result.stderr}"
        if verbose and result.stdout:
            error_msg += f"\nStandard output:\n{result.stdout}"
        raise ConversionError(error_msg)


def convert_audio(
    input_path: Path,
    output_path: Path,
    verbose: bool = False,
) -> None:
    """
    Convert audio files using FFmpeg.

    Supports: mp3, wav, m4a

    Args:
        input_path: Path to input audio file.
        output_path: Path to output audio file.
        verbose: If True, print the command being executed.

    Raises:
        ToolNotFoundError: If FFmpeg is not found.
        ConversionError: If conversion fails.
    """
    if not check_tool_available("ffmpeg"):
        raise ToolNotFoundError(
            "FFmpeg is required for audio conversion. Please install it."
        )

    ext = output_path.suffix.lower().lstrip(".")
    cmd = ["ffmpeg", "-i", str(input_path), "-y"]  # -y to overwrite (we check separately)

    # Configure codec and quality based on target format
    if ext == "mp3":
        # High quality VBR MP3
        cmd.extend(["-codec:a", "libmp3lame", "-q:a", "2"])
    elif ext == "wav":
        # Uncompressed PCM, 16-bit
        cmd.extend(["-codec:a", "pcm_s16le"])
    elif ext == "m4a":
        # AAC at 192 kbps
        cmd.extend(["-codec:a", "aac", "-b:a", "192k"])
    else:
        raise ConversionError(f"Unsupported audio output format: {ext}")

    cmd.append(str(output_path))
    run_command(cmd, verbose=verbose, tool_name="FFmpeg")


def convert_video(
    input_path: Path,
    output_path: Path,
    verbose: bool = False,
) -> None:
    """
    Convert video files using FFmpeg.

    Supports: mov, mp4

    Args:
        input_path: Path to input video file.
        output_path: Path to output video file.
        verbose: If True, print the command being executed.

    Raises:
        ToolNotFoundError: If FFmpeg is not found.
        ConversionError: If conversion fails.
    """
    if not check_tool_available("ffmpeg"):
        raise ToolNotFoundError(
            "FFmpeg is required for video conversion. Please install it."
        )

    ext = output_path.suffix.lower().lstrip(".")
    cmd = ["ffmpeg", "-i", str(input_path), "-y"]  # -y to overwrite (we check separately)

    if ext == "mp4":
        # H.264 video + AAC audio, faststart for web streaming
        cmd.extend(
            [
                "-codec:v",
                "libx264",
                "-codec:a",
                "aac",
                "-movflags",
                "+faststart",
            ]
        )
    elif ext == "mov":
        # H.264 + AAC for MOV
        cmd.extend(["-codec:v", "libx264", "-codec:a", "aac"])
    else:
        raise ConversionError(f"Unsupported video output format: {ext}")

    cmd.append(str(output_path))
    run_command(cmd, verbose=verbose, tool_name="FFmpeg")


def convert_image(
    input_path: Path,
    output_path: Path,
    verbose: bool = False,
) -> None:
    """
    Convert image files using ImageMagick.

    Supports: heic, jpg/jpeg, gif, icns, webp, avif

    Args:
        input_path: Path to input image file.
        output_path: Path to output image file.
        verbose: If True, print the command being executed.

    Raises:
        ToolNotFoundError: If ImageMagick is not found.
        ConversionError: If conversion fails.
    """
    if not check_tool_available("magick"):
        raise ToolNotFoundError(
            "ImageMagick is required for image conversion. Please install it."
        )

    cmd = ["magick", str(input_path), str(output_path)]
    run_command(cmd, verbose=verbose, tool_name="ImageMagick")


def convert_office(
    input_path: Path,
    output_path: Path,
    verbose: bool = False,
) -> None:
    """
    Convert office documents using LibreOffice.

    Supports documents, spreadsheets, and presentations.

    Args:
        input_path: Path to input office file.
        output_path: Path to output office file.
        verbose: If True, print the command being executed.

    Raises:
        ToolNotFoundError: If LibreOffice is not found.
        ConversionError: If conversion fails.
    """
    if not check_tool_available("soffice"):
        raise ToolNotFoundError(
            "LibreOffice is required for office document conversion. Please install it."
        )

    # LibreOffice expects the target extension without the dot
    target_ext = output_path.suffix.lstrip(".")
    output_dir = output_path.parent
    output_basename = output_path.stem

    # LibreOffice writes to --outdir with the same basename but new extension
    cmd = [
        "soffice",
        "--headless",
        "--convert-to",
        target_ext,
        "--outdir",
        str(output_dir),
        str(input_path),
    ]

    run_command(cmd, verbose=verbose, tool_name="LibreOffice")

    # LibreOffice creates the file with the input basename but new extension
    # We need to find it and rename it to match the requested output path
    expected_output = output_dir / f"{input_path.stem}.{target_ext}"

    if not expected_output.exists():
        raise ConversionError(
            f"LibreOffice did not produce expected output file: {expected_output}"
        )

    # If the basename differs, rename the file
    if expected_output != output_path:
        if verbose:
            print(f"Renaming {expected_output} to {output_path}")
        expected_output.rename(output_path)

