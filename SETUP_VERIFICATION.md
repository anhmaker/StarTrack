# Проверка установки - Этап 1

Этот файл содержит инструкции для проверки успешной настройки окружения (Этап 1).

## ✅ Что было создано

### 1. Docker инфраструктура
- `docker-compose.yml` - Оркестрация всех сервисов
- `.env` - Конфигурация окружения
- `.gitignore` - Игнорируемые файлы

### 2. Backend
- `backend/Dockerfile` - Docker образ для Flask
- `backend/requirements.txt` - Python зависимости
- `backend/app.py` - Точка входа приложения
- `backend/app/` - Структура приложения

### 3. Frontend
- `frontend/Dockerfile` - Docker образ с Nginx
- `frontend/nginx.conf` - Конфигурация прокси
- `frontend/package.json` - Node.js зависимости
- `frontend/vite.config.ts` - Конфигурация сборщика
- `frontend/tsconfig.json` - TypeScript конфигурация
- `frontend/src/` - Исходники Svelte приложения

## 🚀 Пошаговая проверка

### Шаг 1: Проверка файлов конфигурации

```powershell
# Проверка наличия docker-compose.yml
Test-Path docker-compose.yml

# Проверка наличия .env
Test-Path .env

# Проверка backend файлов
Test-Path backend/Dockerfile
Test-Path backend/requirements.txt

# Проверка frontend файлов
Test-Path frontend/Dockerfile
Test-Path frontend/package.json
```

Все команды должны вернуть `True`.

### Шаг 2: Запуск Docker Compose

```powershell
# Запуск всех сервисов
docker-compose up --build
```

**Ожидаемый результат:**
- MinIO запускается и проходит healthcheck
- Backend собирается и запускается на порту 5000
- Frontend собирается и запускается на порту 3000

### Шаг 3: Проверка сервисов

Откройте новый терминал и выполните:

```powershell
# Проверка MinIO
curl http://localhost:9000/minio/health/live

# Проверка Backend
curl http://localhost:5000/health

# Проверка Frontend
curl http://localhost:3000
```

**Ожидаемые результаты:**

1. **MinIO:** Пустой ответ (200 OK)
2. **Backend:** `{"status":"ok"}`
3. **Frontend:** HTML страница с "NASA APOD Viewer"

### Шаг 4: Проверка MinIO Console

1. Откройте браузер: http://localhost:9001
2. Войдите с учетными данными:
   - Username: `minioadmin`
   - Password: `minioadmin`
3. Вы должны увидеть MinIO панель управления

### Шаг 5: Проверка Frontend в браузере

1. Откройте браузер: http://localhost:3000
2. Вы должны увидеть страницу с заголовком "NASA APOD Viewer"
3. Текст: "Приложение в разработке..."

### Шаг 6: Проверка Docker сети

```powershell
# Просмотр запущенных контейнеров
docker-compose ps

# Проверка сети
docker network inspect startrack_startrack-network
```

**Ожидаемый результат:**
Все три контейнера должны быть в статусе "Up":
- startrack-minio
- startrack-backend
- startrack-frontend

## 🔍 Диагностика проблем

### MinIO не запускается

```powershell
# Просмотр логов MinIO
docker-compose logs minio

# Остановка и очистка
docker-compose down -v
docker-compose up minio
```

### Backend не запускается

```powershell
# Просмотр логов Backend
docker-compose logs backend

# Проверка зависимостей Python
docker-compose run backend pip list
```

### Frontend не собирается

```powershell
# Просмотр логов Frontend
docker-compose logs frontend

# Пересборка только Frontend
docker-compose up --build frontend
```

### Порты заняты

```powershell
# Проверка занятых портов
netstat -ano | findstr :3000
netstat -ano | findstr :5000
netstat -ano | findstr :9000
netstat -ano | findstr :9001

# Если порты заняты, остановите конфликтующие процессы или измените порты в docker-compose.yml
```

## 📊 Структура директорий после установки

```
StarTrack/
├── .env                      ✅ Создан
├── .gitignore               ✅ Создан
├── docker-compose.yml       ✅ Создан
├── README.md                ✅ Создан
├── SETUP_VERIFICATION.md    ✅ Создан
├── backend/
│   ├── Dockerfile           ✅ Создан
│   ├── requirements.txt     ✅ Создан
│   ├── app.py              ✅ Создан
│   └── app/
│       ├── __init__.py     ✅ Создан
│       └── storage/        ✅ Создан
└── frontend/
    ├── Dockerfile          ✅ Создан
    ├── nginx.conf          ✅ Создан
    ├── package.json        ✅ Создан
    ├── vite.config.ts      ✅ Создан
    ├── tsconfig.json       ✅ Создан
    ├── index.html          ✅ Создан
    └── src/
        ├── main.ts         ✅ Создан
        ├── App.svelte      ✅ Создан
        ├── app.css         ✅ Создан
        └── lib/            ✅ Создан
```

## ✅ Критерии успеха Этапа 1

- [ ] Docker Compose запускается без ошибок
- [ ] MinIO доступен на портах 9000 и 9001
- [ ] Backend API отвечает на /health
- [ ] Frontend отображает базовую страницу
- [ ] Все контейнеры в одной сети
- [ ] MinIO Console доступен через браузер

## 🎯 Следующий этап

После успешной проверки всех пунктов переходите к **Этапу 2: MVP - Минимальная работающая версия**.

Этап 2 включает:
- Реализацию Flask API с endpoint `/api/apod`
- Создание NASA Service для запросов к NASA API
- Базовый Svelte UI для отображения изображений

---

**Статус:** Этап 1 завершен ✅
**Дата:** 2025-12-16

