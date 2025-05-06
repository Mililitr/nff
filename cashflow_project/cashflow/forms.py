from django import forms
from django.utils import timezone
from .models import CashFlow, Status, Type, Category, Subcategory


class CashFlowForm(forms.ModelForm):
    """
    Форма для создания и редактирования записей о движении денежных средств.
    """
    date = forms.DateField(
        initial=timezone.now().date(),
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Дата"
    )
    
    class Meta:
        model = CashFlow
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
        }
    
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Если форма редактирования (есть instance)
    if self.instance.pk:
        # Фильтруем категории по выбранному типу
        if self.instance.type:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
        
        # Фильтруем подкатегории по выбранной категории
        if self.instance.category:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)
    else:
        # Для новой записи загружаем все категории и подкатегории
        # Это временное решение, JavaScript должен фильтровать их динамически
        self.fields['category'].queryset = Category.objects.all()
        self.fields['subcategory'].queryset = Subcategory.objects.all()
    
    # Добавляем классы Bootstrap для стилизации
    for field_name, field in self.fields.items():
        field.widget.attrs['class'] = 'form-control'

class StatusForm(forms.ModelForm):
    """
    Форма для создания и редактирования статусов.
    """
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class TypeForm(forms.ModelForm):
    """
    Форма для создания и редактирования ти��ов.
    """
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CategoryForm(forms.ModelForm):
    """
    Форма для создания и редактирования категорий.
    """
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }


class SubcategoryForm(forms.ModelForm):
    """
    Форма для создания и редактирования подкатегорий.
    """
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


class CashFlowFilterForm(forms.Form):
    """
    Форма для фильтрации записей о движении денежных средств.
    """
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Дата с"
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Дата по"
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Статус"
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тип"
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Категория"
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Подкатегория"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Если выбран тип, фильтруем категории
        if 'type' in self.data and self.data['type']:
            try:
                type_id = int(self.data['type'])
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        
        # Если выбрана категория, фильтруем подкатегории
        if 'category' in self.data and self.data['category']:
            try:
                category_id = int(self.data['category'])
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass