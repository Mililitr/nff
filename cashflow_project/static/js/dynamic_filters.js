/**
 * Скрипт для динамической фильтрации категорий и подкатегорий
 * в зависимости от выбранного типа и категории.
 */

// Функция для обновления категорий при изменении типа
function updateCategories(typeSelectId, categorySelectId, apiUrl) {
    const typeSelect = document.getElementById(typeSelectId);
    const categorySelect = document.getElementById(categorySelectId);
    
    if (!typeSelect || !categorySelect) return;
    
    typeSelect.addEventListener('change', function() {
        const typeId = this.value;
        
        // Очищаем список категорий
        categorySelect.innerHTML = '<option value="">---------</option>';
        
        if (typeId) {
            // Загружаем категории для выбранного типа
            fetch(`${apiUrl}?type_id=${typeId}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category.id;
                        option.textContent = category.name;
                        categorySelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Ошибка при загрузке категорий:', error));
        }
        
        // Вызываем событие change для обновления подкатегорий
        const event = new Event('change');
        categorySelect.dispatchEvent(event);
    });
}

// Функция для обновления подкатегорий при изменении категории
function updateSubcategories(categorySelectId, subcategorySelectId, apiUrl) {
    const categorySelect = document.getElementById(categorySelectId);
    const subcategorySelect = document.getElementById(subcategorySelectId);
    
    if (!categorySelect || !subcategorySelect) return;
    
    categorySelect.addEventListener('change', function() {
        const categoryId = this.value;
        
        // Очищаем список подкатегорий
        subcategorySelect.innerHTML = '<option value="">---------</option>';
        
        if (categoryId) {
            // Загружаем подкатегории для выбранной катег��рии
            fetch(`${apiUrl}?category_id=${categoryId}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(subcategory => {
                        const option = document.createElement('option');
                        option.value = subcategory.id;
                        option.textContent = subcategory.name;
                        subcategorySelect.appendChild(option);
                    });
                })
                .catch(error => console.error('Ошибка при загрузке подкатегорий:', error));
        }
    });
}

// Инициализация фильтров на странице создания/редактирования записи
function initCashFlowFormFilters() {
    const typeSelectId = 'id_type';
    const categorySelectId = 'id_category';
    const subcategorySelectId = 'id_subcategory';
    
    updateCategories(typeSelectId, categorySelectId, '/api/get-categories/');
    updateSubcategories(categorySelectId, subcategorySelectId, '/api/get-subcategories/');
}

// Инициализация фильтров на странице списка записей
function initCashFlowListFilters() {
    const typeSelectId = 'id_type';
    const categorySelectId = 'id_category';
    const subcategorySelectId = 'id_subcategory';
    
    updateCategories(typeSelectId, categorySelectId, '/api/get-categories/');
    updateSubcategories(categorySelectId, subcategorySelectId, '/api/get-subcategories/');
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Определяем текущую страницу и инициализируем соответствующие фильтры
    if (document.getElementById('cashflow-form')) {
        initCashFlowFormFilters();
    } else if (document.getElementById('filter-form')) {
        initCashFlowListFilters();
    }
});