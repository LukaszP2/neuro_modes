import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_alarm(flow, user_input=None):
    if user_input is not None:
        sources = [{"entity_id": user_input["alarm_entity"], "state": "triggered", "weight": 100}]
        return flow.async_create_entry(title="", data={"sources": sources})
    return flow.async_show_form(step_id="template_alarm", data_schema=vol.Schema({
        vol.Required("alarm_entity"): selector.EntitySelector(selector.EntitySelectorConfig(domain="alarm_control_panel"))
    }))