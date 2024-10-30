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
3. Run the alembic migration to initialize a local sqlite db (or update to the latest version):
```sh
reflex db migrate
```
4. Run using 
```sh
poetry run reflex run
```
5. Your running app should be available at http://localhost:3000/home