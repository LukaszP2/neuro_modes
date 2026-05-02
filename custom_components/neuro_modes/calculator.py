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

    # Obsługa operatora Większe lub równe (np. ">= 5")
    elif expected.startswith(">="):
        try:
            return float(actual) >= float(expected.replace(">=", "").strip())
        except ValueError:
            return False

    elif expected.startswith("<="):
        try:
            return float(actual) <= float(expected.replace("<=", "").strip())
        except ValueError:
            return False

    elif expected.startswith("!="):
        return actual != expected.replace("!=", "").strip()

    return actual == expected


def calculate_bayesian_state(hass, sources, threshold, delta, current_state):

    score = 0
    active_sources = []

    for src in sources:
        entity_id = src.get("entity_id")
        expected_state = src.get("state")
        weight = src.get("weight", 0)

        state_obj = hass.states.get(entity_id)
        
        if state_obj and is_source_active(state_obj.state, expected_state):
            score += weight
            active_sources.append(entity_id)

    if not current_state and score >= threshold:
        new_state = True
    elif current_state and score >= (threshold - delta):
        new_state = True
    else:
        new_state = False

    return new_state, score, active_sources