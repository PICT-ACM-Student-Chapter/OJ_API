from django.contrib.auth.models import User
from rest_framework import serializers


# Serializer to get only safe fields (exclude sensitive data like pass-hash)
# Can be merged if others serializers added
# ENSURING ONLY THE FIELDS BELOW ARE ALLOWED
class UserSafeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
