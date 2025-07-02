from framefox.core.form.type.form_type_interface import FormTypeInterface
from framefox.core.form.form_builder import FormBuilder

from framefox.core.form.type.entity_type import EntityType



from framefox.core.form.type.entity_type import EntityType


from framefox.core.form.type.number_type import NumberType

from framefox.core.form.type.text_type import TextType
class RecipeIngredientType(FormTypeInterface):
    """Form of the entity RecipeIngredient."""
    
    def build_form(self, builder: FormBuilder) -> None:
        """Configure properties of the form."""
        
        
        
        
        builder.add('recipe', EntityType, {
            'class': 'Recipe',
            'required': False,
            'label': 'Recipe',
            'choice_label': 'name',
            'show_id': True,
        })
        
        
        
        
        
        
        
        builder.add('ingredient', EntityType, {
            'class': 'Ingredient',
            'required': False,
            'label': 'Ingredient',
            'choice_label': 'name',
            'show_id': True,
        })
        
        
        
        
        
        
        builder.add('quantity', NumberType, {
            'required': False,
            'label': 'Quantity',
            
            'attr': {'step': '0.01'},
            
        })
        
        
        
        
        
        builder.add('unit', TextType, {
            'required': False,
            'label': 'Unit',
        })
        
        
        
        
    def get_options(self) -> dict:
        return {
            'attr': {'class': 'needs-validation', 'novalidate': 'novalidate'}
        }