from dataclasses import dataclass

import reflex as rx
from sqlalchemy import select

from .models import Event, EventTag, EventType, EventType_x_Org, Location, Org
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
class OrgSeries:
    org: Org
    series: list[EventExtended]


@dataclass
class RegionData:
    orgs: list[Org]
    org_series: list[OrgSeries]
    locations: list[Location]
    event_types: list[EventType]

    locations_select: list[tuple[str, int]]
    orgs_select: list[tuple[str, int]]
    event_types_select: list[tuple[str, int]]

    def __init__(self, region_id: int):
        with rx.session() as session:
            query = (
                select(Event, Org, Location, EventType, EventTag)
                .select_from(Event)
                .join(Org, Event.org_id == Org.id)
                .join(Location, Event.location_id == Location.id)
                .join(EventType, Event.event_type_id == EventType.id)
                .outerjoin(EventTag, Event.event_tag_id == EventTag.id)
                .filter(Org.parent_id == region_id, Event.is_active, Event.is_series)
                .order_by(Event.start_time)
            )
            all_series = [EventExtended(*row) for row in session.exec(query).all()]
            for series in all_series:
                series.start_time = series.event.start_time.strftime("%H%M")
                series.day_of_week = DAYS_OF_WEEK[series.event.day_of_week]
            self.orgs = [row[0] for row in session.exec(select(Org).where(Org.parent_id == region_id)).all()]
            self.orgs_select = [(org.name, org.id) for org in self.orgs]
            self.locations = [
                row[0]
                for row in session.exec(select(Location).where(Location.org_id == region_id, Location.is_active)).all()
            ]
            self.locations_select = [(location.name, location.id) for location in self.locations]
            self.event_types = [
                row[0]
                for row in session.exec(
                    select(EventType).join(EventType_x_Org).where(EventType_x_Org.org_id == region_id)
                ).all()
            ]
            self.event_types_select = [(event_type.name, event_type.id) for event_type in self.event_types]

        self.org_series = [
            OrgSeries(org, [series for series in all_series if series.org.id == org.id]) for org in self.orgs
        ]
