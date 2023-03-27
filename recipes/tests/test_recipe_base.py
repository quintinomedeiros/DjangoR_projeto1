from django.test import TestCase
from recipes.models import Category, Recipe, User

class RecipeTestBase(TestCase):
    # Métodos setUp e tearDown
    def setUp(self) -> None:
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='laset name',
            password='user1234',
            email='user@email.com',
        )
        recipe = Recipe.objects.create(
            category=category, 
            author=author,
            title = 'Recipe title',
            description = 'Recipe description', 
            slug = 'recipe-slug', 
            preparation_time = '12', 
            preparation_time_unit = 'minutes', 
            servings = '3', 
            servings_unit = 'porcoes', 
            preparation_steps = 'Recipe preparation_steps', 
            preparation_steps_is_html = False, 
            is_published = True, 
            cover = 'recipes/covers/2023/03/26/2042255534.jpg'
        )
        return super().setUp()