from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            Subscribe, Tag)
from users.models import User
from .fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeCreateIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeGetIngredientsSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    ingredients = RecipeGetIngredientsSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True
    )
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=True)


class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.PrimaryKeyRelatedField(
        required=True,
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = RecipeCreateIngredientsSerializer(
        source='recipeingredient_set',
        many=True,
    )
    image = Base64ImageField(required=True)

    def validate_ingredients(self, data):
        try:
            ingredients = {
                get_object_or_404(
                    Ingredient, id=item.get('ingredient').get('id')):
                item.get('amount') for item in data}
        except Exception:
            raise serializers.ValidationError(
                'Такого ингредиента нет в базе')
        if len(data) != len(ingredients):
            raise serializers.ValidationError(
                'Один или несколько ингредиентов повторяются')
        return ingredients

    @staticmethod
    def bulk_create(recipe, ingredients):
        bulk_create_data = (
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount)
            for ingredient, amount in ingredients.items()
        )
        RecipeIngredient.objects.bulk_create(bulk_create_data)

    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.bulk_create(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(
            recipe__id=instance.id).delete()
        self.bulk_create(instance, ingredients)

        return super().update(instance, validated_data)


class SubscribeAuthorSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)
    recipes_amount = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'is_subscribed',
                  'recipes', 'recipes_amount')

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            if Subscribe.objects.filter(
                user=self.context.get('user'),
                following=self.context.get('following')
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого автора.')
        if (self.context.get('user') == self.context.get('following')):
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя.'})
        return attrs

    def get_is_subscribed(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Subscribe.objects.filter(user=self.context.get('request').user,
                                         following=obj).exists())

    def get_recipes_amount(self, obj):
        return obj.recipes.count()


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Subscribe.objects.filter(
                user=request.user, following=obj).exists())

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeSerializer(recipes, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (
            request.user.is_authenticated
            and Subscribe.objects.filter(
                user=request.user, following=obj).exists())


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
