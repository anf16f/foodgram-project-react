from django.contrib import admin

from .models import (
    Ingredient, Recipe, Tag, Favorites,
    RecipesIngredients, ShopingCart, Subscribe)

# admin.site.register(Ingredient)
# admin.site.register(Recipe)
# admin.site.register(Tag)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    list_editable = ('user', 'following')
    empty_value_display = '-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('^name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    search_fields = ('user', 'recipe',)


class RecipesIngredientsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


if not hasattr(admin, 'display'):
    def display(empty_value):
        def decorator(fn):
            fn.empty_value = empty_value
            return fn
        return decorator
    setattr(admin, 'display', display)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_amount',)
    search_fields = ('^name',)
    list_filter = ('author', 'name', 'tags',)

    @admin.display(empty_value='Не добавляли')
    def favorite_amount(self, obj):
        return Favorites.objects.filter(recipe=obj).count()

    favorite_amount.short_description = 'Сколько раз добавили в избранное'


class ShopingСartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


admin.site.register(Favorites, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipesIngredients, RecipesIngredientsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShopingCart, ShopingСartAdmin)
admin.site.register(Tag, TagAdmin)
