from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins,
                            permissions, status, viewsets)
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            ShopingCart, Subscribe, Tag)
from users.models import User
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, RecipeShortSerializer,
                          SubscribeAuthorSerializer, SubscriptionsSerializer,
                          TagSerializer,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('tags', 'author', 'ingredients')
    search_fields = ('name', 'text')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def _p_d_method(self, queryset):
        recipe = self.get_object()
        if self.request.method == 'DELETE':
            get_object_or_404(queryset, recipe_id=recipe.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if queryset.filter(recipe=recipe).exists():
            raise ValidationError('Рецепт уже добавлен')
        queryset.create(recipe=recipe)
        serializer = RecipeShortSerializer(recipe, context={
            'recipe': recipe,
            'user': self.request.user,
            'queryset': queryset,
        })
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['POST', 'DELETE'], )
    def favorite(self, request, pk=None):
        return self._p_d_method(request.user.favorites)

    @action(detail=True,
            permission_classes=[permissions.IsAuthenticated],
            methods=['POST', 'DELETE'], )
    def shopping_cart(self, request, pk=None):
        return self._p_d_method(request.user.cart)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shoping_cart = ShopingCart.objects.filter(user=self.request.user)
        shoping_list = RecipeIngredient.objects.filter(
            recipe__in=shoping_cart.values('recipe_id')
        ).values(
            'ingredient'
        ).annotate(
            amount_sum=Sum('amount')
        )

        add_text = 'Список покупок с сайта Foodgram:\n\n'
        for item in shoping_list:
            ingredient = Ingredient.objects.get(id=item['ingredient'])
            amount_sum = item['amount_sum']
            add_text += (
                f'{ingredient.name}, {amount_sum} '
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
def subscribe_API_View(request, user_id):
    user = request.user
    following = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        serializer = SubscribeAuthorSerializer(
            following, data=request.data, context={
                'request': request,
                'user': user,
                'following': following})
        serializer.is_valid(raise_exception=True)
        Subscribe.objects.create(user=request.user, following=following)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        if not Subscribe.objects.filter(
            user=user,
            following=following
        ).exists():
            raise ValidationError(
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
        return User.objects.filter(following__user=self.request.user)

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = SubscriptionsSerializer(page, many=True,
                                             context={'request': request})
        return self.get_paginated_response(serializer.data)
