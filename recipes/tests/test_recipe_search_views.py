from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase

class RecipeSearchViewTest(RecipeTestBase):
    # SEARCH TESTS
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
           'Receitas | Pesquisa por &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one' 
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='recipe-one', title=title1, author_data={'username': 'author_one'}
        )

        recipe2 = self.make_recipe(
            slug='recipe-two', title=title2, author_data={'username': 'author_two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
       

    def test_recipe_search_can_find_recipe_by_description(self):
        description1 = 'This is recipe three' 
        description2 = 'This is recipe four'

        recipe3 = self.make_recipe(
            slug='recipe-three', description=description1, author_data={'username': 'author_three'}
        )

        recipe4 = self.make_recipe(
            slug='recipe-four', description=description2, author_data={'username': 'author_four'}
        )

        search_url = reverse('recipes:search')
        response3 = self.client.get(f'{search_url}?q={description1}')
        response4 = self.client.get(f'{search_url}?q={ description2}')
        response_both2 = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe3, response3.context['recipes'])
        self.assertNotIn(recipe4, response3.context['recipes'])

        self.assertIn(recipe4, response4.context['recipes'])
        self.assertNotIn(recipe3, response4.context['recipes'])

        self.assertIn(recipe3, response_both2.context['recipes'])
        self.assertIn(recipe4, response_both2.context['recipes'])
        
    def test_recipe_search_can_find_recipe_by_title_is_publishe_true_false(self):
        title5 = 'This is recipe five' 
        title6 = 'This is recipe six'

        recipe5True = self.make_recipe(
            slug='recipe-five', title=title5, author_data={'username': 'author_five'}, is_published=True,
        )

        recipe6False = self.make_recipe(
            slug='recipe-six', title=title6, author_data={'username': 'author_six'}, is_published=False,
        )

        search_url = reverse('recipes:search')
        response5 = self.client.get(f'{search_url}?q={title5}')
        response6 = self.client.get(f'{search_url}?q={title6}')

        self.assertIn(recipe5True, response5.context['recipes'])
        self.assertNotIn(recipe6False, response6.context['recipes'])
        