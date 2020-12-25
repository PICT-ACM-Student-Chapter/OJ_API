from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language"""

    class Meta:
        model = Language
        fields = ['id', 'name', 'monaco_lang_code']


# Serializer to get only safe fields (exclude sensitive data like pass-hash)
# Can be merged if others serializers added
# ENSURING ONLY THE FIELDS BELOW ARE ALLOWED
class UserSafeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        lookup_field = 'id'

# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#
#         errors = dict()
#         try:
#             # validate the password and catch the exception
#             validators.validate_password(password=password, user=User)
#             user.save()
#             return user
#
#         # the exception raised here is different than
#         # serializers.ValidationError
#         except exceptions.ValidationError as e:
#             errors['password'] = list(e.messages)
#
#         if errors:
#             raise serializers.ValidationError(errors)
