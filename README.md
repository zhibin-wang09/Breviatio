# Breviatio

## Get Started
1. Create a virtual environment or Conda environment
2. Pip install requirement.txt
3. Navigate to project root directory
4. `fastapi run server/main.py`

ure
```
my-app/
├── backend/
│   ├── app/
│   │   ├── api/               # All API routes
│   │   │   ├── auth.py
│   │   │   ├── mail.py
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

## Architecture Design

### Modification Pre-req
1. Need to have PlantUML installed
2. Diagrams in `diagrams/` folder
3. Use PlantUML to render the diagrams and edit
Resources: [Plant UML Installation](https://plantuml.com/en-dark/starting)

### Design
[Component Diagram]()
[Use Case Diagram]()
