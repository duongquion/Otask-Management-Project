# api/views.py
from rest_framework import generics

from .serializers import UserSerializer
from .models import CustomUser as User


class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
