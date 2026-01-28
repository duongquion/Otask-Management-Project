# api/views.py
from rest_framework import generics

from .models import CustomUser as User
from .serializers import UserSerializer


class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
