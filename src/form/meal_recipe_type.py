from framefox.core.form.type.form_type_interface import FormTypeInterface
from framefox.core.form.form_builder import FormBuilder

from framefox.core.form.type.entity_type import EntityType



from framefox.core.form.type.entity_type import EntityType


from framefox.core.form.type.number_type import NumberType
class MealRecipeType(FormTypeInterface):
    """Form of the entity MealRecipe."""
    
    def build_form(self, builder: FormBuilder) -> None:
        """Configure properties of the form."""
        
        
        
        
        builder.add('meal', EntityType, {
            'class': 'Meal',
            'required': False,
            'label': 'Meal',
            'choice_label': 'name',
            'show_id': True,
        })
        
        
        
        
        
        
        
        builder.add('recipe', EntityType, {
            'class': 'Recipe',
            'required': False,
            'label': 'Recipe',
            'choice_label': 'name',
            'show_id': True,
        })
        
        
        
        
        
        
        builder.add('servings', NumberType, {
            'required': False,
            'label': 'Servings',
            
        })
        
        
        
        
    def get_options(self) -> dict:
        return {
            'attr': {'class': 'needs-validation', 'novalidate': 'novalidate'}
        }