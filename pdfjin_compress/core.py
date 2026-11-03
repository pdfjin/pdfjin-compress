from pathlib import Path
from typing import Union, BinaryIO, Optional
import io
import pikepdf


def compress_pdf(
    input_pdf: Union[str, Path, bytes, BinaryIO],
    output: Optional[Union[str, Path, BinaryIO]] = None,
) -> Union[bytes, Path]:
    """
    Compress and optimize a PDF file by deduplicating and compressing object streams.
    """
    if isinstance(input_pdf, (str, Path)):
        src = pikepdf.open(str(input_pdf))
    elif isinstance(input_pdf, bytes):
        src = pikepdf.open(io.BytesIO(input_pdf))
    else:
        src = pikepdf.open(input_pdf)

    with src:
        save_options = {
            "compress_streams": True,
            "object_stream_mode": pikepdf.ObjectStreamMode.generate,
            "linearize": False,
        }

        if output is None:
            buf = io.BytesIO()
            src.save(buf, **save_options)
            return buf.getvalue()

        if isinstance(output, (str, Path)):
            out_path = Path(output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            src.save(str(out_path), **save_options)
            return out_path

        src.save(output, **save_options)
        return output
