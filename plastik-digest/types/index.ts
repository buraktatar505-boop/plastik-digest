export interface Article {
  date: string;
  category: "aesthetic" | "reconstructive";
  pmid: string;
  title: string;
  authors: string;
  journal: string;
  year: number | null;
  doi: string;
  pubmed_url: string;
  citation_count: number;
  rcr: number | null;
  abstract: string;
  abstract_tr: string;
  score: number;
}

export interface TodayData {
  date: string | null;
  articles: Article[];
}
