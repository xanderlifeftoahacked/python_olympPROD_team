import asyncio
from datetime import datetime

from routing.routing import find_closest_agents
from schemas.meetings import LocationSchema
from schemas.routes import PointSchema, RouteSchema
from db.crud.routes import add_route, get_route, update_route_points


async def test():
    routes = [
        RouteSchema(agent_id=2, locations=[
            PointSchema(
                longitude=37.6208, latitude=55.7539, date_time=datetime(
                    year=2024, month=4, day=1, hour=12, minute=10), meeting_id=1),
            PointSchema(
                longitude=37.6183, latitude=55.7517, date_time=datetime(
                    year=2024, month=4, day=1, hour=16, minute=30), meeting_id=2)
        ]),
        RouteSchema(agent_id=3, locations=[
            PointSchema(
                longitude=37.6155, latitude=55.7558, date_time=datetime(
                    year=2024, month=4, day=1, hour=13, minute=45), meeting_id=3),
        ]),
    ]

    await find_closest_agents(routes, LocationSchema(
        name='Test', longitude=36.9163, latitude=56.0060), target_time=datetime(
        year=2024, month=4, day=1, hour=13, minute=45))

    await find_closest_agents(routes, LocationSchema(
        name='Test', longitude=36.9163, latitude=56.0060), target_time=datetime(
        year=2024, month=4, day=1, hour=13, minute=45))

    await add_route(route=RouteSchema(agent_id=1,
                                      locations=[
                                          PointSchema(
                                              longitude=37.6208, latitude=55.7539, date_time=datetime(
                                                  year=2024, month=4, day=1, hour=12, minute=10), meeting_id=1)]))
    route = await get_route(7)
    print(route)
    locs = route.locations
    locs.append(PointSchema(
        longitude=39.6208, latitude=56.7539, date_time=datetime(
            year=2024, month=4, day=2, hour=12, minute=10)))
    await update_route_points(7, locs)
    print(await get_route(7))
