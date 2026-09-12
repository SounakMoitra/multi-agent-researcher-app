import { useState } from "react";

function ResultItem({ question, answer, index }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="border border-slate-200 rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between px-4 py-3 text-left bg-slate-50 hover:bg-slate-100 transition-colors"
      >
        <span className="text-sm font-medium text-slate-800">
          {index + 1}. {question}
        </span>
        <span className="text-slate-400 text-xs">{open ? "▲" : "▼"}</span>
      </button>
      {open && (
        <div className="px-4 py-3 text-sm text-slate-600 whitespace-pre-wrap bg-white">
          {answer}
        </div>
      )}
    </div>
  );
}

export default function ResearchResultsList({ results }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
      <h3 className="text-sm font-semibold text-slate-800 mb-3">
        Findings ({results.length})
      </h3>
      <div className="space-y-2">
        {results.map((r, i) => (
          <ResultItem
            key={i}
            index={i}
            question={r.question}
            answer={r.answer}
          />
        ))}
      </div>
    </div>
  );
}
