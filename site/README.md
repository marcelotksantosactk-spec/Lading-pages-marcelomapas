# Páginas puxadas da Hostinger (22/09/2026)

Backup de trabalho das páginas de venda que hoje vivem soltas em `public_html/` na Hostinger
(`marcelomapas.com`), puxado direto das URLs públicas — não é um mirror completo do servidor,
é só o que a gente precisa editar hoje: as páginas dos funis com CTR baixo (`constitucional`,
`processo-civil`, `carreiras-policiais`) e as duas versões do Penal (`penal` e `penal02`), a
prioridade da call de 21/09.

Cada arquivo é um `index.html` de página única (CSS e imagens embutidas ou referenciadas por URL
absoluta para `marcelomapas.com`), exatamente como está publicado — sem build, sem framework.

## Como isso volta pro ar

**Não tem deploy automático ainda.** `site/public_html/<produto>/index.html` aqui é o espelho de
`public_html/<produto>/index.html` na Hostinger. Depois de editar aqui, sobe o mesmo arquivo pelo
Gerenciador de Arquivos da Hostinger (ou FTP/SSH, se configurado), sobrescrevendo o `index.html`
da pasta correspondente. Ligar isso a deploy automático do GitHub é o próximo passo, não algo
que já existe.

## Não incluído aqui

Bump/upsell (`up.html`, `down.html`, `obrigado.html` de `carreiras-policiais/`), imagens soltas
(ex. `processo-civil/amostra-*.jpg`) e o resto de `public_html` (`enem`, `OAB02`, `pcma`, etc.).
Puxar quando precisar, mesmo processo.
