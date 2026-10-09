#!/usr/bin/env python3
"""V8 — versão mais visual. Reaproveita o conteúdo (T) de build.py e troca o template."""
import os, sys, json, html, datetime
TODAY = datetime.date.today().isoformat()

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read().split("def build(lang):")[0]
ns = {}
exec(src, ns)
T, L, LANGS, FILES, BASE, SP, BE, e = (ns[k] for k in ("T", "L", "LANGS", "FILES", "BASE", "SP", "BE", "e"))


def ic(name):
    p = {
        "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/>',
        "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',
        "flow": '<circle cx="5" cy="6" r="2.2"/><circle cx="5" cy="18" r="2.2"/><circle cx="19" cy="12" r="2.2"/><path d="M7.2 6h4.3a3 3 0 0 1 3 3v0.8M7.2 18h4.3a3 3 0 0 0 3-3v-0.8"/>',
        "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21M8.5 21h7"/>',
        "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
        "vote": '<rect x="4" y="11" width="16" height="9" rx="1.5"/><path d="M8 11l2.5-6h5L18 11M9.5 15.5l2 2 3.5-4"/>',
        "city": '<path d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/>',
        "ball": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5l4 3-1.5 4.7h-5L8 10.5zM12 3v4.5M3.6 9.5L8 10.5M20.4 9.5L16 10.5M6.5 19l3-3.8M17.5 19l-3-3.8"/>',
        "doc": '<path d="M6 3h8l4 4v14H6zM14 3v4h4M9 12h6M9 16h6"/>',
        "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3.3 3 14.7 0 18M12 3c-3 3.3-3 14.7 0 18"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'


X = dict(
    title=L("Alexandre Leite | Portfólio de Marketing Digital, SEO e Jornalismo",
            "Alexandre Leite | Digital Marketing, SEO & Journalism Portfolio",
            "Alexandre Leite | Portafolio de Marketing Digital, SEO y Periodismo"),
    desc=L("Portfólio de Alexandre Leite, profissional de marketing digital e jornalista em Contagem (MG): mídia paga, SEO, CRM e conteúdo, cases com resultados e matérias na Rádio Itatiaia.",
           "Portfolio of Alexandre Leite, digital marketer and journalist based in Brazil: paid media, SEO, CRM and content, case studies with results and stories at Rádio Itatiaia.",
           "Portafolio de Alexandre Leite, profesional de marketing digital y periodista en Brasil: medios pagos, SEO, CRM y contenido, casos con resultados y notas en Rádio Itatiaia."),
    bio=L("Alexandre Leite é profissional de marketing digital e jornalista em Contagem, na região de Belo Horizonte (MG). Trabalha com mídia paga, SEO, CRM e conteúdo há mais de 5 anos e cobre as Eleições 2026 para a Rádio Itatiaia.",
          "Alexandre Leite is a digital marketer and journalist based in Contagem, in the Belo Horizonte area, Brazil. He has worked in paid media, SEO, CRM and content for 5+ years and covers the 2026 elections for Rádio Itatiaia.",
          "Alexandre Leite es profesional de marketing digital y periodista en Contagem, en la región de Belo Horizonte, Brasil. Trabaja con medios pagos, SEO, CRM y contenido desde hace más de 5 años y cubre las Elecciones 2026 para Rádio Itatiaia."),
    hero_sub=L("5+ anos em mídia paga, SEO, CRM e conteúdo para SaaS B2B e pequenas empresas no Brasil e nos EUA.",
               "5+ years in paid media, SEO, CRM and content for B2B SaaS companies and small businesses in Brazil and the U.S.",
               "Más de 5 años en medios pagos, SEO, CRM y contenido para SaaS B2B y pequeñas empresas en Brasil y EE. UU."),
    where=L("Onde já trabalhei", "Where I've worked", "Dónde he trabajado"),
    brands=["Rádio Itatiaia", "Saipos", "Meta Wholesale", "Ozen", "TFLA Idiomas", "Fazza Motors"],
    what=L("O que eu faço", "What I do", "Lo que hago"),
    services=[("target", L("Mídia paga", "Paid media", "Medios pagos"),
               L("Meta Ads e Google Ads, com testes A/B de criativos e landing pages.", "Meta Ads and Google Ads, with A/B tests on creatives and landing pages.", "Meta Ads y Google Ads, con pruebas A/B de creatividades y landing pages.")),
              ("search", L("SEO e conteúdo", "SEO & content", "SEO y contenido"),
               L("SEO técnico, on-page e GEO/AEO para buscas com IA.", "Technical and on-page SEO, plus GEO/AEO for AI search.", "SEO técnico, on-page y GEO/AEO para búsquedas con IA.")),
              ("flow", L("CRM e automação", "CRM & automation", "CRM y automatización"),
               L("HubSpot, réguas de follow-up e agentes de IA que qualificam leads.", "HubSpot, follow-up sequences and AI agents that qualify leads.", "HubSpot, secuencias de seguimiento y agentes de IA que califican leads.")),
              ("mic", L("Jornalismo", "Journalism", "Periodismo"),
               L("Reportagem e checagem de dados, hoje nas Eleições 2026.", "Reporting and fact-checking, currently on the 2026 elections.", "Reportajes y verificación de datos, hoy en las Elecciones 2026."))],
    res_lead=L("Quatro trabalhos recentes e o que mudou em cada um.", "Four recent pieces of work and what changed in each.", "Cuatro trabajos recientes y lo que cambió en cada uno."),
    before=L("Antes", "Before", "Antes"), after=L("Depois", "After", "Después"),
    details=L("Ver como foi feito", "See how it was done", "Ver cómo se hizo"),
    did=L("Ver o que fiz", "See what I did", "Ver lo que hice"),
    formats=[L("Perfis", "Profiles", "Perfiles"), L("Debates", "Debates", "Debates"), L("Pesquisas", "Polling", "Encuestas"),
             L("Planos de governo", "Platforms", "Planes de gobierno"), L("Apuração", "Results", "Escrutinio")],
    case_bar=[84, 91, 91, None], case_ic=["target", "search", "chart", "mic"],
    job_brand=["Rádio Itatiaia", "Meta Wholesale", "Ozen", "Saipos"],
    job_place=[L("remoto", "remote", "remoto"), L("Pompano Beach, EUA · remoto", "Pompano Beach, FL · remote", "Pompano Beach, EE. UU. · remoto"),
               L("projetos freelance · remoto", "freelance projects · remote", "proyectos freelance · remoto"), L("SaaS B2B · remoto", "B2B SaaS · remote", "SaaS B2B · remoto")],
    job_role=[L("Jornalista freelancer · Eleições 2026", "Freelance Journalist · 2026 Elections", "Periodista freelance · Elecciones 2026"),
              L("Gerente de Marketing e BDC", "Marketing & BDC Manager", "Gerente de Marketing y BDC"),
              L("Head de Marketing e Conteúdo (único responsável, freelancer)", "Head of Marketing & Content (sole lead, freelance)", "Head de Marketing y Contenido (único responsable, freelance)"),
              L("Analista de Conteúdo (promovido de Redator)", "Content Analyst (promoted from Writer)", "Analista de Contenido (ascendido desde Redactor)")],
    mk_lead=L("Artigos de SEO publicados e projetos de estratégia, copy e mídias sociais.", "Published SEO articles and strategy, copy and social media projects.", "Artículos de SEO publicados y proyectos de estrategia, copy y redes sociales."),
    jr_lead=L("Eleições 2026 na Rádio Itatiaia, política local e esporte.", "2026 elections at Rádio Itatiaia, local politics and sports.", "Elecciones 2026 en Rádio Itatiaia, política local y deporte."),
    cert_title=L("Certificados", "Certificates", "Certificados"),
    more_cred=L("Outras formações", "Other credentials", "Otras formaciones"),
    sk_ic=["target", "search", "chart", "flow", "mic", "globe"],
)


BLOG_SLOT = """
        <section id="blog">
            <div class="container">
                <p class="eyebrow">Blog</p>
                <h2 class="section-title">Últimos artigos</h2>
                <p class="section-lead">Textos sobre SEO, buscas com IA, marketing e jornalismo.</p>
                <div class="rail rail-wrap">
<!--blog:start-->
<!--blog:end-->
                </div>
                <a class="text-link" href="blog/">Ver todos os artigos →</a>
            </div>
        </section>
"""


def build(lang):
    g = lambda v: v[lang] if isinstance(v, dict) else v
    t = lambda k: g(X[k]) if k in X else g(T[k])
    url = BASE + ("" if lang == "pt" else FILES[lang])
    o = []
    w = o.append
    person = {"@type": "Person", "@id": BASE + "#person", "name": "Alexandre Leite", "alternateName": "Alexandre Augusto de Oliveira Leite",
              "jobTitle": t("jobtitle"), "description": t("bio"), "url": BASE, "image": BASE + "assets/profile.jpg", "email": "mailto:alexandreaugusto145@gmail.com",
              "address": {"@type": "PostalAddress", "addressLocality": "Contagem", "addressRegion": "MG", "addressCountry": "BR"},
              "nationality": {"@type": "Country", "name": "Brazil"},
              "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidade Federal de Viçosa (UFV)"}, {"@type": "CollegeOrUniversity", "name": "UniAmérica Descomplica"}],
              "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": "MBA em Marketing Digital e Vendas", "credentialCategory": "degree"},
                                {"@type": "EducationalOccupationalCredential", "name": "Bacharelado em Comunicação Social / Jornalismo", "credentialCategory": "degree"}],
              "hasOccupation": [{"@type": "Occupation", "name": "Digital Marketing Specialist", "skills": "SEO, GEO/AEO, Meta Ads, Google Ads, CRM, HubSpot, CRO, GA4, Copywriting, Inbound Marketing"},
                                {"@type": "Occupation", "name": "Journalist", "skills": "Reporting, fact-checking, election coverage, sports journalism"}],
              "worksFor": {"@type": "Organization", "name": "Rádio Itatiaia", "url": "https://www.itatiaia.com.br/"},
              "knowsLanguage": ["pt-BR", "en", "es"],
              "knowsAbout": ["Marketing digital", "SEO", "GEO/AEO", "Mídia paga", "Meta Ads", "Google Ads", "CRM", "HubSpot", "Marketing de conteúdo", "Inbound marketing", "Copywriting", "Jornalismo", "Cobertura eleitoral", "Jornalismo esportivo"],
              "sameAs": ["https://www.linkedin.com/in/alexandreleitemkt/", "https://www.instagram.com/alexandreleite_mkt/", "https://www.itatiaia.com.br/autor/alexandre-leite/", "https://github.com/alexx145", "https://www.behance.net/"][:4]}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE + "#website", "url": BASE, "name": "Alexandre Leite", "inLanguage": ["pt-BR", "en", "es"], "publisher": {"@id": BASE + "#person"}},
        {"@type": "ProfilePage", "@id": url + "#profile", "url": url, "name": t("title"), "description": t("desc"), "inLanguage": t("htmllang"),
         "isPartOf": {"@id": BASE + "#website"}, "dateModified": TODAY, "mainEntity": {"@id": BASE + "#person"}},
        person]}
    w(f'''<!DOCTYPE html>
<html lang="{t("htmllang")}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(t("title"))}</title>
    <meta name="description" content="{e(t("desc"))}">
    <meta name="author" content="Alexandre Leite">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
    <meta name="theme-color" content="#004488">
    <link rel="canonical" href="{url}">''')
    for l2 in LANGS:
        w(f'    <link rel="alternate" hreflang="{T["htmllang"][l2]}" href="{BASE + ("" if l2 == "pt" else FILES[l2])}">')
    w(f'''    <link rel="alternate" hreflang="x-default" href="{BASE}">
    <meta property="og:type" content="profile">
    <meta property="og:title" content="{e(t("title"))}">
    <meta property="og:description" content="{e(t("desc"))}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{BASE}assets/profile.jpg">
    <meta property="og:locale" content="{ {"pt": "pt_BR", "en": "en_US", "es": "es_ES"}[lang] }">
    <meta name="twitter:card" content="summary">
    <meta property="og:site_name" content="Alexandre Leite">
    <meta property="profile:first_name" content="Alexandre">
    <meta property="profile:last_name" content="Leite">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23004488'/%3E%3Ctext x='32' y='43' font-family='Arial,sans-serif' font-size='30' font-weight='700' text-anchor='middle' fill='white'%3EAL%3C/text%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
    <a href="#main" class="skip-link">{t("skip")}</a>
    <header class="navbar">
        <div class="container nav-container">
            <a href="#home" class="brand">Alexandre Leite</a>
            <nav aria-label="{t("skip")}">
                <ul class="nav-links">''')
    for hid, lab in T["nav"]:
        if hid == "contato":
            w('                    <li><a href="blog/">Blog</a></li>')
        w(f'                    <li><a href="#{hid}">{g(lab)}</a></li>')
    w('                </ul>\n            </nav>\n            <div class="lang-switcher">')
    for l2 in LANGS:
        w(f'                <a href="{FILES[l2]}" hreflang="{T["htmllang"][l2]}"{" class=\"active\" aria-current=\"page\"" if l2 == lang else ""}>{l2.upper()}</a>')
    w(f'''            </div>
        </div>
    </header>

    <main id="main">
        <section class="hero" id="home">
            <div class="container hero-grid">
                <div class="hero-photo-wrap">
                    <img src="assets/profile.jpg" alt="{e(t("photo_alt"))}" class="hero-photo" width="420" height="420">
                </div>
                <div class="hero-text">
                    <p class="eyebrow">{t("hero_eyebrow")}</p>
                    <h1 class="hero-title">Alexandre Leite</h1>
                    <p class="hero-role">{t("hero_role")}</p>
                    <p class="hero-subtitle">{t("hero_sub")}</p>
                    <div class="hero-actions">
                        <a href="#resultados" class="btn btn-primary">{t("cta_work")}</a>
                        <a href="#contato" class="btn btn-secondary">{t("cta_contact")}</a>
                    </div>
                    <div class="hero-meta">''')
    for p in T["pills"]:
        w(f'                        <span class="pill">{g(p)}</span>')
    w('                    </div>\n                </div>\n            </div>\n        </section>\n\n        <section class="band" aria-label="' + t("res_title") + '">\n            <div class="container stats">')
    for v, lab in T["stats"]:
        w(f'                <div class="stat"><span class="stat-value">{v}</span><span class="stat-label">{g(lab)}</span></div>')
    w(f'''            </div>
        </section>

        <section class="brands-strip" aria-label="{t("where")}">
            <div class="container">
                <p class="eyebrow">{t("where")}</p>
                <ul class="brands">''')
    for b in X["brands"]:
        w(f'                    <li>{b}</li>')
    w(f'''                </ul>
            </div>
        </section>

        <section id="sobre">
            <div class="container">
                <p class="eyebrow">{t("about_title")}</p>
                <h2 class="section-title">{t("what")}</h2>
                <p class="section-lead">{t("bio")}</p>
                <div class="service-grid">''')
    for icon, name, line in X["services"]:
        w(f'                    <div class="service reveal"><span class="ic-wrap">{ic(icon)}</span><h3>{g(name)}</h3><p>{g(line)}</p></div>')
    w(f'''                </div>
            </div>
        </section>

        <section class="alt" id="resultados">
            <div class="container">
                <p class="eyebrow">{t("res_eyebrow")}</p>
                <h2 class="section-title">{t("res_title")}</h2>
                <p class="section-lead">{t("res_lead")}</p>
                <div class="case-grid">''')
    for i, c in enumerate(T["cases"]):
        bar = X["case_bar"][i]
        if bar:
            visual = (f'<div class="bars" aria-hidden="true"><div class="bar-row"><span>{t("before")}</span><i style="width:70%"></i></div>'
                      f'<div class="bar-row bar-after"><span>{t("after")}</span><i style="width:{bar}%"></i></div></div>')
        else:
            visual = '<div class="chips">' + "".join(f'<span>{g(f)}</span>' for f in X["formats"]) + '</div>'
        w(f'''                    <article class="case-card reveal">
                        <div class="case-top">
                            <span class="ic-wrap">{ic(X["case_ic"][i])}</span>
                            <p class="case-company">{g(c["co"])}</p>
                        </div>
                        <p class="case-result">{c["v"]}</p>
                        <h3 class="case-result-label">{g(c["lab"])}</h3>
                        {visual}
                        <details>
                            <summary>{t("details")}</summary>
                            <dl>
                                <dt>{t("k_ctx")}</dt><dd>{g(c["ctx"])}</dd>
                                <dt>{t("k_act")}</dt><dd>{g(c["act"])}</dd>
                                <dt>{t("k_res")}</dt><dd>{g(c["res"])}</dd>
                            </dl>
                        </details>
                    </article>''')
    w(f'''                </div>
            </div>
        </section>

        <section id="experiencia">
            <div class="container">
                <h2 class="section-title">{t("exp_title")}</h2>
                <ol class="timeline">''')
    for i, j in enumerate(T["jobs"]):
        w(f'''                    <li class="job reveal">
                        <span class="job-date">{g(j["date"])}</span>
                        <h3 class="job-brand">{X["job_brand"][i]} <small>{g(X["job_place"][i])}</small></h3>
                        <p class="job-role">{g(X["job_role"][i])}</p>
                        <details>
                            <summary>{t("did")}</summary>''')
        if g(j["ctx"]):
            w(f'                            <p class="job-ctx">{g(j["ctx"])}</p>')
        w('                            <ul>')
        for b in j["b"]:
            w(f'                                <li>{g(b)}</li>')
        w('                            </ul>\n                        </details>\n                    </li>')
    w(f'                </ol>\n\n                <div class="two-col">\n                    <details class="more">\n                        <summary>{t("proj_title")} ({len(T["projs"])})</summary>\n                        <div class="mini-list">')
    for n, d in T["projs"]:
        w(f'                            <div class="mini-item"><strong>{n}</strong> — {g(d)}</div>')
    w(f'                        </div>\n                    </details>\n                    <details class="more">\n                        <summary>{t("other_title")} ({len(T["others"])})</summary>\n                        <div class="mini-list">')
    for n, r, d in T["others"]:
        w(f'                            <div class="mini-item"><strong>{n}</strong> — {g(r)}<span>{g(d)}</span></div>')
    w(f'''                        </div>
                    </details>
                </div>
            </div>
        </section>

        <section class="alt" id="projetos">
            <div class="container">
                <p class="eyebrow">{t("mk_eyebrow")}</p>
                <h2 class="section-title">{t("mk_title")}</h2>
                <p class="section-lead">{t("mk_lead")}</p>

                <h3 class="sub-title">{t("saipos_title")}</h3>
                <div class="rail">''')
    for path, tag, title in T["saipos"]:
        w(f'''                    <a class="tile" href="{SP}{path}" target="_blank" rel="noopener">
                        <span class="tile-top tile-green">{ic("doc")}<span>{g(tag)}</span></span>
                        <span class="tile-body"><strong>{e(g(title))}</strong><small>{t("saipos_meta")}{t("in_pt")}</small><em>{t("read_article")}</em></span>
                    </a>''')
    w('                </div>')
    for key, items in (("strat_title", [(i, None, n) for i, n in T["strat"]]), ("social_title", T["social"])):
        w(f'\n                <h3 class="sub-title">{t(key)}</h3>\n                <div class="rail rail-embed">')
        for pid, tag, name in items:
            w(f'''                    <div class="embed-card">
                        <div class="embed-frame"><iframe src="{BE % pid}" title="{e(g(name))}" loading="lazy" allowfullscreen allow="clipboard-write" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
                        <div class="embed-info">{f'<span class="tag">{g(tag)}</span>' if tag else ""}<h4>{g(name)}</h4></div>
                    </div>''')
        w('                </div>')
    w(f'''            </div>
        </section>

        <section id="jornalismo">
            <div class="container">
                <p class="eyebrow">{t("jr_eyebrow")}</p>
                <h2 class="section-title">{t("jr_title")}</h2>
                <p class="section-lead">{t("jr_lead")}</p>
                <div class="filter-bar">''')
    for i, (val, lab) in enumerate(T["filters"]):
        w(f'                    <button type="button" class="filter-btn{" active" if i == 0 else ""}" data-filter="{val}" aria-pressed="{"true" if i == 0 else "false"}">{g(lab)}</button>')
    w('                </div>\n                <div class="rail rail-wrap">')
    sty = {"itatiaia": ("tile-red", "vote"), "politics": ("tile-blue", "city"), "sports": ("tile-navy", "ball")}
    for cat, href, tag, meta, title in T["stories"]:
        cls, icon = sty[cat]
        w(f'''                    <a class="tile journalism-card" data-category="{cat}" href="{href}" target="_blank" rel="noopener">
                        <span class="tile-top {cls}">{ic(icon)}<span>{g(tag)}</span></span>
                        <span class="tile-body"><strong>{e(g(title))}</strong><small>{meta}{t("in_pt")}</small><em>{t("read_story")}</em></span>
                    </a>''')
    w(f'''                </div>
                <a class="text-link" href="https://www.itatiaia.com.br/autor/alexandre-leite/" target="_blank" rel="noopener">{t("all_itatiaia")}</a>
            </div>
        </section>

        <section class="alt" id="internacional">
            <div class="container">
                <p class="eyebrow">{ {"pt": "EUA · 2025", "en": "USA · 2025", "es": "EE. UU. · 2025"}[lang] }</p>
                <h2 class="section-title">{ {"pt": "Intercâmbio internacional", "en": "International exchange", "es": "Intercambio internacional"}[lang] }</h2>
                <div class="photo-card">
                    <img src="assets/camp-stonewall.jpg" alt="{e(t("intl_alt"))}" loading="lazy" width="480" height="320">
                    <div>
                        <span class="tag">Camp Counselor · InterExchange</span>
                        <h4>{t("intl_name")}</h4>
                        <p>{t("intl_desc")}</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="formacao">
            <div class="container">
                <h2 class="section-title">{t("edu_title")}</h2>
                <div class="rail rail-cert">''')
    rest = []
    for name, org, desc, img in T["edu"]:
        if not img:
            rest.append((name, org))
            continue
        tag = f'<img src="assets/{img}" alt="{e(g(name))}" loading="lazy" width="300" height="212">'
        inner = f'{tag}<figcaption><strong>{g(name)}</strong><small>{g(org)}</small></figcaption>'
        w('                    <figure class="cert">' + (inner if img == "diploma-ufv.jpg" else f'<a href="assets/{img}" target="_blank" rel="noopener">{inner}</a>') + '</figure>')
    w(f'                </div>\n                <h3 class="sub-title">{t("more_cred")}</h3>\n                <ul class="cred-list">')
    for name, org in rest:
        w(f'                    <li><strong>{g(name)}</strong><span>{g(org)}</span></li>')
    w(f'''                </ul>
            </div>
        </section>

        <section class="alt" id="habilidades">
            <div class="container">
                <h2 class="section-title">{t("sk_title")}</h2>
                <div class="skill-groups">''')
    for i, (name, items) in enumerate(T["skills"]):
        w(f'                    <div class="skill-group">\n                        <h3><span class="ic-wrap">{ic(X["sk_ic"][i])}</span>{g(name)}</h3>\n                        <ul class="skill-tags">')
        for s in g(items):
            w(f'                            <li class="skill-tag">{s}</li>')
        w('                        </ul>\n                    </div>')
    w(f'''                </div>
            </div>
        </section>
{BLOG_SLOT if lang == "pt" else ""}    </main>

    <footer class="footer" id="contato">
        <div class="container">
            <h2 class="footer-title">{t("ct_title")}</h2>
            <p class="footer-desc">{t("ct_desc")}</p>
            <div class="footer-links">
                <a href="mailto:alexandreaugusto145@gmail.com" class="btn btn-light" onclick="copyEmail()">{t("email")}</a>
                <a href="https://api.whatsapp.com/send?phone=5531982034543" target="_blank" rel="noopener" class="btn btn-ghost">WhatsApp</a>
                <a href="https://www.linkedin.com/in/alexandreleitemkt/" target="_blank" rel="noopener" class="btn btn-ghost">LinkedIn</a>
                <a href="https://www.instagram.com/alexandreleite_mkt/" target="_blank" rel="noopener" class="btn btn-ghost">Instagram</a>
            </div>

            <details class="form-container" id="form-contato">
                <summary>{t("form_title")}</summary>
                <form id="waForm" onsubmit="sendWhatsApp(event)" data-template="{e(t("f_tpl"))}">
                    <div class="form-group">
                        <label for="waName">{t("f_name")}</label>
                        <input type="text" id="waName" autocomplete="name" placeholder="{t("f_name_ph")}" required>
                    </div>
                    <div class="form-group">
                        <label for="waPhone">{t("f_phone")}</label>
                        <input type="tel" id="waPhone" autocomplete="tel" placeholder="(XX) XXXXX-XXXX" required>
                    </div>
                    <div class="form-group">
                        <label for="waEmail">{t("f_email")}</label>
                        <input type="email" id="waEmail" autocomplete="email" placeholder="{t("f_email_ph")}" required>
                    </div>
                    <div class="form-group">
                        <label for="waReason">{t("f_reason")}</label>
                        <select id="waReason" required>
                            <option value="">{t("f_select")}</option>''')
    for op in T["f_opts"]:
        w(f'                            <option value="{e(g(op))}">{g(op)}</option>')
    w(f'''                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">{t("f_send")}</button>
                </form>
            </details>

            <div class="footer-bottom">
                <p>&copy; <span id="year">2026</span> | Alexandre Leite · Contagem, MG</p>
            </div>
        </div>
    </footer>

    <a href="#contato" class="fab fab-hidden" id="fab">{ic("chat")}{g(T["nav"][-1][1])}</a>

    <div id="emailToast" class="toast-notification" role="status" aria-live="polite">
        {t("toast")}
        <span>alexandreaugusto145@gmail.com</span>
    </div>

    <script src="script.js"></script>
</body>
</html>''')
    return "\n".join(o) + "\n"


with open(os.path.join(OUT, "index-pt.html"), "w", encoding="utf-8") as f:
    f.write('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n    <meta charset="UTF-8">\n    <title>Alexandre Leite</title>\n    <link rel="canonical" href="%s">\n    <meta http-equiv="refresh" content="0; url=./">\n    <meta name="robots" content="noindex">\n</head>\n<body>\n    <p><a href="./">Alexandre Leite — portfólio</a></p>\n</body>\n</html>\n' % BASE)
for lang in LANGS:
    with open(os.path.join(OUT, FILES[lang]), "w", encoding="utf-8") as f:
        f.write(build(lang))
    print(FILES[lang], "ok")

urls = "".join(
    f"  <url>\n    <loc>{BASE + ('' if l == 'pt' else FILES[l])}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
    + "".join(f'    <xhtml:link rel="alternate" hreflang="{T["htmllang"][m]}" href="{BASE + ("" if m == "pt" else FILES[m])}"/>\n' for m in LANGS)
    + "  </url>\n" for l in LANGS)
open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
g = lambda v: v["pt"] if isinstance(v, dict) else v
llms = ["# Alexandre Leite", "", "> " + X["bio"]["pt"], "",
        "Portfólio pessoal em português, inglês e espanhol. Contato: alexandreaugusto145@gmail.com · https://www.linkedin.com/in/alexandreleitemkt/", "",
        "## Páginas", f"- [Portfólio (português)]({BASE})", f"- [Portfolio (English)]({BASE}index-en.html)", f"- [Portafolio (español)]({BASE}index-es.html)", "",
        "## Resultados"] + [f"- {c['v']} {g(c['lab'])} — {g(c['co'])}. {g(c['res'])}" for c in T["cases"]] + ["", "## Experiência"] + \
       [f"- {g(j['role'])} — {g(j['co'])} ({g(j['date'])})" for j in T["jobs"]] + ["", "## Formação"] + \
       [f"- {g(n)} — {g(o)}" for n, o, d, i in T["edu"][:3]] + ["", "## Habilidades"] + [f"- {g(n)}: {', '.join(g(i))}" for n, i in T["skills"]] + \
       ["", "## Jornalismo", "- [Matérias na Rádio Itatiaia](https://www.itatiaia.com.br/autor/alexandre-leite/)"] + [f"- [{g(ti)}]({h})" for c, h, tg, m, ti in T["stories"]]
open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(llms) + "\n")
print("sitemap.xml robots.txt llms.txt ok")

import shutil
shutil.copy(os.path.join(HERE, "style.css"), os.path.join(OUT, "style.css"))
shutil.copy(os.path.join(HERE, "script.js"), os.path.join(OUT, "script.js"))
print("style.css script.js ok — agora rode: python3 tools/blog.py build")
