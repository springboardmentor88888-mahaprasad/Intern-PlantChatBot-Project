# Chatbot module for Plant Disease ChatBot

from knowledge import get_treatment, format_treatment_response
from knowledge.treatments import _diseases_data as TREATMENTS


class PlantDiseaseBot:
    """A chatbot that provides information about plant diseases and treatments."""
    
    def get_greeting(self) -> str:
        """Return a greeting message."""
        return (
            "🌿 Hello! I'm your Plant Disease Assistant.\n\n"
            "I can help you with:\n"
            "• Information about plant diseases\n"
            "• Treatment recommendations\n"
            "• Prevention tips\n\n"
            "Upload an image or describe your plant's symptoms!"
        )
    
    def get_disease_list(self) -> str:
        """Return a list of diseases the bot knows about."""
        diseases = [info['disease'] for info in TREATMENTS.values()]
        response = "🌱 **Diseases I can help with:**\n\n"
        for disease in diseases:
            response += f"  • {disease}\n"
        return response
    
    def respond_to_disease(self, disease_class: str) -> str:
        """Generate a response for a detected disease."""
        return format_treatment_response(disease_class)
    
    def respond_to_query(self, query: str) -> str:
        """Process a user query and generate an appropriate response."""
        query_lower = query.lower().strip()
        
        # Check for greetings
        if any(greet in query_lower for greet in ['hi', 'hello', 'hey', 'start', 'help']):
            return self.get_greeting()
        
        # Check for disease list request
        if 'list' in query_lower or 'diseases' in query_lower:
            return self.get_disease_list()
        
        # Default response
        return (
            "I'm not sure I understand. Try:\n"
            "• Uploading an image of a plant leaf\n"
            "• Describing your plant's symptoms\n"
            "• Typing 'list' to see all diseases I know about"
        )


# Default bot instance
bot = PlantDiseaseBot()


def get_response(query: str) -> str:
    """Get a response from the chatbot for a given query."""
    return bot.respond_to_query(query)


def get_disease_response(disease_class: str) -> str:
    """Get treatment information for a detected disease."""
    return bot.respond_to_disease(disease_class)