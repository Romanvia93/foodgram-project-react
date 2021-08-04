from import_export import resources
from .models import Ingredient


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ('id','title','dimension' )
