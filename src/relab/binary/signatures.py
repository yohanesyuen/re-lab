import re
from dataclasses import dataclass

from puremagic.main import magic_data


KINDS = {
    ".gz": "gzip",
    ".zip": "zip",
    ".png": "png",
    ".jpg": "jpeg",
    ".jpeg": "jpeg",
    ".xml": "xml",
    ".ole": "ole",
}


@dataclass(frozen=True, order=True)
class SignatureMatch:
    offset: int
    kind: str


def kind(magic):
    return KINDS.get(magic.extension.lower())


def validate_gzip(blob, offset):
    if len(blob) - offset < 10:
        return False

    if blob[offset : offset + 3] != b"\x1f\x8b\x08":
        return False

    flags = blob[offset + 3]
    return not flags & 0xE0


VALIDATORS = {
    ".gz": validate_gzip,
}


MAGIC, _, _, _ = magic_data()


def valid(magic, blob, offset):
    validator = VALIDATORS.get(magic.extension.lower())
    return validator is None or validator(blob, offset)


def find_signatures(blob):
    return sorted(
        SignatureMatch(
            offset=match.start(),
            kind=kind(magic),
        )
        for magic in MAGIC
        if magic.byte_match
        if kind(magic)
        for match in re.finditer(re.escape(magic.byte_match), blob)
        if valid(magic, blob, match.start())
    )
