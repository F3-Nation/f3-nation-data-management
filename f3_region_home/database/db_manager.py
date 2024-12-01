from typing import List
from typing import TypeVar as T

import reflex as rx
from sqlalchemy import select


def get_engine():
    return rx.session().get_bind()


class DbManager:
    def get(cls: T, id: int) -> T:
        with rx.session() as session:
            return session.scalars(select(cls).where(cls.id == id)).one()

    def create_records(records: List[T]) -> List[T]:
        with rx.session() as session:
            try:
                session.add_all(records)
                session.flush()
                session.expunge_all()
            finally:
                session.commit()
                return records  # noqa

    def find_records(cls: T, filters) -> List[T]:
        with rx.session() as session:
            try:
                records = session.scalars(select(cls).filter(*filters)).all()
                for r in records:
                    session.expunge(r)
                return records
            finally:
                session.rollback()

    def find_first_record(cls: T, filters) -> T:
        with rx.session() as session:
            try:
                record = session.scalars(select(cls).filter(*filters)).first()
                if record:
                    session.expunge(record)
                return record
            finally:
                session.rollback()
