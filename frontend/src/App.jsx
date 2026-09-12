import { useCallback, useEffect, useState } from "react";
import TopicForm from "./components/TopicForm";
import StatusStepper from "./components/StatusStepper";
import ResearchPlanList from "./components/ResearchPlanList";
import ResearchResultsList from "./components/ResearchResultsList";
import ReportViewer from "./components/ReportViewer";
import JobHistorySidebar from "./components/JobHistorySidebar";
import { startResearch, listResearchJobs } from "./api/client";
import { useResearchJob } from "./hooks/useResearchJob";

export default function App() {
  const [selectedJobId, setSelectedJobId] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const { job, error: pollError } = useResearchJob(selectedJobId);

  const refreshJobList = useCallback(async () => {
    try {
      const data = await listResearchJobs();
      setJobs(data);
    } catch {
      // silently ignore — sidebar just won't update this cycle
    }
  }, []);

  useEffect(() => {
    refreshJobList();
  }, [refreshJobList]);

  // Keep the sidebar's status labels in sync while a job is active
  useEffect(() => {
    if (!job) return;
    refreshJobList();
  }, [job?.status, refreshJobList]);

  async function handleStartResearch(topic, modelName) {
    setIsSubmitting(true);
    setSubmitError(null);
    try {
      const result = await startResearch(topic, modelName);
      setSelectedJobId(result.job_id);
      refreshJobList();
    } catch (err) {
      setSubmitError(err.response?.data?.detail || err.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <h1 className="text-lg font-semibold text-slate-900">
            🤖 Multi-Agent Research Assistant
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Planner → Search → Synthesizer, backed by LangChain + OpenAI
          </p>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-6 grid grid-cols-1 md:grid-cols-[220px_1fr] gap-6">
        <JobHistorySidebar
          jobs={jobs}
          selectedJobId={selectedJobId}
          onSelect={setSelectedJobId}
        />

        <div className="space-y-4">
          <TopicForm
            onSubmit={handleStartResearch}
            isSubmitting={isSubmitting}
          />

          {submitError && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">
              {submitError}
            </div>
          )}

          {pollError && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">
              {pollError}
            </div>
          )}

          {job && (
            <>
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="text-sm font-semibold text-slate-800 truncate pr-4">
                    {job.topic}
                  </h2>
                </div>
                <StatusStepper status={job.status} />
                {job.status === "failed" && job.error && (
                  <p className="text-xs text-red-500 mt-2">{job.error}</p>
                )}
              </div>

              <ResearchPlanList plan={job.plan} />
              <ResearchResultsList results={job.research_results} />
              <ReportViewer report={job.final_report} />
            </>
          )}

          {!job && !submitError && (
            <div className="text-sm text-slate-400 text-center py-12">
              Start a research job above to see live progress here.
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
