from django.contrib import admin
from .models import (Recipe, Tag, Ingredient, IngredientRecipe, ShoppingList,
                     Favorite, Follow)
from .resources import CategoryResource
from import_export.admin import ImportMixin


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk','name','author')
    list_filter = ('author', 'name', 'tags')

admin.site.register(Recipe, RecipeAdmin)    


class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    list_filter = ('name','measurement_unit' )
    list_filter = ( 'name',)
    resource_class = CategoryResource

admin.site.register(Ingredient, IngredientAdmin)  

admin.site.register(IngredientRecipe)  
admin.site.register(Tag)  
admin.site.register(ShoppingList)
admin.site.register( Favorite)
admin.site.register( Follow)


