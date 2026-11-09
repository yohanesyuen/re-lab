from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class Entry:
    path: PurePosixPath
    data: bytes

    def __post_init__(self):
        object.__setattr__(
            self,
            "path",
            PurePosixPath(self.path),
        )


class Archive(Mapping):
    def __init__(self, streams):
        self._streams = {stream.path: stream for stream in streams}

    def __getitem__(self, path):
        return self._streams[PurePosixPath(path)]

    def __iter__(self):
        return iter(self._streams)

    def __len__(self):
        return len(self._streams)
