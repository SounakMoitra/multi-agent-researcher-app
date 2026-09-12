import { useState } from "react";

const MODEL_OPTIONS = [
  { value: "gpt-4o-mini", label: "GPT-4o mini (fast, cheap)" },
  { value: "gpt-4o", label: "GPT-4o (higher quality)" },
];

export default function TopicForm({ onSubmit, isSubmitting }) {
  const [topic, setTopic] = useState("");
  const [modelName, setModelName] = useState("gpt-4o-mini");

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = topic.trim();
    if (trimmed.length < 3) return;
    onSubmit(trimmed, modelName);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow-sm border border-slate-200 p-5"
    >
      <label
        htmlFor="topic"
        className="block text-sm font-medium text-slate-700 mb-1"
      >
        Research topic
      </label>
      <textarea
        id="topic"
        rows={2}
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="e.g. The impact of AI on renewable energy"
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
        disabled={isSubmitting}
      />

      <div className="flex items-center justify-between mt-3">
        <select
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          disabled={isSubmitting}
          className="text-sm rounded-lg border border-slate-300 px-2 py-1.5 bg-white"
        >
          {MODEL_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        <button
          type="submit"
          disabled={isSubmitting || topic.trim().length < 3}
          className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          {isSubmitting ? "Starting…" : "Start research"}
        </button>
      </div>
    </form>
  );
}
