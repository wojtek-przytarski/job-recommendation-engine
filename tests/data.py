import pytest


@pytest.fixture
def candidates():
    return [
        {"name": "Liv", "bio": "Senior Software Engineer looking for a new challenge in London"},
        {"name": "Bella", "bio": "Graphics and UX Designer with 5 years experience trying to relocate to Edinburgh"},
        {"name": "Zander", "bio": "Looking for a new job in sales with remote working"},
    ]


@pytest.fixture
def jobs():
    return [
        {"title": "Software Engineer", "location": "London"},
        {"title": "UX Designer", "location": "Edinburgh"},
        {"title": "Sales Executive", "location": "London"},
        {"title": "Software Developer", "location": "Edinburgh"},
        {"title": "Marketing Manager", "location": "London"},
        {"title": "UI/UX Designer", "location": "London"},
    ]