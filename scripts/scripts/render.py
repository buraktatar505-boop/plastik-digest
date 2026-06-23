import os
from collections import defaultdict

DOCS = "docs"

MONTHS = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran",
          "Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
DAYS = ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"]

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f8fafc;color:#1e293b}
header{background:#fff;border-bottom:1px solid #e2e8f0;padding:1.2rem 1.5rem;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:10}
h1{font-size:1.2rem;font-weight:700}
.sub{font-size:.8rem;color:#64748b;margin-top:.2rem}
header a{font-size:.85rem;color:#64748b;text-decoration:none}
header a:hover{color:#1e293b}
main{max-width:960px;margin:0 auto;padding:2.5rem 1rem}
.lbl{font-size:.65rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#94a3b8;margin-bottom:1.5rem}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
@media(max-width:640px){.grid{grid-template-columns:1fr}}
.card{background:#fff;border-radius:1rem;padding:1.5rem;box-shadow:0 1px 3px rgba(0,0,0,.08);display:flex;flex-direction:column;gap:1rem}
.ae{border-left:4px solid #60a5fa}
.re{border-left:4px solid #34d399}
.cat{display:flex;align-items:center;gap:.5rem;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em}
.ae .cat{color:#3b82f6} .re .cat{color:#10b981}
.dot{width:8px;height:8px;border-radius:50%}
.ae .dot{background:#60a5fa} .re .dot{background:#34d399}
.card h2{font-size:.9375rem;font-weight:600;line-height:1.4}
.card h2 a{color:#1e293b;text-decoration:none}
.card h2 a:hover{text-decoration:underline}
.meta{font-size:.8rem;color:#64748b}
.meta b{color:#475569}
.badges{display:flex;flex-wrap:wrap;gap:.5rem}
.badge{font-size:.75rem;padding:.2rem .6rem;border-radius:.375rem;border:1px solid #e2e8f0;background:#f8fafc;color:#64748b}
.rcr{background:#fef3c7;border-color:#fde68a;color:#92400e}
.tr-box{background:#f8fafc;border:1px solid #e2e8f0;border-radius:.75rem;padding:1rem;font-size:.875rem;color:#374151;line-height:1.6}
.tr-lbl{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;margin-bottom:.5rem}
.ae .tr-lbl{color:#3b82f6} .re .tr-lbl{color:#10b981}
details summary{font-size:.75rem;color:#94a3b8;cursor:pointer}
details p{margin-top:.75rem;font-size:.875rem;color:#64748b;line-height:1.6;padding-top:.75rem;border-top:1px solid #f1f5f9}
.doi{font-size:.75rem;color:#94a3b8;text-decoration:none;margin-top:auto}
.doi:hover{color:#64748b}
footer{border-top:1px solid #e2e8f0;padding:1.5rem;text-align:center;font-size:.75rem;color:#94a3b8;margin-top:4rem}
.empty{text-align:center;padding:5rem 0;color:#94a3b8;font-size:1rem}
.archive-section{display:flex;flex-direction:column;gap:3.5rem}
.archive-date{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94a3b8;margin-bottom:1.5rem}
"""

def _fmt(date_str):
    try:
        from datetime import date
        d = date.fromisoformat(date_str)
        return f"{DAYS[d.weekday()]}, {d.day} {MONTHS[d.month-1]} {d.year}"
    except Exception:
        return date_str or ""

def _card(a):
    cat = a.get("category","aesthetic")
    cls = "ae" if cat == "aesthetic" else "re"
    cat_label = "Estetik / Kozmetik" if cat == "aesthetic" else "Rekonstrüktif"
    rcr = a.get("rcr")
    rcr_badge = f'<span class="badge rcr">RCR {rcr:.2f}</span>' if rcr else ""
    tr = ""
    if a.get("abstract_tr"):
        tr = f'<div class="tr-box"><div class="tr-lbl">Türkçe Özet</div>{a["abstract_tr"]}</div>'
    orig = ""
    if a.get("abstract"):
        orig = f'<details><summary>▼ Orijinal abstract</summary><p>{a["abstract"]}</p></details>'
    doi = f'<a class="doi" href="https://doi.org/{a["doi"]}" target="_blank">DOI: {a["doi"]}</a>' if a.get("doi") else ""
    return f'''<div class="card {cls}">
<div class="cat"><span class="dot"></span>{cat_label}</div>
<h2><a href="{a.get("pubmed_url","#")}" target="_blank">{a.get("title","")}</a></h2>
<div class="meta"><div>{a.get("authors","")}</div><div><b>{a.get("journal","")}</b>{" · "+str(a["year"]) if a.get("year") else ""}</div></div>
<div class="badges"><span class="badge">{a.get("citation_count",0)} atıf</span>{rcr_badge}</div>
{tr}{orig}{doi}
</div>'''

def _page(title, heading, sub, body, back_href, back_label):
    return f'''<!DOCTYPE html>
<html lang="tr"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>{CSS}</style></head>
<body>
<header>
  <div><div style="font-size:1.2rem;font-weight:700">{heading}</div><div class="sub">{sub}</div></div>
  <a href="{back_href}">{back_label}</a>
</header>
<main>{body}</main>
<footer>Kaynak: PubMed · NIH iCite · Anthropic Claude — Klinik karar desteği değildir.</footer>
</body></html>'''

def render_today(data):
    os.makedirs(DOCS, exist_ok=True)
    articles = data.get("articles", [])
    date_str = _fmt(data.get("date",""))
    if not articles:
        body = '<p class="empty">Bugün henüz makale seçilmedi.</p>'
    else:
        cards = "".join(_card(a) for a in articles)
        body = f'<p class="lbl">Günün Seçimi — 2 Makale</p><div class="grid">{cards}</div>'
    html = _page("Plastik Cerrahi Digest","Plastik Cerrahi Digest",date_str,body,"archive.html","Arşiv →")
    with open(os.path.join(DOCS,"index.html"),"w",encoding="utf-8") as f:
        f.write(html)

def render_archive(all_articles):
    os.makedirs(DOCS, exist_ok=True)
    groups = defaultdict(list)
    for a in all_articles:
        groups[a["date"]].append(a)
    sections = ""
    for date in sorted(groups.keys(), reverse=True):
        cards = "".join(_card(a) for a in groups[date])
        sections += f'<div><div class="archive-date">{_fmt(date)}</div><div class="grid">{cards}</div></div>'
    body = f'<div class="archive-section">{sections}</div>' if sections else '<p class="empty">Henüz arşiv kaydı yok.</p>'
    html = _page("Arşiv — Plastik Cerrahi Digest","Arşiv","",body,"index.html","← Bugün")
    with open(os.path.join(DOCS,"archive.html"),"w",encoding="utf-8") as f:
        f.write(html)
