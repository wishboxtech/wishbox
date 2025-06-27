from rest_framework import serializers

from src.apps.wallet.models import Card


class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ("id", "user", "card_number")
