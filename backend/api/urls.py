from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (IngredientViewSet, TagViewSet, RecipesViewSet,
                    download_shopping_cart, ShoppingListViewSet,
                    FavoriteViewSet, FollowViewSet, ListFollowViewSet)


router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path(
        'users/subscriptions/',
        ListFollowViewSet.as_view(),
        name='subscriptions'
    ),

    path(
        'users/<int:author_id>/subscribe/',
        FollowViewSet.as_view(),
        name='subscribe'
    ),
    path(
        'recipes/download_shopping_cart/',
        download_shopping_cart,
        name='download'
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingListViewSet.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteViewSet.as_view(),
        name='favorite'
    ),

    path('', include(router.urls))
]
