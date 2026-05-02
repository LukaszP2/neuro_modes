class NeuroEngine:
    def __init__(self, hass):
        self.hass = hass
        self.states = {}  # Live state storage for all modes

    def set_manual_override(self, mode_name, is_on):
        """Handle manual override from Home Assistant UI."""
        if mode_name not in self.states:
            self.states[mode_name] = {}
            
        self.states[mode_name]["state"] = is_on
        
        # When manually enabled, force 100% confidence to prevent system override
        if is_on:
            self.states[mode_name]["confidence"] = 100
        else:
            self.states[mode_name]["confidence"] = 0
            
        # Mark that human made this decision
        self.states[mode_name]["human_override"] = True
