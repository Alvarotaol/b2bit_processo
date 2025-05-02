# Mini Twitter 🐦

A minimalist social network to log work-related activities — think Twitter, but for developers.

## Tech Stack

- **Backend:** Django, Django REST Framework, Celery, Redis, PostgreSQL
- **Frontend:** React + TypeScript + Vite
- **CI:** GitHub Actions

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Alvarotaol/b2bit_processo.git
cd b2bit_processo
```

### 2. Environment variables

You’ll find a `.env.example` file inside the `backend/` folder. Just copy and rename it to `.env`, then adjust the values as needed:

```bash
cp backend/.env.example backend/.env
```

### 3. Start production environment

To spin up the production setup, you can use:

```bash
make prod
```

Or manually:

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## 🧪 Running Tests

With the containers running:

```bash
make test
```

```bash
docker-compose exec backend python manage.py test
```

## 📄 API Documentation
Just access:
http://localhost/swagger


## ✅ CI

Every push runs automated tests via **GitHub Actions**.
Workflow defined in: `.github/workflows/ci.yml`

## 📁 Project Structure

```
.
├── backend
│   ├── users, posts, etc.
│   ├── mini_twitter/
│   ├── Dockerfile / Dockerfile.prod
│   └── .env.example
├── frontend
│   ├── nginx/
│   ├── src/
│   └── Dockerfile / Dockerfile.prod
├── docker-compose.yml
├── docker-compose.prod.yml
└── .github/workflows/
```

## ✨ Features

- Upload, update and remove post images
- Edit posts with preview and image options
- Suggest users to follow
- Throttled login/signup with JWT authentication
- Background tasks via Celery + Redis

## 📝 License

[MIT](LICENSE)
