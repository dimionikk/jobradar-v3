from pydantic import BaseModel, Field
from typing import Optional


class CoverLetterRequest(BaseModel):
    vacancy_id: int = Field(gt=0)


class CoverLetterResponse(BaseModel):
    cover_letter: str


class MatchedVacancy(BaseModel):
    vacancy_id: int
    title: str
    company: Optional[str] = None
    match_score: int = Field(ge=0, le=100, description="Match percentage between user profile and vacancy")
    reason: str = Field(description="AI explanation for the assigned match score")


class MatchingResponse(BaseModel):
    matches: list[MatchedVacancy]