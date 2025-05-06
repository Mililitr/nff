from django.db import models
from django.core.validators import MinValueValidator


class Status(models.Model):
    """
    Модель для хранения статусов движения денежных средств.
    Примеры: Бизнес, Личное, Налог
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название статуса")
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Type(models.Model):
    """
    Модель для хранения типов движения денежных средств.
    Примеры: Пополнение, Списание
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Модель для хранения категорий движения денежных средств.
    Примеры: Инфраструктура, Маркетинг
    
    Категория связана с типом (например, категория "Маркетинг" относится к типу "Списание").
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories', verbose_name="Тип")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
        unique_together = ['name', 'type']  # Уникальность по имени и типу
    
    def __str__(self):
        return f"{self.name} ({self.type})"


class Subcategory(models.Model):
    """
    Модель для хранения подкатегорий движения денежных средств.
    Примеры: VPS, Proxy (для категории "Инфраструктура")
    
    Подкатегория связана с категорией.
    """
    name = models.CharField(max_length=100, verbose_name="Название подкатегории")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name="Категория")
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['name']
        unique_together = ['name', 'category']  # Уникальность по имени и категории
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"


class CashFlow(models.Model):
    """
    Модель для хранения записей о движении денежных средств.
    """
    date = models.DateField(verbose_name="Дата")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Сумма (руб.)")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания записи")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления записи")
    
    class Meta:
        verbose_name = "Движение денежных средств"
        verbose_name_plural = "Движение денежных средств"
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.date} - {self.type} - {self.category} - {self.amount} руб."
    
def clean(self):
    """
    Проверка логических зависимостей между сущностями:
    1. Подкатегория должна быть связана с выбранной категорией
    2. Категория должна быть связана с выбранным типом
    """
    from django.core.exceptions import ValidationError
    
    # Проверяем связь между подкатегорией и категорией
    if hasattr(self, 'subcategory_id') and self.subcategory_id is not None and \
       hasattr(self, 'category_id') and self.category_id is not None:
        subcategory = Subcategory.objects.get(pk=self.subcategory_id)
        if subcategory.category_id != self.category_id:
            raise ValidationError({
                'subcategory': f'Подкатегория "{subcategory}" не относится к категории "{self.category}"'
            })
    
    # Проверяем связь между категорией и типом
    if hasattr(self, 'category_id') and self.category_id is not None and \
       hasattr(self, 'type_id') and self.type_id is not None:
        category = Category.objects.get(pk=self.category_id)
        if category.type_id != self.type_id:
            raise ValidationError({
                'category': f'Категория "{category}" не относится к типу "{self.type}"'
            })