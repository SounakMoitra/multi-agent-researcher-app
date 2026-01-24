import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.synthesizer_agent import SynthesizerAgent


load_dotenv()


class ResearchAssistant:
    """Main orchestrator for the multi-agent research system"""
    
    def __init__(self, api_key: str = None, model_name: str = "gpt-4o-mini"):
        """
        Initialize the research assistant
        
        Args:
            api_key: OpenAI API key (if not provided, will use OPENAI_API_KEY env var)
            model_name: OpenAI model to use (gpt-4o-mini is cost-effective and capable)
        """
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable "
            )
        
        if not os.getenv("TAVILY_API_KEY"):
            raise ValueError(
                "Tavily API key not found. Set TAVILY_API_KEY environment variable. "
            )
        
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7
        )
        
        
        self.planner = PlannerAgent(self.llm)
        self.searcher = SearchAgent(self.llm)
        self.synthesizer = SynthesizerAgent(self.llm)
    
    def research(self, topic: str) -> str:
        """
        Conduct research on a topic and generate a comprehensive report
        
        Args:
            topic: The research topic
            
        Returns:
            Final research report as a string
        """
        print(f"\n🚀 Starting research process for: '{topic}'\n")
        
        
        # Step 1: Create research plan
        research_plan = self.planner.create_plan(topic)
        if not research_plan:
            return "Error: Could not create a research plan."
        
        print() 
        
        # Step 2: Research each question
        research_results = []
        for question in research_plan:
            research_data = self.searcher.research_question(question)
            research_results.append((question, research_data))
        
        if not research_results:
            return "Error: Could not gather any research data."
        
        print() 
        
        
        # Step 3: Synthesize final report
        final_report = self.synthesizer.synthesize_report(topic, research_results)
        
        return final_report