import os

import reflex as rx

config = rx.Config(
    app_name="f3_region_home",
    db_url=f"postgresql://{os.environ["DATABASE_USER"]}:{os.environ["DATABASE_PASSWORD"]}@{os.environ["DATABASE_HOST"]}:5432/{os.environ["DATABASE_SCHEMA"]}",
)
