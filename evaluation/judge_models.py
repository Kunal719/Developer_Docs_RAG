from pydantic import BaseModel, Field

class Score(BaseModel):
    score: float = Field(ge=0.0, le=5.0, description="Evaluation score between 0.0 and 5.0.")
    justification: str


class JudgeEvaluation(BaseModel):
    correctness: Score
    groundedness: Score
    completeness: Score
    hallucination: Score
    missing_concepts: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)