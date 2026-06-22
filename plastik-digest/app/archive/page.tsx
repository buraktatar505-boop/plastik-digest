import { existsSync, readFileSync } from "fs";
import Link from "next/link";
import path from "path";

import ArticleCard from "@/components/ArticleCard";
import type { Article } from "@/types";

export const dynamic = "force-dynamic";

function loadArchive(): Article[] {
  const filePath = path.join(process.cwd(), "data", "archive.json");
  if (!existsSync(filePath)) return [];
  try {
    return JSON.parse(readFileSync(filePath, "utf8")) as Article[];
  } catch {
    return [];
  }
}

function groupByDate(articles: Article[]): [string, Article[]][] {
  const map = new Map<string, Article[]>();
  for (const a of articles) {
    const existing = map.get(a.date) ?? [];
    existing.push(a);
    map.set(a.date, existing);
  }
  return Array.from(map.entries()).sort(([a], [b]) => b.localeCompare(a));
}

function formatDate(dateStr: string): string {
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

export default function ArchivePage() {
  const articles = loadArchive();
  const grouped = groupByDate(articles);

  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Arşiv</h1>
          <Link
            href="/"
            className="text-sm text-slate-500 hover:text-slate-900 transition-colors font-medium"
          >
            ← Bugün
          </Link>
        </div>
      </header>

      {/* Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10 space-y-14">
        {grouped.length === 0 ? (
          <p className="text-center text-slate-400 py-24">Henüz arşiv kaydı yok.</p>
        ) : (
          grouped.map(([date, dayArticles]) => (
            <section key={date}>
              <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-5">
                {formatDate(date)}
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                {dayArticles.map((a) => (
                  <ArticleCard key={a.pmid} article={a} />
                ))}
              </div>
            </section>
          ))
        )}
      </div>

      <footer className="border-t border-slate-200 mt-16 py-6 text-center text-xs text-slate-400">
        Kaynak: PubMed · NIH iCite · Anthropic Claude — Klinik karar desteği değildir.
      </footer>
    </main>
  );
}
