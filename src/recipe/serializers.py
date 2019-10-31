from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """ Serializer for tag objects """

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """ serializer for ingredient objects """

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """ Serialize a recipe """

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all(),
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(),)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "ingredients",
            "tags",
            "time_minutes",
            "price",
            "link",
        )
        read_only_fields = ("id",)


# using base serializer
class RecipeDetailSerializer(RecipeSerializer):
    """ Serialize a recipe details """

    # MANY means that you can have many ingredients associated with recipe
    # you cant' create recipe by providing this value (READ_ONLY)
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

