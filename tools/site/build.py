#!/usr/bin/env python3
"""Gera index.html (EN), index-pt.html e index-es.html a partir de um único conteúdo."""
import html, json, os, sys

OUT = sys.argv[1]
BASE = "https://alexandreleite-mkt.vercel.app/"
FILES = {"pt": "index.html", "en": "index-en.html", "es": "index-es.html"}
LANGS = ["pt", "en", "es"]
IT = "https://www.itatiaia.com.br/politica/eleicoes/"
FN = "https://ofutebolnewsreal.wordpress.com/2020/"
JV = "https://jornaldevicosa.home.blog/2020/"
SP = "https://saipos.com/"
BE = "https://www.behance.net/embed/project/%s?ilo0=1"

def L(pt, en, es):
    return {"pt": pt, "en": en, "es": es}

T = dict(
    htmllang=L("pt-BR", "en", "es"),
    title=L("Alexandre Leite | Marketing Digital, SEO, CRM e Jornalismo",
            "Alexandre Leite | Digital Marketing, SEO, CRM & Journalism",
            "Alexandre Leite | Marketing Digital, SEO, CRM y Periodismo"),
    desc=L("Portfólio de Alexandre Leite: profissional de marketing digital e jornalista com 5+ anos em mídia paga, SEO, CRM e conteúdo. Cases com resultados, matérias na Rádio Itatiaia e contato.",
           "Portfolio of Alexandre Leite: digital marketer and journalist with 5+ years in paid media, SEO, CRM and content. Case studies with results, Rádio Itatiaia stories and contact.",
           "Portafolio de Alexandre Leite: profesional de marketing digital y periodista con más de 5 años en medios pagos, SEO, CRM y contenido. Casos con resultados, notas en Rádio Itatiaia y contacto."),
    skip=L("Pular para o conteúdo", "Skip to content", "Saltar al contenido"),
    nav=[("sobre", L("Sobre", "About", "Sobre mí")), ("resultados", L("Resultados", "Results", "Resultados")),
         ("experiencia", L("Experiência", "Experience", "Experiencia")), ("projetos", L("Marketing", "Marketing", "Marketing")),
         ("jornalismo", L("Jornalismo", "Journalism", "Periodismo")), ("formacao", L("Formação", "Education", "Formación")),
         ("habilidades", L("Habilidades", "Skills", "Habilidades")), ("contato", L("Contato", "Contact", "Contacto"))],
    hero_eyebrow=L("Olá, eu sou", "Hello, I am", "Hola, soy"),
    hero_role=L("Marketing digital, SEO e CRM, com formação em jornalismo.",
                "Digital marketing, SEO and CRM, with a journalism degree.",
                "Marketing digital, SEO y CRM, con formación en periodismo."),
    hero_sub=L("Há mais de 5 anos cuido de mídia paga, SEO, CRM e conteúdo para SaaS B2B e pequenas empresas no Brasil e nos EUA. Escrevo os textos, roteiros e landing pages das minhas próprias campanhas.",
               "For 5+ years I have run paid media, SEO, CRM and content for B2B SaaS companies and small businesses in Brazil and the U.S. I write my own ad copy, video scripts and landing pages.",
               "Desde hace más de 5 años gestiono medios pagos, SEO, CRM y contenido para SaaS B2B y pequeñas empresas en Brasil y EE. UU. Escribo los textos, guiones y landing pages de mis propias campañas."),
    pills=[L("Contagem, MG · Brasil", "Contagem, MG · Brazil", "Contagem, MG · Brasil"),
           L("Português, inglês e espanhol", "Portuguese, English and Spanish", "Portugués, inglés y español")],
    pill_live=L("Disponível para início imediato", "Available to start immediately", "Disponible para empezar de inmediato"),
    cta_work=L("Ver resultados", "See results", "Ver resultados"),
    cta_contact=L("Entrar em contato", "Get in touch", "Contactar"),
    stats=[("+20%", L("conversão de lead em venda (Meta Wholesale, EUA)", "lead-to-sale conversion (Meta Wholesale, U.S.)", "conversión de lead a venta (Meta Wholesale, EE. UU.)")),
           ("+30%", L("posicionamento orgânico (Saipos, SaaS B2B)", "organic search rankings (Saipos, B2B SaaS)", "posicionamiento orgánico (Saipos, SaaS B2B)")),
           ("+30%", L("captação de novos clientes (projetos freelance)", "new-client acquisition (freelance projects)", "captación de nuevos clientes (proyectos freelance)")),
           ("250+", L("matérias assinadas na Rádio Itatiaia", "bylined stories at Rádio Itatiaia", "notas firmadas en Rádio Itatiaia"))],
    about_title=L("Sobre mim", "About me", "Sobre mí"),
    about=[L("Profissional de marketing digital com mais de 5 anos à frente de mídia paga, SEO, site e relatórios para a diretoria, sozinho ou com equipe enxuta.",
             "Digital marketer with 5+ years owning paid media, SEO, website and leadership reporting, solo or with a lean team.",
             "Profesional de marketing digital con más de 5 años al frente de medios pagos, SEO, sitio web e informes para la dirección, solo o con un equipo reducido."),
           L("Até agosto de 2026 gerenciei Meta Ads e Google Ads de uma revenda de veículos na Flórida, onde a conversão de lead em venda subiu 20%. Antes, cuidei de SEO e conteúdo na Saipos, SaaS B2B de gestão para restaurantes.",
             "Through August 2026 I ran Meta and Google Ads for a Florida car dealership, where lead-to-sale conversion rose 20%. Before that, I handled SEO and content at Saipos, a B2B SaaS for restaurant management.",
             "Hasta agosto de 2026 gestioné Meta Ads y Google Ads de una concesionaria de vehículos en Florida, donde la conversión de lead a venta subió un 20%. Antes me ocupé del SEO y el contenido en Saipos, un SaaS B2B de gestión para restaurantes."),
           L("Sou jornalista formado pela UFV e hoje cubro as Eleições 2026 para a Rádio Itatiaia. Também construo agentes de IA e automações para qualificar e distribuir leads.",
             "I hold a journalism degree from UFV and currently cover Brazil's 2026 elections for Rádio Itatiaia. I also build AI agents and automations to qualify and route leads.",
             "Soy periodista graduado en la UFV y hoy cubro las Elecciones 2026 de Brasil para Rádio Itatiaia. También construyo agentes de IA y automatizaciones para calificar y distribuir leads.")],
    focus=[L("SEO e GEO/AEO", "SEO & GEO/AEO", "SEO y GEO/AEO"), L("Conteúdo e inbound B2B", "Content & B2B inbound", "Contenido e inbound B2B"),
           L("Growth e mídia paga", "Growth & paid media", "Growth y medios pagos"), L("CRM e lifecycle", "CRM & lifecycle", "CRM y lifecycle"),
           L("IA aplicada ao marketing", "AI applied to marketing", "IA aplicada al marketing"), L("Jornalismo", "Journalism", "Periodismo")],
    res_eyebrow=L("Cases", "Case studies", "Casos"),
    res_title=L("Resultados", "Results", "Resultados"),
    res_lead=L("Quatro trabalhos recentes, com o contexto, o que eu fiz e o que mudou.",
               "Four recent pieces of work: the context, what I did and what changed.",
               "Cuatro trabajos recientes: el contexto, lo que hice y lo que cambió."),
    k_ctx=L("Contexto", "Context", "Contexto"), k_act=L("O que eu fiz", "What I did", "Lo que hice"), k_res=L("Resultado", "Result", "Resultado"),
    cases=[
        dict(v="+20%", lab=L("conversão de lead em venda", "lead-to-sale conversion", "conversión de lead a venta"),
             co=L("Meta Wholesale · Mídia paga, CRO e IA", "Meta Wholesale · Paid media, CRO & AI", "Meta Wholesale · Medios pagos, CRO e IA"),
             ctx=L("Revenda de veículos seminovos na Flórida. Eu respondia pela mídia paga, pela central de atendimento de leads (BDC) e pelos relatórios aos sócios.",
                   "Used-car dealership in Florida. I owned paid media, the lead-handling team (BDC) and reporting to the owners.",
                   "Concesionaria de vehículos seminuevos en Florida. Yo era responsable de los medios pagos, del equipo de atención de leads (BDC) y de los informes a los socios."),
             act=L("Reestruturei a conta de Meta Ads em campanhas por idioma (inglês e espanhol) com público aberto, refiz as landing pages, padronizei o follow-up dos vendedores e implantei um agente de IA conversacional que qualifica leads fora do horário comercial.",
                   "Rebuilt the Meta Ads account into language-based campaigns (English and Spanish) with broad targeting, rebuilt the landing pages, standardized the sales follow-up sequence and deployed a conversational AI agent that qualifies leads after hours.",
                   "Reestructuré la cuenta de Meta Ads en campañas por idioma (inglés y español) con público abierto, rehice las landing pages, estandaricé el seguimiento de los vendedores e implementé un agente de IA conversacional que califica leads fuera del horario comercial."),
             res=L("Conversão de lead em venda 20% maior, com relatório semanal de CAC, CPL e vendas por canal para os sócios.",
                   "Lead-to-sale conversion up 20%, with weekly CAC, CPL and sales-by-channel reporting to the owners.",
                   "Conversión de lead a venta un 20% mayor, con informe semanal de CAC, CPL y ventas por canal para los socios.")),
        dict(v="+30%", lab=L("posicionamento orgânico", "organic search rankings", "posicionamiento orgánico"),
             co=L("Saipos · SEO e conteúdo para SaaS B2B", "Saipos · SEO & content for B2B SaaS", "Saipos · SEO y contenido para SaaS B2B"),
             ctx=L("SaaS B2B de gestão para restaurantes, com modelo de receita recorrente.",
                   "B2B SaaS for restaurant management with a recurring-revenue model.",
                   "SaaS B2B de gestión para restaurantes, con modelo de ingresos recurrentes."),
             act=L("Fiz SEO técnico e de conteúdo, acompanhei no GA4 tráfego, tempo de sessão e pedidos de demonstração e transformei os dados em ajustes de conversão nas páginas-chave. Também escrevi a comunicação de lançamento de funcionalidades.",
                   "Ran technical and content SEO, tracked traffic, session duration and demo requests in GA4 and turned the data into conversion fixes on key pages. Also wrote launch communications for new features.",
                   "Hice SEO técnico y de contenido, seguí en GA4 el tráfico, el tiempo de sesión y las solicitudes de demostración y convertí los datos en ajustes de conversión en las páginas clave. También escribí la comunicación de lanzamiento de funcionalidades."),
             res=L("Posicionamento orgânico do site 30% melhor.", "Organic search rankings improved 30%.", "Posicionamiento orgánico del sitio un 30% mejor.")),
        dict(v="+30%", lab=L("captação de novos clientes", "new-client acquisition", "captación de nuevos clientes"),
             co=L("Ozen · Projetos freelance", "Ozen · Freelance projects", "Ozen · Proyectos freelance"),
             ctx=L("Projeto pessoal em parceria com um desenvolvedor, atendendo pequenas empresas de forma pontual. Eu era o único responsável por marketing e conteúdo.",
                   "Personal venture with a developer partner, serving small businesses on a project basis. I was the sole marketing and content lead.",
                   "Proyecto personal junto a un desarrollador, atendiendo a pequeñas empresas de forma puntual. Yo era el único responsable de marketing y contenido."),
             act=L("Geri Meta Ads e Google Ads de ponta a ponta, com testes A/B contínuos de ângulos, criativos e landing pages, e executei SEO técnico e on-page com arquitetura de conteúdo voltada a buscas de alta intenção comercial.",
                   "Managed Meta and Google Ads end to end, with continuous A/B tests on angles, creatives and landing pages, and ran technical and on-page SEO with a content architecture built around high-intent commercial searches.",
                   "Gestioné Meta Ads y Google Ads de principio a fin, con pruebas A/B continuas de ángulos, creatividades y landing pages, y ejecuté SEO técnico y on-page con una arquitectura de contenido orientada a búsquedas de alta intención comercial."),
             res=L("Captação de novos clientes 30% maior, combinando SEO, mídia paga e um novo site.",
                   "New-client acquisition up 30% through SEO, paid media and a rebuilt website.",
                   "Captación de nuevos clientes un 30% mayor, combinando SEO, medios pagos y un nuevo sitio.")),
        dict(v="250+", lab=L("matérias assinadas", "bylined stories", "notas firmadas"),
             co=L("Rádio Itatiaia · Eleições 2026", "Rádio Itatiaia · 2026 elections", "Rádio Itatiaia · Elecciones 2026"),
             ctx=L("Cobertura nacional das Eleições 2026 para a principal rede de rádio e notícias de Minas Gerais.",
                   "National coverage of Brazil's 2026 elections for the leading radio and news network in Minas Gerais.",
                   "Cobertura nacional de las Elecciones 2026 de Brasil para la principal red de radio y noticias de Minas Gerais."),
             act=L("Produzo perfis de candidatos, cobertura de debates, comparativos de planos de governo, pesquisas e apuração de vários estados, conferindo cada dado nos registros oficiais do TSE.",
                   "I produce candidate profiles, debate coverage, platform comparisons, polling and results stories across several states, checking every data point against official electoral court (TSE) records.",
                   "Produzco perfiles de candidatos, cobertura de debates, comparativos de planes de gobierno, encuestas y resultados de varios estados, verificando cada dato en los registros oficiales del tribunal electoral (TSE)."),
             res=L("Mais de 250 matérias publicadas e um manual editorial (hierarquia de fontes, checagem de dados, links internos para SEO) adotado pela equipe.",
                   "250+ published stories and a set of editorial guidelines (source hierarchy, fact-checking, SEO internal linking) adopted by the team.",
                   "Más de 250 notas publicadas y un manual editorial (jerarquía de fuentes, verificación de datos, enlaces internos para SEO) adoptado por el equipo.")),
    ],
    exp_title=L("Experiência", "Experience", "Experiencia"),
    jobs=[
        dict(role=L("Jornalista freelancer · Eleições 2026", "Freelance Journalist · 2026 Brazilian Elections", "Periodista freelance · Elecciones 2026"),
             co=L("Rádio Itatiaia · remoto", "Rádio Itatiaia · remote", "Rádio Itatiaia · remoto"),
             date=L("ago/2026 – atual", "Aug 2026 – Present", "ago. 2026 – actualidad"),
             ctx=L("", "Leading radio and news network in Minas Gerais, Brazil.", "Principal red de radio y noticias de Minas Gerais, Brasil."),
             b=[L("Produzo perfis de candidatos, cobertura de debates e matérias de pesquisas eleitorais de vários estados, conferindo cada dado nos registros oficiais do TSE.",
                  "Produce candidate profiles, debate coverage and polling stories across several states, checking every data point against official electoral court (TSE) records.",
                  "Produzco perfiles de candidatos, cobertura de debates y notas de encuestas electorales de varios estados, verificando cada dato en los registros oficiales del TSE."),
                L("Escrevi o manual editorial da cobertura (hierarquia de fontes, checagem de dados, links internos para SEO), adotado pela equipe.",
                  "Wrote the coverage's editorial guidelines (source hierarchy, fact-checking, SEO internal linking), adopted by the team.",
                  "Escribí el manual editorial de la cobertura (jerarquía de fuentes, verificación de datos, enlaces internos para SEO), adoptado por el equipo.")]),
        dict(role=L("Gerente de Marketing e BDC", "Marketing & BDC Manager", "Gerente de Marketing y BDC"),
             co=L("Meta Wholesale · Pompano Beach, EUA (remoto)", "Meta Wholesale · Pompano Beach, FL (remote)", "Meta Wholesale · Pompano Beach, EE. UU. (remoto)"),
             date=L("jan/2026 – ago/2026", "Jan 2026 – Aug 2026", "ene. 2026 – ago. 2026"),
             ctx=L("Revenda de veículos seminovos. Respondia pela mídia paga, pela central de atendimento de leads (BDC) e pelos relatórios aos sócios.",
                   "Used-car dealership. Owned paid media, the lead-handling team (BDC) and reporting to the owners.",
                   "Concesionaria de vehículos seminuevos. Responsable de los medios pagos, del equipo de atención de leads (BDC) y de los informes a los socios."),
             b=[L("Reestruturei a conta de Meta Ads, trocando campanhas separadas por vendedor por campanhas por idioma (inglês e espanhol) com público aberto, o que concentrou verba e dados de aprendizado.",
                  "Rebuilt the Meta Ads account from per-salesperson campaigns into language-based campaigns (English and Spanish) with broad targeting, concentrating budget and learning data.",
                  "Reestructuré la cuenta de Meta Ads, cambiando campañas separadas por vendedor por campañas por idioma (inglés y español) con público abierto, lo que concentró presupuesto y datos de aprendizaje."),
                L("Aumentei em 20% a conversão de lead em venda ao refazer as landing pages e padronizar a sequência de follow-up dos vendedores.",
                  "Raised lead-to-sale conversion 20% by rebuilding landing pages and standardizing the sales team's follow-up sequence.",
                  "Aumenté un 20% la conversión de lead a venta al rehacer las landing pages y estandarizar la secuencia de seguimiento de los vendedores."),
                L("Implantei e treinei um agente de IA conversacional (Sophia AI) que qualifica leads fora do horário comercial, dá suporte à equipe de vendas e agenda as visitas dos clientes à loja.",
                  "Deployed and trained a conversational AI agent (Sophia AI) that qualifies leads after hours, supports the sales team and books customer visits to the store.",
                  "Implementé y entrené un agente de IA conversacional (Sophia AI) que califica leads fuera del horario comercial, apoya al equipo de ventas y agenda las visitas de los clientes a la tienda."),
                L("Criei campanha de reativação de clientes inativos a partir da base do CRM, com segmentação e sequência de contato próprias.",
                  "Built a win-back campaign for inactive customers from the CRM base, with its own segmentation and contact sequence.",
                  "Creé una campaña de reactivación de clientes inactivos a partir de la base del CRM, con segmentación y secuencia de contacto propias."),
                L("Enviava relatório semanal de CAC, CPL e vendas por canal aos sócios e usava esses dados para redistribuir a verba entre Meta e Google.",
                  "Reported CAC, CPL and sales by channel to the owners every week and used that data to shift budget between Meta and Google.",
                  "Enviaba un informe semanal de CAC, CPL y ventas por canal a los socios y usaba esos datos para redistribuir el presupuesto entre Meta y Google.")]),
        dict(role=L("Head de Marketing e Conteúdo (único responsável pela área, freelancer)", "Head of Marketing & Content (sole marketing lead, freelance)", "Head de Marketing y Contenido (único responsable del área, freelance)"),
             co=L("Ozen (projetos freelance) · remoto", "Ozen (freelance projects) · remote", "Ozen (proyectos freelance) · remoto"),
             date=L("abr/2023 – jan/2026", "Apr 2023 – Jan 2026", "abr. 2023 – ene. 2026"),
             ctx=L("Projeto pessoal em parceria com um desenvolvedor, atendendo pequenas empresas de forma pontual. Em paralelo à Saipos até mar/2024.",
                   "Personal venture with a developer partner, serving small businesses on a project basis. Part-time alongside Saipos until Mar 2024.",
                   "Proyecto personal junto a un desarrollador, atendiendo a pequeñas empresas de forma puntual. En paralelo a Saipos hasta mar. 2024."),
             b=[L("Aumentei em 30% a captação de novos clientes combinando SEO, mídia paga e um novo site.",
                  "Grew new-client acquisition 30% through SEO, paid media and a rebuilt website.",
                  "Aumenté un 30% la captación de nuevos clientes combinando SEO, medios pagos y un nuevo sitio."),
                L("Geri Meta Ads e Google Ads de ponta a ponta, com testes A/B contínuos de ângulos, criativos e landing pages para reduzir o custo de aquisição.",
                  "Managed Meta and Google Ads end to end, running continuous A/B tests on ad angles, creatives and landing pages to lower acquisition cost.",
                  "Gestioné Meta Ads y Google Ads de principio a fin, con pruebas A/B continuas de ángulos, creatividades y landing pages para reducir el costo de adquisición."),
                L("Executei SEO técnico e on-page, com arquitetura de conteúdo voltada a buscas de alta intenção comercial.",
                  "Ran technical and on-page SEO with a content architecture built around high-intent commercial searches.",
                  "Ejecuté SEO técnico y on-page, con una arquitectura de contenido orientada a búsquedas de alta intención comercial.")]),
        dict(role=L("Analista de Conteúdo (promovido de Redator de Conteúdo Web em out/2022)", "Content Analyst (promoted from Web Content Writer, Oct 2022)", "Analista de Contenido (ascendido desde Redactor de Contenido Web en oct. 2022)"),
             co=L("Saipos · remoto", "Saipos · remote", "Saipos · remoto"),
             date=L("abr/2022 – mar/2024", "Apr 2022 – Mar 2024", "abr. 2022 – mar. 2024"),
             ctx=L("SaaS B2B de gestão para restaurantes, modelo de receita recorrente.", "B2B SaaS for restaurant management, recurring-revenue model.", "SaaS B2B de gestión para restaurantes, modelo de ingresos recurrentes."),
             b=[L("Melhorei em 30% o posicionamento orgânico do site com SEO técnico e conteúdo.",
                  "Improved organic search rankings 30% through technical SEO and content.",
                  "Mejoré un 30% el posicionamiento orgánico del sitio con SEO técnico y contenido."),
                L("Acompanhei no GA4 as métricas do SaaS (tráfego, tempo de sessão, pedidos de demonstração) e transformei os dados em ajustes de conversão nas páginas-chave.",
                  "Tracked SaaS metrics in GA4 (traffic, session duration, demo requests) and turned them into conversion fixes on key pages.",
                  "Seguí en GA4 las métricas del SaaS (tráfico, tiempo de sesión, solicitudes de demostración) y convertí los datos en ajustes de conversión en las páginas clave."),
                L("Apoiei ações de retenção e redução de churn com conteúdo e comunicação para a base de clientes.",
                  "Supported retention and churn-reduction efforts with content and customer communications.",
                  "Apoyé acciones de retención y reducción de churn con contenido y comunicación para la base de clientes."),
                L("Escrevi a comunicação de lançamento de funcionalidades do produto.",
                  "Wrote launch communications for new product features.",
                  "Escribí la comunicación de lanzamiento de funcionalidades del producto.")]),
    ],
    proj_title=L("Projetos próprios", "Own projects", "Proyectos propios"),
    projs=[("Agenciamo", L("CRM SaaS B2B com SDR de IA para agências de marketing imobiliário (atual). Criei o fluxo de lead scoring (BANT) em n8n, a landing page e o playbook de anúncios no Meta.",
                           "B2B SaaS CRM with an AI SDR for real estate marketing agencies (ongoing). Built the n8n lead-scoring workflow (BANT), the landing page and the Meta Ads playbook.",
                           "CRM SaaS B2B con SDR de IA para agencias de marketing inmobiliario (actual). Creé el flujo de lead scoring (BANT) en n8n, la landing page y el playbook de anuncios en Meta.")),
           ("Fluvia", L("SaaS de cálculo hidráulico para engenheiros civis. Fiz a análise de concorrentes, a estratégia de conteúdo orgânico e a landing page.",
                        "Hydraulic calculation SaaS for civil engineers. Ran the competitor analysis, organic content strategy and landing page.",
                        "SaaS de cálculo hidráulico para ingenieros civiles. Hice el análisis de competidores, la estrategia de contenido orgánico y la landing page."))],
    other_title=L("Outras experiências", "Other experience", "Otras experiencias"),
    others=[("TFLA Idiomas", L("Professor de inglês", "English Teacher", "Profesor de inglés"), L("jan/2026 – atual", "Jan 2026 – Present", "ene. 2026 – actualidad")),
            ("Fazza Motors", L("BDR (pré-vendas, setor automotivo)", "BDR (sales development, automotive)", "BDR (preventa, sector automotriz)"), L("ago/2025 – jan/2026", "Aug 2025 – Jan 2026", "ago. 2025 – ene. 2026")),
            ("Camp Stonewall, EUA", L("Camp Counselor (intercâmbio cultural)", "Camp Counselor (cultural exchange program)", "Camp Counselor (intercambio cultural)"), L("jun/2025 – ago/2025", "Jun 2025 – Aug 2025", "jun. 2025 – ago. 2025")),
            ("Nilo Lima Fotografia", L("Copywriter, depois Copywriter Pleno", "Copywriter, then Mid-level Copywriter", "Copywriter, luego Copywriter Semi-Senior"), L("dez/2020 – mar/2022", "Dec 2020 – Mar 2022", "dic. 2020 – mar. 2022")),
            ("O Melhor do Futebol", L("Repórter esportivo freelancer", "Freelance Sports Reporter", "Reportero deportivo freelance"), L("set/2021 – mai/2022", "Sep 2021 – May 2022", "sep. 2021 – may. 2022")),
            ("Jornal de Viçosa (UFV)", L("Jornalista, projeto de extensão", "Journalist, university outreach project", "Periodista, proyecto de extensión"), L("mai/2020 – set/2020", "May 2020 – Sep 2020", "may. 2020 – sep. 2020")),
            ("FutebolNews", L("Redator esportivo freelancer", "Freelance Sports Writer", "Redactor deportivo freelance"), L("mar/2020 – jun/2020", "Mar 2020 – Jun 2020", "mar. 2020 – jun. 2020")),
            ("Rádio Universitária 100,7 FM (UFV)", L("Âncora e comentarista esportivo", "Sports Anchor & Commentator", "Presentador y comentarista deportivo"), L("jul/2018 – fev/2020", "Jul 2018 – Feb 2020", "jul. 2018 – feb. 2020"))],
    mk_eyebrow=L("Portfólio", "Portfolio", "Portafolio"),
    mk_title=L("Marketing e SEO", "Marketing & SEO", "Marketing y SEO"),
    mk_lead=L("Artigos de SEO publicados, estratégias, copy e projetos de mídias sociais.",
              "Published SEO articles, strategy, copy and social media projects.",
              "Artículos de SEO publicados, estrategias, copy y proyectos de redes sociales."),
    saipos_title=L("SEO e inbound para SaaS B2B (Saipos)", "SEO & inbound for B2B SaaS (Saipos)", "SEO e inbound para SaaS B2B (Saipos)"),
    saipos_meta=L("Conteúdo SEO · Saipos", "SEO content · Saipos", "Contenido SEO · Saipos"),
    read_article=L("Ler artigo ↗", "Read article ↗", "Leer artículo ↗"),
    read_story=L("Ler matéria ↗", "Read story ↗", "Leer nota ↗"),
    in_pt=L("", " · in Portuguese", " · en portugués"),
    saipos=[("cardapio-digital/marketing/estrategias-de-marketing-de-relacionamento", L("Marketing de retenção B2B", "B2B retention marketing", "Marketing de retención B2B"),
             L("Fidelização de clientes: como conquistar e manter os seus", "Customer loyalty: how to win and keep yours", "Fidelización de clientes: cómo conquistar y mantener los tuyos")),
            ("sistema/lanchonete/montar-lanchonete/analise-de-mercado-de-uma-lanchonete", L("Estratégia de mercado B2B", "B2B market strategy", "Estrategia de mercado B2B"),
             L("Análise do mercado de lanchonetes 2025: vale a pena investir?", "Snack bar market analysis 2025: is it worth investing?", "Análisis del mercado de cafeterías 2025: ¿vale la pena invertir?")),
            ("cardapio-digital/marketing/crm-restaurante", L("SaaS, tecnologia e gestão", "SaaS, tech & management", "SaaS, tecnología y gestión"),
             L("CRM para restaurantes: como usar e os benefícios do sistema", "CRM for restaurants: how to use it and the system's benefits", "CRM para restaurantes: cómo usarlo y los beneficios del sistema")),
            ("sistema/restaurante/vendas-na-copa-do-mundo", L("Vendas e eventos sazonais", "Sales & seasonal events", "Ventas y eventos estacionales"),
             L("Vendas na Copa do Mundo: 8 estratégias para vencer a concorrência", "World Cup sales: 8 strategies to beat the competition", "Ventas en la Copa del Mundo: 8 estrategias para vencer a la competencia"))],
    strat_title=L("Estratégia e redação", "Strategy and copywriting", "Estrategia y redacción"),
    social_title=L("Estratégia de mídias sociais", "Social media strategy", "Estrategia de redes sociales"),
    swipe=L("Deslize para ver mais →", "Swipe to see more →", "Desliza para ver más →"),
    strat=[("221741271", L("Redação de Conteúdo SEO", "SEO Content Writing", "Redacción de Contenido SEO")),
           ("216158925", L("Copywriting para Landing Pages", "High-Converting Landing Page Copy", "Copywriting para Landing Pages")),
           ("214013391", L("Planejamento Estratégico Digital", "Strategic Digital Planning", "Planificación Estratégica Digital")),
           ("214355161", L("Criação e Design de E-books", "E-book Design and Content Creation", "Creación y Diseño de E-books"))],
    social=[("208116689", L("Educação", "Education", "Educación"), L("Professor de Inglês", "English Teacher", "Profesor de Inglés")),
            ("214010573", L("Saúde", "Healthcare", "Salud"), L("Fisioterapia", "Physiotherapy", "Fisioterapia")),
            ("208140079", L("Gastronomia", "Gastronomy", "Gastronomía"), L("Negócios de Alimentação", "Food Business", "Negocios de Alimentación")),
            ("193703629", L("Comércio local", "Local business", "Comercio local"), L("Barbearia e Negócios Locais", "Barbershop & Local Business", "Barbería y Negocios Locales")),
            ("200509793", L("Jurídico", "Legal", "Jurídico"), L("Advocacia", "Law Firms", "Abogacía"))],
    jr_eyebrow=L("Reportagem", "Reporting", "Reportajes"),
    jr_title=L("Jornalismo", "Journalism", "Periodismo"),
    jr_lead=L("Cobertura das Eleições 2026 para a Rádio Itatiaia, além de política local e jornalismo esportivo.",
              "Coverage of Brazil's 2026 elections for Rádio Itatiaia, plus local politics and sports journalism.",
              "Cobertura de las Elecciones 2026 de Brasil para Rádio Itatiaia, además de política local y periodismo deportivo."),
    filters=[("itatiaia", L("Itatiaia · Eleições 2026", "Itatiaia · 2026 elections", "Itatiaia · Elecciones 2026")),
             ("politics", L("Política e cidade", "Politics & city", "Política y ciudad")),
             ("sports", L("Esporte", "Sports", "Deporte")),
             ("all", L("Todos", "All", "Todos"))],
    all_itatiaia=L("Ver todas as matérias na Itatiaia ↗", "See all stories on Itatiaia ↗", "Ver todas las notas en Itatiaia ↗"),
    stories=[
        ("itatiaia", IT + "saude-veja-o-que-propoem-os-principais-candidatos-ao-governo-de-minas/", L("Planos de governo", "Platform comparison", "Planes de gobierno"), "Rádio Itatiaia · 2026",
         L("Saúde: veja o que propõem os principais candidatos ao governo de Minas", "Health: what the main candidates for Minas Gerais governor propose", "Salud: qué proponen los principales candidatos al gobierno de Minas")),
        ("itatiaia", IT + "divida-e-propag-veja-o-que-propoem-os-principais-candidatos-ao-governo-de-minas/", L("Planos de governo", "Platform comparison", "Planes de gobierno"), "Rádio Itatiaia · 2026",
         L("Dívida e Propag: veja o que propõem os principais candidatos ao governo de Minas", "State debt and Propag: what the main candidates for Minas Gerais governor propose", "Deuda y Propag: qué proponen los principales candidatos al gobierno de Minas")),
        ("itatiaia", IT + "mansoes-e-apartamentos-de-luxo-os-imoveis-declarados-ao-tse-pelos-candidatos-ao-governo-de-mg/", L("Dados do TSE", "Electoral court data", "Datos del TSE"), "Rádio Itatiaia · 2026",
         L("Mansões e apartamentos de luxo: os imóveis declarados ao TSE pelos candidatos ao governo de MG", "Mansions and luxury apartments: the real estate candidates for Minas Gerais governor declared to the electoral court", "Mansiones y apartamentos de lujo: los inmuebles declarados al TSE por los candidatos al gobierno de MG")),
        ("itatiaia", IT + "do-gramado-as-urnas-veja-os-candidatos-ligados-ao-futebol-nas-eleicoes-de-2026/", L("Especial", "Feature", "Especial"), "Rádio Itatiaia · 2026",
         L("Do gramado às urnas: veja os candidatos ligados ao futebol nas eleições de 2026", "From the pitch to the polls: the football-linked candidates in the 2026 elections", "De la cancha a las urnas: los candidatos vinculados al fútbol en las elecciones de 2026")),
        ("itatiaia", IT + "veja-quais-foram-os-melhores-momentos-do-1o-debate-com-candidatos-ao-governo-de-mg/", L("Debates", "Debates", "Debates"), "Rádio Itatiaia · 2026",
         L("Veja quais foram os melhores momentos do 1º debate com candidatos ao governo de MG", "The highlights of the first debate between candidates for Minas Gerais governor", "Los mejores momentos del 1.er debate entre candidatos al gobierno de MG")),
        ("itatiaia", IT + "pesquisas/quaest-raquel-lyra-41-e-joao-campos-39-empatam-tecnicamente-no-1o-turno-em-pe/", L("Pesquisas eleitorais", "Polling", "Encuestas"), "Rádio Itatiaia · 2026",
         L("Quaest: Raquel Lyra (41%) e João Campos (39%) empatam tecnicamente no 1º turno em PE", "Quaest poll: Raquel Lyra (41%) and João Campos (39%) in a statistical tie in Pernambuco's first round", "Quaest: Raquel Lyra (41%) y João Campos (39%) en empate técnico en la 1.ª vuelta en PE")),
        ("itatiaia", IT + "sergio-moro-pl-e-eleito-governador-do-parana-no-1o-turno/", L("Apuração", "Election night", "Escrutinio"), "Rádio Itatiaia · 2026",
         L("Sergio Moro (PL) é eleito governador do Paraná no 1º turno", "Sergio Moro (PL) elected governor of Paraná in the first round", "Sergio Moro (PL) es elegido gobernador de Paraná en la 1.ª vuelta")),
        ("itatiaia", IT + "conheca-a-carreira-politica-de-flavio-bolsonaro-pre-candidato-a-presidencia/", L("Perfil de candidato", "Candidate profile", "Perfil de candidato"), "Rádio Itatiaia · 2026",
         L("Conheça a carreira política de Flávio Bolsonaro, pré-candidato à Presidência", "The political career of Flávio Bolsonaro, presidential pre-candidate", "Conoce la carrera política de Flávio Bolsonaro, precandidato a la Presidencia")),
        ("itatiaia", IT + "adesivo-eleitoral-no-carro-pode-anular-o-seguro-saiba-como-evitar-o-prejuizo/", L("Serviço", "Explainer", "Servicio"), "Rádio Itatiaia · 2026",
         L("Adesivo eleitoral no carro pode anular o seguro; saiba como evitar o prejuízo", "A campaign sticker on your car can void your insurance; how to avoid the loss", "Un adhesivo electoral en el auto puede anular el seguro; cómo evitar la pérdida")),
        ("politics", JV + "08/26/prefeito-de-vicosa-se-posiciona-sobre-peticao-para-cancelamento-de-rodizio-de-cpf/", L("Política e cidade", "Politics & city", "Política y ciudad"), "Jornal de Viçosa · 2020",
         L("Prefeito de Viçosa se posiciona sobre petição para cancelamento de rodízio de CPF", "Mayor of Viçosa takes a stand on petition to cancel the CPF rotation", "El alcalde de Viçosa se posiciona sobre la petición para cancelar la rotación por CPF")),
        ("politics", JV + "11/17/conheca-os-vereadores-e-prefeitos-eleitos-em-vicosa-e-cidades-vizinhas/", L("Política", "Politics", "Política"), "Jornal de Viçosa · 2020",
         L("Conheça os vereadores e prefeitos eleitos em Viçosa e cidades vizinhas", "Meet the councilors and mayors elected in Viçosa and neighboring cities", "Conoce a los concejales y alcaldes electos en Viçosa y ciudades vecinas")),
        ("politics", JV + "10/01/programa-vendedor-legal-normatiza-comercio-ambulante-em-vicosa/", L("Cidade e economia", "City & economy", "Ciudad y economía"), "Jornal de Viçosa · 2020",
         L("Programa \"Vendedor Legal\" normatiza comércio ambulante em Viçosa", "\"Vendedor Legal\" program regulates street vending in Viçosa", "El programa \"Vendedor Legal\" regula el comercio ambulante en Viçosa")),
        ("sports", FN + "06/22/alavancado-pelo-sucesso-do-manto-da-massa-atletico-chega-a-43-mil-socios/", L("Futebol brasileiro", "Brazilian football", "Fútbol brasileño"), "FutebolNews · 2020",
         L("Alavancado pelo sucesso do 'Manto da Massa', Atlético chega a 43 mil sócios", "Boosted by the success of 'Manto da Massa', Atlético reaches 43,000 members", "Impulsado por el éxito del 'Manto da Massa', Atlético llega a 43 mil socios")),
        ("sports", FN + "03/23/como-o-jogo-entre-atalanta-e-valencia-pode-ter-sido-responsavel-por-agravar-o-surto-do-coronavirus-na-italia/", L("Esporte e saúde", "Sports & health", "Deporte y salud"), "FutebolNews · 2020",
         L("Como o jogo entre Atalanta e Valencia pode ter agravado o surto do coronavírus na Itália", "How Atalanta vs Valencia may have worsened the coronavirus outbreak in Italy", "Cómo el partido Atalanta-Valencia pudo haber agravado el brote de coronavirus en Italia")),
        ("sports", FN + "06/22/a-corrida-pelo-titulo-da-la-liga-esta-totalmente-em-aberto-quem-leva-essa/", L("Futebol internacional", "International football", "Fútbol internacional"), "FutebolNews · 2020",
         L("A corrida pelo título da La Liga está totalmente em aberto: quem leva essa?", "The race for the La Liga title is wide open: who will take it?", "La carrera por el título de La Liga está totalmente abierta: ¿quién se lo lleva?")),
        ("sports", FN + "05/27/juninho-pernambucano-e-mesmo-o-maior-jogador-nordestino/", L("Opinião e análise", "Opinion & analysis", "Opinión y análisis"), "FutebolNews · 2020",
         L("Juninho Pernambucano é mesmo o maior jogador nordestino da história?", "Is Juninho Pernambucano really the greatest northeastern player in history?", "¿Es Juninho Pernambucano realmente el mejor jugador nordestino de la historia?")),
        ("sports", FN + "06/01/jornal-elege-20-piores-contratacoes-da-premier-league-brasileiros-estao-na-lista/", L("Futebol internacional", "International football", "Fútbol internacional"), "FutebolNews · 2020",
         L("Jornal elege 20 piores contratações da Premier League; brasileiros estão na lista", "Newspaper picks the 20 worst Premier League signings; Brazilians on the list", "Un diario elige los 20 peores fichajes de la Premier League; hay brasileños en la lista")),
    ],
    intl_title=L("Experiência internacional", "International experience", "Experiencia internacional"),
    intl_tag=L("Intercâmbio · Staff", "Exchange program · Staff", "Intercambio · Staff"),
    intl_name=L("Camp Stonewall, EUA", "Camp Stonewall, USA", "Camp Stonewall, EE. UU."),
    intl_desc=L("Vivência multicultural, liderança de grupos de jovens e comunicação diária integral em inglês.",
                "Multicultural experience, leading youth groups and full-time daily communication in English.",
                "Vivencia multicultural, liderazgo de grupos de jóvenes y comunicación diaria completa en inglés."),
    intl_alt=L("Alexandre Leite no Camp Stonewall, nos Estados Unidos", "Alexandre Leite at Camp Stonewall, United States", "Alexandre Leite en Camp Stonewall, Estados Unidos"),
    edu_title=L("Formação e certificados", "Education & certificates", "Formación y certificados"),
    see_cert=L("Ver certificado ↗", "View certificate ↗", "Ver certificado ↗"),
    edu=[(L("MBA em Marketing Digital e Vendas", "MBA in Digital Marketing and Sales", "MBA en Marketing Digital y Ventas"), "UniAmérica Descomplica · 2024", None, "cert-mba.jpg"),
         (L("Bacharelado em Comunicação Social / Jornalismo", "B.A. in Social Communication / Journalism", "Licenciatura en Comunicación Social / Periodismo"),
          L("UFV – Universidade Federal de Viçosa · 2018–2023", "UFV – Federal University of Viçosa · 2018–2023", "UFV – Universidad Federal de Viçosa · 2018–2023"), None, "diploma-ufv.jpg"),
         (L("Ensino médio técnico em Informática (com programação)", "Technical High School Diploma in Computer Science (programming)", "Bachillerato técnico en Informática (con programación)"), "IFMG", None, None),
         (L("EF SET English Certificate 66/100 (C1 Avançado)", "EF SET English Certificate 66/100 (C1 Advanced)", "EF SET English Certificate 66/100 (C1 Avanzado)"), "EF SET · 2025", None, "cert-efset.jpg"),
         (L("Formação em Copywriting", "Copywriting Certification", "Formación en Copywriting"), "O Novo Mercado · 2025", None, "cert-copywriting.jpg"),
         (L("Inbound Marketing", "Inbound Marketing", "Inbound Marketing"), "HubSpot Academy", None, None),
         (L("Storytelling", "Storytelling", "Storytelling"), "Santander Open Academy", None, None),
         (L("Certificações em Marketing Digital e Conteúdo", "Digital Marketing & Content Certifications", "Certificaciones en Marketing Digital y Contenido"), "Ion Interactive · 2020",
          L("CRO · Customer Success · Instagram Marketing · Gestão de Redes Sociais · Branding · WordPress · Inbound Marketing · Marketing de Conteúdo Avançado · Produção de Conteúdo · Revisão de Conteúdo para Web",
            "CRO · Customer Success · Instagram Marketing · Social Media Management · Branding · WordPress · Inbound Marketing · Advanced Content Marketing · Content Production · Web Content Review",
            "CRO · Customer Success · Instagram Marketing · Gestión de Redes Sociales · Branding · WordPress · Inbound Marketing · Marketing de Contenido Avanzado · Producción de Contenido · Revisión de Contenido Web"), None),
         (L("Programa de Intercâmbio Cultural Camp USA", "Camp USA Cultural Exchange Program", "Programa de Intercambio Cultural Camp USA"), "InterExchange & Camp Stonewall · 2025", None, "cert-campusa.jpg"),
         (L("Especialização em Jornalismo Esportivo (120h)", "Sports Journalism Specialization (120h)", "Especialización en Periodismo Deportivo (120 h)"), "Futebol Interativo · 2023", None, "cert-futebol-interativo.jpg"),
         (L("Experiência prática em clube profissional", "Practical experience at a professional club", "Experiencia práctica en un club profesional"), "Coimbra Sports · 2024", None, "cert-coimbra.jpg")],
    sk_title=L("Ferramentas e habilidades", "Tools & skills", "Herramientas y habilidades"),
    skills=[(L("Mídia paga", "Paid media", "Medios pagos"), L(["Meta Ads", "Google Ads", "Tráfego pago", "Testes A/B", "Testes de criativo"], ["Meta Ads", "Google Ads", "Paid traffic", "A/B testing", "Creative testing"], ["Meta Ads", "Google Ads", "Tráfico pago", "Pruebas A/B", "Pruebas de creatividades"])),
            (L("SEO e conteúdo", "SEO & content", "SEO y contenido"), L(["SEO técnico", "SEO on-page", "Pesquisa de palavras-chave", "Arquitetura de conteúdo", "GEO/AEO (buscas com IA)", "Copywriting", "Inbound marketing", "SEMrush", "WordPress"], ["Technical SEO", "On-page SEO", "Keyword research", "Content architecture", "GEO/AEO (AI search)", "Copywriting", "Inbound marketing", "SEMrush", "WordPress"], ["SEO técnico", "SEO on-page", "Investigación de palabras clave", "Arquitectura de contenido", "GEO/AEO (búsquedas con IA)", "Copywriting", "Inbound marketing", "SEMrush", "WordPress"])),
            (L("Conversão e dados", "Conversion & analytics", "Conversión y datos"), L(["CRO", "Landing pages", "GA4", "Google Search Console", "CAC e CPL", "Métricas de atribuição", "Dashboards", "SQL", "Power BI", "Excel"], ["CRO", "Landing pages", "GA4", "Google Search Console", "CAC & CPL", "Attribution metrics", "Dashboards", "SQL", "Power BI", "Excel"], ["CRO", "Landing pages", "GA4", "Google Search Console", "CAC y CPL", "Métricas de atribución", "Dashboards", "SQL", "Power BI", "Excel"])),
            (L("CRM e automação", "CRM & automation", "CRM y automatización"), L(["HubSpot", "Salesforce", "E-mail marketing", "Réguas de follow-up", "Lead scoring", "n8n", "IA conversacional", "Engenharia de prompt", "Asana"], ["HubSpot", "Salesforce", "Email marketing", "Follow-up sequences", "Lead scoring", "n8n", "Conversational AI", "Prompt engineering", "Asana"], ["HubSpot", "Salesforce", "Email marketing", "Secuencias de seguimiento", "Lead scoring", "n8n", "IA conversacional", "Ingeniería de prompts", "Asana"])),
            (L("Jornalismo", "Journalism", "Periodismo"), L(["Reportagem", "Checagem de dados", "Cobertura eleitoral", "Jornalismo esportivo", "Rádio e podcast", "Edição de texto"], ["Reporting", "Fact-checking", "Election coverage", "Sports journalism", "Radio & podcast", "Copy editing"], ["Reportajes", "Verificación de datos", "Cobertura electoral", "Periodismo deportivo", "Radio y podcast", "Edición de texto"])),
            (L("Idiomas", "Languages", "Idiomas"), L(["Português (nativo)", "Inglês (fluente)", "Espanhol (fluente)"], ["Portuguese (native)", "English (fluent)", "Spanish (fluent)"], ["Portugués (nativo)", "Inglés (fluido)", "Español (fluido)"]))],
    ct_title=L("Vamos conversar?", "Let's talk?", "¿Hablamos?"),
    ct_desc=L("Estou aberto a novas oportunidades em marketing e jornalismo, remotas ou na região de Belo Horizonte.",
              "I am open to new opportunities in marketing and journalism, remote or in the Belo Horizonte area.",
              "Estoy abierto a nuevas oportunidades en marketing y periodismo, remotas o en la región de Belo Horizonte."),
    email=L("E-mail", "Email", "Correo"),
    form_title=L("Deixe uma mensagem", "Leave a message", "Deja un mensaje"),
    f_name=L("Nome completo", "Full name", "Nombre completo"), f_name_ph=L("Seu nome", "Your name", "Tu nombre"),
    f_phone=L("Telefone / WhatsApp", "Phone / WhatsApp", "Teléfono / WhatsApp"),
    f_email=L("E-mail", "Email", "Correo electrónico"), f_email_ph=L("seuemail@exemplo.com", "you@example.com", "tucorreo@ejemplo.com"),
    f_reason=L("Motivo do contato", "Reason for contact", "Motivo del contacto"), f_select=L("Selecione uma opção...", "Select an option...", "Selecciona una opción..."),
    f_opts=[L("Proposta de emprego / oportunidade", "Job offer / opportunity", "Propuesta de empleo / oportunidad"),
            L("Projeto freelance / consultoria", "Freelance project / consulting", "Proyecto freelance / consultoría"),
            L("Networking", "Networking", "Networking")],
    f_send=L("Enviar pelo WhatsApp", "Send via WhatsApp", "Enviar por WhatsApp"),
    f_tpl=L("Olá! Meu nome é {name}.\nTelefone: {phone}\nE-mail: {email}\nMotivo do contato: {reason}",
            "Hello! My name is {name}.\nPhone: {phone}\nEmail: {email}\nReason for contact: {reason}",
            "¡Hola! Mi nombre es {name}.\nTeléfono: {phone}\nCorreo: {email}\nMotivo del contacto: {reason}"),
    toast=L("E-mail copiado para a área de transferência!", "Email copied to clipboard!", "¡Correo copiado al portapapeles!"),
    photo_alt=L("Foto de Alexandre Leite", "Photo of Alexandre Leite", "Foto de Alexandre Leite"),
    jobtitle=L("Profissional de Marketing Digital e Jornalista", "Digital Marketer and Journalist", "Profesional de Marketing Digital y Periodista"),
)

e = lambda s: html.escape(s, quote=True)


def build(lang):
    g = lambda v: v[lang] if isinstance(v, dict) else v
    t = lambda k: g(T[k])
    url = BASE + ("" if lang == "pt" else FILES[lang])
    o = []
    w = o.append
    ld = {"@context": "https://schema.org", "@type": "Person", "name": "Alexandre Leite", "alternateName": "Alexandre Augusto de Oliveira Leite",
          "jobTitle": t("jobtitle"), "description": t("desc"), "url": url, "image": BASE + "assets/profile.jpg", "email": "mailto:alexandreaugusto145@gmail.com",
          "address": {"@type": "PostalAddress", "addressLocality": "Contagem", "addressRegion": "MG", "addressCountry": "BR"},
          "alumniOf": [{"@type": "CollegeOrUniversity", "name": "Universidade Federal de Viçosa (UFV)"}, {"@type": "CollegeOrUniversity", "name": "UniAmérica Descomplica"}],
          "knowsLanguage": ["pt-BR", "en", "es"],
          "knowsAbout": ["Digital Marketing", "SEO", "GEO/AEO", "Paid Media", "Meta Ads", "Google Ads", "CRM", "HubSpot", "Content Marketing", "Copywriting", "Journalism"],
          "sameAs": ["https://www.linkedin.com/in/alexandreleitemkt/", "https://www.instagram.com/alexandreleite_mkt/", "https://www.itatiaia.com.br/autor/alexandre-leite/", "https://github.com/alexx145"]}
    w(f'''<!DOCTYPE html>
<html lang="{t("htmllang")}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{e(t("title"))}</title>
    <meta name="description" content="{e(t("desc"))}">
    <meta name="author" content="Alexandre Leite">
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
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23004488'/%3E%3Ctext x='32' y='43' font-family='Arial,sans-serif' font-size='30' font-weight='700' text-anchor='middle' fill='white'%3EAL%3C/text%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
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
        w(f'                    <li><a href="#{hid}">{g(lab)}</a></li>')
    w('                </ul>\n            </nav>\n            <div class="lang-switcher">')
    for l2 in LANGS:
        w(f'                <a href="{FILES[l2]}" hreflang="{T["htmllang"][l2]}"{" class=\"active\" aria-current=\"page\"" if l2 == lang else ""}>{l2.upper()}</a>')
    w(f'''            </div>
        </div>
    </header>

    <main id="main">
        <section class="hero" id="home">
            <div class="container">
                <div class="hero-grid">
                    <img src="assets/profile.jpg" alt="{e(t("photo_alt"))}" class="hero-photo" width="280" height="280">
                    <div>
                        <p class="eyebrow">{t("hero_eyebrow")}</p>
                        <h1 class="hero-title">Alexandre Leite</h1>
                        <p class="hero-role">{t("hero_role")}</p>
                        <p class="hero-subtitle">{t("hero_sub")}</p>
                        <div class="hero-meta">
                            <span class="pill pill-live">{t("pill_live")}</span>''')
    for p in T["pills"]:
        w(f'                            <span class="pill">{g(p)}</span>')
    w(f'''                        </div>
                        <div class="hero-actions">
                            <a href="#resultados" class="btn btn-primary">{t("cta_work")}</a>
                            <a href="#contato" class="btn btn-secondary">{t("cta_contact")}</a>
                            <a href="https://www.linkedin.com/in/alexandreleitemkt/" target="_blank" rel="noopener" class="btn btn-secondary">LinkedIn ↗</a>
                        </div>
                    </div>
                </div>
                <div class="stats">''')
    for v, lab in T["stats"]:
        w(f'                    <div class="stat"><span class="stat-value">{v}</span><span class="stat-label">{g(lab)}</span></div>')
    w(f'''                </div>
            </div>
        </section>

        <section class="alt" id="sobre">
            <div class="container about-text reveal">
                <h2 class="section-title">{t("about_title")}</h2>''')
    for p in T["about"]:
        w(f'                <p>{g(p)}</p>')
    w('                <div class="focus-list">')
    for f in T["focus"]:
        w(f'                    <span class="pill">{g(f)}</span>')
    w(f'''                </div>
            </div>
        </section>

        <section id="resultados">
            <div class="container">
                <p class="eyebrow">{t("res_eyebrow")}</p>
                <h2 class="section-title">{t("res_title")}</h2>
                <p class="section-lead">{t("res_lead")}</p>
                <div class="case-grid">''')
    for c in T["cases"]:
        w(f'''                    <article class="case-card reveal">
                        <p class="case-company">{g(c["co"])}</p>
                        <p class="case-result">{c["v"]}</p>
                        <h3 class="case-result-label">{g(c["lab"])}</h3>
                        <dl>
                            <dt>{t("k_ctx")}</dt><dd>{g(c["ctx"])}</dd>
                            <dt>{t("k_act")}</dt><dd>{g(c["act"])}</dd>
                            <dt>{t("k_res")}</dt><dd>{g(c["res"])}</dd>
                        </dl>
                    </article>''')
    w(f'''                </div>
            </div>
        </section>

        <section class="alt" id="experiencia">
            <div class="container">
                <h2 class="section-title">{t("exp_title")}</h2>
                <div class="timeline">''')
    for j in T["jobs"]:
        w(f'''                    <article class="job reveal">
                        <div class="job-head">
                            <h3 class="job-role">{g(j["role"])}</h3>
                            <span class="job-date">{g(j["date"])}</span>
                        </div>
                        <p class="job-company">{g(j["co"])}</p>''')
        if g(j["ctx"]):
            w(f'                        <p class="job-ctx">{g(j["ctx"])}</p>')
        w('                        <ul>')
        for b in j["b"]:
            w(f'                            <li>{g(b)}</li>')
        w('                        </ul>\n                    </article>')
    w(f'                </div>\n\n                <h3 class="sub-title">{t("proj_title")}</h3>\n                <div class="mini-list">')
    for n, d in T["projs"]:
        w(f'                    <div class="mini-item"><strong>{n}</strong> — {g(d)}</div>')
    w(f'                </div>\n\n                <details class="more">\n                <summary>{t("other_title")} ({len(T["others"])})</summary>\n                <div class="mini-list">')
    for n, r, d in T["others"]:
        w(f'                    <div class="mini-item"><strong>{n}</strong> — {g(r)}<span>{g(d)}</span></div>')
    w(f'''                </div>
                </details>
            </div>
        </section>

        <section id="projetos">
            <div class="container">
                <p class="eyebrow">{t("mk_eyebrow")}</p>
                <h2 class="section-title">{t("mk_title")}</h2>
                <p class="section-lead">{t("mk_lead")}</p>

                <h3 class="sub-title">{t("saipos_title")}</h3>
                <div class="card-grid">''')
    for path, tag, title in T["saipos"]:
        w(f'''                    <a class="link-card reveal" href="{SP}{path}" target="_blank" rel="noopener">
                        <span class="tag tag-green">{g(tag)}</span>
                        <h4>{e(g(title))}</h4>
                        <span class="card-meta">{t("saipos_meta")}{t("in_pt")}</span>
                        <span class="card-cta">{t("read_article")}</span>
                    </a>''')
    w('                </div>')
    for key, items in (("strat_title", [(i, None, n) for i, n in T["strat"]]), ("social_title", T["social"])):
        w(f'\n                <h3 class="sub-title">{t(key)}</h3>\n                <p class="swipe-hint">{t("swipe")}</p>\n                <div class="embed-row">')
        for pid, tag, name in items:
            w(f'''                    <div class="embed-card">
                        <div class="embed-frame"><iframe src="{BE % pid}" title="{e(g(name))}" loading="lazy" allowfullscreen allow="clipboard-write" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>
                        <div class="embed-info">{f'<span class="tag">{g(tag)}</span>' if tag else ""}<h4>{g(name)}</h4></div>
                    </div>''')
        w('                </div>')
    w(f'''            </div>
        </section>

        <section class="alt" id="jornalismo">
            <div class="container">
                <p class="eyebrow">{t("jr_eyebrow")}</p>
                <h2 class="section-title">{t("jr_title")}</h2>
                <p class="section-lead">{t("jr_lead")}</p>
                <div class="filter-bar">''')
    for i, (val, lab) in enumerate(T["filters"]):
        w(f'                    <button type="button" class="filter-btn{" active" if i == 0 else ""}" data-filter="{val}" aria-pressed="{"true" if i == 0 else "false"}">{g(lab)}</button>')
    w('                </div>\n                <div class="card-grid">')
    for cat, href, tag, meta, title in T["stories"]:
        w(f'''                    <a class="link-card journalism-card" data-category="{cat}" href="{href}" target="_blank" rel="noopener">
                        <span class="tag{" tag-red" if cat == "itatiaia" else ""}">{g(tag)}</span>
                        <h4>{e(g(title))}</h4>
                        <span class="card-meta">{meta}{t("in_pt")}</span>
                        <span class="card-cta">{t("read_story")}</span>
                    </a>''')
    w(f'''                </div>
                <a class="text-link" href="https://www.itatiaia.com.br/autor/alexandre-leite/" target="_blank" rel="noopener">{t("all_itatiaia")}</a>

                <h3 class="sub-title">{t("intl_title")}</h3>
                <div class="photo-card">
                    <img src="assets/camp-stonewall.jpg" alt="{e(t("intl_alt"))}" loading="lazy" width="480" height="320">
                    <div>
                        <span class="tag">{t("intl_tag")}</span>
                        <h4>{t("intl_name")}</h4>
                        <p>{t("intl_desc")}</p>
                    </div>
                </div>
            </div>
        </section>

        <section id="formacao">
            <div class="container">
                <h2 class="section-title">{t("edu_title")}</h2>
                <div class="edu-list">''')
    for name, org, desc, img in T["edu"]:
        w(f'                    <div class="edu-item">\n                        <h4>{g(name)}</h4>\n                        <p class="card-meta">{g(org)}</p>')
        if desc:
            w(f'                        <p class="desc">{g(desc)}</p>')
        if img:
            tag = f'<img class="cert-thumb" src="assets/{img}" alt="{e(g(name))}" loading="lazy" width="300" height="212">'
            w('                        ' + (tag if img == "diploma-ufv.jpg" else f'<a class="cert-link" href="assets/{img}" target="_blank" rel="noopener">{tag}</a>'))
        w('                    </div>')
    w(f'''                </div>
            </div>
        </section>

        <section class="alt" id="habilidades">
            <div class="container">
                <h2 class="section-title">{t("sk_title")}</h2>
                <div class="skill-groups">''')
    for name, items in T["skills"]:
        w(f'                    <div class="skill-group">\n                        <h4>{g(name)}</h4>\n                        <ul class="skill-tags">')
        for s in g(items):
            w(f'                            <li class="skill-tag">{s}</li>')
        w('                        </ul>\n                    </div>')
    w(f'''                </div>
            </div>
        </section>
    </main>

    <footer class="footer" id="contato">
        <div class="container">
            <h2 class="footer-title">{t("ct_title")}</h2>
            <p class="footer-desc">{t("ct_desc")}</p>
            <div class="footer-links">
                <a href="mailto:alexandreaugusto145@gmail.com" class="btn btn-primary" onclick="copyEmail()">{t("email")}</a>
                <a href="https://api.whatsapp.com/send?phone=5531982034543" target="_blank" rel="noopener" class="btn btn-secondary">WhatsApp</a>
                <a href="https://www.linkedin.com/in/alexandreleitemkt/" target="_blank" rel="noopener" class="btn btn-secondary">LinkedIn</a>
                <a href="https://www.instagram.com/alexandreleite_mkt/" target="_blank" rel="noopener" class="btn btn-secondary">Instagram</a>
            </div>

            <div class="form-container" id="form-contato">
                <h3>{t("form_title")}</h3>
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
            </div>

            <div class="footer-bottom">
                <p>&copy; <span id="year">2026</span> | Alexandre Leite · Contagem, MG</p>
            </div>
        </div>
    </footer>

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
