from django.urls import path
from . import views

urlpatterns = [
    # Маршруты для записей о движении денежных средств
    path('', views.CashFlowListView.as_view(), name='cashflow_list'),
    path('cashflow/add/', views.CashFlowCreateView.as_view(), name='cashflow_create'),
    path('cashflow/<int:pk>/edit/', views.CashFlowUpdateView.as_view(), name='cashflow_update'),
    path('cashflow/<int:pk>/delete/', views.CashFlowDeleteView.as_view(), name='cashflow_delete'),
    
    # Маршруты для справочников
    path('dictionaries/', views.dictionaries_view, name='dictionaries'),
    
    # Маршруты для статусов
    path('dictionaries/statuses/', views.StatusListView.as_view(), name='status_list'),
    path('dictionaries/statuses/add/', views.StatusCreateView.as_view(), name='status_create'),
    path('dictionaries/statuses/<int:pk>/edit/', views.StatusUpdateView.as_view(), name='status_update'),
    path('dictionaries/statuses/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),
    
    # Маршруты для типов
    path('dictionaries/types/', views.TypeListView.as_view(), name='type_list'),
    path('dictionaries/types/add/', views.TypeCreateView.as_view(), name='type_create'),
    path('dictionaries/types/<int:pk>/edit/', views.TypeUpdateView.as_view(), name='type_update'),
    path('dictionaries/types/<int:pk>/delete/', views.TypeDeleteView.as_view(), name='type_delete'),
    
    # Маршруты для категорий
    path('dictionaries/categories/', views.CategoryListView.as_view(), name='category_list'),
    path('dictionaries/categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('dictionaries/categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('dictionaries/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # Маршруты для подкатегорий
    path('dictionaries/subcategories/', views.SubcategoryListView.as_view(), name='subcategory_list'),
    path('dictionaries/subcategories/add/', views.SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('dictionaries/subcategories/<int:pk>/edit/', views.SubcategoryUpdateView.as_view(), name='subcategory_update'),
    path('dictionaries/subcategories/<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
    
    # API для динамической фильтрации
    path('api/get-categories/', views.get_categories_by_type, name='get_categories_by_type'),
    path('api/get-subcategories/', views.get_subcategories_by_category, name='get_subcategories_by_category'),
]