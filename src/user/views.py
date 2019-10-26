from rest_framework import generics
from user.serializers import *


class CreateUserView(generics.CreateAPIView):
    """ create a new user in the system """
    serializer_class = UserSerializer

