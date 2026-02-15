Общая структура проекта:

financial_dashboard/
├── common_core/                  # Общие данные и логика
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                 # Общие модели данных
│   ├── services.py               # Общие сервисы и функции
│   ├── tasks.py                  # Общие асинхронные задачи
│   ├── tests.py
│   └── views.py
├── home_finance/                # Модуль "Домашнее хозяйство"
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                 # Специфичные модели
│   ├── services.py               # Дополнительные сервисы
│   ├── tasks.py                  # Специальные задачи
│   ├── tests.py
│   └── views.py
├── trading_investments/         # Модуль "Трейдинг и инвестиции"
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                 # Специфичные модели
│   ├── services.py               # Дополнительные сервисы
│   ├── tasks.py                  #Специальные задачи
│   ├── tests.py
│   └── views.py
├── consulting/                  # Модуль "Финансовое консультирование"
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                 # Специфичные модели
│   ├── services.py               # Дополнительные сервисы
│   ├── tasks.py                  # Специальные задачи
│   ├── tests.py
│   └── views.py
├── templates/                   # Общие шаблоны
│   ├── base.html
│   ├── error_pages/
│   ├── home_finance/
│   ├── trading_investments/
│   └── consulting/
├── static/                       # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
├── db.sqlite3                    # Базовая база данных
├── manage.py                     # Основной управляющий файл
└── settings.py                   # Настройки проекта

1. Модуль common_core

Здесь размещаются общие модели данных, которые используются всеми тремя приложениями:

- Пользователи: Аккаунты пользователей.
- Семейные профили: Информация о членах семьи.
- Категории расходов и доходов: Каталог категорий, используемый всеми модулями.
- Общие настройки: Глобальные настройки проекта.

Пример модели из common_core/models.py:

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Пользователь с дополнительными полями"""
    phone_number = models.CharField(max_length=15, blank=True)

class FamilyMember(models.Model):
    """Член семьи"""
    user = models.ForeignKey(CustomUser, related_name='family_members', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)

class Category(models.Model):
    """Категория расходов и доходов"""
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[
        ('INCOME', 'Доход'),
        ('EXPENSE', 'Расход')
    ])



🚀 Установка и настройка pre-commit

Чтобы включить автоматические проверки качества кода перед каждой фиксацией, выполните следующие шаги:

📌 Предварительные условия

- Установленный Python и virtualenv (или аналогичный инструмент управления окружением)
- Активированное виртуальное окружение для проекта

🔧 Установка pre-commit

Откройте терминал и перейдите в корень проекта:

cd path/to/your/project
Установите pre-commit:

pip install pre-commit
⭐️ Активация git hook'ов

Выполните команду для инициализации git-hook'ов:

pre-commit install
Эта команда установит специальные хуки, которые будут автоматически запускать проверки перед каждым коммитом.

✅ Проверка работоспособности

Проверьте, что всё настроено верно, попытавшись создать фиксацию:

git add .
git commit -m "Test commit with pre-commit"
Если установлены правильные конфигурации и проверки выполняются успешно, вы увидите вывод результатов проверок в консоли.

HouseKeeperHub - главная страница и единая точка входа в проект с приложениями.