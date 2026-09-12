from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Incoming payload to start a new research job."""

    topic: str = Field(..., min_length=3, description="The topic to research")
    model_name: str = Field(default="gpt-4o-mini", description="OpenAI model to use")

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "The impact of AI on renewable energy",
                "model_name": "gpt-4o-mini",
            }
        }