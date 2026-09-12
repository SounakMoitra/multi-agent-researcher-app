import ReactMarkdown from "react-markdown";

export default function ReportViewer({ report }) {
  if (!report) return null;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h3 className="text-sm font-semibold text-slate-800 mb-4">
        Final report
      </h3>
      <article className="prose prose-slate prose-sm max-w-none">
        <ReactMarkdown>{report}</ReactMarkdown>
      </article>
    </div>
  );
}
