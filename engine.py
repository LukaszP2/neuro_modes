class NeuroEngine:
    def __init__(self, hass):
        self.hass = hass
        self.states = {}  # Tutaj trzymamy żywe stany wszystkich trybów

    def set_manual_override(self, mode_name, is_on):
        """Obsługa kliknięcia z palca w Home Assistant (Dashboard)."""
        if mode_name not in self.states:
            self.states[mode_name] = {}
            
        self.states[mode_name]["state"] = is_on
        
        # Jeśli włączamy palcem, wymuszamy 100% pewności, żeby system nas nie nadpisał
        if is_on:
            self.states[mode_name]["confidence"] = 100
        else:
            self.states[mode_name]["confidence"] = 0
            
        # Zapisujemy informację, że to człowiek podjął decyzję (do wykorzystania później)
        self.states[mode_name]["human_override"] = True
