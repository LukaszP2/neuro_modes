"""Router for options flow - Strangler Fig Pattern.

Intercepts the initial step to route between:
- manage_sources (existing Bayesian configuration)
- manage_reactions (new execution layer)
"""
import voluptuous as vol
from homeassistant.helpers import selector


async def async_step_init_router(flow, user_input=None):
    """Initial router step - choose between sources or reactions."""
    if user_input is not None:
        choice = user_input.get("config_type")
        
        if choice == "manage_sources":
            # Route to existing sources management
            return await flow.async_step_manage_sources()
        elif choice == "manage_reactions":
            # Route to new reactions wizard
            from .router import async_step_reactions_start
            return await async_step_reactions_start(flow, None)
    
    return flow.async_show_form(
        step_id="init_router",
        data_schema=vol.Schema({
            vol.Required("config_type"): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=[
                        {"value": "manage_sources", "label": "Manage Sources"},
                        {"value": "manage_reactions", "label": "Manage Reactions"},
                    ],
                    mode="list",
                )
            ),
        }),
        translation_key="init_router",
    )


async def async_step_reactions_start(flow, user_input=None):
    """Start reactions configuration wizard."""
    return flow.async_show_menu(
        step_id="reactions_start",
        menu_options=["step_scope", "init"],
        translation_key="reactions_start",
    )
