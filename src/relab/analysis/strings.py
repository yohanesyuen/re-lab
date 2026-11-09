"""Extract printable strings embedded in binary data."""

from __future__ import annotations

import re


def find_strings(data, min_length=4):
    ascii_run = rb"[\x20-\x7e]{%d,}" % min_length
    matches = [
        (match.start(), match.end(), "ascii", match.group().decode("ascii"))
        for match in re.finditer(ascii_run, data)
    ]

    for encoding, unit in (
        ("utf-16le", rb"[\x20-\x7e]\x00"),
        ("utf-16be", rb"\x00[\x20-\x7e]"),
    ):
        pattern = re.compile(unit * min_length)
        unit_pattern = re.compile(unit)
        cursor = 0

        while match := pattern.search(data, cursor):
            start, end = match.span()

            while end + 1 < len(data):
                if unit_pattern.fullmatch(data[end : end + 2]) is None:
                    break
                end += 2

            matches.append((start, end, encoding, data[start:end].decode(encoding)))
            cursor = end

    utf16le = [match for match in matches if match[2] == "utf-16le"]
    matches = [
        match
        for match in matches
        if not (
            match[2] == "utf-16be"
            and any(
                match[3] == other[3] and match[0] < other[1] and other[0] < match[1]
                for other in utf16le
            )
        )
    ]

    return tuple((offset, encoding, text) for offset, _, encoding, text in sorted(matches))
