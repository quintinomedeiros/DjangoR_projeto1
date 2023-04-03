from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'), # Home
    path('recipes/search/', views.search, name='search'), # Página de Pesquisa
    path('recipes/category/<int:category_id>/', views.category, name='category'), # Categorias
    path('recipes/<int:id>/', views.recipe, name='recipe'), # Receitas
]