from typing import List

import spacy

from api.types import Job, Candidate, JobFitScore


class RecommendationsEngine:
    """
    A base class for recommendations engines
    """

    def __init__(self, jobs: List[Job], desired_location_bonus: float = 0.1):
        self.jobs = jobs
        self.desired_location_bonus = desired_location_bonus

        self._prepare_jobs_data()

    def _prepare_jobs_data(self):
        pass

    def get_recommendations(self, candidate: Candidate, **kwargs) -> List[Job]:
        job_fit_scores = self.get_job_fit_scores(candidate)

        return [
            job_fit_score["job"] for job_fit_score in self.filter_recommendations(job_fit_scores, **kwargs)
        ]

    def get_job_fit_scores(self, candidate: Candidate, **kwargs) -> List[JobFitScore]:
        raise NotImplementedError

    def filter_recommendations(
            self,
            recommendations: List[JobFitScore],
            max_recommendations: int = 3,
            min_score: float = 0.5,
            max_delta: float = 0.2,
            **kwargs
    ) -> List[JobFitScore]:
        """
        Filters recommendations based on score and delta between scores

        :param recommendations:
        :param max_recommendations: maximum number of recommendations to return
        :param min_score: recommendations must have a score greater than this
        :param max_delta: recommendations must have a score within this delta of the highest score
        :return:
        """
        recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
        max_score = recommendations[0]["score"]
        recommendations = filter(lambda x: x["score"] >= min_score, recommendations)
        recommendations = filter(lambda x: max_score - x["score"] <= max_delta, recommendations)
        recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)
        return list(recommendations)[:max_recommendations]


class SpacyRecommendationsEngine(RecommendationsEngine):
    """
    A recommendations engine that uses Spacy to extract keywords from a candidate's bio and match them to job titles
    """
    IMPERFECT_MATCH_SCORE = 0.8

    def _prepare_jobs_data(self):
        self.nlp = spacy.load("en_core_web_md")

    def get_job_fit_scores(self, candidate: Candidate, **kwargs) -> List[JobFitScore]:
        bio_nlp = self.nlp(candidate["bio"])

        nouns = [token.text for token in bio_nlp if not token.is_stop and token.pos_ == "NOUN"]
        locations = [location for location in bio_nlp.ents if location.label_ == "GPE"]

        for token in filter(lambda token: not token.is_stop, bio_nlp):
            if token.dep_ == "compound":
                nouns.append(f"{token.text} {token.head.text}")

        keywords = [noun.lower() for noun in nouns]
        locations = [location.text for location in locations]

        return [
            JobFitScore(job=job, score=self.score_job_fit(job, keywords, locations)) for job in self.jobs
        ]

    def score_job_fit(self, job: Job, keywords: List[str], locations: List[str]) -> float:
        score = 0

        job_title = job["title"].lower()

        for keyword in keywords:
            if keyword == job_title:
                score = 1.0
                break

            if keyword in job_title:
                score = max(score, self.IMPERFECT_MATCH_SCORE)

            if keyword_score := self.nlp(keyword).similarity(self.nlp(job_title)):
                score = max(score, keyword_score)

        for location in locations:
            if location.lower() == job["location"].lower():
                score += self.desired_location_bonus
                break

        return score


class SimpleRecommendationsEngine(RecommendationsEngine):
    def get_job_fit_scores(self, candidate: Candidate, **kwargs) -> List[JobFitScore]:
        return [
            JobFitScore(job=job, score=self.score_job_fit(job, candidate)) for job in self.jobs
        ]

    def score_job_fit(self, job: Job, candidate: Candidate) -> float:
        score = 0.0
        job_title = job["title"].lower()

        if job_title in candidate["bio"]:
            score += 1.0
        else:
            job_title_tokens = job_title.split()
            if any(token in candidate["bio"] for token in job_title_tokens):
                score += 1 / len(job_title_tokens)

        if job["location"] in candidate["bio"]:
            score += self.desired_location_bonus

        return score
