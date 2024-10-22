import json

from toy.daos.example_dao import ExampleDAO


def example_route(data: str) -> str:
    return data


def example_route_add_param(data: int) -> int:
    return data ** data


def example_route_get_id(name: str) -> str:
    dao = ExampleDAO()
    return dao.get(name=name)


def example_route_create(data: bytes) -> str:
    create_data = json.loads(data)

    name: str = create_data['name']
    dao = ExampleDAO()
    result: int = dao.create(name=name)
    return name
