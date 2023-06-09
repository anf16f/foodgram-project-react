from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SubscriptionsViewSet,
                    TagViewSet, subscribe)

app_name = 'api'

router_v1 = DefaultRouter()


router_v1.register(
    'ingredients',
    IngredientViewSet,
    basename='ingredients'
)

router_v1.register(
    'tags',
    TagViewSet,
    basename='tags'
)

router_v1.register(
    'recipes',
    RecipeViewSet,
    basename='recipes'
)

router_v1.register(
    r'users/subscriptions',
    SubscriptionsViewSet,
    basename='subscriptions',
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('users/<int:user_id>/subscribe/', subscribe, name='subscribe')
]
