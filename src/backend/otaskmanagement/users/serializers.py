import email
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.utils import setup_user_email
try:
    from allauth.account.adapter import get_adapter
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

STAFF_DOMAIN = ["otask.com", "admin.otask.com"]

class UserRegisterSerializer(RegisterSerializer):
    username = None

    def validate_password1(self, password):
        email = (self.initial_data.get("email") or "").strip().lower()
        is_staff_domain = email.split('@')[-1].lower()
        if email and is_staff_domain in STAFF_DOMAIN:
            return password
        return super().validate_password1(password)
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        email = (self.cleaned_data.get("email") or "").strip().lower()
        is_staff_domain = email.split('@')[-1].lower()
        is_staff = True if is_staff_domain in STAFF_DOMAIN else False
        if not is_staff and "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
