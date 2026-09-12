from typing import List
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from app.models.responses import ResearchQuestion


class SynthesizerAgent:
    """Combines all research findings into one structured markdown report."""

    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """ You are an expert research analyst. Create a comprehensive,
                        well-structured report based on the research notes provided.

                        The report should include an engaging introduction, well-organized body
                        sections covering key findings, and a thoughtful conclusion.
                        Use markdown formatting for better readability.
                    """,
                ),
                (
                    "human",
                    """Topic: {topic}

                    Research Notes:
                    {research_notes}

                    Write a comprehensive research report.""",
                ),
            ]
        )

    def synthesize_report(self, topic: str, research_results: List[ResearchQuestion]) -> str:
        research_notes = ""
        for item in research_results:
            research_notes += f"### Question: {item.question}\n\n{item.answer}\n\n---\n\n"

        chain = self.prompt | self.model
        response = chain.invoke({"topic": topic, "research_notes": research_notes})
        return response.content