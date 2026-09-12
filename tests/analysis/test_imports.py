"""Import smoke test for relab.analysis; replace with real tests as modules gain behaviour."""
from __future__ import annotations

import importlib
import pkgutil

import relab.analysis


def test_submodules_import() -> None:
    for module in pkgutil.iter_modules(relab.analysis.__path__):
        importlib.import_module(f"relab.analysis.{module.name}")
