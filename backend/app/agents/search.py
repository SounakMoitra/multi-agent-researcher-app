from langchain.prompts import ChatPromptTemplate
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI


class SearchAgent:
    """Researches a single question using live web search + LLM synthesis."""

    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.search_tool = TavilySearchResults(max_results=3)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert researcher. Use the provided search results
            to give a comprehensive, accurate answer to the question. Synthesize information
            from multiple sources and cite key facts.""",
                ),
                (
                    "human",
                    """Question: {question}

Search Results: {search_results}

Provide a detailed answer based on the search results above.""",
                ),
            ]
        )

    def research_question(self, question: str) -> str:
        search_results = self.search_tool.invoke({"query": question})
        formatted_results = "\n\n".join(
            f"Source {i + 1}: {result.get('content', '')}"
            for i, result in enumerate(search_results)
        )
        chain = self.prompt | self.model
        response = chain.invoke(
            {"question": question, "search_results": formatted_results}
        )
        return response.content