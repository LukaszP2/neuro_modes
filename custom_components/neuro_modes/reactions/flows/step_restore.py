"""Step: Configure restore behavior when mode ends."""
import voluptuous as vol
from homeassistant.helpers import selector

async def async_step_restore(flow, user_input=None):
    """Configure what happens when this reaction mode ends."""
    if user_input is not None:
        if not hasattr(flow, "options_data"):
            flow.options_data = {}
        flow.options_data["restore_action"] = user_input.get("restore_action")
        
        current_options = dict(flow._entry.options)
        reactions = list(current_options.get("reactions", []))
        
        # LOGIKA EDYCJI vs DODAWANIA
        if hasattr(flow, "edit_reaction_index") and flow.edit_reaction_index is not None:
            # Nadpisujemy istniejącą reakcję
            reactions[flow.edit_reaction_index] = flow.options_data
        else:
            # Dodajemy nową
            reactions.append(flow.options_data)
            
        current_options["reactions"] = reactions
        
        return flow.async_create_entry(title="", data=current_options)
    
    # Wczytywanie domyślnych (przy edycji)
    default_restore = flow.options_data.get("restore_action", "restore_previous") if hasattr(flow, "options_data") else "restore_previous"

    return flow.async_show_form(
        step_id="reactions_restore",
        data_schema=vol.Schema({
            vol.Required("restore_action", default=default_restore): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "restore_previous", "label": "Przywróć stan poprzedni (Zalecane)"},
                        {"value": "turn_off_all", "label": "Zgaś wszystkie światła"},
                        {"value": "enable_al", "label": "Zresetuj i wymuś włączenie Adaptive Lighting"},
                    ],
                    mode="list",
                )
            ),
        }),
    )