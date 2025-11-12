from typing import Optional

from pydantic import BaseModel, Field


class CardSubgrades(BaseModel):
    """A model to represent the individual subgrades of a card."""

    centering: Optional[float] = Field(
        None, ge=1.0, le=10.0, description="The centering score, from 1.0 to 10.0"
    )
    corners: Optional[float] = Field(
        None, ge=1.0, le=10.0, description="The corners score, from 1.0 to 10.0"
    )
    edges: Optional[float] = Field(
        None, ge=1.0, le=10.0, description="The edges score, from 1.0 to 10.0"
    )
    surface: Optional[float] = Field(
        None, ge=1.0, le=10.0, description="The surface score, from 1.0 to 10.0"
    )


class CardGrade(BaseModel):
    """A model to represent the final grade of a card."""

    overall_score: float = Field(
        ...,
        ge=1.0,
        le=10.0,
        description="The final, overall score for the card, from 1.0 to 10.0",
    )
    score_explanation: str = Field(
        ..., description="A brief explanation of how the overall score was determined."
    )
    subgrades: CardSubgrades = Field(..., description="The individual subgrade scores.")
