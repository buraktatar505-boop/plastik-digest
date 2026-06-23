"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import ArticleCard from "@/components/ArticleCard";
import type { Article } from "@/types";

function formatDate(dateStr: string): string {
  try {
    return new Date(dateStr + "T12:00:00").toLocaleDateString("tr-TR", {
      weekday: "long", year: "numeric", month: "long", day: "numeric",
    });
  } catch { return dateStr; }
}

function groupByDate(articles: Article[]): [string, Article[]][] {
  const map = new Map<string, Article[]>();
  for (const a of articles) {
    const list = map.get(a.date) ?? [];
    list.push(a);
    map.set(a.date, list);
  }
  return Array.from(map.entries()).sort(([a], [b]) => b.localeCompare(a));
}

export default function ArchivePage() {
  const [grouped, setGrouped] = useState<[string, Article[]][]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/data/archive.json")
      .then((r) => r.json())
      .then((data: Article[]) => setGrouped(groupByDate(data)))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Arşiv</h1>
          <Link href="/" className="text-sm text-slate-500 hover:text-slate-900 font-medium">← Bugün</Link>
        </div>
      </header>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10 space-y-14">
        {loading ? (
          <p className="text-center text-slate-400 py-24">Yükleniyor...</p>
        ) : grouped.length === 0 ? (
          <p className="text-center text-slate-400 py-24">Henüz arşiv kaydı yok.</p>
        ) : (
          grouped.map(([date, arts]) => (
            <section key={date}>
              <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-5">{formatDate(date)}</h2>
              <div className="grid md:grid-cols-2 gap-6">
                {arts.map((a) => <ArticleCard key={a.pmid} article={a} />)}
              </div>
            </section>
          ))
        )}
      </div>
    </main>
  );
}
