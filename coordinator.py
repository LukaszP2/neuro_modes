from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event, async_call_later
from .calculator import calculate_bayesian_state
from .const import CONF_NAME, CONF_SOURCES, CONF_THRESHOLD, CONF_DELTA, CONF_OVERRIDE_TIMEOUT

class NeuroModesCoordinator:
    def __init__(self, hass: HomeAssistant, entry, engine):
        self.hass = hass
        self.entry = entry
        self.engine = engine
        self._listeners = []
        self._unsub = []
        self._timer_unsub = None
        self.mode_name = entry.data.get(CONF_NAME)

    def async_add_listener(self, update_callback):
        self._listeners.append(update_callback)
        def remove_listener():
            if update_callback in self._listeners:
                self._listeners.remove(update_callback)
        return remove_listener

    def notify_listeners(self):
        for listener in self._listeners:
            listener()

    async def async_setup(self):
        if not self.mode_name:
            return
        self._recalculate()
        sources = self.entry.options.get(CONF_SOURCES, self.entry.data.get(CONF_SOURCES, []))
        if sources:
            entity_ids = [src["entity_id"] for src in sources]
            unsub = async_track_state_change_event(self.hass, entity_ids, self._handle_state_change)
            self._unsub.append(unsub)

    @callback
    def _handle_state_change(self, event):
        self._recalculate()

    def set_override(self, is_on):
        """Obsługa kliknięcia z czasem wygasania."""
        self.engine.set_manual_override(self.mode_name, is_on)
        self.notify_listeners()

        # Ustawiamy stoper, jeśli zdefiniowano w opcjach czas > 0
        timeout_mins = self.entry.data.get(CONF_OVERRIDE_TIMEOUT, 0)
        if timeout_mins > 0:
            if self._timer_unsub:
                self._timer_unsub() # Kasujemy stary stoper
            self._timer_unsub = async_call_later(self.hass, timeout_mins * 60, self._clear_override)

    @callback
    def _clear_override(self, _now):
        """Resetuje nadpisanie i pozwala automatowi odzyskać kontrolę."""
        mode_state = self.engine.states.get(self.mode_name, {})
        if mode_state.get("human_override"):
            mode_state["human_override"] = False
            self._recalculate()

    def _recalculate(self):
        mode_state = self.engine.states.get(self.mode_name, {})
        if mode_state.get("human_override"):
            return

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
        self.notify_listeners()

    async def async_unload(self):
        for unsub in self._unsub:
            unsub()
        if self._timer_unsub:
            self._timer_unsub()
