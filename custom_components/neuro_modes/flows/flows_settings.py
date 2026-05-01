import voluptuous as vol
from ..const import CONF_ENTRY_TYPE, ENTRY_TYPE_MODE

async def async_step_edit_settings(flow, user_input=None):
    if user_input is not None:
        new_data = {**flow._entry.data, **user_input}

        entry_type = flow._entry.data.get(CONF_ENTRY_TYPE)
        prefix = "Mode" if entry_type == ENTRY_TYPE_MODE else "Modifier"
        
        flow.hass.config_entries.async_update_entry(
            flow._entry, 
            title=f"{prefix}: {user_input['name']}", 
            data=new_data
        )
        # Aktualizujemy główny tytuł integracji i dane wewnątrz
        flow.hass.config_entries.async_update_entry(
            flow._entry, 
            title=f"{prefix}: {user_input['name']}", 
            data=new_data
        )
        # NAPRAWA: Zwracamy obecne opcje, żeby ich nie wykasowało!
        return flow.async_create_entry(title="", data=flow._entry.options)

    return flow.async_show_form(
        step_id="edit_settings",
        data_schema=vol.Schema({
            vol.Required("name", default=flow._entry.data.get("name", "")): str,
            vol.Required("threshold", default=flow._entry.data.get("threshold", 70)): vol.All(vol.Coerce(int), vol.Range(0, 100)),
            vol.Required("delta", default=flow._entry.data.get("delta", 20)): vol.All(vol.Coerce(int), vol.Range(0, 100)),
            vol.Required("override_timeout", default=flow._entry.data.get("override_timeout", 120)): vol.All(vol.Coerce(int), vol.Range(0, 1440)),
        })
    )    
