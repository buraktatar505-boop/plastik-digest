import Link from "next/link";
import ArticleCard from "@/components/ArticleCard";
import type { Article } from "@/types";
import todayData from "@/data/today.json";

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "";
  try {
    return new Date(dateStr + "T12:00:00").toLocaleDateString("tr-TR", {
      weekday: "long", year: "numeric", month: "long", day: "numeric",
    });
  } catch { return dateStr; }
}

export default function HomePage() {
  const articles = (todayData as { date: string | null; articles: Article[] }).articles;
  const aesthetic = articles.find((a) => a.category === "aesthetic");
  const reconstructive = articles.find((a) => a.category === "reconstructive");
  const date = (todayData as { date: string | null }).date;

  return (
    <main className="min-h-screen">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-slate-900 tracking-tight">Plastik Cerrahi Digest</h1>
            {date && <p className="text-slate-500 text-sm mt-0.5">{formatDate(date)}</p>}
          </div>
          <Link href="/archive" className="text-sm text-slate-500 hover:text-slate-900 font-medium">Arşiv →</Link>
        </div>
      </header>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10">
        {!aesthetic && !reconstructive ? (
          <div className="text-center py-24 text-slate-400">
            <p className="text-lg font-medium text-slate-600">Bugün henüz makale seçilmedi</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {aesthetic && <ArticleCard article={aesthetic} />}
            {reconstructive && <ArticleCard article={reconstructive} />}
          </div>
        )}
      </div>
      <footer className="border-t border-slate-200 mt-16 py-6 text-center text-xs text-slate-400">
        Kaynak: PubMed · NIH iCite · Anthropic Claude — Klinik karar desteği değildir.
      </footer>
    </main>
  );
}
