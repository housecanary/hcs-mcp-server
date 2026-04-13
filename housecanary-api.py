"""Compatibility wrapper for the packaged housecanary_mcp entrypoint."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"

if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from housecanary_mcp.server import main


if __name__ == "__main__":
    main()