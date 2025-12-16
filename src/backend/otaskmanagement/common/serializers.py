from rest_framework import serializers


class TestEmailSerializer(serializers.Serializer):

    class Meta:
        fields = ["email"]

    email = serializers.EmailField(required=True)
