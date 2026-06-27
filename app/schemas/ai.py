from pydantic import BaseModel


class CoverLetterRequest(BaseModel):
    vacancy_id: int


class CoverLetterResponse(BaseModel):
    cover_letter: str

class MatchedVacancy(BaseModel):
    vacancy_id: int
    title: str
    company: str
    match_score: int
    reason: str


class MatchingResponse(BaseModel):
    matches: list[MatchedVacancy]