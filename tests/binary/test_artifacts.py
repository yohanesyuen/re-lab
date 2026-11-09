from __future__ import annotations

import gzip
from io import BytesIO
from zipfile import ZipFile

from relab.analysis.strings import find_strings
from relab.binary.decoders import decode_blob


def test_odd_aligned_utf16le_wins_over_equivalent_utf16be() -> None:
    data = b"\x00\x00\x00" + "Workset1".encode("utf-16le")

    assert find_strings(data) == ((3, "utf-16le", "Workset1"),)


def test_decode_blob_recurses_into_gzip_and_zip() -> None:
    zipped = BytesIO()
    with ZipFile(zipped, "w") as archive:
        archive.writestr("note.bin", b"plain text")

    artifact = decode_blob(gzip.compress(zipped.getvalue()), "test")

    assert "raw.bin" in artifact
    assert "gzip@00000000/raw.bin" in artifact
    assert "gzip@00000000/zip@00000000/raw.bin" in artifact
    assert "gzip@00000000/zip@00000000/note.bin/strings.txt" in artifact
