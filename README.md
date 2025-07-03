🎓 Django REST Framework Проект: LMS (Образовательная платформа)
Этот проект представляет собой API для образовательной платформы, где пользователи могут регистрироваться, проходить курсы и уроки, а также оплачивать обучение.
Проект реализован с использованием Django и Django REST Framework (DRF) с поддержкой JWT-авторизации, прав доступа и ограничений на основе ролей.

🔧 Основные функции
✅ Регистрация и авторизация через JWT
✅ CRUD для курсов и уроков
✅ Группа модераторов с ограниченными правами
✅ Платежи за курсы и уроки
✅ Разграничение прав:
Обычные пользователи видят только свои данные
Модераторы могут редактировать все курсы/уроки, но не могут удалять или создавать новые
✅ Кастомная модель пользователя
✅ Фикстуры и кастомные команды для загрузки данных
📁 Структура проекта
lms_project/
├── config/             # Настройки проекта (settings.py, urls.py, wsgi.py)
├── user/              # Пользователи, платежи, права доступа
│   ├── models.py       # Кастомный User, Payment
│   ├── serializers.py  # Сериализаторы для User, Payment
│   ├── views.py        # ViewSet и Generic для пользователей и платежей
│   ├── permissions.py  # Права доступа (IsModer, IsOwner)
│   └── urls.py
├── materials/          # Курсы и уроки
│   ├── models.py       # Course, Lesson
│   ├── serializers.py  # Сериализаторы с методами для количества уроков и связанного вывода
│   ├── views.py        # ViewSet и Generic классы с разграничением прав
│   └── urls.py
├── manage.py
├── requirements.txt    # Зависимости проекта
└── README.md           # Документация (этот файл)

🛠 Как запустить проект локально
Шаг 1: Клонируй репозиторий
git clone https://github.com/oksanafedorova07/Django-REST-Framework
cd lms_project

Шаг 2: Активируй виртуальное окружение и установи зависимости
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

poetry install
python manage.py migrate

Шаг 3: Запусти сервер
python manage.py runserver
Открой http://127.0.0.1:8000

🧪 Админка
Создай суперпользователя:

python manage.py createsuperuser
Перейди по адресу /admin и добавь пользователей в группу Moderators.
