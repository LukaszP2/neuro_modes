import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_vacation(flow, user_input=None):
    if user_input is not None:
        sources = [
            # Zamiast osoby sprawdzamy strefę domową (zone.home == 0 oznacza, że nikogo nie ma)
            {"entity_id": user_input["home_zone"], "state": "0", "weight": 60},
        ]
        if "alarm_entity" in user_input:
            # Alarm potwierdza, że dom jest pusty
            sources.append({"entity_id": user_input["alarm_entity"], "state": "armed_away", "weight": 40})
            
        return flow.async_create_entry(title="", data={"sources": sources})

    return flow.async_show_form(
        step_id="template_vacation",
        data_schema=vol.Schema({
            vol.Required("home_zone", default="zone.home"): selector.EntitySelector(selector.EntitySelectorConfig(domain="zone")),
            vol.Optional("alarm_entity"): selector.EntitySelector(selector.EntitySelectorConfig(domain="alarm_control_panel")),
            vol.Required("min_hours", default=48): int,
        })
    )