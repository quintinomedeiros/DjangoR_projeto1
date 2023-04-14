from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'), # Home
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'), # Página de Pesquisa
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'), # Categorias
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe'), # Receitas
    path('recipes/api/v1/', views.RecipeListViewHomeApi.as_view(), name='recipe_api_v1'), # Receitas API
    path('recipes/api/v1/<int:pk>', views.RecipeDetailViewApi.as_view(), name='recipe_api_v1_detail'), # Receitas API
]