from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import RecipeFilter
from .permissions import AdminOrAuthorOrReadOnly
from .models import (Ingredient, Tag, Recipe, ShoppingList, IngredientRecipe,
                     Favorite, Follow)
from .serializers import (IngredientSerializer, TagSerializer,
                          ListRecipeSerializer, CreateRecipeSerializer,
                          ShoppingListSerializer, FavoriteSerializer,
                          FollowSerializer, ShowFollowSerializer)
from users.models import User


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Used to list Ingredients.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    search_fields = ('name', )
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Used to list tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """
    View with post, delete, put options.
    Used to post, delete, put recipes.
    """
    queryset = Recipe.objects.all()
    filter_class = RecipeFilter
    permission_classes = [AdminOrAuthorOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListRecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class ShoppingListViewSet(APIView):
    """
    View with post and delete options.
    Used to create and delete recipes in shopping list.
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        shopping_cart_exist = ShoppingList.objects.filter(
            user=user,
            recipe__id=recipe_id
        ).exists()
        if shopping_cart_exist:
            return Response(
                {"Error": "This recipe is already in your basket"},
                status=status.HTTP_400_BAD_REQUEST
            )
        context = {'request': request}
        serializer = ShoppingListSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not ShoppingList.objects.filter(user=user, recipe=recipe).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def download_shopping_cart(request):
    """
    Function to download ingredients for recipes in shopping list.
    """

    user = request.user
    shopping_cart = user.shopping_list.all()
    buying_list = {}
    for record in shopping_cart:
        recipe = record.recipe
        ingredients = IngredientRecipe.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                buying_list[name]['amount'] = (buying_list[name]['amount']
                                               + amount)
    wishlist = []
    for name, data in buying_list.items():
        wishlist.append(
            f"{name} ({data['measurement_unit']}) - {data['amount']} \n")
    response = HttpResponse(wishlist, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response


class FavoriteViewSet(APIView):
    """
    View with post and delete options.
    Used to create and delete recipes in favorite list.
    """

    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        if Favorite.objects.filter(user=user, recipe__id=recipe_id).exists():
            return Response(
                {"Error": "You have already added recipe in favorite list"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FavoriteSerializer(
            data=data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(APIView):
    """
    View with post and delete options.
    Used to create and delete Follow objects.
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request, author_id):
        user = request.user
        follow_exist = Follow.objects.filter(
            user=user,
            author__id=author_id
        ).exists()
        if user.id == author_id or follow_exist:
            return Response(
                {"Error": "You have already followed this person"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'user': user.id,
            'author': author_id
        }
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        obj = get_object_or_404(Follow, user=request.user, author=author_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFollowViewSet(generics.ListAPIView):
    """
    View with post and delete options.
    Used to list Follow objects.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShowFollowSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
