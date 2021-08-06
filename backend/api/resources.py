from import_export import resources
from .models import Ingredient


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit', )
        import_id_fields = ('name', 'measurement_unit', )
