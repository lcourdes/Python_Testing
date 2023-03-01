import pytest

from server import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def tests_clubs(mocker):
    clubs = [
        {
            "name": "name",
            "email": "test@test.co",
            "points": "1"
        },
        {
            "name": "name2",
            "email": "test2@test.co",
            "points": "13"
        }
    ]
    mocker.patch('server.clubs', clubs)

@pytest.fixture(autouse=True)
def test_competitions(mocker):
    competitions = [
        {
            "name": "name",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "5"
        },
        {
            "name": "name2",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "15"
        },
        {
            "name": "past event",
            "date": "1900-03-27 10:00:00",
            "numberOfPlaces": "15"
        }
    ]
    mocker.patch('server.competitions', competitions)