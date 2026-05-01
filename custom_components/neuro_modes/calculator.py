def is_source_active(actual_state, expected_state):
    """Inteligentne porównywanie stanów z obsługą operatorów (> , < , !=)."""
    if actual_state is None:
        return False
        
    actual = str(actual_state).strip().lower()
    expected = str(expected_state).strip().lower()

    # Obsługa operatora Większe niż (np. "> 0")
    if expected.startswith(">"):
        try:
            return float(actual) > float(expected.replace(">", "").strip())
        except ValueError:
            return False

    # Obsługa operatora Mniejsze niż (np. "< 5")
    elif expected.startswith("<"):
        try:
            return float(actual) < float(expected.replace("<", "").strip())
        except ValueError:
            return False

    # Obsługa operatora Różne od (np. "!= not_home")
    elif expected.startswith("!="):
        return actual != expected.replace("!=", "").strip()

    # Zwykłe porównanie tekstu (np. "on" == "on")
    return actual == expected


def calculate_bayesian_state(hass, sources, threshold, delta, current_state):
    """
    Czysta funkcja matematyczna wyliczająca stan z poszlak.
    Zwraca: (nowy_stan_boolean, zdobyte_punkty_int, lista_aktywnych_encij)
    """
    score = 0
    active_sources = []

    # 1. Zbieramy punkty z HA
    for src in sources:
        entity_id = src.get("entity_id")
        expected_state = src.get("state")
        weight = src.get("weight", 0)

        state_obj = hass.states.get(entity_id)
        
        # ---> TUTAJ JEST MAGIA: Zmieniony IF korzystający z nowej funkcji <---
        if state_obj and is_source_active(state_obj.state, expected_state):
            score += weight
            active_sources.append(entity_id)

    # 2. Przerzutnik Schmitta (Histereza)
    if not current_state and score >= threshold:
        new_state = True
    elif current_state and score >= (threshold - delta):
        new_state = True
    else:
        new_state = False

    return new_state, score, active_sources