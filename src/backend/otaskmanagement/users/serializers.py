"""DRF data serializers for User app."""

from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.utils import setup_user_email

try:
    from allauth.account.adapter import get_adapter
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from .models import CustomUser as User

STAFF_DOMAIN = ["otask.com", "admin.otask.com"]


class UserRegisterSerializer(RegisterSerializer):
    """
    Custom registration serializer that modifies password validation
    and user creation behavior.
    """

    username = None

    def validate(self, data):
        email = data["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email have already exists"})
        return super().validate(data)

    def validate_password1(self, password):
        email = (self.initial_data.get("email") or "").strip().lower()
        is_staff_domain = email.split("@")[-1].lower()
        if email and is_staff_domain in STAFF_DOMAIN:
            return password
        return super().validate_password1(password)

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)

        email = (self.cleaned_data.get("email") or "").strip().lower()
        is_staff_domain = email.split("@")[-1].lower()
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


class UserSerializer(serializers.ModelSerializer):
    """Serializer for list User"""

    class Meta:
        model = User
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail User"""

    full_name = serializers.CharField(source="fullname", read_only=True)

    class Meta:
        model = User
        fields = ["full_name", "code", "last_login", "email", "is_active"]
