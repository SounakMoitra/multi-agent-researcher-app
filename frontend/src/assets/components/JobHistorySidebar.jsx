export default function JobHistorySidebar({ jobs, selectedJobId, onSelect }) {
  return (
    <aside className="bg-white rounded-xl shadow-sm border border-slate-200 p-4 h-fit">
      <h3 className="text-sm font-semibold text-slate-800 mb-3">Past jobs</h3>
      {jobs.length === 0 && (
        <p className="text-xs text-slate-400">
          No jobs yet — start one on the right.
        </p>
      )}
      <ul className="space-y-1">
        {jobs.map((job) => (
          <li key={job.job_id}>
            <button
              onClick={() => onSelect(job.job_id)}
              className={`w-full text-left px-3 py-2 rounded-lg text-xs transition-colors ${
                job.job_id === selectedJobId
                  ? "bg-indigo-50 text-indigo-700 font-medium"
                  : "hover:bg-slate-50 text-slate-600"
              }`}
            >
              <div className="truncate">{job.topic}</div>
              <div className="text-slate-400 mt-0.5 capitalize">
                {job.status}
              </div>
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
}
