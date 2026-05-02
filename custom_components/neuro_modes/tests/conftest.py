"""Pytest configuration for neuro_modes tests.

Mocks are already set up by root conftest.py
"""
import pytest
from types import SimpleNamespace


@pytest.fixture
def fake_hass():
    """Fixture: fake Home Assistant instance."""
    hass = SimpleNamespace()
    hass.states = {}
    hass.config_entries = SimpleNamespace()
    hass.config_entries.async_entries = lambda domain: []
    hass.async_create_task = lambda coro: None
    return hass
