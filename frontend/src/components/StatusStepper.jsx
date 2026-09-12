const STEPS = [
  { key: "pending", label: "Queued" },
  { key: "planning", label: "Planning" },
  { key: "researching", label: "Researching" },
  { key: "synthesizing", label: "Synthesizing" },
  { key: "completed", label: "Done" },
];

export default function StatusStepper({ status }) {
  if (status === "failed") {
    return (
      <div className="flex items-center gap-2 text-sm font-medium text-red-600">
        <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
        Failed
      </div>
    );
  }

  const currentIndex = STEPS.findIndex((s) => s.key === status);

  return (
    <div className="flex items-center gap-2">
      {STEPS.map((step, i) => {
        const done = i < currentIndex || status === "completed";
        const active = i === currentIndex && status !== "completed";
        return (
          <div key={step.key} className="flex items-center gap-2">
            <div
              className={`flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full ${
                done
                  ? "bg-emerald-100 text-emerald-700"
                  : active
                    ? "bg-indigo-100 text-indigo-700"
                    : "bg-slate-100 text-slate-400"
              }`}
            >
              {active && (
                <span className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse" />
              )}
              {step.label}
            </div>
            {i < STEPS.length - 1 && <span className="text-slate-300">—</span>}
          </div>
        );
      })}
    </div>
  );
}
