# Chatbot module for Plant Disease ChatBot

from knowledge import get_treatment, format_treatment_response
from knowledge.treatments import _diseases_data as TREATMENTS



class PlantDiseaseBot:
    """
    A chatbot that provides information about plant diseases and treatments.
    """
    
    def __init__(self):
        self.disease_keywords = {
            "late blight": "Tomato___Late_blight",
            "early blight": "Tomato___Early_blight",
            "leaf mold": "Tomato___Leaf_Mold",
            "septoria": "Tomato___Septoria_leaf_spot",
            "bacterial spot": "Tomato___Bacterial_spot",
            "yellow leaf curl": "Tomato___YellowLeaf__Curl_Virus",
            "curl virus": "Tomato___YellowLeaf__Curl_Virus",
            "mosaic": "Tomato___mosaic_virus",
            "mosaic virus": "Tomato___mosaic_virus",
            "healthy": "Tomato___healthy"
        }
    
    def get_greeting(self) -> str:
        """Return a greeting message."""
        return (
            "🌿 Hello! I'm your Plant Disease Assistant.\n\n"
            "I can help you with:\n"
            "• Information about plant diseases\n"
            "• Treatment recommendations\n"
            "• Prevention tips\n\n"
            "Upload an image or ask me about a specific disease!"
        )
    
    def get_disease_list(self) -> str:
        """Return a list of diseases the bot knows about."""
        diseases = [info['disease'] for info in TREATMENTS.values()]
        response = "🌱 **Diseases I can help with:**\n\n"
        for disease in diseases:
            response += f"  • {disease}\n"
        return response
    
    def respond_to_disease(self, disease_class: str) -> str:
        """
        Generate a response for a detected disease.
        
        Args:
            disease_class: The disease classification from the model
            
        Returns:
            Formatted response with treatment information
        """
        return format_treatment_response(disease_class)
    
    def respond_to_query(self, query: str) -> str:
        """
        Process a user query and generate an appropriate response.
        
        Args:
            query: User's text input
            
        Returns:
            Bot response string
        """
        query_lower = query.lower().strip()
        
        # Check for greetings
        greetings = ['hi', 'hello', 'hey', 'start', 'help']
        if any(greet in query_lower for greet in greetings):
            return self.get_greeting()
        
        # Check for disease list request
        if 'list' in query_lower or 'diseases' in query_lower or 'what can you' in query_lower:
            return self.get_disease_list()
        
        # Check for specific disease mentions
        for keyword, disease_class in self.disease_keywords.items():
            if keyword in query_lower:
                return self.respond_to_disease(disease_class)
        
        # Default response
        return (
            "I'm not sure I understand. Try:\n"
            "• Uploading an image of a plant leaf\n"
            "• Asking about a specific disease (e.g., 'What is late blight?')\n"
            "• Typing 'list' to see all diseases I know about"
        )


# Create a default bot instance
bot = PlantDiseaseBot()


def get_response(query: str) -> str:
    """
    Get a response from the chatbot for a given query.
    
    Args:
        query: User's text input
        
    Returns:
        Bot response string
    """
    return bot.respond_to_query(query)


def get_disease_response(disease_class: str) -> str:
    """
    Get treatment information for a detected disease.
    
    Args:
        disease_class: Disease classification from the model
        
    Returns:
        Formatted treatment information
    """
    return bot.respond_to_disease(disease_class)