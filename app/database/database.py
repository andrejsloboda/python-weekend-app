from typing import List
from datetime import date, timedelta 
from slugify import slugify
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.types import Date
from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy.sql.expression import cast
from ..schemas import Route, RouteCombination 
from ..settings import settings 
from ..database.models import RouteORM, Base


DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@\
{settings.db_hostname}:{settings.db_port}/{settings.db_database}"

engine = create_engine(DATABASE_URL, echo=True, poolclass=NullPool)
Base.metadata.create_all(engine)
Session = sessionmaker(engine, autocommit=False, autoflush=False)


def add_routes_to_db(routes: List[Route]) -> None:
    if routes:
        with Session() as session:
            for route in routes:
                session.add(RouteORM(**dict(route)))
            session.commit()


def get_routes_from_db(origin: str, destination: str, departure_date: date) -> List[RouteORM]:
    with Session() as session:
        routes = session.query(RouteORM).filter(
            RouteORM.origin == slugify(origin),
            RouteORM.destination == slugify(destination),
            cast(RouteORM.departure, Date) == departure_date
        ).all()
    return routes


def is_in_db(origin: str, destination: str, departure_date: date) -> bool:
    with Session() as session:
        if session.query(RouteORM).filter(
            RouteORM.origin == slugify(origin),
            RouteORM.destination == slugify(destination),
            cast(RouteORM.departure, Date) == departure_date
        ).all():
            return True
        else:
            return False


def get_combinations_from_db(origin: str, destination: str, departure_date: date) -> List[RouteCombination]:
    seg1 = aliased(RouteORM, name="segment1")
    seg2 = aliased(RouteORM, name="segment2")
    with Session() as session:
        result = session.query(
            seg1, seg2
        ).join(
            seg2, 
            seg1.destination == seg2.origin
        ).filter(
            seg1.origin == slugify(origin),
            seg2.destination == slugify(destination),
            seg2.departure - seg1.arrival > timedelta(hours=1),
            seg2.departure - seg1.arrival < timedelta(hours=6),
            cast(seg1.departure, Date) == departure_date
        ).all()
        
    return [RouteCombination(routes=[seg1, seg2]) for seg1, seg2 in result]
