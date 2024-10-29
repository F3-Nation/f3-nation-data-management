# F3 Nation Data Management UI

This is a proof of concept project to create an admin app to manage F3 regions' data. This will include locations, AOs, schedules, backblasts, etc. It is written in [Reflex](https://reflex.dev/), a Python framework for building modern web apps.

# Installation

1. Clone the repo:
```sh
git clone https://github.com/F3-Nation/f3-nation-data-management.git
```
2. Use Poetry to install dependencies:
```sh
poetry install
```
3. Modify `rxconfig.py` to point to a local db. I pass in environment variables through a `.env` file (see `.env.example`)
4. TODO: add steps for initializing database (should just be some alembic commands)
5. Run using 
```sh
source .env && poetry run reflex run
```
6. Your running app should be available at http://localhost:3000