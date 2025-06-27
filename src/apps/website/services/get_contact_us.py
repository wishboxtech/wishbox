from src.apps.website.selectors import get_contact_us as get_contact_us_selector
from src.apps.website.serializers import ContactUsSerializer

def get_contact_us():
    
        contact_us_instance = get_contact_us_selector()
        if contact_us_instance is None:
            return None
        
        serializer = ContactUsSerializer(contact_us_instance)
        
        return serializer.data