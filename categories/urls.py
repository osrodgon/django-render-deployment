from django.urls import path
from .views import CategoriesView

urlpatterns = [
    path('', CategoriesView.categoriesList, name='category-list'),
    path('create', CategoriesView.categoriesCreate, name='category-create'),
    path('<int:pk>', CategoriesView.categoriesDetail, name='category-detail'),
]