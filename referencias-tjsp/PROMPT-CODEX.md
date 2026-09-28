# Prompt para o Codex: deixar a página do TJSP (`/tjsp/`) com cara de TJSP

> **Atualização 28/09, tarde:** o André pediu para o Claude fazer a parte visual direto, e o tema
> do TJSP já está aplicado e no ar (cores do brasão, faixa da bandeira de SP, padrão de ícones de
> tribunal no estilo Gaby no Tribunal, fachada nas seções escuras, faixa da cúpula, capa nova). Está
> no bloco `<style id="tema-tjsp">` gerado por `tjsp-build.py` (seção "tema visual TJSP"). Se usar
> este prompt, parta do que está no ar e **edite o `tjsp-build.py`**, não o `index.html`, porque o
> tema agora é gerado pelo script.

Cole tudo abaixo da linha no Codex, com o repositório `~/marcelomapas-site` aberto.

---

## Contexto

A página de vendas **já está pronta e no ar**: `https://marcelomapas.com/tjsp/`, arquivo
`public_html/tjsp/index.html`. Ainda não tem anúncio apontando para ela.

O produto é o material do **concurso do TJSP (Escrevente Técnico Judiciário)** do Marcelo Mapas:
resumos ilustrados (mapas mentais, esquemas, mnemônicos) em PDF, **R$ 97**, checkout Kiwify
`zRttdvv`.

A página é um clone da `/oab-v2/`, que por sua vez é clone da página de Carreiras Policiais do
mesmo cliente (`https://resumosmapasdireito.com/3-0/`), a que mais vende. Hoje ela ainda tem as
**cores e o clima da página de Carreiras/OAB** (creme, verde escuro, laranja/dourado). Só o texto e
a capa do livro foram trocados para TJSP.

**O seu trabalho é a camada visual: fazer a página parecer feita para quem vai prestar o TJSP.**
Cores do TJSP, fotos do Palácio da Justiça, elementos visuais de tribunal. A estrutura, a ordem
das seções e o texto ficam como estão.

Referências nesta pasta, `~/marcelomapas-site/referencias-tjsp/`. Ela fica fora de `public_html/` e
não vai para o ar.

```
referencias-tjsp/
├── PROMPT-CODEX.md               ← este arquivo
├── 01-marca-tjsp/
│   ├── logo-tjsp-original.png    ← logo oficial (241×129, pequeno: não ampliar muito)
│   └── PALETA.md                 ← cores medidas no logo, com o papel de cada uma
├── 02-fotos-tjsp/                ← 10 fotos do Palácio da Justiça, licença livre
│   ├── CREDITOS.md               ← autor, licença e o que tem em cada foto
│   ├── baixar.py                 ← como foram baixadas (Wikimedia Commons)
│   └── foto-01.jpg … foto-14.jpg
└── 03-dobra-atual/               ← como a imagem da dobra foi feita
    ├── capa.py                   ← gera a capa plana do livro (600×900) com Pillow
    ├── capa-tjsp.png             ← a capa atual
    ├── mockup.py                 ← aplica a capa no mockup por perspectiva
    ├── homografia-capa.npy       ← matriz da perspectiva do livro (já calculada, não refaça)
    └── dobra-tjsp.png            ← resultado: a dobra atual (980×1225)
```

Outras referências no repositório:
- `referencias-oab-v2/02-paginas-reais/`: páginas **reais** do material (Penal, Constitucional,
  Administrativo). As do carrossel da `/tjsp/` saíram daqui.
- `referencias-oab-v2/03-marca-e-bonus/`: logo do Marcelo Mapas e capas dos bônus.
- `public_html/oab-v2/` e `https://resumosmapasdireito.com/3-0/`: as páginas-irmãs, para comparar.

---

## A direção visual

**Paleta do TJSP** (detalhe em `01-marca-tjsp/PALETA.md`):

| Papel | Cor |
|---|---|
| Vermelho do brasão | `#D02020` |
| Preto-azulado (listras da bandeira de SP) | `#101820` |
| Dourado do brasão | `#A89838`, sombra `#B07830` |
| Branco | `#F8F8F8` |

A partir daí, o clima que eu quero é o de um **tribunal**: o dourado dos salões e da cúpula do
Palácio da Justiça, madeira escura, pedra clara da fachada, o vermelho do brasão como acento e as
listras preto e branco da bandeira de São Paulo como elemento gráfico (faixa, divisor de seção,
detalhe de borda). Sério e institucional, sem perder a pegada de venda direta que a página já tem.

### O que trocar

1. **Cores da página.** Troque o verde e o laranja/dourado atuais pela paleta do TJSP, **só dentro
   de `public_html/tjsp/index.html`**. As variáveis ficam no `<style>` do próprio arquivo
   (`--gold`, `--gold-light`, `--gold-dark`, `--verde*`, `--creme`, `--bg`, e as classes
   `.gold-grad`, `.btn-gold`). Existem definições repetidas das mesmas variáveis em blocos
   diferentes: procure todas antes de mudar, e confira o resultado seção por seção.
   - **Destaques do título** (`.gold-grad`, hoje o verde de "5x mais rápido" e "lista dos
     aprovados"): vermelho do brasão ou dourado, o que ler melhor sobre o fundo.
   - **Botões de compra** (`.btn-gold`, `.ck-cta`, `.tira-cta`): continuam sendo o elemento de
     maior contraste da página, mesmo formato e tamanho. Dourado do TJSP com texto escuro, ou
     vermelho do brasão com texto branco. Contraste mínimo de 4,5:1 no texto do botão.
   - **Fundo creme** (`#F7F0E5` e parecidos): pode virar o tom de pedra clara da fachada ou um
     branco quente. O fundo da imagem da dobra tem que emendar com o fundo da seção, sem borda.
   - Seções escuras (`.sec-escura`, `.el-sec--dark`): preto-azulado `#101820` no lugar do preto.
2. **Fotos do Palácio da Justiça.** Use as de `02-fotos-tjsp/` como:
   - fundo da dobra (`.hero-bg`) ou de uma ou duas seções, **com baixa opacidade ou sob uma
     camada de cor**, para o texto continuar legível;
   - faixa decorativa entre seções (a cúpula dourada, `foto-02`, e o teto, `foto-08`, funcionam
     bem cortados na horizontal);
   - fundo da seção de garantia ou da de "mais de 6 anos", se ficar bom.
   Não use todas: duas ou três bem colocadas valem mais que dez. Reexporte cada uma para WebP,
   largura máxima de 1600 px, **até 180 KB**, com nome novo em `public_html/tjsp/img/`.
3. **Elementos visuais de tribunal.** Listras da bandeira de SP, balança da justiça, colunas,
   ornamento dourado, textura de mármore ou de papel timbrado. Pode desenhar em CSS/SVG simples ou
   gerar imagem com IA, **desde que seja decoração** (ver proibições abaixo).
4. **A capa do livro na dobra.** Hoje é a fachada em preto e branco com "CONCURSO TJSP",
   "RESUMOS MAPEADOS" e "Escrevente Técnico Judiciário" (veja `03-dobra-atual/capa-tjsp.png`).
   Pode redesenhar a capa com a paleta nova (por exemplo, faixa vermelha, listras de SP na lombada,
   dourado na tipografia, a cúpula no lugar da fachada). O caminho que já funciona:
   - edite `03-dobra-atual/capa.py` e rode (gera `capa-tjsp.png`, 600×900);
   - rode `03-dobra-atual/mockup.py` (aplica a capa no livro com a perspectiva certa, mantém a luz
     e a folha que fica na frente do livro; gera `dobra-tjsp.png`);
   - converta para WebP 980×1225, **até 200 KB**, e salve com **nome novo**, por exemplo
     `public_html/tjsp/img/dobra-tjsp-v2.webp`.
   - O texto da capa tem que sair perfeito, soletrado certo, com acento. Escreva com fonte de
     verdade (Montserrat 800/900); IA só para fundo ou figura, se quiser.
   - O monitor e as folhas do mockup mostram páginas reais de Direito Penal, que cai no TJSP.
     Não mexa nelas.
5. **Imagem de compartilhamento.** Refaça `og-tjsp.jpg` (1200×630, JPG até 150 KB) na paleta
   nova, com a dobra nova à direita e, à esquerda, "Revise 5x mais rápido para o concurso do
   TJSP". Salve com nome novo (`og-tjsp-v2.jpg`) e atualize `og:image` no `<head>`.
6. **Crédito das fotos no rodapé.** Hoje o rodapé credita só a foto da capa. Para **cada** foto que
   você usar, o rodapé tem que dizer autor e licença, no formato já existente:
   "Foto do Palácio da Justiça: {autor}, Wikimedia Commons, {licença}." (dados em
   `02-fotos-tjsp/CREDITOS.md`). As CC BY-SA exigem crédito; sem ele, não use a foto.

### Como deve ficar (critério)

Quem chega do anúncio tem que reconhecer em um segundo que **é material para o concurso do TJSP**,
sem achar que **é o site do TJSP**. O tom é "editora de material para concurso com a cara do
tribunal", não "portal oficial".

---

## Proibido

- **Mexer em texto, preço, oferta, estrutura ou ordem das seções.** Isso inclui títulos, lista do
  sumário, itens da oferta, FAQ e rodapé (exceto a linha de crédito das fotos). Se achar que um
  texto precisa mudar, escreva no relatório final; não mude.
- **Mexer em checkout (`zRttdvv`), pixel da Meta (`591918135496369`), UTMify ou em qualquer
  `<script>` de rastreamento.** Os links de compra recebem UTM por script; confira no fim que
  continuam recebendo.
- **Fazer a página parecer oficial:** nada de copiar o cabeçalho, o menu ou o layout do portal
  `tjsp.jus.br`; nada de "site oficial", "parceiro", "credenciado", "aprovado pelo TJSP".
- **Usar o logo ou o brasão como selo de aprovação.** O logo aparece hoje pequeno, no selo "Foco
  total: Escrevente TJSP" do topo, e fica assim. Não coloque o logo na capa do livro, no botão, na
  oferta nem em tamanho grande. Não redesenhe nem distorça o brasão. Não gere brasão com IA.
- **Gerar com IA uma página do material.** As páginas do carrossel são reais e continuam as mesmas.
  Mostrar ao comprador um conteúdo gerado seria mostrar algo que não existe no produto.
- **Pessoas reconhecíveis** nas fotos ou em imagem gerada.
- **Reaproveitar nome de imagem.** O site está atrás do Cloudflare, que guarda imagem por 180 dias:
  trocar o arquivo com o mesmo nome faz o celular do cliente continuar vendo a versão velha. Toda
  imagem alterada ganha nome novo, e o `<img>` passa a apontar para ele.
- **Rodar `tjsp-build.py`.** Ele remonta a página do zero a partir da `/oab-v2/` e apagaria o seu
  trabalho. Edite `public_html/tjsp/index.html` direto.
- Mexer em qualquer outra pasta de `public_html/` (principalmente `oab-v2/`, que está no ar com
  anúncio).
- **Publicar.** O André revisa primeiro.

---

## Como testar antes de dizer que terminou

1. Sirva localmente: `python3 -m http.server 8791 --directory public_html` e abra
   `http://localhost:8791/tjsp/`.
2. **Celular (375 px):** a dobra aparece inteira, o selo do topo fica em uma linha, o título lê
   bem sobre o fundo, a capa do livro dá para ler, e não há rolagem lateral
   (`document.documentElement.scrollWidth` igual à largura da janela).
3. **Desktop (1280 px):** mesma conferência.
4. **Contraste:** todo texto sobre foto ou cor nova passa 4,5:1 (3:1 para título grande). Meça,
   não estime, principalmente texto sobre foto.
5. **Carrossel de páginas e carrossel de prints:** arraste até o fim, toque em cada item, o
   lightbox abre o item certo e as setas navegam em ordem.
6. **Links de compra:** clique num botão e confira que abre `pay.kiwify.com.br/zRttdvv` com os
   parâmetros `utm_` na URL.
7. Console sem erro, nenhuma imagem com 404, nenhuma imagem nova acima do limite.
8. **Busca de sobra:** `grep -n "dobra-tjsp.webp\|og-tjsp.jpg" public_html/tjsp/index.html` não pode
   achar os nomes antigos se você trocou as imagens.
9. Compare lado a lado com a versão atual no ar (`https://marcelomapas.com/tjsp/`) e com a `/3-0/`:
   a hierarquia (título, dobra, botão) tem que continuar igual ou melhor.

## Como entregar

- **Não publique.** Quando o André aprovar, o comando é `./deploy.sh --pra-valer tjsp` (sobe só esta
  pasta; o script nunca usa `--delete`, e não pode usar: o servidor tem 1 GB de vídeo que não está
  no repositório).
- Commit em português, estilo `feat: identidade visual do TJSP na /tjsp/`.
- No fim, liste:
  - arquivos criados e alterados;
  - as cores novas e onde entrou cada uma;
  - quais fotos usou e onde;
  - os contrastes medidos dos textos sobre foto e dos botões;
  - prints em celular e desktop: dobra, uma seção com foto, oferta, rodapé;
  - o que ficou de fora e por quê.
