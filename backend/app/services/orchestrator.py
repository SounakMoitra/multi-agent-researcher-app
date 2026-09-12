import asyncio
from typing import List
from app.agents.planner import PlannerAgent
from app.agents.search import SearchAgent
from app.agents.synthesizer import SynthesizerAgent
from app.models.enums import JobStatus
from app.models.responses import ResearchQuestion
from app.services import job_store
from app.services.llm_factory import get_llm


async def run_research_job(job_id: str, topic: str, model_name: str) -> None:
    """
        Planner -> Search -> Synthesizer pipeline
    """
    try:
        llm = get_llm(model_name)
        planner = PlannerAgent(llm)
        searcher = SearchAgent(llm)
        synthesizer = SynthesizerAgent(llm)

        # Plannning
        job_store.update_job(job_id, status=JobStatus.PLANNING)
        plan = await asyncio.to_thread(planner.create_plan, topic)
        if not plan:
            raise ValueError("Planner returned no questions.")
        job_store.update_job(job_id, plan=plan)

        # Research
        job_store.update_job(job_id, status=JobStatus.RESEARCHING)
        research_results: List[ResearchQuestion] = []
        for question in plan:
            answer = await asyncio.to_thread(searcher.research_question, question)
            research_results.append(ResearchQuestion(question=question, answer=answer))

            # Incremental update so polling clients see live progress
            job_store.update_job(job_id, research_results=list(research_results))

        if not research_results:
            raise ValueError("No research data could be gathered.")

        # Synthesis
        job_store.update_job(job_id, status=JobStatus.SYNTHESIZING)
        final_report = await asyncio.to_thread(
            synthesizer.synthesize_report, topic, research_results
        )

        job_store.update_job(
            job_id, final_report=final_report, status=JobStatus.COMPLETED
        )

    except Exception as e:
        job_store.update_job(job_id, status=JobStatus.FAILED, error=str(e))
