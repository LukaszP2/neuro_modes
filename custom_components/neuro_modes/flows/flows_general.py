import voluptuous as vol
from homeassistant import config_entries
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
    CONF_OVERRIDE_TIMEOUT,
    CONF_SOURCES
)

_TEMPLATE_PRESETS = {
    "none": [],
    "home": [{"entity_id": "zone.home", "state": "> 0", "weight": 80}],
    "away": [{"entity_id": "zone.home", "state": "0", "weight": 80}],
    "night": [{"entity_id": "sun.sun", "state": "below_horizon", "weight": 40}],
}


def _name_exists(flow, name: str) -> bool:
    target = name.strip().lower()
    for entry in flow._async_current_entries():
        existing = str(entry.data.get(CONF_NAME, "")).strip().lower()
        if existing and existing == target:
            return True
    return False

async def async_step_setup_engine(flow, user_input=None):

    
    if user_input is not None:
        if user_input.get("install_defaults"):

            defaults = [
                {"title": "Mode: Dom", "data": {CONF_ENTRY_TYPE: ENTRY_TYPE_MODE, CONF_NAME: "Dom", CONF_THRESHOLD: 70, CONF_DELTA: 20, CONF_OVERRIDE_TIMEOUT: 120, CONF_SOURCES: [{"entity_id": "zone.home", "state": "> 0", "weight": 80}]}},
                {"title": "Mode: Poza domem", "data": {CONF_ENTRY_TYPE: ENTRY_TYPE_MODE, CONF_NAME: "Poza domem", CONF_THRESHOLD: 70, CONF_DELTA: 20, CONF_OVERRIDE_TIMEOUT: 120, CONF_SOURCES: [{"entity_id": "zone.home", "state": "0", "weight": 80}]}},
                {"title": "Modifier: Noc", "data": {CONF_ENTRY_TYPE: ENTRY_TYPE_MODIFIER, CONF_NAME: "Noc", CONF_THRESHOLD: 70, CONF_DELTA: 20, CONF_OVERRIDE_TIMEOUT: 120, CONF_SOURCES: [{"entity_id": "sun.sun", "state": "below_horizon", "weight": 40}]}},
                {"title": "Mode: Wakacje", "data": {CONF_ENTRY_TYPE: ENTRY_TYPE_MODE, CONF_NAME: "Wakacje", CONF_THRESHOLD: 70, CONF_DELTA: 20, CONF_OVERRIDE_TIMEOUT: 1440, CONF_SOURCES: [{"entity_id": "zone.home", "state": "0", "weight": 40}]}},
                {"title": "Modifier: Filmowy", "data": {CONF_ENTRY_TYPE: ENTRY_TYPE_MODIFIER, CONF_NAME: "Filmowy", CONF_THRESHOLD: 70, CONF_DELTA: 20, CONF_OVERRIDE_TIMEOUT: 120, CONF_SOURCES: []}}, # Filmowy pusty, uczy się po konfiguracji TV
            ]
            
            for mode in defaults:

                flow.hass.async_create_task(
                    flow.hass.config_entries.flow.async_init(
                        DOMAIN,
                        context={"source": config_entries.SOURCE_IMPORT},
                        data=mode
                    )
                )

        return flow.async_create_entry(
            title="Engine Neuro Modes", 
            data={CONF_ENTRY_TYPE: ENTRY_TYPE_ENGINE}
        )

    return flow.async_show_form(
        step_id="setup_engine", 
        data_schema=vol.Schema({
            vol.Optional("install_defaults", default=True): bool
        })
    )

async def async_step_setup_mode(flow, user_input=None):

    if user_input is not None:
        if _name_exists(flow, user_input[CONF_NAME]):
            return flow.async_show_form(step_id="setup_mode", data_schema=_get_mode_schema(user_input), errors={"name": "name_exists"})

        template_key = user_input.get("initial_template", "none")
        initial_sources = list(_TEMPLATE_PRESETS.get(template_key, []))
        return flow.async_create_entry(
            title=f"Mode: {user_input[CONF_NAME]}", 
            data={
                **{k: v for k, v in user_input.items() if k != "initial_template"},
                CONF_ENTRY_TYPE: ENTRY_TYPE_MODE, 
                CONF_SOURCES: initial_sources,
            }
        )

    return flow.async_show_form(
        step_id="setup_mode", 
        data_schema=_get_mode_schema()
    )

async def async_step_setup_modifier(flow, user_input=None):

    if user_input is not None:
        if _name_exists(flow, user_input[CONF_NAME]):
            return flow.async_show_form(step_id="setup_modifier", data_schema=_get_mode_schema(user_input), errors={"name": "name_exists"})

        template_key = user_input.get("initial_template", "none")
        initial_sources = list(_TEMPLATE_PRESETS.get(template_key, []))
        return flow.async_create_entry(
            title=f"Modifier: {user_input[CONF_NAME]}", 
            data={
                **{k: v for k, v in user_input.items() if k != "initial_template"},
                CONF_ENTRY_TYPE: ENTRY_TYPE_MODIFIER, 
                CONF_SOURCES: initial_sources,
            }
        )

    return flow.async_show_form(
        step_id="setup_modifier", 
        data_schema=_get_mode_schema()
    )

def _get_mode_schema(defaults=None):

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
        vol.Required("initial_template", default=defaults.get("initial_template", "none")): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[
                    {"value": "none", "label": "None"},
                    {"value": "home", "label": "Home"},
                    {"value": "away", "label": "Away"},
                    {"value": "night", "label": "Night"},
                ],
                mode="list"
            )
        ),
    })