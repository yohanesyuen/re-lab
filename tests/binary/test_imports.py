"""Import smoke test for relab.binary; replace with real tests as modules gain behaviour."""
from __future__ import annotations

import importlib
import pkgutil

import relab.binary


def test_submodules_import() -> None:
    for module in pkgutil.iter_modules(relab.binary.__path__):
        importlib.import_module(f"relab.binary.{module.name}")
