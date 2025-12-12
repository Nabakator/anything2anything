#!/usr/bin/env python3
"""
Compatibility shim for backwards compatibility.

This allows `python anything2anything.py ...` to continue working
after the package has been restructured.
"""

from anything2anything.cli import cli

if __name__ == "__main__":
    cli()
