from typing import TypedDict


class Candidate(TypedDict):
    name: str
    bio: str


class Job(TypedDict):
    title: str
    location: str


class JobFitScore(TypedDict):
    job: Job
    score: float
