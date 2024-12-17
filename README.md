# Currency Exchange API

## Описание

Currency Exchange API предоставляет функционал для регистрации и аутентификации пользователей, а также конвертацию валют и получение списка валют через внешнее API.

## Установка и настройка

### Требования

- Python 3.8 или выше
- `pip`

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/currency-exchange.git
   cd currency_exchange```
2. Создайте виртуальное окружение:
```bash
	python -m venv venv
```
3. Активируйте виртуальное окружение:
-   На Windows:
```bash
	venv\Scripts\activate
```
- На macOS и Linux:
```bash
	source venv/bin/activate
```
4. Установите зависимости:
```bash
	pip install -r requirements.txt
```

### Настройка

1. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:
```env
	SECRET_KEY=your_secret_key
	ALGORITHM=HS256
	ACCESS_TOKEN_EXPIRE_MINUTES=30
	PAYLOAD={}
	HEADERS={"apikey": your_api_key}
```
2. Настройте `settings.py` для использования переменных окружения:
```python
	model_config  =  SettingsConfigDict(env_file=path_to_env)
```

## Запуск

1. Запустите сервер:
```bash
	uvicorn currency_exchange.main:api_v1_app --reload
```
2. Откройте в браузере http://127.0.0.1:8000/docs, чтобы просмотреть автоматически сгенерированную документацию API.

## Примеры запросов API и ответов

### Регистрация пользователя

**Запрос:**

```http
	POST /register/
	Content-Type: application/json

	{
	  "username": "newuser",
	  "password": "@gOOd123@"
	}
```

**Ответ:**

```http
	200 OK
	{
	  "message": "Welcome to the club, newuser"
	}
```

### Аутентификация пользователя

**Запрос:**

```http
	POST /login/
	Content-Type: application/x-www-form-urlencoded

	username=newuser&password=@gOOd123@

```

**Ответ:**

```http
	200 OK
	{
	  "access_token": "your_jwt_token",
	  "token_type": "bearer"
	}
```

### Получение списка валют

**Запрос:**

```http
	GET /list/
	Authorization: Bearer your_jwt_token
```

**Ответ:**

```http
	200 OK
	{
	  "currencies": {
	    "USD": "United States Dollar",
	    "EUR": "Euro",
	    ...
	  }
	}
```

### Конвертация валют

**Запрос:**

```http
	POST /exchange/
	Content-Type: application/json
	Authorization: Bearer your_jwt_token

	{
	  "from_currency": "USD",
	  "to_currency": "EUR",
	  "amount": 100
	}
```

**Ответ:**
```bash
	200 OK
	{
	  "total": 85.00
	}
```

## Используемые фичи

-   **Регистрация и аутентификация пользователей**: Использование JWT токенов для обеспечения безопасности.
-   **Валидация паролей**: Проверка паролей на соответствие заданным требованиям.
-   **Запросы к внешнему API**: Использование `aiohttp` для асинхронных запросов к внешнему API валют.
-   **Логгирование**: Ведение логов для отслеживания выполнения и ошибок.
-   **SQLite**: Использование SQLite в качестве базы данных для хранения информации о пользователях.