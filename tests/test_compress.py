import pytest
import io
import pikepdf
from pathlib import Path
from pdfjin_compress.core import compress_pdf


def create_dummy_pdf() -> bytes:
    pdf = pikepdf.new()
    for _ in range(3):
        pdf.add_blank_page(page_size=(300, 300))
    buf = io.BytesIO()
    pdf.save(buf)
    return buf.getvalue()


def test_compress_in_memory():
    raw = create_dummy_pdf()
    compressed = compress_pdf(raw)
    assert len(compressed) > 0
    with pikepdf.open(io.BytesIO(compressed)) as p:
        assert len(p.pages) == 3
