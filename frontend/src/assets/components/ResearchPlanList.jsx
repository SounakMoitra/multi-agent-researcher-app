export default function ResearchPlanList({ plan }) {
  if (!plan || plan.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
      <h3 className="text-sm font-semibold text-slate-800 mb-3">
        Research plan
      </h3>
      <ol className="space-y-2">
        {plan.map((question, i) => (
          <li key={i} className="flex gap-2 text-sm text-slate-700">
            <span className="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-50 text-indigo-600 text-xs font-semibold flex items-center justify-center">
              {i + 1}
            </span>
            {question}
          </li>
        ))}
      </ol>
    </div>
  );
}
