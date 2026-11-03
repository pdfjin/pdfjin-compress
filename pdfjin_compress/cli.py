import sys
import argparse
from pathlib import Path
try:
    from .core import compress_pdf
    from . import __version__
except (ImportError, ValueError):
    from pdfjin_compress.core import compress_pdf
    from pdfjin_compress import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="pdfjin-compress",
        description="Compress and optimize PDF file size.",
        epilog="Online web version available at https://pdfjin.com/pages/compress-pdf.html",
    )
    parser.add_argument("input", metavar="INPUT_PDF", help="Path to the PDF to compress")
    parser.add_argument("-o", "--output", required=True, metavar="OUTPUT_PDF", help="Path to save compressed PDF")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    try:
        in_path = Path(args.input)
        out_path = compress_pdf(in_path, output=args.output)
        orig_sz = in_path.stat().st_size
        new_sz = Path(out_path).stat().st_size
        saved_pct = max(0.0, (1 - (new_sz / orig_sz)) * 100) if orig_sz > 0 else 0
        print(f"✨ Compressed: {orig_sz:,} bytes -> {new_sz:,} bytes ({saved_pct:.1f}% reduction)")
    except Exception as e:
        print(f"❌ Compression failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
