from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    # Criação de receitas sem os campos com valores padrão (no default)
    def make_recipe_no_defaults(self):
        recipe = Recipe(
        category=self.make_category(name='test defaul category'),
        author=self.make_author(username='author test default'),
        title = 'Recipe title',
        description = 'Recipe description', 
        slug = 'recipe-slug-for-no-defaults', 
        preparation_time = '12', 
        preparation_time_unit = 'minutes', 
        servings = '3', 
        servings_unit = 'porcoes', 
        preparation_steps = 'Recipe preparation_steps', 
        cover = 'recipes/covers/2023/03/26/2042255534.jpg',
        )
        recipe.full_clean() #Validação dos erros
        recipe.save()
        return recipe

    # Teste parametrizado para verificar tamanho máximo dos campos da receita
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError): # Informa que o teste irá gerar um erro
            self.recipe.full_clean() # Aqui corre a validação do campo (geração do erro, pois o campo não é válido)

    def test_recipe_prepararion_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html, msg='Recipe preparation steps is html is not false') 

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published, msg='Recipe is published is not false')
    
    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), needed, msg='Recipe string representation must be "{needed}" but "{str(self.recipe)}" was received.')
       
