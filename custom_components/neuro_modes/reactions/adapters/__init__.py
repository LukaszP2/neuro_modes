"""Adapters for reactions - Adapter pattern implementation."""
from .lighting.adaptive_lighting import AdaptiveLightingAdapter
from .presence.magic_areas import MagicAreasAdapter

__all__ = ["AdaptiveLightingAdapter", "MagicAreasAdapter"]
