from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Sum

from .models import CashFlow, Status, Type, Category, Subcategory
from .forms import (
    CashFlowForm, StatusForm, TypeForm, CategoryForm, 
    SubcategoryForm, CashFlowFilterForm
)


class CashFlowListView(ListView):
    """
    Представление для отображения списка записей о движении денежных средств
    с возможностью фильтрации.
    """
    model = CashFlow
    template_name = 'cashflow/cashflow_list.html'
    context_object_name = 'cashflows'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Получаем параметры фильтрации из GET-запроса
        self.filter_form = CashFlowFilterForm(self.request.GET)
        
        if self.filter_form.is_valid():
            data = self.filter_form.cleaned_data
            
            # Фильтрация по дате
            if data.get('date_from'):
                queryset = queryset.filter(date__gte=data['date_from'])
            if data.get('date_to'):
                queryset = queryset.filter(date__lte=data['date_to'])
            
            # Фильтрация по статусу
            if data.get('status'):
                queryset = queryset.filter(status=data['status'])
            
            # Фильтрация по типу
            if data.get('type'):
                queryset = queryset.filter(type=data['type'])
            
            # Фильтрация по категории
            if data.get('category'):
                queryset = queryset.filter(category=data['category'])
            
            # Фильтрация по подкатегории
            if data.get('subcategory'):
                queryset = queryset.filter(subcategory=data['subcategory'])
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        
        # Добавляем суммарную статистику
        queryset = self.get_queryset()
        income_sum = queryset.filter(type__name='Пополнение').aggregate(Sum('amount'))['amount__sum'] or 0
        expense_sum = queryset.filter(type__name='Списание').aggregate(Sum('amount'))['amount__sum'] or 0
        
        context['income_sum'] = income_sum
        context['expense_sum'] = expense_sum
        context['balance'] = income_sum - expense_sum
        
        return context


class CashFlowCreateView(CreateView):
    """
    Представление для создания новой записи о движении денежных средств.
    """
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно создана.')
        return super().form_valid(form)


class CashFlowUpdateView(UpdateView):
    """
    Представление для редактирования записи о движении денежных средств.
    """
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена.')
        return super().form_valid(form)


class CashFlowDeleteView(DeleteView):
    """
    Представление для удаления записи о движении денежных средств.
    """
    model = CashFlow
    template_name = 'cashflow/cashflow_confirm_delete.html'
    success_url = reverse_lazy('cashflow_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return super().delete(request, *args, **kwargs)


# Представления для управления справочниками

class StatusListView(ListView):
    model = Status
    template_name = 'cashflow/dictionaries/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'cashflow/dictionaries/status_form.html'
    success_url = reverse_lazy('status_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан.')
        return super().form_valid(form)


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'cashflow/dictionaries/status_form.html'
    success_url = reverse_lazy('status_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен.')
        return super().form_valid(form)


class StatusDeleteView(DeleteView):
    model = Status
    template_name = 'cashflow/dictionaries/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Статус успешно удален.')
        return super().delete(request, *args, **kwargs)


class TypeListView(ListView):
    model = Type
    template_name = 'cashflow/dictionaries/type_list.html'
    context_object_name = 'types'


class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm
    template_name = 'cashflow/dictionaries/type_form.html'
    success_url = reverse_lazy('type_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Тип успешно создан.')
        return super().form_valid(form)


class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm
    template_name = 'cashflow/dictionaries/type_form.html'
    success_url = reverse_lazy('type_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Тип успешно обновлен.')
        return super().form_valid(form)


class TypeDeleteView(DeleteView):
    model = Type
    template_name = 'cashflow/dictionaries/type_confirm_delete.html'
    success_url = reverse_lazy('type_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Тип успешно удален.')
        return super().delete(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'cashflow/dictionaries/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cashflow/dictionaries/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана.')
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'cashflow/dictionaries/category_form.html'
    success_url = reverse_lazy('category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена.')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'cashflow/dictionaries/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Категория успешно удалена.')
        return super().delete(request, *args, **kwargs)


class SubcategoryListView(ListView):
    model = Subcategory
    template_name = 'cashflow/dictionaries/subcategory_list.html'
    context_object_name = 'subcategories'


class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cashflow/dictionaries/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно создана.')
        return super().form_valid(form)


class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = 'cashflow/dictionaries/subcategory_form.html'
    success_url = reverse_lazy('subcategory_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Подкатег��рия успешно обновлена.')
        return super().form_valid(form)


class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    template_name = 'cashflow/dictionaries/subcategory_confirm_delete.html'
    success_url = reverse_lazy('subcategory_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Подкатегория успешно удалена.')
        return super().delete(request, *args, **kwargs)


# API для динамической фильтрации категорий и подкатегорий

def get_categories_by_type(request):
    """
    API-метод для получения категорий по выбранному типу.
    """
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(type_id=type_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)


def get_subcategories_by_category(request):
    """
    API-метод для получения подкатегорий по выбранной категории.
    """
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)


# Страница управления справочниками
def dictionaries_view(request):
    """
    Представление для страницы управления справочниками.
    """
    return render(request, 'cashflow/dictionaries/dictionaries.html')