from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions


# Get the UserModel
UserModel = get_user_model()


class OEELoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = None

        # Must supply either email or user name.
        if not (username or email):
            msg = _('Must supply either a username or email.')
            raise exceptions.ValidationError(msg)

        if not username:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        user = authenticate(
            username=username,
            password=password
        )

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs
