# Breviatio

## File Structure
```
my-app/
├── backend/
│   ├── app/
│   │   ├── api/               # All API routes
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── ...
│   │   ├── core/              # Configs, constants
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/            # DB models (SQLAlchemy, Pydantic, etc.)
│   │   │   ├── user.py
│   │   │   └── ...
│   │   ├── services/          # Business logic, integrations (e.g., Google API)
│   │   │   ├── google_oauth.py
│   │   │   └── user_service.py
│   │   ├── db/                # DB connection, session, CRUD utils
│   │   │   ├── session.py
│   │   │   └── user_crud.py
│   │   ├── schemas/           # Pydantic schemas for request/response models
│   │   │   ├── user.py
│   │   │   └── ...
│   │   ├── main.py            # Entry point (FastAPI/Flask app)
│   │   └── dependencies.py    # Common dependencies (e.g. get_current_user)
│
│   ├── requirements.txt
│   └── .env                   # Secrets, env vars
│
├── frontend/                  # React, Vue, etc.
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/          # API calls (fetch/axios)
│   │   ├── App.js
│   │   └── ...
│   ├── package.json
│   └── vite.config.js / next.config.js / ...
│
├── docker-compose.yml         # For local dev env
├── README.md
└── .gitignore
```