"""Reaction templates - predefined configurations."""
from .cinema import CINEMA_TEMPLATE

TEMPLATES = {
    "cinema": CINEMA_TEMPLATE,
}


def get_template(template_name: str) -> dict:
    """Get template by name.
    
    Args:
        template_name: Template name (e.g., 'cinema')
        
    Returns:
        Template configuration dict
    """
    return TEMPLATES.get(template_name, {})
