# Ferramentas do site

Site estático, sem banco de dados. Tudo é gerado por dois scripts Python (sem dependências).

## Portfólio (home em PT, EN e ES)

- Conteúdo: `tools/site/build.py` (dicionário `T`) e `tools/site/build2.py` (dicionário `X` e o template).
- Estilo e script: `tools/site/style.css` e `tools/site/script.js` (são copiados para a raiz).
- Gerar: `python3 tools/site/build2.py .` e depois `python3 tools/blog.py build`.

## Blog

- Cada artigo é um arquivo `blog/src/<slug>.json`. Campos: `slug`, `title`, `seo_title` (até 60),
  `description` (até 155), `date` (AAAA-MM-DD), `category` (SEO e IA, Marketing, CRM e automação,
  Jornalismo ou Carreira), `keywords`, `quick_answer` (40 a 60 palavras), `body_html`
  (h2 em forma de pergunta, h3, p, ul/ol, table, blockquote; sem h1), `faq` (3 a 8 itens `{q, a}`)
  e `updated` (opcional).
- Gerar: `python3 tools/blog.py build`. Ele valida os artigos e escreve só o que mudou:
  `blog/<slug>.html`, `blog/index.html`, `blog/feed.xml`, `sitemap.xml`, `llms.txt` e os 3 últimos
  artigos na home (`index.html`, entre os marcadores `<!--blog:start-->` e `<!--blog:end-->`).
- Cada artigo é uma página própria e leve (cerca de 17 KB, sem imagens além da foto do autor),
  então publicar todo dia não deixa a home nem o índice mais pesados. O índice pagina de 12 em 12.

## Agendar artigos

Artigo com `date` no futuro fica agendado: o `build` só publica artigos com data até hoje (horário de Brasília).
O GitHub Actions (`.github/workflows/publicar-blog.yml`) roda o `build` todo dia às 8h05 e faz o commit
sozinho quando um artigo agendado chega no dia. Também dá para rodar na mão em Actions > Publicar blog > Run workflow.

## Publicar

Enviar os arquivos alterados (`git status --short`) para a branch `main`. O Vercel publica sozinho.
Sem acesso por git, usar a página de upload do GitHub, uma pasta por vez:
`/upload/main` (raiz), `/upload/main/blog` e `/upload/main/blog/src`.
