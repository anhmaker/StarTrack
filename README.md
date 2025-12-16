# NASA APOD PWA

Progressive Web App для просмотра NASA Astronomy Picture of the Day.

## Архитектура

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Frontend      │────▶│   Backend       │────▶│   MinIO         │
│   (Svelte PWA)  │     │   (Flask API)   │     │   (S3 Storage)  │
│   Port: 3000    │     │   Port: 5000    │     │   Port: 9000    │
│                 │     │                 │     │   Console: 9001 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌─────────────────┐
                        │                 │
                        │   NASA API      │
                        │                 │
                        └─────────────────┘
```

## Технологии

- **Frontend:** Svelte 4 + TypeScript + Vite
- **Backend:** Flask + Gunicorn + Flask-CORS
- **Storage:** MinIO (S3-compatible object storage)
- **PWA:** Service Worker + Web App Manifest
- **Container:** Docker + Docker Compose

## Быстрый старт

### 1. Получите NASA API ключ

Зарегистрируйтесь на [https://api.nasa.gov/](https://api.nasa.gov/) для получения бесплатного API ключа.

### 2. Настройте переменные окружения

Создайте файл `.env` в корне проекта:

```env
NASA_API_KEY=ваш_api_ключ
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=apod-cache
```

> **Примечание:** Можно использовать `DEMO_KEY` для тестирования, но он имеет лимит запросов.

### 3. Запустите приложение

```bash
docker-compose up --build
```

### 4. Откройте в браузере

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:5000/api/apod](http://localhost:5000/api/apod)
- **MinIO Console:** [http://localhost:9001](http://localhost:9001) (minioadmin/minioadmin)

## API Endpoints

### GET /api/apod

Получить Astronomy Picture of the Day.

**Query параметры:**
- `date` (опционально) - дата в формате YYYY-MM-DD (последние 30 дней)

**Примеры:**

```bash
# Сегодняшнее изображение
curl http://localhost:5000/api/apod

# Изображение за конкретную дату
curl http://localhost:5000/api/apod?date=2025-12-15
```

**Ответ:**

```json
{
  "date": "2025-12-16",
  "title": "...",
  "explanation": "...",
  "url": "/storage/image/2025-12-16",
  "hdurl": "/storage/image/2025-12-16/hd",
  "media_type": "image",
  "cached": true
}
```

### GET /storage/image/{date}

Получить кэшированное изображение.

### GET /storage/image/{date}/hd

Получить HD версию кэшированного изображения.

### GET /api/health

Проверка состояния сервиса.

## Функции

- ✅ Просмотр APOD за сегодня
- ✅ Навигация по датам (последние 30 дней)
- ✅ Кэширование изображений в MinIO
- ✅ Скачивание HD изображений
- ✅ PWA: оффлайн режим и установка
- ✅ Адаптивный космический дизайн
- ✅ Навигация с клавиатуры (← →)

## Структура проекта

```
StarTrack/
├── backend/
│   ├── app/
│   │   ├── __init__.py      # Flask app factory
│   │   ├── routes.py         # API endpoints
│   │   ├── apod_service.py   # NASA API + caching logic
│   │   └── storage/
│   │       ├── minio_client.py  # MinIO operations
│   │       └── minio_proxy.py   # Image proxy endpoints
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.svelte        # Main component
│   │   ├── main.ts           # Entry point + SW registration
│   │   ├── app.css           # Global styles
│   │   └── lib/
│   │       ├── types/apod.ts     # TypeScript types
│   │       ├── services/api.ts   # API client
│   │       └── stores/apod.ts    # Svelte stores
│   ├── public/
│   │   ├── manifest.json     # PWA manifest
│   │   └── sw.js             # Service Worker
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Разработка

### Локальный запуск без Docker

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt
export NASA_API_KEY=your_key
flask run
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

### Пересборка контейнеров

```bash
docker-compose down
docker-compose up --build
```

## Лицензия

MIT
