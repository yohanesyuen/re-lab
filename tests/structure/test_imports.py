"""Import smoke test for relab.structure; replace with real tests as modules gain behaviour."""
from __future__ import annotations

import importlib
import pkgutil

import relab.structure


def test_submodules_import() -> None:
    for module in pkgutil.iter_modules(relab.structure.__path__):
        importlib.import_module(f"relab.structure.{module.name}")
