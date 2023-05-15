from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShopingCart, Subscribe, Tag)


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


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_amount',)
    search_fields = ('^name',)
    list_filter = ('author', 'name', 'tags',)

    @admin.display(empty_value='Не добавляли')
    def favorite_amount(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorite_amount.short_description = 'Сколько раз добавили в избранное'


class ShopingСartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipesIngredientsAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShopingCart, ShopingСartAdmin)
admin.site.register(Tag, TagAdmin)
