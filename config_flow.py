from homeassistant import config_entries
from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ENGINE
from .flows.flows_general import async_step_setup_engine, async_step_setup_mode, async_step_setup_modifier
from .flows.flows_settings import async_step_edit_settings
from .flows.flows_sources import (
    async_step_manage_sources, 
    async_step_add_source, 
    async_step_edit_source_menu,
    async_step_edit_source_form,
    async_step_delete_source_action
)
from .flows.flows_home import async_step_template_home
from .flows.flows_away import async_step_template_away
from .flows.flows_night import async_step_template_night
from .flows.flows_cinema import async_step_template_cinema
from .flows.flows_alarm import async_step_template_alarm
from .flows.flows_work import async_step_template_work
from .flows.flows_guests import async_step_template_guests
from .flows.flows_vacation import async_step_template_vacation
from .flows.flows_children import async_step_template_children

class NeuroModesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN): # type: ignore
    """Obsługa pierwszej instalacji."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        return self.async_show_menu(step_id="user", menu_options=["setup_engine", "setup_mode", "setup_modifier"])

    async def async_step_setup_engine(self, user_input=None):
        return await async_step_setup_engine(self, user_input)

    async def async_step_setup_mode(self, user_input=None):
        return await async_step_setup_mode(self, user_input)

    async def async_step_setup_modifier(self, user_input=None):
        return await async_step_setup_modifier(self, user_input)

    @staticmethod
    def async_get_options_flow(config_entry):
        return NeuroModesOptionsFlow(config_entry)

class NeuroModesOptionsFlow(config_entries.OptionsFlow):
    """Główne menu opcji."""
    def __init__(self, config_entry):
        self._entry = config_entry
        self._selected_source_id = None

    async def async_step_init(self, user_input=None):
        if self._entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ENGINE:
            return self.async_abort(reason="engine_no_options")
        return self.async_show_menu(step_id="init", menu_options=["edit_settings", "manage_sources", "select_template"])

    async def async_step_edit_settings(self, user_input=None):
        return await async_step_edit_settings(self, user_input)

    async def async_step_manage_sources(self, user_input=None):
        return await async_step_manage_sources(self, user_input)

    async def async_step_add_source(self, user_input=None):
        return await async_step_add_source(self, user_input)

    async def async_step_edit_source_menu(self, user_input=None):
        return await async_step_edit_source_menu(self, user_input)
    
    async def async_step_delete_source_action(self, user_input=None):
        return await async_step_delete_source_action(self, user_input)
    
    async def async_step_edit_source_form(self, user_input=None):
        return await async_step_edit_source_form(self, user_input)

    async def async_step_select_template(self, user_input=None):
        """Wielojęzyczne menu szablonów z przyciskiem wstecz."""
        return self.async_show_menu(
            step_id="select_template",
            menu_options=[
                "template_home", 
                "template_away", 
                "template_night", 
                "template_cinema", 
                "template_alarm", 
                "template_work", 
                "template_guests", 
                "template_vacation", 
                "template_children",
                "init"  # Magiczny guzik Wstecz (cofa do menu init)
            ]
        )

    async def async_step_template_work(self, user_input=None):
        return await async_step_template_work(self, user_input)

    async def async_step_template_guests(self, user_input=None):
        return await async_step_template_guests(self, user_input)

    async def async_step_template_vacation(self, user_input=None):
        return await async_step_template_vacation(self, user_input)

    async def async_step_template_children(self, user_input=None):
        return await async_step_template_children(self, user_input)

    async def async_step_template_home(self, user_input=None):
        return await async_step_template_home(self, user_input)
    
    async def async_step_template_away(self, user_input=None):
        return await async_step_template_away(self, user_input)
    
    async def async_step_template_night(self, user_input=None):
        return await async_step_template_night(self, user_input)
    
    async def async_step_template_cinema(self, user_input=None):
        return await async_step_template_cinema(self, user_input)
    
    async def async_step_template_alarm(self, user_input=None):
        return await async_step_template_alarm(self, user_input)    