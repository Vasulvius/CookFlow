from framefox.core.form.type.form_type_interface import FormTypeInterface
from framefox.core.form.form_builder import FormBuilder

from framefox.core.form.type.entity_type import EntityType


from framefox.core.form.type.text_type import TextType

from framefox.core.form.type.text_type import TextType
class MealType(FormTypeInterface):
    """Form of the entity Meal."""
    
    def build_form(self, builder: FormBuilder) -> None:
        """Configure properties of the form."""
        
        
        
        
        builder.add('meal_recipes', EntityType, {
            'class': 'MealRecipe',
            'multiple': True,
            'required': False,
            'label': 'Meal_recipes',
            'choice_label': 'name',
            'show_id': True,
        })
        
        
        
        
        
        
        builder.add('name', TextType, {
            'required': False,
            'label': 'Name',
        })
        
        
        
        
        
        builder.add('notes', TextType, {
            'required': False,
            'label': 'Notes',
        })
        
        
        
        
    def get_options(self) -> dict:
        return {
            'attr': {'class': 'needs-validation', 'novalidate': 'novalidate'}
        }