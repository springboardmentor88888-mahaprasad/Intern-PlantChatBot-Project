# Knowledge module for Plant Disease ChatBot
# Provides structured disease data and treatment lookup

from .treatments import (
    get_treatment,
    get_uncertain_response,
    format_treatment_response,
    get_all_disease_keys
)

__all__ = [
    "get_treatment",
    "get_uncertain_response", 
    "format_treatment_response",
    "get_all_disease_keys"
]
