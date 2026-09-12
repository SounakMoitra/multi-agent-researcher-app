from langchain_openai import ChatOpenAI
from app.core.config import get_settings


def get_llm(model_name: str | None = None) -> ChatOpenAI:
    """Builds a configured ChatOpenAI instance. Central place to tweak temperature, etc."""
    settings = get_settings()
    return ChatOpenAI(
        model=model_name or settings.default_model_name,
        temperature=settings.default_temperature,
        api_key=settings.openai_api_key,
    )