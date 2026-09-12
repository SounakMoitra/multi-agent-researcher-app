from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from typing import List


class SynthesizerAgent:
    """Agent responsible for synthesizing research into a final report"""
    
    def __init__(self, model: ChatOpenAI):
        self.model = model
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert research analyst. Create a comprehensive, 
            well-structured report based on the research notes provided. 
            
            The report should include:
            - An engaging introduction
            - Well-organized body sections covering key findings
            - A thoughtful conclusion
            - Clear, professional writing
            
            Use markdown formatting for better readability."""),
            ("human", """Topic: {topic}

            Research Notes:
            {research_notes}

            Write a comprehensive research report.""")
        ])
    
    def synthesize_report(self, topic: str, research_results: List[tuple]) -> str:
        """Synthesize research results into a final report"""
        print("📝 Synthesizer Agent: Writing the final report...")
        
        # Format research notes
        research_notes = ""
        for question, data in research_results:
            research_notes += f"### Question: {question}\n\n{data}\n\n---\n\n"
        
        try:
            chain = self.prompt | self.model
            response = chain.invoke({
                "topic": topic,
                "research_notes": research_notes
            })
            
            print("Report completed!")
            return response.content
        
        except Exception as e:
            print(f"Error in Synthesizer Agent: {e}")
            return "Error: Could not generate the final report."