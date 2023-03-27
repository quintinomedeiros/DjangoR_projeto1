from django.shortcuts import get_list_or_404, get_object_or_404, render
from .models import Recipe

# Create your views here.
def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context =
        {
            'recipes': recipes,
})

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context =
        {
            'recipes': recipes,
            'title': f' | Categoria | {recipes[0].category.name}', # Pesquisa para atribuir à variável title como string o nome da categoria para ser lança no título da página
})

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context = {
        'recipe': recipe,
        'is_detail_page': True,    
})
