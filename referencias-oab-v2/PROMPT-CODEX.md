# Prompt para o Codex — elementos visuais da página OAB (`/oab-v2/`)

Cole tudo abaixo da linha no Codex, com o repositório `~/marcelomapas-site` aberto.

---

## Contexto

Você vai completar a parte visual de uma página de vendas que **já está pronta e no ar**:
`https://marcelomapas.com/oab-v2/`, arquivo `public_html/oab-v2/index.html`.

O produto é o **Combo OAB 1ª Fase** do Marcelo Mapas: resumos ilustrados (mapas mentais,
esquemas, mnemônicos) das 16 disciplinas da primeira fase do Exame da OAB, em PDF. R$117.

A página é um **clone exato** da página de Carreiras Policiais do mesmo cliente
(`https://resumosmapasdireito.com/3-0/`), que é a que mais vende. Estrutura, CSS, ordem das
seções e textos já foram adaptados para OAB. **Não mexa em estrutura, copy, preço, oferta,
pixel, UTMify nem checkout.** O seu trabalho é só imagem e as tags `<img>` que apontam para ela.

Todas as referências estão em `~/marcelomapas-site/referencias-oab-v2/` (esta pasta).
Ela fica fora de `public_html/`, então não vai para o ar.

```
referencias-oab-v2/
├── PROMPT-CODEX.md                         ← este arquivo
├── 01-mockup/
│   ├── mockup-carreiras-ORIGINAL.webp      ← dobra da página de Carreiras (980×1225)
│   └── capa-livro-carreiras-RECORTE.png    ← recorte só do livro, para ver a capa de perto
├── 02-paginas-reais/                       ← páginas REAIS do material (não geradas)
│   ├── constitucional-direitos-fundamentais.webp
│   ├── administrativo-bens-publicos.webp
│   ├── penal-crime-impossivel.webp
│   ├── penal-lei-penal-no-espaco.webp
│   ├── penal-conflito-aparente-de-normas.webp
│   ├── penal-tempo-e-lugar-do-crime.webp
│   ├── penal-principios-e-fontes.webp
│   └── legislacao-especial-lei-13431.webp
└── 03-marca-e-bonus/
    ├── logo-marcelomapas.webp
    ├── capa-bonus-mnemonicos.webp
    ├── capa-bonus-manual-memorizacao.webp
    └── perfil-instagram-marcelomapas.webp
```

---

## Tarefa 1 (a principal): mockup da OAB para a dobra

**Hoje:** a dobra da `/oab-v2/` mostra uma página solta de Direito Penal
(`public_html/oab-v2/img/01.webp`, 716×1012), porque o mockup de Carreiras não serve: tem um
livro escrito "CARREIRA POLICIAL" com um soldado da SWAT na capa.

**Quero:** a mesma cena de `01-mockup/mockup-carreiras-ORIGINAL.webp`, com o livro trocado por
um livro da OAB. Abra a referência e o recorte antes de começar.

### O que fica igual à referência

- Composição inteira: monitor com páginas na tela, pilha de folhas impressas à esquerda, uma
  folha solta em pé na frente, livro em pé à direita, atrás da folha solta.
- Enquadramento, ângulo, luz, sombras e o fundo creme liso (RGB ≈ 247, 240, 229, `#F7F0E5`).
  O fundo tem que emendar com a seção da página, sem borda nem vinheta.
- Tamanho final: **980×1225 px**, WebP, **até 200 KB**.

### O que muda: só a capa do livro

Mantenha o **layout** da capa de Carreiras (veja o recorte): faixa branca no alto com o nome,
tarja amarela "RESUMOS", palavra "MAPEADOS" embaixo, lista curta à esquerda, `@marcelomapas`
no rodapé, fundo escuro com uma figura em meio-tom preto e branco.

Troque:

| Elemento | Carreiras (hoje) | OAB (novo) |
|---|---|---|
| Faixa branca do alto | CARREIRA POLICIAL | **EXAME DA OAB · 1ª FASE** |
| Tarja amarela | RESUMOS | **RESUMOS** (igual) |
| Abaixo da tarja | MAPEADOS | **MAPEADOS** (igual) |
| Figura | Policial da SWAT com fuzil | **Advogado ou advogada de terno escuro**, meio corpo, segurando um Vade Mecum ou pasta, luz dramática lateral, mesmo tratamento P&B de alto contraste. Alternativa se a figura humana ficar ruim: **balança da justiça** grande, no mesmo tratamento |
| Lista à esquerda | Noções de direito / leis especiais / Português / Informática | **16 disciplinas / Ética da OAB / Legislação especial / 500 questões** |
| Rodapé | @marcelomapas | **@marcelomapas** (igual) |

Proibido na capa:
- **Brasão, selo ou logotipo oficial da OAB** (Ordem dos Advogados do Brasil). A página diz que
  o material não tem vínculo com a OAB; o selo diria o contrário.
- Qualquer promessa: "aprovação garantida", "passe na OAB", número de aprovados.
- Arma, farda ou qualquer elemento policial que sobre da referência.

### Como fazer (em ordem de preferência)

1. **Editar a imagem de referência, não gerar do zero.** Use edição com máscara (inpainting)
   só na região do livro, que fica mais ou menos em `x 640–975, y 240–790` da imagem original.
   Assim o monitor, as folhas e a luz ficam idênticos.
2. Se a edição não segurar o texto da capa legível, **gere a capa sozinha** como imagem plana
   (frontal, ~600×900) e **aplique no livro por perspectiva** (4 pontos, com Pillow, OpenCV ou
   ImageMagick), preservando a lombada e a sombra do livro original.
3. Só em último caso gere a cena toda de novo, usando a referência como imagem de entrada.

**Texto da capa tem que sair perfeito**: soletrado certo, com acento ("1ª FASE"), sem letra
inventada. Se o gerador errar o texto, escreva o texto por cima com fonte de verdade
(Montserrat 800/900, já usada na página) e só use a IA para a figura e o fundo da capa.

**As páginas que aparecem no monitor e nas folhas não precisam mudar.** São de Direito Penal,
que também cai na OAB. Se quiser trocar a folha da frente, use uma página real de
`02-paginas-reais/` aplicada por perspectiva. **Nunca gere com IA uma página do material**:
seria mostrar ao comprador um conteúdo que não existe no produto.

### Onde aplicar

- Salve como `public_html/oab-v2/img/01.webp` (substitui a página de Penal que está lá).
- Em `index.html`, na `<img src="img/01.webp" ...>` da dobra (dentro de `.hero-amostra`):
  - `width="980" height="1225"`
  - `alt="Material ilustrado para a 1ª fase da OAB no computador, impresso e em livro"`
- Guarde a capa plana em `referencias-oab-v2/01-mockup/capa-livro-oab.png` para reuso em
  criativo de anúncio.

---

## Tarefa 2: variar as páginas do carrossel "Veja algumas das páginas"

**Hoje:** o carrossel (`#tiraVp`, cada item é um `<figure class="tira-card amt-item" data-i="N">`)
tem 6 páginas, e 4 são de Direito Penal. Para quem vai fazer OAB, parece material de uma
matéria só.

**Quero:** 6 páginas, com no máximo 2 de Penal. Use **somente** arquivos de
`02-paginas-reais/`. Ordem sugerida:

| data-i | Arquivo | Título (`figcaption`) | Linha de baixo (`<span>`) |
|---|---|---|---|
| 0 | constitucional-direitos-fundamentais.webp | Direitos e Garantias Fundamentais | Direito Constitucional |
| 1 | penal-lei-penal-no-espaco.webp (= img/04.webp atual) | Lei Penal no Espaço | Direito Penal · Parte Geral |
| 2 | administrativo-bens-publicos.webp | Bens Públicos e Desafetação | Direito Administrativo |
| 3 | penal-crime-impossivel.webp | Crime Impossível | Direito Penal · Parte Geral |
| 4 | legislacao-especial-lei-13431.webp (= img/09.webp atual) | Lei nº 13.431/2017 | Legislação Especial |
| 5 | penal-tempo-e-lugar-do-crime.webp (= img/06.webp atual) | Tempo e Lugar do Crime | Direito Penal · Parte Geral |

Regras:
- **Abra cada imagem e confira que o título bate com o que está escrito na página.** Não
  confie no nome do arquivo.
- Copie as novas para `public_html/oab-v2/img/` com nome curto (`pg-const.webp`, `pg-adm.webp`,
  `pg-penal-ci.webp`) e reexporte para ~707×1000 se forem maiores, WebP até 150 KB.
- Atualize em cada `<figure>`: `src`, `alt` ("Amostra real do material — {título}"),
  `aria-label` ("Ampliar amostra: {título}"), `figcaption` e mantenha `data-i` de 0 a 5 em
  sequência: o lightbox (`#amtLb`) usa esse índice.
- As 3 páginas de Penal que saírem (`05`, `07`) ficam na pasta sem uso; pode apagar de
  `public_html/oab-v2/img/` se nada mais apontar para elas (confira com busca antes).

Se o André mandar páginas de **Ética da OAB, Direito Civil ou Processo Civil**, elas entram no
lugar das de Penal: são as que mais pesam na prova. Não existem ainda nesta pasta.

---

## Tarefa 3: imagem de compartilhamento (og:image)

A página não tem `og:image`, então o link aparece sem imagem no WhatsApp e no Instagram.

- Monte `public_html/oab-v2/img/og.jpg`, **1200×630**, fundo creme `#F7F0E5`, o mockup da
  Tarefa 1 à direita ocupando a altura toda, e à esquerda em Montserrat 900 verde-escuro
  (mesmo verde dos títulos da página): "Revise 5x mais rápido para a 1ª fase da OAB".
  JPG até 150 KB.
- Em `index.html`, dentro do `<head>`, junto das outras `og:`:
  `<meta property="og:image" content="https://marcelomapas.com/oab-v2/img/og.jpg">`
  e `<meta name="twitter:card" content="summary_large_image">` (troque o `summary` atual).

---

## Como testar antes de dizer que terminou

1. Sirva localmente: `python3 -m http.server 8791 --directory public_html` e abra
   `http://localhost:8791/oab-v2/`.
2. Em **375 px de largura** (celular): a dobra mostra o mockup inteiro, sem corte, e o texto da
   capa do livro dá para ler. Tire um print e compare lado a lado com a dobra de
   `https://resumosmapasdireito.com/3-0/`.
3. Carrossel: arraste até o fim, toque em cada uma das 6 páginas e confira que o lightbox abre a
   página certa, e que as setas navegam na ordem.
4. Console do navegador sem erro. Nenhuma imagem com 404 (confira na aba de rede).
5. Peso: nenhuma imagem nova acima do limite dado em cada tarefa.
6. Busca de sobra: `grep -n "01.webp\|og:image\|data-i=" public_html/oab-v2/index.html`.

## Como entregar

- **Não publique.** O André revisa primeiro. Quando ele aprovar, o comando é:
  `./deploy.sh --pra-valer oab-v2` (sobe só esta pasta; o script **nunca** usa `--delete`, e
  não pode usar: o servidor tem 1 GB de vídeo que não está no repositório).
- **Não rode `oab-v2-build.py`.** Ele remonta a página do zero a partir de arquivos
  temporários que não existem mais e apagaria o que você fez. Edite `index.html` direto.
- Commit em português, estilo `feat: mockup da OAB na dobra da /oab-v2/`.
- No fim, liste: arquivos criados, arquivos alterados, o que ficou fora e por quê, e os prints
  do teste em celular (dobra, carrossel, og:image).

## Resumo do que não pode

- Mexer em copy, preço, oferta, checkout (`TGerrqk`), pixel (`591918135496369`) ou UTMify.
- Gerar página do material com IA.
- Usar selo ou brasão oficial da OAB.
- Deixar sobrar qualquer elemento policial (farda, arma, SWAT, "carreira policial").
- Publicar sem aprovação.
