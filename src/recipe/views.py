from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Tag, Ingredient
from .serializers import *


class BaseRecipeAttrViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
):
    """ Base viewset for user owned recipe attributes """

    authentication_classes = (TokenAuthentication,)
    premission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user.id).order_by("-name")

    def perform_create(self, serializer):
        """ Create a new object """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage tags in the database """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    """ Because it's they are importing from BaseClassAttribute as they are same """
    # def get_queryset(self):
    #     """ Return objects for the current authenticated user """
    #     return self.queryset.filter(user=self.request.user.id).order_by("-name")

    # def perform_create(self, serializer):
    #     """ Create a new tag """
    #     serializer.save(user=self.request.user)


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage ingredient in the database """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    # def get_queryset(self):
    #     """ return objects for the current authenticated user """
    #     return self.queryset.filter(user=self.request.user).order_by("-name")

    # def perform_create(self, serializer):
    #     """ Create a new ingredient"""
    #     serializer.save(user=self.request.user)
