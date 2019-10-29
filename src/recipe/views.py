from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Tag
from .serializers import *


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Manage tags i the database """

    authentication_classes = (TokenAuthentication,)
    premission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """ Return objects for the current authenticated user """
        return self.queryset.filter(user=self.request.user).order_by("-name")

