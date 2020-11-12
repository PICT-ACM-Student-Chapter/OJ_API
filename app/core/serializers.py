from core.models import Language
from rest_framework import serializers


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language"""

    class Meta:
        model = Language
        fields = ['id', 'name']
