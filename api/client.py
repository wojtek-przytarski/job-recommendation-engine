from os import path
from typing import List, Union, Dict

import requests

from api.types import Job, Candidate


class Client:
    base_url = "https://bn-hiring-challenge.fly.dev"

    def get_jobs(self) -> List[Job]:
        return self.get("jobs.json")

    def get_candidates(self) -> List[Candidate]:
        return self.get("members.json")

    def get(self, endpoint: str, *args, **kwargs) -> Union[List, Dict]:
        return self.request("GET", endpoint, *args, **kwargs)

    def request(self, method: str, endpoint: str, *args, **kwargs) -> Union[List, Dict]:
        url = path.join(self.base_url, endpoint)
        response = requests.request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response.json()
