import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import List
from pydantic import BaseModel, Field

load_dotenv()


class ResearchPlan(BaseModel):
    """Model for research plan output"""
    questions: List[str] = Field(description="List of research questions")


class PlannerAgent:
    """Agent responsible for creating research plans"""
    
    def __init__(self, model: ChatOpenAI):
        self.model = model
        self.parser = PydanticOutputParser(pydantic_object=ResearchPlan)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert research planner. Your task is to break down 
            topics into 3-5 specific, answerable questions that will help thoroughly 
            research the topic.
            
            {format_instructions}"""),
            ("human", "Create a research plan for the following topic: {topic}")
        ])
    
    def create_plan(self, topic: str) -> List[str]:
        """Create a research plan for the given topic"""
        print("Planner Agent: Creating a research plan...")
        
        try:
            chain = self.prompt | self.model | self.parser
            result = chain.invoke({
                "topic": topic,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            print("Plan created:")
            for i, question in enumerate(result.questions, 1):
                print(f"   {i}. {question}")
            
            return result.questions
        
        except Exception as e:
            print(f"Error in Planner Agent: {e}")
            return []