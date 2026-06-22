import { existsSync, readFileSync } from "fs";
import Link from "next/link";
import path from "path";

import ArticleCard from "@/components/ArticleCard";
import type { Article, TodayData } from "@/types";

// Her istekte taze JSON oku (next dev'de de, production'da da)


function loadToday(): TodayData {
  const filePath = path.join(process.cwd(), "data", "today.json");
  if (!existsSync(filePath)) return { date: null, articles: [] };
  try {
    return JSON.parse(readFileSync(filePath, "utf8")) as TodayData;
  } catch {
    return { date: null, articles: [] };
  }
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "";
  try {
    return new Date(dateStr + "T12:00:00").toLocaleDateString("tr-TR", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  } catch {
    return dateStr;
  }
}

export default function HomePage() {
  const data = loadToday();
  const aesthetic = data.articles.find((a: Article) => a.category === "aesthetic");
  const reconstructive = data.articles.find((a: Article) => a.category === "reconstructive");
  const hasArticles = aesthetic || reconstructive;

  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">
              Plastik Cerrahi Digest
            </h1>
            {data.date && (
              <p className="text-slate-500 text-sm mt-0.5">{formatDate(data.date)}</p>
            )}
          </div>
          <Link
            href="/archive"
            className="text-sm text-slate-500 hover:text-slate-900 transition-colors font-medium"
          >
            Arşiv →
          </Link>
        </div>
      </header>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
        {!hasArticles ? (
          <div className="text-center py-24 text-slate-400">
            <p className="text-5xl mb-4">📄</p>
            <p className="text-lg font-medium text-slate-600">Bugün henüz makale seçilmedi</p>
            <p className="text-sm mt-2">
              Günlük iş çalıştırıldığında estetik ve rekonstrüktif makaleler burada görünecek.
            </p>
            <code className="block mt-4 text-xs bg-slate-100 rounded px-3 py-2 inline-block text-slate-500">
              python -m scripts.daily_job
            </code>
          </div>
        ) : (
          <>
            <p className="text-xs text-slate-400 uppercase tracking-wider font-semibold mb-6">
              Günün seçimi — 2 makale
            </p>
            <div className="grid md:grid-cols-2 gap-6">
              {aesthetic && <ArticleCard article={aesthetic} />}
              {reconstructive && <ArticleCard article={reconstructive} />}
            </div>
          </>
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-200 mt-16 py-6 text-center text-xs text-slate-400">
        Kaynak: PubMed · NIH iCite · Anthropic Claude — Klinik karar desteği değildir.
      </footer>
    </main>
  );
}
