import asyncio
from datetime import datetime, timedelta
from typing import Tuple

# from config import external_api_config
from routing.client import client
from schemas.meetings import LocationSchema
from schemas.routes import PointSchema, RouteSchema

graphhopper_url = 'https://graphhopper.com/api/1/'


def generate_graphhopper_url(points: list[Tuple[float, float]]) -> str:
    graph_points = '&point='.join([','.join([str(point[1]), str(point[0])])
                                   for point in points])
    key = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
    return f'{graphhopper_url}route?point={graph_points}&vehicle=car&key={key}'


async def get_route_time(point_a: Tuple[float, float], point_b: Tuple[float, float],
                         point_c: Tuple[float, float]):
    response = await client.get(generate_graphhopper_url([point_a, point_b, point_c]))

    if response.status_code != 200:
        raise RuntimeError(response.json())

    route_data = response.json()
    if 'paths' in route_data or not route_data['paths']:
        time = route_data['paths'][0]['time']
    else:
        raise RuntimeError('ROUTING ERROR')
    return time


async def find_closest_agents(routes: list[RouteSchema], point: PointSchema) -> list[Tuple[int, int]]:
    target_lon, target_lat = point.longitude, point.latitude
    target_time = point.date_time

    agents = []
    for route in routes:

        if len(route.locations) == 1:
            left_point_time = route.locations[0].date_time
            route_time = await get_route_time(
                (route.locations[0].longitude,
                 route.locations[0].latitude),
                (target_lon, target_lat),
                (target_lon, target_lat))
            time_delta = timedelta(minutes=(int(route_time) + 30))
            agents.append((route.agent_id, route_time))

        else:
            route.locations.sort(key=lambda x: x.date_time)
            for i in range(1, len(route.locations)):
                right_point_time = route.locations[i].date_time
                left_point_time = route.locations[i - 1].date_time
                if right_point_time > target_time and left_point_time < target_time:
                    route_time = await get_route_time(
                        (route.locations[i - 1].longitude,
                         route.locations[i - 1].latitude),
                        (target_lon, target_lat),
                        (route.locations[i].longitude,
                         route.locations[i].latitude))
                    time_delta = timedelta(minutes=(int(route_time) + 30))

                    if left_point_time + time_delta < right_point_time:
                        agents.append((route.agent_id, route_time))

    agents = sorted(agents, key=lambda x: x[1])
    return agents[:10]
