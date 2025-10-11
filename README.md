# Breviatio

## Get Started
1. Create a virtual environment or Conda environment
2. Pip install requirement.txt
3. Set up environment variables
4. Download `credentials.json` from Google Cloud Console
3. Navigate to project root directory
4. `fastapi run server/main.py`

## ENV variables
```
export DB_CONNECTION_STRING=
```
Store `.env` file at folder root and run `source .env`

## System Components
1. Set up Redis using docker [redis-py guideline](https://github.com/redis/redis-py)
2. Set up PostgreSQL with database name `Brevatio`

## Architecture Design

### Modification Pre-req
1. Need to have PlantUML installed
2. Diagrams in `diagrams/` folder
3. Use PlantUML to render the diagrams and edit
Resources: [Plant UML Installation](https://plantuml.com/en-dark/starting)

### Design
[Component Diagram]()
[Use Case Diagram]()
