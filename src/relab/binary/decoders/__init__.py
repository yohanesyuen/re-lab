from io import BytesIO
from pathlib import PurePosixPath
from zipfile import ZipFile

import olefile
import zlib
from PIL import Image, UnidentifiedImageError


from relab.analysis.strings import find_strings
from relab.binary.signatures import find_signatures
from .archive import Archive, Entry
from dataclasses import dataclass


@dataclass(frozen=True)
class DecodeResult:
    data: bytes
    consumed: int


def decode_deflate(blob, dictionary=None):
    WINDOW_SIZE = 32 * 1024
    z = (
        zlib.decompressobj(-15, zdict=dictionary[-WINDOW_SIZE:])
        if dictionary
        else zlib.decompressobj(-15)
    )

    data = z.decompress(blob)

    return z, data


def decode_gzip(blob: bytes) -> DecodeResult:
    if blob[:3] != b"\x1f\x8b\x08":
        raise ValueError("Not gzip")

    body = blob[10:]
    z, data = decode_deflate(body)

    if not z.eof:
        raise ValueError("Incomplete DEFLATE stream")

    return DecodeResult(
        data=data,
        consumed=10 + len(body) - len(z.unused_data),
    )


def decode_rvt(blob: bytes) -> Archive:
    with olefile.OleFileIO(BytesIO(blob)) as ole:
        return Archive(
            Entry(
                path=PurePosixPath(*parts),
                data=ole.openstream(parts).read(),
            )
            for parts in ole.listdir(streams=True, storages=False)
        )


def decode_zip(blob: bytes) -> Archive:
    with ZipFile(BytesIO(blob)) as z:
        return Archive(
            Entry(
                path=PurePosixPath(info.filename),
                data=z.read(info),
            )
            for info in z.infolist()
            if not info.is_dir()
        )


def decode_blob(blob: bytes, source="") -> Archive:
    entries = [Entry("raw.bin", blob)]
    strings = find_strings(blob)

    if strings:
        lines = ["offset\tencoding\ttext"]
        lines.extend(f"0x{offset:08x}\t{encoding}\t{text}" for offset, encoding, text in strings)
        entries.append(Entry("strings.txt", ("\n".join(lines) + "\n").encode()))

    for hit in find_signatures(blob):
        data = blob[hit.offset :]

        if hit.kind in {"jpeg", "png"}:
            try:
                image = Image.open(BytesIO(data))
                image.load()
            except (UnidentifiedImageError, OSError):
                continue

            output = BytesIO()
            image.save(output, format=image.format)
            extension = "jpg" if image.format == "JPEG" else "png"
            entries.append(Entry(f"image@{hit.offset:08x}.{extension}", output.getvalue()))

        elif hit.kind == "gzip":
            try:
                decoded = decode_gzip(data)
            except Exception as exc:
                print(f"gzip failed: {source} @ 0x{hit.offset:x}: {exc}")
                continue

            child = decode_blob(
                decoded.data,
                f"{source}/gzip@{hit.offset:x}",
            )
            prefix = PurePosixPath(f"gzip@{hit.offset:08x}")
            entries.extend(Entry(prefix / path, stream.data) for path, stream in child.items())

        elif hit.kind == "zip":
            try:
                archive = decode_zip(data)
            except Exception as exc:
                print(f"zip failed: {source} @ 0x{hit.offset:x}: {exc}")
                continue

            prefix = PurePosixPath(f"zip@{hit.offset:08x}")
            entries.append(Entry(prefix / "raw.bin", data))

            for path, stream in archive.items():
                child = decode_blob(
                    bytes(stream.data),
                    f"{source}/zip@{hit.offset:x}/{path}",
                )

                if len(child) > 1:
                    entries.extend(
                        Entry(prefix / path / child_path, child_stream.data)
                        for child_path, child_stream in child.items()
                    )
                else:
                    entries.append(Entry(prefix / path, stream.data))

        elif hit.kind in {"xml", "ole"}:
            entries.append(Entry(f"{hit.kind}@{hit.offset:08x}.{hit.kind}", data))

    return Archive(entries)
