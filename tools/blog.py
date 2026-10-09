#!/usr/bin/env python3
"""Gerador do blog (estático, sem banco de dados).

Uso, a partir da raiz do repositório:
    python3 tools/blog.py build        # regenera tudo a partir de blog/src/*.json
    python3 tools/blog.py check        # valida os arquivos-fonte sem escrever nada

Cada artigo é um JSON em blog/src/<slug>.json com os campos:
    slug, title, seo_title (<=60), description (<=155), date (AAAA-MM-DD), category,
    quick_answer (40 a 60 palavras), body_html (h2/h3/p/ul/ol/table/blockquote),
    faq [{q, a}], keywords [..], updated (opcional)

O script escreve: blog/<slug>.html, blog/index.html (+ pagina-N.html), blog/feed.xml,
sitemap.xml, o bloco "## Blog" do llms.txt e os 3 últimos artigos na home (index.html).
Cada artigo vira uma página própria, então a home e o índice não ficam mais pesados.
"""
import glob, html, json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://alexandreleite-mkt.vercel.app/"
BLOG = BASE + "blog/"
PER_PAGE = 12
CATS = {"SEO e IA": "c-blue", "Marketing": "c-green", "CRM e automação": "c-navy", "Jornalismo": "c-red", "Carreira": "c-navy"}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
e = lambda s: html.escape(s, quote=True)


def data_br(d):
    y, m, dd = map(int, d.split("-"))
    return f"{dd} de {MESES[m - 1]} de {y}"


def slugify(t):
    t = re.sub(r"<[^>]+>", "", t).lower()
    for a, b in zip("áàâãéêíóôõúüç", "aaaaeeiooouuc"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def load():
    posts = []
    for f in glob.glob(os.path.join(ROOT, "blog", "src", "*.json")):
        p = json.load(open(f, encoding="utf-8"))
        assert p["slug"] == os.path.basename(f)[:-5], f"slug diferente do nome do arquivo: {f}"
        words = len(re.sub(r"<[^>]+>", " ", p["body_html"]).split()) + len(p["quick_answer"].split())
        p["read_min"] = max(2, round(words / 200))
        p["words"] = words
        posts.append(p)
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


def check(posts):
    probs = []
    for p in posts:
        s = p["slug"]
        if len(p["seo_title"]) > 60: probs.append(f"{s}: seo_title com {len(p['seo_title'])} caracteres (máx. 60)")
        if len(p["description"]) > 155: probs.append(f"{s}: description com {len(p['description'])} caracteres (máx. 155)")
        n = len(p["quick_answer"].split())
        if not 35 <= n <= 65: probs.append(f"{s}: quick_answer com {n} palavras (ideal 40 a 60)")
        if p["category"] not in CATS: probs.append(f"{s}: categoria desconhecida: {p['category']}")
        if not 3 <= len(p["faq"]) <= 8: probs.append(f"{s}: FAQ deve ter de 3 a 8 perguntas")
        if "<h1" in p["body_html"]: probs.append(f"{s}: body_html não pode ter h1")
        if p["body_html"].count("<h2") < 3: probs.append(f"{s}: use pelo menos 3 subtítulos h2")
        if not 600 <= p["words"] <= 1800: probs.append(f"{s}: {p['words']} palavras (ideal 800 a 1.400)")
        if "—" in p["body_html"]: probs.append(f"{s}: evite travessão no corpo")
    return probs


HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="author" content="Alexandre Leite">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="theme-color" content="#004488">
    <link rel="canonical" href="{url}">
    <link rel="alternate" type="application/rss+xml" title="Blog de Alexandre Leite" href="{blog}feed.xml">
    <meta property="og:type" content="{ogtype}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{base}assets/profile.jpg">
    <meta property="og:locale" content="pt_BR">
    <meta property="og:site_name" content="Alexandre Leite">
    <meta name="twitter:card" content="summary">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23004488'/%3E%3Ctext x='32' y='43' font-family='Arial,sans-serif' font-size='30' font-weight='700' text-anchor='middle' fill='white'%3EAL%3C/text%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="blog.css">
    <script type="application/ld+json">{ld}</script>
</head>
<body>
    <a href="#main" class="skip-link">Pular para o conteúdo</a>
    <header class="navbar">
        <div class="wrap nav-row">
            <a href="../" class="brand">Alexandre Leite</a>
            <nav aria-label="Navegação">
                <a href="../">Portfólio</a>
                <a href="./"{cur}>Blog</a>
                <a href="../#contato" class="nav-cta">Contato</a>
            </nav>
        </div>
    </header>
"""

FOOT = """
    <footer class="foot">
        <div class="wrap">
            <p class="foot-title">Vamos conversar?</p>
            <p>Estou aberto a oportunidades em marketing e jornalismo, remotas ou na região de Belo Horizonte.</p>
            <p class="foot-links"><a href="../#contato">Contato</a><a href="https://www.linkedin.com/in/alexandreleitemkt/" target="_blank" rel="noopener">LinkedIn</a><a href="../">Portfólio</a><a href="feed.xml">RSS</a></p>
            <p class="foot-copy">&copy; {year} Alexandre Leite · Contagem, MG</p>
        </div>
    </footer>
</body>
</html>
"""

PERSON = {"@type": "Person", "@id": BASE + "#person", "name": "Alexandre Leite", "url": BASE, "image": BASE + "assets/profile.jpg",
          "jobTitle": "Profissional de Marketing Digital e Jornalista",
          "sameAs": ["https://www.linkedin.com/in/alexandreleitemkt/", "https://www.instagram.com/alexandreleite_mkt/", "https://www.itatiaia.com.br/autor/alexandre-leite/"]}


def card(p, prefix=""):
    return (f'<a class="card" href="{prefix}{p["slug"]}.html"><span class="card-top {CATS[p["category"]]}">{e(p["category"])}</span>'
            f'<span class="card-body"><strong>{e(p["title"])}</strong><span>{e(p["description"])}</span>'
            f'<small><time datetime="{p["date"]}">{data_br(p["date"])}</time> · {p["read_min"]} min de leitura</small></span></a>')


def add_ids(body):
    toc = []

    def rep(m):
        text = re.sub(r"<[^>]+>", "", m.group(2))
        hid = slugify(text)[:60]
        toc.append((hid, text))
        return f'<h2 id="{hid}"{m.group(1)}>{m.group(2)}</h2>'

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", rep, body, flags=re.S), toc


def post_page(p, older):
    url = f"{BLOG}{p['slug']}.html"
    body, toc = add_ids(p["body_html"])
    body = re.sub(r"<table", '<div class="table-wrap"><table', body).replace("</table>", "</table></div>")
    mod = p.get("updated", p["date"])
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": url + "#article", "headline": p["title"], "description": p["description"], "url": url,
         "mainEntityOfPage": url, "datePublished": p["date"], "dateModified": mod, "inLanguage": "pt-BR", "wordCount": p["words"],
         "articleSection": p["category"], "keywords": ", ".join(p.get("keywords", [])), "image": BASE + "assets/profile.jpg",
         "author": {"@id": BASE + "#person"}, "publisher": {"@id": BASE + "#person"},
         "isPartOf": {"@type": "Blog", "@id": BLOG + "#blog", "name": "Blog de Alexandre Leite", "url": BLOG}},
        PERSON,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Portfólio", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BLOG},
            {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", f["a"])}} for f in p["faq"]]}]}
    o = [HEAD.format(title=e(p["seo_title"] + " | Alexandre Leite" if len(p["seo_title"]) <= 42 else p["seo_title"]), desc=e(p["description"]), url=url,
                     blog=BLOG, base=BASE, ogtype="article", ld=json.dumps(ld, ensure_ascii=False), cur="")]
    o.append(f'''    <main id="main">
        <article class="wrap post">
            <nav class="crumbs" aria-label="Você está em"><a href="../">Portfólio</a> › <a href="./">Blog</a> › <span>{e(p["category"])}</span></nav>
            <span class="tag {CATS[p["category"]]}">{e(p["category"])}</span>
            <h1>{e(p["title"])}</h1>
            <div class="byline">
                <img src="../assets/profile.jpg" alt="Alexandre Leite" width="44" height="44">
                <p><a href="../" rel="author">Alexandre Leite</a><span><time datetime="{p["date"]}">{data_br(p["date"])}</time> · {p["read_min"]} min de leitura{" · atualizado em " + data_br(mod) if mod != p["date"] else ""}</span></p>
            </div>
            <aside class="quick" aria-label="Resposta rápida">
                <strong>Resposta rápida</strong>
                <p>{p["quick_answer"]}</p>
            </aside>
            <nav class="toc" aria-label="Neste artigo">
                <strong>Neste artigo</strong>
                <ol>''')
    for hid, text in toc:
        o.append(f'                    <li><a href="#{hid}">{e(text)}</a></li>')
    o.append('                    <li><a href="#perguntas-frequentes">Perguntas frequentes</a></li>\n                </ol>\n            </nav>\n            <div class="prose">')
    o.append(body)
    o.append('                <h2 id="perguntas-frequentes">Perguntas frequentes</h2>')
    for f in p["faq"]:
        o.append(f'                <h3>{e(f["q"])}</h3>\n                <p>{f["a"]}</p>')
    o.append('''            </div>
            <aside class="author">
                <img src="../assets/profile.jpg" alt="Alexandre Leite" width="72" height="72" loading="lazy">
                <div>
                    <strong>Alexandre Leite</strong>
                    <p>Profissional de marketing digital e jornalista em Contagem (MG). Trabalha com SEO, mídia paga, CRM e conteúdo há mais de 5 anos e cobre as Eleições 2026 para a Rádio Itatiaia.</p>
                    <p class="author-links"><a href="../#resultados">Ver resultados</a><a href="https://www.linkedin.com/in/alexandreleitemkt/" target="_blank" rel="noopener">LinkedIn</a><a href="../#contato">Contato</a></p>
                </div>
            </aside>
        </article>''')
    if older:
        o.append('        <section class="wrap more">\n            <h2>Continue lendo</h2>\n            <div class="grid">')
        o += ["                " + card(q) for q in older]
        o.append("            </div>\n        </section>")
    o.append("    </main>" + FOOT.format(year=p["date"][:4] if False else datetime.date.today().year))
    return "\n".join(o)


def index_page(posts, page, pages):
    name = "index.html" if page == 1 else f"pagina-{page}.html"
    url = BLOG if page == 1 else BLOG + name
    title = "Blog de Alexandre Leite | SEO, IA, marketing e jornalismo" + (f" (página {page})" if page > 1 else "")
    desc = "Artigos de Alexandre Leite sobre SEO, buscas com IA (AEO/GEO), marketing de conteúdo, CRM e jornalismo, escritos a partir da prática."
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Blog", "@id": BLOG + "#blog", "name": "Blog de Alexandre Leite", "url": BLOG, "description": desc, "inLanguage": "pt-BR",
         "author": {"@id": BASE + "#person"},
         "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{BLOG}{p['slug']}.html", "datePublished": p["date"]} for p in posts]},
        PERSON,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Portfólio", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": BLOG}]}]}
    o = [HEAD.format(title=e(title), desc=e(desc), url=url, blog=BLOG, base=BASE, ogtype="website", ld=json.dumps(ld, ensure_ascii=False), cur=' aria-current="page"')]
    o.append('''    <main id="main">
        <section class="wrap blog-head">
            <p class="eyebrow">Blog</p>
            <h1>SEO, buscas com IA, marketing e jornalismo</h1>
            <p>Textos curtos e práticos sobre o que eu faço no dia a dia: conteúdo que ranqueia, páginas que a IA cita, mídia paga, CRM e apuração.</p>
        </section>
        <section class="wrap">
            <div class="grid">''')
    o += ["                " + card(p) for p in posts]
    o.append("            </div>")
    if pages > 1:
        o.append('            <nav class="pager" aria-label="Páginas">')
        for n in range(1, pages + 1):
            href = "./" if n == 1 else f"pagina-{n}.html"
            o.append(f'                <a href="{href}"{" aria-current=\"page\"" if n == page else ""}>{n}</a>')
        o.append("            </nav>")
    o.append("        </section>\n    </main>" + FOOT.format(year=datetime.date.today().year))
    return name, "\n".join(o)


def write(rel, content):
    path = os.path.join(ROOT, rel)
    old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if old != content:
        open(path, "w", encoding="utf-8").write(content)
        print("escrito:", rel)


def build(posts):
    for i, p in enumerate(posts):
        same = [q for q in posts[i + 1:] if q["category"] == p["category"]]
        rest = [q for q in posts[i + 1:] if q["category"] != p["category"]]
        rel = (same + rest)[:3]
        rel += list(reversed(posts[:i]))[:3 - len(rel)]  # os mais antigos completam com os vizinhos mais novos (estável)
        write(f"blog/{p['slug']}.html", post_page(p, rel))
    pages = max(1, -(-len(posts) // PER_PAGE))
    for n in range(1, pages + 1):
        name, content = index_page(posts[(n - 1) * PER_PAGE:n * PER_PAGE], n, pages)
        write("blog/" + name, content)
    # RSS
    items = "".join(f"<item><title>{e(p['title'])}</title><link>{BLOG}{p['slug']}.html</link><guid>{BLOG}{p['slug']}.html</guid>"
                    f"<pubDate>{datetime.datetime.strptime(p['date'], '%Y-%m-%d').strftime('%a, %d %b %Y 12:00:00 -0300')}</pubDate>"
                    f"<description>{e(p['description'])}</description></item>\n" for p in posts[:30])
    write("blog/feed.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>Blog de Alexandre Leite</title><link>{BLOG}</link>'
                           f"<description>SEO, buscas com IA, marketing e jornalismo.</description><language>pt-BR</language>\n{items}</channel></rss>\n")
    # sitemap (mantém a data das páginas do portfólio que já estavam lá)
    sm_path = os.path.join(ROOT, "sitemap.xml")
    old = open(sm_path, encoding="utf-8").read() if os.path.exists(sm_path) else ""
    home = re.findall(r"  <url>\n    <loc>" + re.escape(BASE) + r"(?:index-e[ns]\.html)?</loc>.*?</url>\n", old, flags=re.S)
    urls = "".join(home) + f"  <url>\n    <loc>{BLOG}</loc>\n    <lastmod>{posts[0]['date'] if posts else datetime.date.today()}</lastmod>\n  </url>\n"
    urls += "".join(f"  <url>\n    <loc>{BLOG}{p['slug']}.html</loc>\n    <lastmod>{p.get('updated', p['date'])}</lastmod>\n  </url>\n" for p in posts)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
    # llms.txt
    ll_path = os.path.join(ROOT, "llms.txt")
    ll = open(ll_path, encoding="utf-8").read().split("\n## Blog\n")[0].rstrip("\n")
    ll += f"\n\n## Blog\n- [Todos os artigos]({BLOG})\n" + "".join(f"- [{p['title']}]({BLOG}{p['slug']}.html): {p['description']}\n" for p in posts[:50])
    write("llms.txt", ll)
    # últimos 3 na home
    hp = os.path.join(ROOT, "index.html")
    h = open(hp, encoding="utf-8").read()
    cards = "\n".join(
        f'                    <a class="tile" href="blog/{p["slug"]}.html"><span class="tile-top tile-blue"><span>{e(p["category"])}</span></span>'
        f'<span class="tile-body"><strong>{e(p["title"])}</strong><small>{data_br(p["date"])} · {p["read_min"]} min de leitura</small><em>Ler artigo →</em></span></a>'
        for p in posts[:3])
    h2 = re.sub(r"<!--blog:start-->.*?<!--blog:end-->", lambda m: f"<!--blog:start-->\n{cards}\n<!--blog:end-->", h, flags=re.S)
    assert "<!--blog:start-->" in h2, "marcador do blog não encontrado em index.html"
    write("index.html", h2)


if __name__ == "__main__":
    posts = load()
    probs = check(posts)
    for x in probs:
        print("ATENÇÃO:", x)
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        sys.exit(1 if probs else 0)
    build(posts)
    print(f"{len(posts)} artigo(s) no blog.")
