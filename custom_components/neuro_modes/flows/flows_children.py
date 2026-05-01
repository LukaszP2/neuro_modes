import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_template_children(flow, user_input=None):
    """Kreator trybu Dzieci z walidacją krzyżową."""
    errors = {}
    
    if user_input is not None:
        # Konwersja na zbiory by łatwo sprawdzić duplikaty
        children_set = set(user_input["children_entities"])
        parents_set = set(user_input["parent_entities"])
        
        # Jeśli zbiory mają część wspólną (ta sama osoba tu i tu)
        if children_set.intersection(parents_set):
            errors["base"] = "duplicate_person"
        else:
            sources = []
            for child in user_input["children_entities"]:
                sources.append({"entity_id": child, "state": "home", "weight": 60})
            for parent in user_input["parent_entities"]:
                sources.append({"entity_id": parent, "state": "home", "weight": -100})
            return flow.async_create_entry(title="", data={"sources": sources})

    return flow.async_show_form(
        step_id="template_children",
        errors=errors,
        data_schema=vol.Schema({
            vol.Required("children_entities"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="person", multiple=True)
            ),
            vol.Required("parent_entities"): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="person", multiple=True)
            ),
        })
    )