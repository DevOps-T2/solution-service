from typing import List

from pydantic import BaseModel


class SolutionRequest(BaseModel):
    user_id: str
    computation_id: str
    body: str


class PastComputations(BaseModel):
    computation_ids: List[str]
