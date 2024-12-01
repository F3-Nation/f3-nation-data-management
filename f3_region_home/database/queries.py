from dataclasses import dataclass

import reflex as rx
from sqlalchemy import or_, select

from .models import Event, EventTag, EventType, EventType_x_Org, Location, Org, Role, Role_x_User_x_Org, User
from ..constants import DAYS_OF_WEEK


@dataclass
class EventExtended:
    event: Event
    org: Org
    location: Location
    event_type: EventType
    event_tag: EventTag
    start_time: str = None
    day_of_week: str = None


@dataclass
class LocationExtended(Location):
    lat_str: str = None
    lon_str: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lat_str = str(self.lat) if self.lat else None
        self.lon_str = str(self.lon) if self.lon else None


@dataclass
class OrgExtended(Org):
    default_location_id_str: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_location_id_str = str(self.default_location_id) if self.default_location_id else None


@dataclass
class OrgSeries:
    org: OrgExtended
    series: list[EventExtended]


@dataclass
class RegionData:
    orgs: list[OrgExtended]
    org_series: list[OrgSeries]
    locations: list[LocationExtended]
    event_types: list[EventType]
    admin_users: list[User]

    locations_select: list[tuple[str, str]]
    orgs_select: list[tuple[str, str]]
    event_types_select: list[tuple[str, str]]

    def __init__(self, region_id: int):
        with rx.session() as session:
            query = (
                select(Event, Org, Location, EventType, EventTag)
                .select_from(Event)
                .join(Org, Event.org_id == Org.id)
                .join(Location, Event.location_id == Location.id)
                .join(EventType, Event.event_type_id == EventType.id)
                .outerjoin(EventTag, Event.event_tag_id == EventTag.id)
                .filter(Org.parent_id == region_id, Event.is_active, Event.is_series, Org.is_active)
                .order_by(Event.start_time)
            )
            all_series = [EventExtended(*row) for row in session.exec(query).all()]
            for series in all_series:
                series.start_time = series.event.start_time.strftime("%H%M")
                series.day_of_week = DAYS_OF_WEEK[series.event.day_of_week - 1]
            self.orgs = [
                row[0] for row in session.exec(select(Org).where(Org.parent_id == region_id, Org.is_active)).all()
            ]
            self.orgs = [OrgExtended(**org.__dict__) for org in self.orgs]
            self.orgs_select = [(org.name, str(org.id)) for org in self.orgs]
            self.locations = [
                row[0]
                for row in session.exec(select(Location).where(Location.org_id == region_id, Location.is_active)).all()
            ]
            self.locations = [LocationExtended(**location.__dict__) for location in self.locations]
            self.locations_select = [(location.name, str(location.id)) for location in self.locations]
            self.event_types = [
                row[0]
                for row in session.exec(
                    select(EventType).join(EventType_x_Org).where(EventType_x_Org.org_id == region_id)
                ).all()
            ]
            self.event_types_select = [(event_type.name, str(event_type.id)) for event_type in self.event_types]
            self.admin_users = [
                row[0]
                for row in session.exec(
                    select(User)
                    .join(Role_x_User_x_Org)
                    .where(Role_x_User_x_Org.org_id == region_id, Role_x_User_x_Org.role_id == 1)
                ).all()
            ]

        self.org_series = [
            OrgSeries(org, [series for series in all_series if series.org.id == org.id]) for org in self.orgs
        ]


def get_user_roles(user_id: int, region_id: int) -> list[str]:
    with rx.session() as session:
        query = (
            select(Role)
            .join(Role_x_User_x_Org)
            .where(Role_x_User_x_Org.user_id == user_id, Role_x_User_x_Org.org_id == region_id)
        )
        return [row[0].name for row in session.exec(query).all()]


def user_search(search_str: str, region: Org = None, limit: int = None) -> list[User]:
    with rx.session() as session:
        query = select(User).where(
            or_(
                User.f3_name.contains(search_str),
                User.email.contains(search_str),
                User.home_region_id == region.id if region else True,
            )
        )

        users = [row[0] for row in session.exec(query).all()]
        scored_users = []

        for user in users:
            score = 0
            if search_str in user.f3_name:
                score += 4
            if region and user.home_region_id == region.id:
                score += 3
            if search_str in user.email:
                score += 2
            scored_users.append((user, score))

        scored_users.sort(key=lambda x: x[1], reverse=True)
        top_users = [user for user, score in scored_users[:limit]]

    return top_users
