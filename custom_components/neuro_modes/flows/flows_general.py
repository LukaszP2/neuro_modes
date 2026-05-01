import voluptuous as vol
from homeassistant.helpers import selector
from ..const import (
    DOMAIN, 
    CONF_ENTRY_TYPE, 
    ENTRY_TYPE_ENGINE, 
    ENTRY_TYPE_MODE, 
    ENTRY_TYPE_MODIFIER,
    CONF_NAME, 
    CONF_THRESHOLD, 
    CONF_DELTA, 
    CONF_SOURCES, 
    CONF_OVERRIDE_TIMEOUT
)

async def async_step_setup_engine(flow, user_input=None):
    """Krok instalacji głównego silnika Neuro Modes."""
    # Sprawdzamy czy silnik już istnieje
    for entry in flow._async_current_entries():
        if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
            return flow.async_abort(reason="single_instance_allowed")

    if user_input is not None:
        return flow.async_create_entry(
            title="Engine Neuro Modes", 
            data={CONF_ENTRY_TYPE: ENTRY_TYPE_ENGINE}
        )

    return flow.async_show_form(step_id="setup_engine", data_schema=vol.Schema({}))

async def async_step_setup_mode(flow, user_input=None):
    """Krok tworzenia nowego Trybu Bazowego (np. Dom, Poza)."""
    if user_input is not None:
        return flow.async_create_entry(
            title=f"Mode: {user_input[CONF_NAME]}", 
            data={
                **user_input, 
                CONF_ENTRY_TYPE: ENTRY_TYPE_MODE, 
                CONF_SOURCES: []
            }
        )

    return flow.async_show_form(
        step_id="setup_mode", 
        data_schema=_get_mode_schema()
    )

async def async_step_setup_modifier(flow, user_input=None):
    """Krok tworzenia nowego Modyfikatora (np. Goście, Noc)."""
    if user_input is not None:
        return flow.async_create_entry(
            title=f"Modifier: {user_input[CONF_NAME]}", 
            data={
                **user_input, 
                CONF_ENTRY_TYPE: ENTRY_TYPE_MODIFIER, 
                CONF_SOURCES: []
            }
        )

    return flow.async_show_form(
        step_id="setup_modifier", 
        data_schema=_get_mode_schema()
    )

def _get_mode_schema(defaults=None):
    """Pomocniczy schemat formularza dla trybów i modyfikatorów."""
    if defaults is None: 
        defaults = {}
    return vol.Schema({
        vol.Required(CONF_NAME, default=defaults.get(CONF_NAME, "")): str,
        vol.Required(CONF_THRESHOLD, default=defaults.get(CONF_THRESHOLD, 70)): vol.All(
            vol.Coerce(int), vol.Range(0, 100)
        ),
        vol.Required(CONF_DELTA, default=defaults.get(CONF_DELTA, 20)): vol.All(
            vol.Coerce(int), vol.Range(0, 100)
        ),
        vol.Required(CONF_OVERRIDE_TIMEOUT, default=defaults.get(CONF_OVERRIDE_TIMEOUT, 120)): vol.All(
            vol.Coerce(int), vol.Range(0, 1440)
        ),
    })