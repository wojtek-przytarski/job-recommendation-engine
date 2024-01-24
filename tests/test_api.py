# test api using pytest
import pytest
import requests

from api.client import Client
from tests.data import jobs, candidates


def test_get_jobs(requests_mock, jobs):
    requests_mock.get("https://bn-hiring-challenge.fly.dev/jobs.json", json=jobs)
    client = Client()

    assert jobs == client.get_jobs()


def test_get_candidates(requests_mock, candidates):
    requests_mock.get("https://bn-hiring-challenge.fly.dev/members.json", json=candidates)
    client = Client()
    assert candidates == client.get_candidates()


def test_error_response(requests_mock):
    requests_mock.get("https://bn-hiring-challenge.fly.dev/jobs.json", status_code=500)
    client = Client()
    with pytest.raises(requests.exceptions.HTTPError):
        client.get_jobs()
