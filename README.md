# Stage 7 Lab - Project Tracker

A full-stack Project Tracker built as **one application contract** implemented with multiple frameworks:

- **Database:** PostgreSQL (Docker Compose)
- **Backends:** Django REST Framework and Flask, exposing an equivalent REST API
- **Frontends:** React and Angular, providing equivalent functionality

```
PostgreSQL
   ├── Django API ── React / Angular
   └── Flask API  ── React / Angular
```

Any frontend works with any backend. Switching backends only requires changing the configured API base URL.

## Repository structure

```
stage7-lab/
├── docker-compose.yml
├── .env.example
├── compare.sh
├── database/
│   └── schema.sql
├── django-api/
├── flask-api/
├── react-app/
├── angular-app/
└── README.md
```

## Requirements

| Tool | Version |
|---|---|
| Docker and Docker Compose | Recent version (`docker compose` command) |
| Python | 3.11 or higher |
| Node.js and npm | Node 20 or higher |
| Angular CLI | `npm install -g @angular/cli` |

## Default ports

| Component | Port |
|---|---|
| PostgreSQL | 5432 (configurable with `DB_PORT`) |
| Flask API | 5000 |
| Django API | 8000 |
| React (Vite) | 5173 |
| Angular | 4200 |

## 1. Environment variables

From the repository root:

```bash
cp .env.example .env
```

Edit `.env` if needed:

```env
DB_CONTAINER_NAME=project_tracker_db
DB_NAME=project_tracker
DB_USER=tracker
DB_PASSWORD=change_me
DB_HOST=localhost
DB_PORT=5432
```

The same `.env` is read by Docker Compose, the Django API, and the Flask API.

> If you already have a local PostgreSQL using port 5432, set `DB_PORT=5433`.

## 2. Database (PostgreSQL)

`database/schema.sql` is the single source of truth for the data structure. Neither Django nor Flask creates the `projects` and `tasks` tables; both adapt to them.

### Recommended: Docker Compose

From the repository root:

```bash
docker compose up -d
docker compose ps
```

The status must show `healthy`. PostgreSQL runs `schema.sql` automatically the first time the database volume is created.

Verify the tables:

```bash
docker compose exec db psql -U tracker -d project_tracker -c "\dt"
```

Use the values from your `.env` if you changed the user or database name.

Recreate the database from scratch (deletes all data):

```bash
docker compose down -v
docker compose up -d
```

Stop the database keeping the data:

```bash
docker compose stop
```

### Alternative: local PostgreSQL (no Docker)

```bash
psql -U postgres -c "CREATE DATABASE project_tracker;"
psql -U postgres -d project_tracker -f database/schema.sql
```

Make sure the values in `.env` match your local PostgreSQL user, password, host, and port.

### Database design decisions

- **Project deletion:** `tasks.project_id` uses `ON DELETE CASCADE`. Deleting a project also deletes all of its tasks.
- **Integrity:** the foreign key prevents tasks from referencing a nonexistent project, and `CHECK` constraints restrict `status` and `priority` to valid values.
- **Dates:** `created_at` uses `DEFAULT NOW()` and `updated_at` is maintained by a PostgreSQL trigger, so behavior is identical in both backends.

## 3. Flask API

```bash
cd flask-api
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The API is available at `http://localhost:5000/api`.

Flask models map to the existing tables and `db.create_all()` is never called.

## 4. Django API

```bash
cd django-api
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver 8000
```

The API is available at `http://localhost:8000/api`.

Do **not** run `migrate` or `makemigrations`: the models use `managed = False` and the tables are created only by `schema.sql`.

## 5. API contract summary

Both backends expose the same routes, formats, status codes, and error responses.

| Method | Route | Success |
|---|---|---|
| GET | `/api/projects` | 200 |
| POST | `/api/projects` | 201 |
| GET | `/api/projects/:id` | 200 |
| PUT | `/api/projects/:id` | 200 |
| DELETE | `/api/projects/:id` | 204 |
| GET | `/api/tasks` and `/api/tasks?project_id=<id>` | 200 |
| POST | `/api/tasks` | 201 |
| GET | `/api/tasks/:id` | 200 |
| PUT | `/api/tasks/:id` | 200 |
| DELETE | `/api/tasks/:id` | 204 |

Error format (identical in both APIs; `details` appears only in `validation_error`):

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid input data.",
    "details": { "title": ["This field is required."] }
  }
}
```

| HTTP | `code` | Cases |
|---|---|---|
| 400 | `validation_error` | Missing or invalid fields, invalid status or priority, nonexistent `project_id`, malformed JSON |
| 404 | `not_found` | Resource not found, non-numeric id, unknown route |
| 405 | `method_not_allowed` | Unsupported HTTP method |
| 500 | `database_error` / `server_error` | Database or unexpected server failure |

## 6. React frontend

```bash
cd react-app
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`.

## 7. Angular frontend

```bash
cd angular-app
npm install
ng serve
```

Open `http://localhost:4200`.

## 8. Switching between Django and Flask

The API base URL is configurable and is not hard-coded in the application logic.

| Frontend | Where to change it | Django | Flask |
|---|---|---|---|
| React | `react-app/.env` → `VITE_API_BASE_URL` | `http://localhost:8000/api` | `http://localhost:5000/api` |
| Angular | `angular-app/src/environments/environment.ts` → `apiBaseUrl` | `http://localhost:8000/api` | `http://localhost:5000/api` |

Restart the development server (`npm run dev` or `ng serve`) after changing the value.

## 9. Running the four combinations

1. Start the database (`docker compose up -d`).
2. Start **one** backend (Django or Flask).
3. Point the frontend to that backend and start it.

| Combination | Backend | Frontend |
|---|---|---|
| React → Django → PostgreSQL | port 8000 | `react-app` with `:8000` |
| Angular → Django → PostgreSQL | port 8000 | `angular-app` with `:8000` |
| React → Flask → PostgreSQL | port 5000 | `react-app` with `:5000` |
| Angular → Flask → PostgreSQL | port 5000 | `angular-app` with `:5000` |

All combinations share the same database, so data created in one is visible in the others.

## 10. Comparing Flask and Django responses (optional)

With both APIs running (Flask on 5000 and Django on 8000), from the repository root:

```bash
bash compare.sh
```

The script sends the same error cases to both APIs and prints `OK` when the status code and JSON body match, or `DIFF` with the differences.

## 11. Design decisions

- **Task filtering (USER-07):** done in the frontend. The API only filters tasks by `project_id`; filtering by status and priority happens on the already loaded tasks of the selected project.
- **Project deletion:** `ON DELETE CASCADE` (see the database section).
- **Validation:** performed in the API (Marshmallow in Flask, DRF serializers in Django) and enforced again by the database through `CHECK` constraints and foreign keys.
- **Error handling:** both APIs return the same JSON error format and never return `200 OK` for a failed operation. The frontends show validation and request errors and never present a failed operation as successful.
- **Routes:** no trailing slash (`/api/projects`, not `/api/projects/`).
- **CORS:** both APIs allow any origin in development.

## Troubleshooting

| Problem | Solution |
|---|---|
| `address already in use` on port 5432 | A local PostgreSQL is using it. Set `DB_PORT=5433` in `.env` and run `docker compose down` then `docker compose up -d` |
| APIs cannot connect to the database | Check `docker compose ps` shows `healthy` and that `DB_PORT` matches in `.env` |
| Changed `DB_USER`, `DB_PASSWORD`, or `DB_NAME` and it stopped working | Recreate the volume: `docker compose down -v` then `docker compose up -d` |
| Frontend still calls the old backend | Restart the dev server after changing the API URL |
| `Could not connect to the server` in the UI | The selected backend is not running or the URL/port is wrong |