from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (exceptions, filters, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from recipes.models import (Favorites, Ingredient, Recipe, RecipesIngredients,
                            ShopingCart, Subscribe, Tag)
from users.models import User

from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          RecipeUpdateSerializer, SubscribeAuthorSerializer,
                          SubscriptionsSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('tags', 'author', 'ingredients')
    search_fields = ('name', 'text')

    def create(self, request, *args, **kwargs):
        self.serializer_class = RecipeCreateSerializer
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = RecipeUpdateSerializer
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        new = Recipe.objects.create(
            author=self.request.user,
            name=serializer.validated_data['name'],
            text=serializer.validated_data['text'],
            cooking_time=serializer.validated_data['cooking_time'],
            image=serializer.validated_data['image'],
        )
        new.tags.set(serializer.validated_data['tags'])
        ingredients = serializer.validated_data['ingredients']
        for item in ingredients:
            RecipesIngredients.objects.create(
                recipe=new,
                ingredient=get_object_or_404(Ingredient, id=item['id']),
                amount=item['amount']
            )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if self.request.method == 'POST':
            if Favorites.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError('Рецепт уже в избранном.')

            Favorites.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Favorites.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в избранном, либо он уже удален.'
                )

            favorite = get_object_or_404(Favorites, user=user, recipe=recipe)
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if self.request.method == 'POST':
            if ShopingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепт уже в списке покупок.'
                )

            ShopingCart.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(
                recipe,
                context={'request': request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not ShopingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок.'
                )

            shopping_cart = get_object_or_404(
                ShopingCart,
                user=user,
                recipe=recipe
            )
            shopping_cart.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shoping_cart = ShopingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shoping_cart]
        shoping_list = RecipesIngredients.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )

        add_text = 'Список покупок с сайта Foodgram:\n\n'
        for item in shoping_list:
            ingredient = Ingredient.objects.get(id=item['ingredient'])
            amount = item['amount']
            add_text += (
                f'{ingredient.name}, {amount} '
                f'{ingredient.measurement_unit}\n'
            )

        response = HttpResponse(add_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )

        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')


@api_view(['POST', 'DELETE'])
def SubscribeAPIView(request, user_id):
    user = request.user
    following = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        if Subscribe.objects.filter(
            user=user,
            following=following
        ).exists():
            raise exceptions.ValidationError(
                'Вы уже подписаны на этого автора.')
        serializer = SubscribeAuthorSerializer(
            following, data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.create(user=request.user, following=following)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        if not Subscribe.objects.filter(
            user=user,
            following=following
        ).exists():
            raise exceptions.ValidationError(
                'Вы не подписаны на этого автора'
            )
        subscription = Subscribe.objects.filter(
            user=user,
            following=following
        )

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permissions = (permissions.IsAuthenticated,)
    queryset = Subscribe.objects.all()
    serializer_class = SubscriptionsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        subscriptions = User.objects.filter(following__user=self.request.user)
        return subscriptions

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = SubscriptionsSerializer(page, many=True,
                                             context={'request': request})
        return self.get_paginated_response(serializer.data)
