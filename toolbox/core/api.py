"""Stable import surface for reusable toolkits with lazy loading.

Recommended usage in external projects:
    from toolbox.core.api import ImageToolkit, VideoToolkit
"""

from __future__ import annotations

from importlib import import_module

_EXPORTS: dict[str, tuple[str, str]] = {
    "ExperimentalToolkit": ("toolbox.core.experimental", "ExperimentalToolkit"),
    "FileToolkit": ("toolbox.core.files", "FileToolkit"),
    "GifToolkit": ("toolbox.core.gifs", "GifToolkit"),
    "ImageToolkit": ("toolbox.core.images", "ImageToolkit"),
    "DatasetMetadataToolkit": ("toolbox.core.metadata", "DatasetMetadataToolkit"),
    "OpticalFlowToolkit": ("toolbox.core.optical_flow", "OpticalFlowToolkit"),
    "QwenToolkit": ("toolbox.core.qwen", "QwenToolkit"),
    "VideoToolkit": ("toolbox.core.videos", "VideoToolkit"),
}

__all__ = list(_EXPORTS.keys())


def __getattr__(name: str):
    if name not in _EXPORTS:
        raise AttributeError(f"module {__name__} has no attribute {name}")
    module_name, attr_name = _EXPORTS[name]
    module = import_module(module_name)
    return getattr(module, attr_name)


def __dir__() -> list[str]:
    return sorted(set(globals().keys()) | set(__all__))
