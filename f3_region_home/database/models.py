from datetime import date, datetime, time, timedelta
from typing import Any, Optional

import reflex as rx
from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    UniqueConstraint,
    func,
    null,
    select,
)

# from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declared_attr
from sqlmodel import Field


class TimestampMixin:
    @declared_attr
    def created(cls):
        return Field(
            default=None,
            sa_column=Column(
                "created",
                DateTime(timezone=True),
                server_default=func.timezone("utc", func.now()),
            ),
        )

    @declared_attr
    def updated(cls):
        return Field(
            default=None,
            sa_column=Column(
                "updated",
                DateTime(timezone=True),
                server_default=func.timezone("utc", func.now()),
                onupdate=func.timezone("utc", func.now()),
            ),
        )


class GetDBClass:
    def get_id(self):
        return self.id

    def get(self, attr):
        if attr in [c.key for c in self.__table__.columns]:
            return getattr(self, attr)
        return None

    def to_json(self):
        return {c.key: self.get(c.key) for c in self.__table__.columns if c.key not in ["created", "updated"]}

    def __repr__(self):
        return str(self.to_json())

    def _update(self, fields):
        for k, v in fields.items():
            attr_name = str(k).split(".")[-1]
            setattr(self, attr_name, v)
        return self


class SlackSpace(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "slack_spaces"

    team_id: str = Field(primary_key=True)
    workspace_name: str | None = None
    bot_token: str | None = None
    settings: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))

    def get_id():
        return SlackSpace.team_id


class Org_x_Slack(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "orgs_x_slack"

    org_id: int = Field(foreign_key="orgs.id")
    slack_id: str


class Event(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "events"

    org_id: int | None = Field(default=None, foreign_key="orgs.id")
    location_id: int | None = Field(default=None, foreign_key="locations.id")
    event_type_id: int | None = Field(default=None, foreign_key="event_types.id")
    event_tag_id: int | None = Field(default=None, foreign_key="event_tags.id")
    series_id: int | None = Field(default=None, foreign_key="events.id")
    is_series: bool
    is_active: bool
    highlight: bool
    start_date: date
    end_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    day_of_week: int | None = None
    name: str
    description: str | None = None
    recurrence_pattern: str | None = None
    recurrence_interval: int | None = None
    index_within_interval: int | None = None
    pax_count: int | None = None
    fng_count: int | None = None
    preblast: str | None = None
    backblast: str | None = None
    preblast_rich: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))
    backblast_rich: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))
    preblast_ts: datetime | None = None
    backblast_ts: datetime | None = None
    meta: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))

    def get_week(region_id: int, start_date: datetime):
        start_date = start_date.date()
        with rx.session() as session:
            events = session.exec(
                Event.select()
                .where(
                    # Event.org_id == region_id,
                    Event.is_active,
                    Event.start_date >= start_date,
                    Event.start_date <= start_date + timedelta(7),
                )
                .order_by(Event.start_date)
            ).all()
        return events


class EventType(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "event_types"

    name: str
    category_id: int = Field(foreign_key="event_categories.id")
    description: str | None = Field(default=None, max_length=10000)
    acronym: str | None = None


class EventCategory(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "event_categories"

    name: str
    description: str | None = Field(default=None, max_length=10000)


class Location(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "locations"

    org_id: Optional[int] = Field(default=None, foreign_key="orgs.id")
    name: str
    description: Optional[str] = None
    is_active: bool
    lat: Optional[float] = None
    lon: Optional[float] = None
    address_street: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zip: Optional[str] = None
    meta: Optional[dict[str, Any]] = Field(default_factory=null, sa_column=Column(JSON, nullable=True))

    def get_all(region_id: int):
        with rx.session() as session:
            locations = session.exec(Location.select().where(Location.org_id == region_id, Location.is_active)).all()
        return locations

    def add(region_id: int, fields: dict[str, Any]):
        with rx.session() as session:
            location = Location(org_id=region_id, **fields, is_active=True)
            session.add(location)
            session.commit()
        return location

    def update(location_id: int, fields: dict[str, Any]):
        with rx.session() as session:
            location = session.get(Location, location_id)
            location._update(fields)
            session.commit()
        return location

    def deactivate(location_id: int):
        with rx.session() as session:
            location = session.get(Location, location_id)
            location.is_active = False
            session.commit()
        return location


class User(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "users"

    f3_name: str
    email: str = Field(unique=True)
    home_region_id: int | None = Field(default=None, foreign_key="orgs.id")
    avatar_url: str | None = None
    password: str | None = None
    meta: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))


class SlackUser(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "slack_users"
    slack_id: str
    user_name: str
    email: str
    is_admin: bool
    is_owner: bool
    is_bot: bool
    user_id: int = Field(foreign_key="users.id")
    avatar_url: str | None = None
    slack_team_id: str
    strava_access_token: str | None = None
    strava_refresh_token: str | None = None
    strava_expires_at: datetime | None = None
    strava_athlete_id: int | None = None
    meta: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))
    slack_updated: datetime | None = None


class Attendance(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "attendance"
    event_id: int = Field(foreign_key="events.id")
    user_id: int | None = Field(default=None, foreign_key="users.id")
    attendance_type_id: int = Field(foreign_key="attendance_types.id")
    is_planned: bool
    meta: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))

    __table_args__ = (UniqueConstraint("event_id", "user_id", "attendance_type_id", "is_planned", name="event_user"),)


class AttendanceType(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "attendance_types"

    type: str
    description: str | None = Field(default=None, max_length=10000)


class Org(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "orgs"

    parent_id: int | None = Field(default=None, foreign_key="orgs.id")
    org_type_id: int = Field(foreign_key="org_types.id")
    default_location_id: int | None = None
    name: str
    description: str | None = Field(default=None, max_length=10000)
    is_active: bool
    logo: bytes | None = None
    website: str | None = None
    email: str | None = None
    twitter: str | None = None
    facebook: str | None = None
    instagram: str | None = None
    last_annual_review: date | None = None
    meta: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))

    def get_all_regions() -> list[tuple[str, str]]:
        with rx.session() as session:
            query = select(Org.name, Org.id).where(Org.org_type_id == 2, Org.is_active)
            regions = session.exec(query).all()
        return [(r.name, str(r.id)) for r in regions]

    def get_series(region_id: int) -> dict[int, list[Event]]:
        with rx.session() as session:
            query = select(Event).where(Event.org_id == region_id, Event.is_series, Event.is_active)
            series = session.exec(query).all()
        return {s.id: s for s in series}

    def add_ao(region_id: int, fields: dict[str, Any]):
        with rx.session() as session:
            org = Org(parent_id=region_id, **fields, is_active=True, org_type_id=1)
            session.add(org)
            session.commit()
        return org

    def update(org_id: int, fields: dict[str, Any]):
        with rx.session() as session:
            org = session.get(Org, org_id)
            org._update(fields)
            session.commit()
        return org

    def deactivate(org_id: int):
        with rx.session() as session:
            org = session.get(Org, org_id)
            org.is_active = False
            session.commit()
        return org


class OrgType(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "org_types"

    name: str


class EventType_x_Org(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "event_types_x_org"

    event_type_id: int = Field(foreign_key="event_types.id")
    org_id: int = Field(foreign_key="orgs.id")
    is_default: bool


class EventTag(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "event_tags"

    name: str
    description: str | None = Field(default=None, max_length=10000)
    color: str | None = None


class EventTag_x_Org(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "event_tags_x_org"

    event_tag_id: int = Field(foreign_key="event_tags.id")
    org_id: int = Field(foreign_key="orgs.id")
    color_override: str | None = None


class Role(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "roles"

    name: str
    description: str | None = Field(default=None, max_length=10000)


class Permission(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "permissions"

    name: str
    description: str | None = Field(default=None, max_length=10000)


class Role_x_Permission(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "roles_x_permissions"

    role_id: int = Field(foreign_key="roles.id")
    permission_id: int = Field(foreign_key="permissions.id")


class Role_x_User_x_Org(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "roles_x_users_x_orgs"
    __table_args__ = (UniqueConstraint("role_id", "user_id", "org_id", name="_role_user_org_uc"),)

    role_id: int = Field(foreign_key="roles.id")
    user_id: int = Field(foreign_key="users.id")
    org_id: int = Field(foreign_key="orgs.id")


class Achievement(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "achievements"

    name: str
    description: str | None = Field(default=None, max_length=10000)
    verb: str
    image_url: str | None = None


class Achievement_x_User(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "achievements_x_users"

    achievement_id: int = Field(foreign_key="achievements.id")
    user_id: int = Field(foreign_key="users.id")
    date_awarded: date


class Achievement_x_Org(TimestampMixin, GetDBClass, rx.Model, table=True):
    __tablename__ = "achievements_x_orgs"

    achievement_id: int = Field(foreign_key="achievements.id")
    org_id: int = Field(foreign_key="orgs.id")
