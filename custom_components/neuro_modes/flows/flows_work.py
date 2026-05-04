import voluptuous as vol
from homeassistant.helpers import selector
from homeassistant.helpers import entity_registry as er

async def async_step_template_work(flow, user_input=None):
    errors = {}

    registry = er.async_get(flow.hass)
    workday_entities = [
        entry.entity_id 
        for entry in registry.entities.values() 
        if entry.platform == "workday"
    ]

    has_workday = len(workday_entities) > 0
    default_workday = workday_entities[0] if has_workday else "binary_sensor.workday_sensor"

    if user_input is not None:
        sources = []
        
        if "workday_sensor" in user_input:
            sources.append({"entity_id": user_input["workday_sensor"], "state": "on", "weight": 40})

        for worker in user_input["workers"]:
            sources.append({"entity_id": worker, "state": "home", "weight": 30})
            
        if "activity_sensors" in user_input:
            for sensor in user_input["activity_sensors"]:
                sources.append({"entity_id": sensor, "state": "on", "weight": 40}) 
                
        if "disruptors" in user_input:
            for person in user_input["disruptors"]:
                sources.append({"entity_id": person, "state": "home", "weight": -100})
                
        return flow.async_create_entry(
            title="", 
            data={
                "sources": sources,
                "work_start_time": user_input["work_start_time"],
                "work_end_time": user_input["work_end_time"]
            }
        )

    schema = {
        vol.Required("workers"): selector.EntitySelector(selector.EntitySelectorConfig(domain="person", multiple=True)),
    }
    
    if has_workday:
        schema[vol.Optional("workday_sensor", default=default_workday)] = selector.EntitySelector(
            selector.EntitySelectorConfig(domain="binary_sensor", integration="workday")
        )
        
    schema.update({
        vol.Optional("activity_sensors"): selector.EntitySelector(selector.EntitySelectorConfig(multiple=True)),
        vol.Optional("disruptors"): selector.EntitySelector(selector.EntitySelectorConfig(domain="person", multiple=True)),
        vol.Required("work_start_time", default="07:00:00"): selector.TimeSelector(),
        vol.Required("work_end_time", default="17:00:00"): selector.TimeSelector(),
    })

    # DYNAMICZNY KROK: Jeśli nie ma Workday, odpalamy formularz pod inną nazwą
    current_step_id = "template_work" if has_workday else "template_work_no_workday"

    return flow.async_show_form(
        step_id=current_step_id,
        errors=errors,
        data_schema=vol.Schema(schema)
    )

async def async_step_template_work_no_workday(flow, user_input=None):
    """Przekierowanie formularza bez integracji Workday do głównej logiki."""
    return await async_step_template_work(flow, user_input)