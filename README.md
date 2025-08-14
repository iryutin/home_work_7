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


### 🚀 Запуск через Docker Compose

- **Требования**: установлен Docker Desktop и Docker Compose v2 (Windows/macOS/Linux).
- **Сервисы**: `web` (Django), `db` (PostgreSQL), `redis`, `celery`, `celery-beat`.

1) Создай файл `.env` в корне проекта (значения можно изменить под себя):

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Django DB settings (используются приложением)
NAME=lms_db
USER=lms_user
PASSWORD=lms_password
HOST=db
PORT=5432

# Postgres container env (используются контейнером db)
POSTGRES_DB=lms_db
POSTGRES_USER=lms_user
POSTGRES_PASSWORD=lms_password

# Email (опционально)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe (опционально)
STRIPE_SECRET_KEY=sk_test_your_key
```

2) Собери и запусти контейнеры:

```bash
# Запуск БД и Redis (по желанию отдельно)
docker compose up -d db redis

# Полный запуск (включая web, celery, celery-beat)
docker compose up --build web celery celery-beat
# либо фоном
# docker compose up --build -d
```

3) Применить миграции (если не применились автоматически в `web`):

```bash
docker compose exec web python manage.py migrate
```

4) Создать суперпользователя:

```bash
docker compose exec web python manage.py createsuperuser
```

5) Полезные URL:
- Админка: `http://localhost:8000/admin/`
- Swagger UI: `http://localhost:8000/swagger/`
- Redoc: `http://localhost:8000/redoc/`

6) Остановка и удаление контейнеров/томов:

```bash
# Остановить контейнеры
docker compose down
# Полностью очистить с томами
docker compose down -v
```
