"use client";

import { useState } from "react";
import type { Article } from "@/types";

const STYLE = {
  aesthetic: {
    label: "Estetik / Kozmetik",
    border: "border-blue-400",
    badgeBg: "bg-blue-50 text-blue-700 border border-blue-200",
    accent: "text-blue-600",
    dot: "bg-blue-400",
  },
  reconstructive: {
    label: "Rekonstrüktif",
    border: "border-emerald-400",
    badgeBg: "bg-emerald-50 text-emerald-700 border border-emerald-200",
    accent: "text-emerald-600",
    dot: "bg-emerald-400",
  },
} as const;

function RcrBadge({ rcr }: { rcr: number }) {
  const color =
    rcr >= 2
      ? "bg-amber-100 text-amber-800 border-amber-200"
      : rcr >= 1
      ? "bg-yellow-50 text-yellow-700 border-yellow-200"
      : "bg-slate-100 text-slate-600 border-slate-200";
  return (
    <span className={`text-xs px-2 py-0.5 rounded border font-medium ${color}`}>
      RCR {rcr.toFixed(2)}
    </span>
  );
}

export default function ArticleCard({ article }: { article: Article }) {
  const [showAbstract, setShowAbstract] = useState(false);
  const style = STYLE[article.category] ?? STYLE.aesthetic;

  return (
    <article
      className={`bg-white rounded-2xl border-l-4 ${style.border} shadow-sm hover:shadow-md transition-shadow flex flex-col gap-4 p-6`}
    >
      {/* Category label */}
      <div className="flex items-center gap-2">
        <span className={`w-2 h-2 rounded-full ${style.dot}`} />
        <span className={`text-xs font-semibold tracking-wide uppercase ${style.accent}`}>
          {style.label}
        </span>
      </div>

      {/* Title */}
      <a
        href={article.pubmed_url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-slate-900 font-semibold text-[15px] leading-snug hover:underline underline-offset-2"
      >
        {article.title || "—"}
      </a>

      {/* Authors + Journal */}
      <div className="text-sm text-slate-500 space-y-0.5">
        {article.authors && <p className="truncate">{article.authors}</p>}
        <p>
          <span className="font-medium text-slate-700">{article.journal}</span>
          {article.year ? <span> · {article.year}</span> : null}
        </p>
      </div>

      {/* Metric badges */}
      <div className="flex flex-wrap gap-2">
        <span className="text-xs px-2 py-0.5 rounded border bg-slate-100 text-slate-600 border-slate-200">
          {article.citation_count ?? 0} atıf
        </span>
        {article.rcr != null && <RcrBadge rcr={article.rcr} />}
        {article.score != null && (
          <span className="text-xs px-2 py-0.5 rounded border bg-slate-100 text-slate-600 border-slate-200">
            Skor {(article.score * 100).toFixed(0)}
          </span>
        )}
      </div>

      {/* Turkish summary */}
      {article.abstract_tr && (
        <div className="rounded-xl bg-slate-50 border border-slate-100 p-4 text-sm text-slate-700 leading-relaxed">
          <p className={`text-[11px] font-bold uppercase tracking-wider mb-2 ${style.accent}`}>
            Türkçe Özet
          </p>
          {article.abstract_tr}
        </div>
      )}

      {/* Abstract toggle */}
      {article.abstract && (
        <div>
          <button
            onClick={() => setShowAbstract((v) => !v)}
            className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
          >
            {showAbstract ? "▲ Orijinali gizle" : "▼ Orijinal abstract'ı göster"}
          </button>
          {showAbstract && (
            <p className="mt-3 text-sm text-slate-600 leading-relaxed border-t border-slate-100 pt-3">
              {article.abstract}
            </p>
          )}
        </div>
      )}

      {/* DOI */}
      {article.doi && (
        <a
          href={`https://doi.org/${article.doi}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs text-slate-400 hover:text-slate-600 transition-colors mt-auto"
        >
          DOI: {article.doi}
        </a>
      )}
    </article>
  );
}
