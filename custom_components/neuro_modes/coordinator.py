from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event, async_call_later
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .calculator import calculate_bayesian_state
from .const import CONF_NAME, CONF_SOURCES, CONF_THRESHOLD, CONF_DELTA, CONF_OVERRIDE_TIMEOUT

_LOGGER = logging.getLogger(__name__)

class NeuroModesCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry, engine):
        super().__init__(hass, logger=_LOGGER, name=f"neuro_modes_{entry.entry_id}")
        self.hass = hass
        self.entry = entry
        self.engine = engine
        self._unsub = []
        self._timer_unsub = None
        self.mode_name = entry.data.get(CONF_NAME)

    async def async_setup(self):
        _LOGGER.debug("Coordinator setup started for entry_id=%s mode_name=%s", self.entry.entry_id, self.mode_name)
        if self.mode_name:
            sources = self.entry.options.get(CONF_SOURCES, self.entry.data.get(CONF_SOURCES, []))
            if sources:
                entity_ids = [src["entity_id"] for src in sources]
                unsub = async_track_state_change_event(self.hass, entity_ids, self._handle_state_change)
                self._unsub.append(unsub)
                _LOGGER.debug("Registered %s state listeners for entry_id=%s", len(entity_ids), self.entry.entry_id)

        await self.async_refresh()
        _LOGGER.debug("Coordinator setup finished for entry_id=%s", self.entry.entry_id)

    @callback
    def _handle_state_change(self, event):
        _LOGGER.debug("State change received for entry_id=%s mode_name=%s", self.entry.entry_id, self.mode_name)
        self.hass.async_create_task(self.async_request_refresh())

    def set_override(self, is_on):
        """Obsługa kliknięcia z czasem wygasania."""
        _LOGGER.debug("Manual override set for mode=%s value=%s", self.mode_name, is_on)
        self.engine.set_manual_override(self.mode_name, is_on)
        self.async_set_updated_data(self._current_state())

        # Ustawiamy stoper, jeśli zdefiniowano w opcjach czas > 0
        timeout_mins = self.entry.data.get(CONF_OVERRIDE_TIMEOUT, 0)
        if timeout_mins > 0:
            if self._timer_unsub:
                self._timer_unsub() # Kasujemy stary stoper
            self._timer_unsub = async_call_later(self.hass, timeout_mins * 60, self._clear_override)

    @callback
    def _clear_override(self, _now):
        """Clear manual override and allow automation to regain control."""
        mode_state = self.engine.states.get(self.mode_name, {})
        if mode_state.get("human_override"):
            _LOGGER.debug("Manual override timeout reached for mode=%s", self.mode_name)
            self.engine.set_manual_override(self.mode_name, False)
            self.hass.async_create_task(self.async_refresh())

    async def _async_update_data(self):
        return self._recalculate()

    def _current_state(self) -> dict:
        if not self.mode_name:
            return {}
        return self.engine.states.get(self.mode_name, {})

    def _recalculate(self):
        if not self.mode_name:
            return {}

        mode_state = self.engine.states.get(self.mode_name, {})
        if mode_state.get("human_override"):
            return self._current_state()

        sources = self.entry.options.get(CONF_SOURCES, self.entry.data.get(CONF_SOURCES, []))
        threshold = self.entry.data.get(CONF_THRESHOLD, 70)
        delta = self.entry.data.get(CONF_DELTA, 20)
        current_state = mode_state.get("state", False)

        new_state, score, active_sources = calculate_bayesian_state(self.hass, sources, threshold, delta, current_state)

        self.engine.states[self.mode_name] = {
            "state": new_state,
            "confidence": score,
            "active": active_sources,
            "human_override": False
        }
        _LOGGER.debug(
            "Recalculated mode=%s state=%s confidence=%s active_sources=%s",
            self.mode_name,
            new_state,
            score,
            len(active_sources),
        )
        return self._current_state()

    async def async_unload(self):
        for unsub in self._unsub:
            unsub()
        if self._timer_unsub:
            self._timer_unsub()
        await super().async_shutdown()
