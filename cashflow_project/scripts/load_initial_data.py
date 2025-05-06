#!/usr/bin/env python
"""
Скрипт для загрузки начальных данных в базу данных.
Запускать из корневой директории проекта:
python scripts/load_initial_data.py
"""

import os
import sys
import django

# Добавляем директорию проекта в путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cashflow_project.settings')
django.setup()

# Импортируем модели после настройки Django
from cashflow.models import Status, Type, Category, Subcategory
from django.db import transaction


def create_statuses():
    """Создание статусов"""
    statuses = [
        {"name": "Бизнес"},
        {"name": "Личное"},
        {"name": "Налог"}
    ]
    
    for status_data in statuses:
        Status.objects.get_or_create(name=status_data["name"])
    
    print(f"Создано статусов: {len(statuses)}")


def create_types():
    """Создание типов"""
    types = [
        {"name": "Пополнение"},
        {"name": "Списание"}
    ]
    
    for type_data in types:
        Type.objects.get_or_create(name=type_data["name"])
    
    print(f"Создано типов: {len(types)}")


def create_categories():
    """Создание категорий"""
    # Получаем типы
    income_type = Type.objects.get(name="Пополнение")
    expense_type = Type.objects.get(name="Списание")
    
    categories = [
        {"name": "Зарплата", "type": income_type},
        {"name": "Инвестиции", "type": income_type},
        {"name": "Инфраструктура", "type": expense_type},
        {"name": "Маркетинг", "type": expense_type},
        {"name": "Налоги", "type": expense_type}
    ]
    
    for category_data in categories:
        Category.objects.get_or_create(
            name=category_data["name"],
            type=category_data["type"]
        )
    
    print(f"Создано категорий: {len(categories)}")


def create_subcategories():
    """Создание подкатегорий"""
    # Получаем категории
    salary_category = Category.objects.get(name="Зарплата")
    investments_category = Category.objects.get(name="Инвестиции")
    infrastructure_category = Category.objects.get(name="Инфраструктура")
    marketing_category = Category.objects.get(name="Маркетинг")
    taxes_category = Category.objects.get(name="Налоги")
    
    subcategories = [
        {"name": "Основная работа", "category": salary_category},
        {"name": "Фриланс", "category": salary_category},
        {"name": "Дивиденды", "category": investments_category},
        {"name": "VPS", "category": infrastructure_category},
        {"name": "Proxy", "category": infrastructure_category},
        {"name": "Реклама", "category": marketing_category},
        {"name": "НДФЛ", "category": taxes_category},
        {"name": "НДС", "category": taxes_category}
    ]
    
    for subcategory_data in subcategories:
        Subcategory.objects.get_or_create(
            name=subcategory_data["name"],
            category=subcategory_data["category"]
        )
    
    print(f"Создано подкатегорий: {len(subcategories)}")


@transaction.atomic
def load_all_data():
    """Загрузка всех начальных данных"""
    print("Начало загрузки начальных данных...")
    
    create_statuses()
    create_types()
    create_categories()
    create_subcategories()
    
    print("Загрузка начальных данных завершена успешно!")


if __name__ == "__main__":
    load_all_data()