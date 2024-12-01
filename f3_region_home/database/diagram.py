import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from pydot import Dot
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

from f3_region_home.database.db_manager import get_engine
from f3_region_home.database.models import Base


def create_diagram():
    graph: Dot = create_schema_graph(
        engine=get_engine(),
        metadata=Base.metadata,
        show_datatypes=False,
        show_indexes=False,
        rankdir="LR",
        concentrate=False,
    )
    graph.write_png("f3_region_home/database/diagram.png")


if __name__ == "__main__":
    create_diagram()
