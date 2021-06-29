"""User app serializers """

import logging
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


log = logging.getLogger(__file__)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """ Create a new user with a encrypted password and return it """

        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for User authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get(
            'request'), username=email, password=password)
        log.info(f'Email:{email} password:{password} user:{user}')
        if not user:
            message = _('Unable to authenticate user with given credentials')
            return serializers.ValidationError(message, code='authentication')

        attrs['user'] = user
        return attrs
