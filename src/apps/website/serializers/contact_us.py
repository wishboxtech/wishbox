from rest_framework import serializers

from src.apps.website.models import ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ContactUs
        fields = ['id', 'email', 'created_at', 'updated_at']
