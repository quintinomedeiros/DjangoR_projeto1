from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.db.models import Q
from .models import Recipe
from utils.pagination import make_pagination
import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))

def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html', context =
        {
            'recipes': page_obj,
            'pagination_range': pagination_range,
})

def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id'))

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context =
        {
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title': f' | Categoria | {recipes[0].category.name}', # Pesquisa para atribuir à variável title como string o nome da categoria para ser lança no título da página
})

def recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id, is_published=True)
    return render(request, 'recipes/pages/recipe-view.html', context = {
        'recipe': recipe,
        'is_detail_page': True,    
})

def search(request):
    search_term = request.GET.get('q', '').strip() # Recuperando o conteúdo informado na busca para testar se é vazio (q = input.name vazio). O .strip serve para apagar espaços vazios - pesquisa com espaços
    if not search_term: #Rederizando uma página de erro no caso do formulário ser submetido vázio
        raise Http404()
    
    # Realizando a consulta para retornar o conteúdo desejado, sendo que __icontains serve para encontrar registros que tenham o termo igrnorando maiúsculas e minúsculas
    recipes = Recipe.objects.filter(
        Q (
            Q(title__contains=search_term) | 
            Q(description__contains=search_term)
            ),
            is_published=True 
        ).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f' | Pesquisa por "{search_term}"',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })
