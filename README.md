# anything2anything

A minimalist Python CLI tool for converting files between formats within the same category. This tool acts as a thin wrapper around existing command-line tools (FFmpeg, ImageMagick, LibreOffice) to provide a unified interface for file conversion.

## Features

- **Category-based conversion**: Only converts files within the same category (e.g., image to image, audio to audio)
- **Multiple format support**: Supports audio, video, image, document, spreadsheet, and presentation formats
- **Simple CLI**: Clean, intuitive command-line interface
- **Extensible design**: Easy to add new formats by updating the category mappings

## Requirements

### System dependencies

This tool requires the following external command-line tools to be installed and available in your PATH:

- **FFmpeg**: For audio and video conversions
- **ImageMagick**: For image conversions
- **LibreOffice**: For document, spreadsheet, and presentation conversions

Installation instructions:

- **macOS**: `brew install ffmpeg imagemagick libreoffice`
- **Linux (Ubuntu/Debian)**: `sudo apt-get install ffmpeg imagemagick libreoffice`
- **Windows**: Download installers from the respective project websites

### Python requirements

- Python 3.11 or higher

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd anything2anything
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   ```bash
   # macOS/Linux
   source .venv/bin/activate
   
   # Windows
   .venv\Scripts\activate
   ```

4. Install the package:
   ```bash
   pip install .
   ```

   For development (editable install):
   ```bash
   pip install -e .
   ```

## Usage

### Basic syntax

```bash
anything2anything INPUT_PATH OUTPUT_PATH [options]
```

> **Note**: For backwards compatibility, `python anything2anything.py ...` still works, but the recommended way is to use the `anything2anything` command after installation.

### Options

- `--force`, `-f`: Overwrite output file if it already exists
- `--verbose`, `-v`: Print detailed information about the conversion process
- `--help`: Show help message

### Examples

#### Image conversion

```bash
# Convert HEIC to JPG
anything2anything inputs/photo.heic outputs/photo.jpg

# Convert JPG to WebP with verbose output
anything2anything inputs/image.jpg outputs/image.webp --verbose
```

#### Audio conversion

```bash
# Convert M4A to MP3
anything2anything inputs/audio.m4a outputs/audio.mp3

# Convert WAV to M4A
anything2anything inputs/recording.wav outputs/recording.m4a
```

#### Video conversion

```bash
# Convert MOV to MP4
anything2anything inputs/video.mov outputs/video.mp4

# Convert with force overwrite
anything2anything inputs/video.mp4 outputs/video.mov --force
```

#### Document conversion

```bash
# Convert DOCX to ODT
anything2anything inputs/document.docx outputs/document.odt

# Convert DOC to RTF
anything2anything inputs/document.doc outputs/document.rtf
```

#### Spreadsheet conversion

```bash
# Convert XLSX to ODS
anything2anything inputs/spreadsheet.xlsx outputs/spreadsheet.ods

# Convert CSV to XLSX
anything2anything inputs/data.csv outputs/data.xlsx
```

#### Presentation conversion

```bash
# Convert PPTX to ODP
anything2anything inputs/presentation.pptx outputs/presentation.odp
```

## Supported formats

### Audio
- `.mp3` - MPEG Audio Layer 3
- `.wav` - Waveform Audio
- `.m4a` - MPEG-4 Audio

### Video
- `.mov` - QuickTime Movie
- `.mp4` - MPEG-4 Video

### Image
- `.heic` - High Efficiency Image Container
- `.jpg`, `.jpeg` - JPEG Image
- `.gif` - Graphics Interchange Format
- `.icns` - Apple Icon Image
- `.webp` - WebP Image
- `.avif` - AV1 Image File Format

### Spreadsheet
- `.csv` - Comma-Separated Values
- `.ods` - OpenDocument Spreadsheet
- `.xlsx` - Microsoft Excel (OpenXML)
- `.xls` - Microsoft Excel (Legacy)
- `.xlsm` - Microsoft Excel Macro-Enabled

### Presentation
- `.odp` - OpenDocument Presentation
- `.ppt` - Microsoft PowerPoint (Legacy)
- `.pptx` - Microsoft PowerPoint (OpenXML)

### Document
- `.docx` - Microsoft Word (OpenXML)
- `.doc` - Microsoft Word (Legacy)
- `.odt` - OpenDocument Text
- `.txt` - Plain Text
- `.rtf` - Rich Text Format
- `.pdf` - Portable Document Format

## Error handling

The tool provides clear error messages for common issues:

- **Unsupported format**: If the input or output format is not supported
- **Category mismatch**: If attempting to convert between different categories (e.g., image to audio)
- **Missing tools**: If required external tools (FFmpeg, ImageMagick, LibreOffice) are not found
- **File not found**: If the input file does not exist
- **Conversion failure**: If the underlying tool fails to convert the file

Use the `--verbose` flag to see detailed error output from the underlying tools.

## Project structure

```
anything2anything/
├── anything2anything.py          # Compatibility shim (backwards compatibility)
├── pyproject.toml                # Package configuration and build metadata
├── src/                          # Source code directory
│   └── anything2anything/        # Main package
│       ├── __init__.py
│       ├── cli.py                # CLI entry point
│       ├── categories.py         # Category definitions and extension mapping
│       ├── converters.py         # Backend conversion functions
│       └── dispatcher.py         # Conversion routing logic
├── requirements.txt              # Python dependencies (for reference)
├── .gitignore                    # Git ignore patterns
├── inputs/                       # Directory for sample inputs
├── outputs/                      # Directory for sample outputs
└── README.md                     # This file
```

## Development

### Setup

For development, install the package in editable mode:

```bash
pip install -e .
```

This allows you to make changes to the code and test them immediately without reinstalling.

### Extending the codebase

The codebase is designed to be simple and extensible. To add support for new formats:

1. Add the extension to `EXTENSION_TO_CATEGORY` in `src/anything2anything/categories.py`
2. If needed, add a new converter function in `src/anything2anything/converters.py`
3. Update the dispatcher if a new category is added
