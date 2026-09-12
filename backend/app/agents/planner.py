from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List


class ResearchPlanOutput(BaseModel):
    """Structured output schema the planner LLM call is forced to return."""
    questions: List[str] = Field(description="List of research questions")


class PlannerAgent:
    """Breaks a topic down into 3-5 specific, answerable research questions."""

    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.parser = PydanticOutputParser(pydantic_object=ResearchPlanOutput)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert research planner. Break down topics into
            3-5 specific, answerable questions that will help thoroughly research the topic.

            {format_instructions}""",
                ),
                ("human", "Create a research plan for the following topic: {topic}"),
            ]
        )

    def create_plan(self, topic: str) -> List[str]:
        chain = self.prompt | self.model | self.parser
        result = chain.invoke(
            {
                "topic": topic,
                "format_instructions": self.parser.get_format_instructions(),
            }
        )
        return result.questions