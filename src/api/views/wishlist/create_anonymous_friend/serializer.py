from rest_framework import serializers


class CreateAnonymousFriendInputSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=150)


class CreateAnonymousFriendOutputSerializer(serializers.Serializer):
    anonymous_friend_id = serializers.UUIDField(source="id", read_only=True)
