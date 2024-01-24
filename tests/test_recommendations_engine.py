import pytest

from recommendations.engine import SpacyRecommendationsEngine
from tests.data import jobs, candidates


@pytest.fixture
def engine(jobs):
    return SpacyRecommendationsEngine(jobs)


def test_get_job_fit_scores(engine, jobs):
    score_one = engine.score_job_fit(
        jobs[0],
        keywords=["engineer", "software", "software engineer"],
        locations=[]
    )
    assert score_one == 1

    score_two = engine.score_job_fit(
        jobs[3],
        keywords=["engineer", "software", "software engineer"],
        locations=["Edinburgh"]
    )
    assert score_two >= engine.IMPERFECT_MATCH_SCORE


def test_score_job_fit_with_locations(engine, jobs):
    score_one = engine.score_job_fit(
        jobs[0],
        keywords=["engineer", "software", "software engineer"],
        locations=["Edinburgh"]
    )
    assert score_one == 1  # no bonus for location

    score_two = engine.score_job_fit(
        jobs[3],
        keywords=["engineer", "software", "software engineer"],
        locations=["Edinburgh"]
    )
    assert score_two >= engine.IMPERFECT_MATCH_SCORE + engine.desired_location_bonus  # bonus for location


def test_get_recommendations(engine):
    recommendations = engine.get_recommendations({
        "name": "Victoria",
        "bio": "I'm a software dev proficient in Python looking for a job in London"
    }, max_recommendations=2)

    assert len(recommendations) == 2
    assert recommendations[0]["title"] == "Software Engineer"
    assert recommendations[1]["title"] == "Software Developer"


def test_get_highest_score_recommendation_only(engine):
    recommendations = engine.get_recommendations({
        "name": "Victoria",
        "bio": "I'm a software dev proficient in Python looking for a job in London"
    }, max_delta=0)

    assert len(recommendations) == 1
    assert recommendations[0]["title"] == "Software Engineer"
