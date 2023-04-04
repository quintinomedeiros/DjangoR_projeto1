from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

from unittest.mock import patch

class RecipeHomeViewTest(RecipeTestBase):
    # HOME TESTS
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('Desculpe! Atualmente não temos receitas para exibir.', response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('Recipe title', content)

    def test_recipe_home_template_dont_loads_recipes_no_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('Desculpe! Atualmente não temos receitas para exibir.', response.content.decode('utf-8'))

    def test_recipe_home_is_paginated(self):
        for i in range(9):
            kwargs = {'author_data':{'username': f'u{i}'}, 'slug':f'r{i}'}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3): 
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
    
    def test_invalid_page_querry_uses_page_one(self):
        for i in range(8):
            kwargs = {'author_data':{'username': f'u{i}'}, 'slug':f'r{i}'}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3): 
            response = self.client.get(reverse('recipes:home') + '?page=1A') #Requisição com uma página inválida
            self.assertEqual(response.context['recipes'].number, 1)

            response = self.client.get(reverse('recipes:home') + '?page=2') #Requisição com uma página válida
            self.assertEqual(response.context['recipes'].number, 2)


