"""Monta public_html/portugues-v2/ a partir da /penal-v2/ (mesmo molde de ticket baixo).

Troca conteúdo, imagens e checkout. Cada substituição confere quantas vezes o trecho aparece,
para o script quebrar em vez de gerar página errada se a /penal-v2/ mudar.

Fatos usados (conferidos em 01/10/2026):
- Produto na Kiwify (conta do Marcelo): "PORTUGUÊS ILUSTRADO", id f9460830-447a-11ef-88ea-a90253aa21f6.
  Link de checkout 0anMFje (nome "PORTUGUÊS ILUSTRADO"), R$ 17,00; Pix, cartão e boleto; 5 order bumps
  (Constitucional, Penal, Processo Penal, Administrativo, Leis Especiais). Âncora "De R$ 117 por R$ 17"
  e "Garantia de Satisfação ou Seu Dinheiro de Volta" vêm da própria página do checkout.
- Sumário: foto do material impresso no vídeo PORT-1.mov (videos-base, 28/09), que vai até "48 Questões".
- "52 páginas": página antiga /Portugues02/ (do Marcelo). [PENDENTE DE VALIDAÇÃO]
- Páginas de amostra: public_html/Portugues02/amostras (do Marcelo).
- Depoimentos: prints que já estavam na /Portugues02/ (do Marcelo).
- Autoridade: 00-CONTEXTO do cliente (6 anos, 95 mil alunos).
Imagens com nome novo: o Cloudflare guarda imagem por 180 dias.
"""
import base64
import os
import re
import subprocess

from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = f'{RAIZ}/public_html/penal-v2'
ANTIGA = f'{RAIZ}/public_html/Portugues02'
DEST = f'{RAIZ}/public_html/portugues-v2'
IMG = f'{DEST}/img'
VIDEO = os.path.expanduser('~/clientes/marcelo-mapas/videos-base/PORT-1.mov')
CHECKOUT = 'https://pay.kiwify.com.br/0anMFje'
ROTULO = 'v2'  # nome novo a cada troca de imagem

os.makedirs(IMG, exist_ok=True)

# ---------------------------------------------------------------- imagens
def webp(origem, nome, largura, qualidade=82):
    im = Image.open(origem).convert('RGB')
    h = round(im.height * largura / im.width)
    im = im.resize((largura, h), Image.LANCZOS)
    im.save(f'{IMG}/{nome}', 'WEBP', quality=qualidade, method=6)
    return largura, h


amostras = {
    'ortografia': 'ortografia-s-x-z.jpg',
    'pronomes': 'pronomes-tratamento.jpg',
    'oficio': 'tipos-de-oficio.jpg',
    'requerimento': 'requerimento-estrutura.jpg',
}
dim = {}
for chave, arq in amostras.items():
    src = f'{ANTIGA}/amostras/{arq}'
    dim[chave] = webp(src, f'pg-{chave}-{ROTULO}.webp', 760)
    webp(src, f'pg-{chave}-grande-{ROTULO}.webp', 1300, 80)

# foto do material impresso (frame do vídeo cru PORT-1, só mãos, sem rosto)
quadro = f'{IMG}/_quadro.jpg'
if not os.path.exists(f'{IMG}/foto-material-{ROTULO}.webp'):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-ss', '18.5', '-i', VIDEO,
                    '-frames:v', '1', '-q:v', '2', quadro], check=True)
    im = Image.open(quadro).convert('RGB')
    im = im.crop((0, 380, 1080, 1580))
    im.save(f'{IMG}/foto-material-{ROTULO}.webp', 'WEBP', quality=82, method=6)
    os.remove(quadro)
fm = Image.open(f'{IMG}/foto-material-{ROTULO}.webp').size

# prints de aluno já usados na /Portugues02/ (data URI no HTML antigo)
velho = open(f'{ANTIGA}/index.html', encoding='utf-8').read()
uris = re.findall(r'data:image/webp;base64,([A-Za-z0-9+/=]+)', velho)
assert len(uris) >= 11, len(uris)
# índices 5, 6 e 9 desta lista (conferidos a olho em 01/10): Português, tablet e custo-benefício
provas = {'aluno-a': 5, 'aluno-b': 6, 'aluno-c': 9}
for nome, i in provas.items():
    with open(f'{IMG}/{nome}-{ROTULO}.webp', 'wb') as f:
        f.write(base64.b64decode(uris[i]))

# ---------------------------------------------------------------- HTML
s = open(f'{BASE}/index.html', encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, n, old[:90])
    s = s.replace(old, new)


# partes que ficam como estão: pixel e UTMify
pixel = re.search(r"// Pixel da Meta[\s\S]*?fbq\('track','PageView'\);", s)
assert pixel and s.count("fbq('init'") == 1
PIXEL = ("!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?\n"
         "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;\n"
         "n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;\n"
         "t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,\n"
         "document,'script','https://connect.facebook.net/en_US/fbevents.js');\n"
         "fbq('init','591918135496369');\nfbq('track','PageView');")
assert PIXEL in pixel.group(0).replace("// Pixel da Meta — mesmo id da página atual, para o teste comparar no mesmo pixel\n", '')
UTMIFY = '<script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-xcod-sck data-utmify-prevent-subid async defer></script>'
rep(UTMIFY, UTMIFY)

# CSS do molde, sem o comparador e o sumário recolhível (a página nova usa outros blocos)
css = re.search(r'<style>([\s\S]*?)</style>', s).group(1)
css = re.sub(r'/\* ---- comparador arrastável ---- \*/[\s\S]*?(?=/\* ---- sumário recolhível ---- \*/)', '', css)
assert 'cmp-box' not in css
css = re.sub(r'/\* ---- bônus ---- \*/[\s\S]*?(?=/\* ---- prova ---- \*/)', '', css)
assert '.bonus' not in css

EXTRA_CSS = '''
/* ---- foto + páginas ---- */
.foto{margin:20px 0 0;border-radius:var(--raio);overflow:hidden;border:1px solid var(--borda);
  box-shadow:0 14px 34px -18px rgba(13,13,13,.5)}
.foto img{width:100%;height:auto;aspect-ratio:5/4;object-fit:cover;object-position:50% 45%}
.trilho{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:18px -20px 0;padding:4px 20px 14px;scrollbar-width:thin;-webkit-overflow-scrolling:touch}
.trilho figure{flex:0 0 72%;max-width:300px;scroll-snap-align:center}
.trilho button{display:block;width:100%;padding:0;border:1px solid var(--borda);border-radius:var(--raio-sm);
  overflow:hidden;background:var(--branco);cursor:zoom-in;
  box-shadow:0 10px 24px -16px rgba(13,13,13,.5)}
.trilho button:focus-visible{outline:3px solid var(--verde);outline-offset:2px}
.trilho img{width:100%;height:auto}
.trilho figcaption{margin-top:8px;font-size:.82rem;font-weight:600;color:var(--grafite);line-height:1.35}
.dica{font-size:.82rem;color:var(--cinza);margin-top:2px}
dialog.zoom{border:0;padding:0;background:transparent;max-width:100vw;max-height:100dvh;width:100%;height:100%;
  margin:0;overflow:auto}
dialog.zoom::backdrop{background:rgba(13,13,13,.88)}
dialog.zoom .fecha{position:fixed;top:12px;right:12px;z-index:2;background:var(--branco);color:var(--preto);
  border:0;border-radius:999px;font:700 .9rem Montserrat,sans-serif;padding:10px 16px;cursor:pointer}
dialog.zoom img{display:block;width:min(100%,900px);height:auto;margin:56px auto 24px}

/* ---- sumário em blocos ---- */
.bloco-sum{margin-top:18px;display:grid;gap:12px}
.bloco-sum section{padding:16px;border:1px solid var(--borda);border-radius:var(--raio-sm);background:var(--branco)}
.bloco-sum h3{font-size:.95rem;margin-bottom:8px}
.bloco-sum ul{list-style:none;display:grid;gap:5px;color:var(--grafite);font-size:.92rem;line-height:1.4}
.bloco-sum li{display:flex;gap:10px}
.bloco-sum li b{flex:0 0 26px;color:var(--cinza);font-weight:700;font-variant-numeric:tabular-nums}

/* ---- prova social em tira ---- */
.provas.tres{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:20px -20px 0;padding:0 20px 12px}
.provas.tres img{flex:0 0 78%;max-width:300px;scroll-snap-align:center}
@media (min-width:520px){.provas.tres{display:grid;grid-template-columns:repeat(3,1fr);overflow:visible;margin:20px 0 0;padding:0}
.provas.tres img,.provas.tres img:first-child{max-width:none;width:100%;grid-column:auto}}
'''
css = css.replace('/* ---- fecho ---- */', EXTRA_CSS + '\n/* ---- fecho ---- */')
assert EXTRA_CSS in css


def sum_item(p, t):
    return f'<li><b>{p}</b><span>{t}</span></li>'


blocos = [
    ('Texto e redação oficial', [
        ('04', 'Interpretação e compreensão de textos'), ('04', 'Identificação de tipos textuais'),
        ('06', 'Critérios de textualidade: coerência e coesão'), ('10', 'Gêneros textuais da Redação Oficial'),
        ('10', 'Estrutura interna dos gêneros'), ('14', 'Princípios gerais'),
        ('14', 'Uso dos pronomes de tratamento'), ('35', 'Princípios gerais de leitura e produção de texto'),
        ('36', 'Intertextualidade'), ('38', 'Vozes discursivas: citação, paródia, alusão, paráfrase, epígrafe')]),
    ('Escrita correta', [
        ('15', 'Ortografia'), ('16', 'Acentuação'), ('19', 'Pontuação'), ('22', 'Construção textual'),
        ('47', 'Vícios de linguagem')]),
    ('Palavras e sentido', [
        ('22', 'Classe de palavras'), ('28', 'Tempos e modos verbais'), ('29', 'Semântica'),
        ('32', 'Sinônimo x antônimo'), ('33', 'Sentido próprio e figurado'), ('34', 'Figuras de linguagem'),
        ('37', 'Análise morfológica'), ('37', 'Sílaba tônica'), ('37', 'Frases e tipos de frases')]),
    ('Sintaxe e regras de uso', [
        ('39', 'Sintaxe: oração, período, termos das orações; coordenação e subordinação'),
        ('41', 'Concordância verbal e nominal'), ('43', 'Vozes verbais'), ('44', 'Regência verbal e nominal'),
        ('44', 'Colocação pronominal'), ('45', 'Crase'), ('46', 'Análise morfossintática')]),
    ('Para praticar', [('48', 'Questões')]),
]
n_itens = sum(len(b[1]) for b in blocos)
assert n_itens == 32, n_itens  # o sumário impresso tem 32 linhas
SUMARIO = ''.join(
    f'<section><h3>{t}</h3><ul>{"".join(sum_item(p, x) for p, x in it)}</ul></section>' for t, it in blocos)


def pagina(chave, legenda):
    w, h = dim[chave]
    return (f'<figure><button type="button" data-zoom="img/pg-{chave}-grande-{ROTULO}.webp" '
            f'aria-label="Ampliar: {legenda}"><img src="img/pg-{chave}-{ROTULO}.webp" width="{w}" height="{h}" '
            f'loading="lazy" decoding="async" alt="Página real do material: {legenda}"></button>'
            f'<figcaption>{legenda}</figcaption></figure>')


w0, h0 = dim['ortografia']

BODY = f'''
<!-- ============ 1. DOBRA: problema + prova + preço + CTA ============ -->
<header class="dobra">
  <div class="wrap">
    <span class="rotulo">Português para concursos e OAB</span>
    <h1>Português em 52 páginas ilustradas, para <span class="destaque">revisar rápido e lembrar na prova.</span></h1>
    <p class="sub">Ortografia, crase, concordância, regência e redação oficial em quadros e exemplos. Chega no seu e-mail, em PDF.</p>

    <div class="foto"><img src="img/foto-material-{ROTULO}.webp" width="{fm[0]}" height="{fm[1]}"
         alt="Mãos folheando o material de Português impresso e encadernado em espiral, sobre uma mesa de madeira" fetchpriority="high"></div>

    <div class="oferta">
      <p class="de">De <s>R$ 117</s> por apenas</p>
      <p class="preco"><small>R$</small>17</p>
      <p class="parcela">à vista, uma vez só</p>
      <a class="cta" href="{CHECKOUT}" data-cta="dobra">Quero o Português ilustrado</a>
      <p class="selos"><span>Acesso imediato</span><span>PDF para baixar e imprimir</span><span>Garantia de satisfação</span></p>
    </div>
  </div>
</header>

<!-- ============ 2. NEGAÇÃO DE CATEGORIA ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Esqueça as decorebas cansativas.</h2>
    <p class="sub">Gramática em texto corrido você lê, entende e esquece. Aqui cada regra vem em quadro, com objetivo e exemplo, na mesma página.</p>
    <ul class="itens">
      <li><i class="ok">✓</i><span class="txt"><b>Uma regra por quadro</b>, com o exemplo ao lado, em vez de parágrafos de gramática.</span></li>
      <li><i class="ok">✓</i><span class="txt"><b>Ilustrações e destaques</b> em cada página, para a regra ficar na memória visual.</span></li>
      <li><i class="ok">✓</i><span class="txt"><b>Redação oficial incluída</b>: ofício, requerimento, relatório, parecer e pronomes de tratamento.</span></li>
      <li><i class="ok">✓</i><span class="txt"><b>Questões no final</b>, para testar o que você acabou de revisar.</span></li>
    </ul>
  </div>
</section>

<!-- ============ 3. PÁGINAS REAIS ============ -->
<section class="compacta" style="background:var(--off)">
  <div class="wrap">
    <h2>Veja páginas do material, sem filtro</h2>
    <p class="sub">São páginas reais do PDF. Toque para ampliar.</p>
  </div>
  <div class="wrap">
    <div class="trilho" tabindex="0" aria-label="Páginas de amostra do material, deslize para os lados">
      {pagina('ortografia', 'Ortografia: uso do S, X e Z')}
      {pagina('pronomes', 'Pronomes de tratamento')}
      {pagina('oficio', 'Redação oficial: tipos de ofício')}
      {pagina('requerimento', 'Redação oficial: o requerimento')}
    </div>
    <p class="dica">Deslize para ver as outras páginas.</p>

    <h2 style="margin-top:34px">O que tem dentro</h2>
    <p class="sub">O sumário do material, na ordem do PDF, com a página de cada tema.</p>
    <div class="bloco-sum">{SUMARIO}</div>
  </div>
</section>

<!-- ============ 4. PARA QUEM É / NÃO É ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Para quem isso serve</h2>
    <ul class="itens">
      <li><i class="ok">✓</i><span class="txt">Quem estuda Português para <b>faculdade, OAB, concurso público ou carreira policial</b>.</span></li>
      <li><i class="ok">✓</i><span class="txt">Quem <b>erra questão de conteúdo que já estudou</b> e precisa revisar melhor.</span></li>
      <li><i class="ok">✓</i><span class="txt">Quem tem <b>pouco tempo</b> e não aguenta mais livro e apostila gigante.</span></li>
      <li><i class="ok nao">✕</i><span class="txt">Não serve para quem quer <b>videoaula</b>: é material escrito e ilustrado, para estudo e revisão.</span></li>
      <li><i class="ok nao">✕</i><span class="txt">Não é um curso para <b>aprender Português do zero</b> com explicação passo a passo.</span></li>
    </ul>
  </div>
</section>

<!-- ============ 5. PROVA SOCIAL ============ -->
<section class="compacta" style="background:var(--off)">
  <div class="wrap">
    <h2>O que os alunos mandam</h2>
    <p class="sub">Mensagens recebidas no direct.</p>
    <div class="provas tres">
      <img src="img/aluno-a-{ROTULO}.webp" width="600" height="600" loading="lazy" alt="Mensagem de aluno que comprou o curso e diz que, em Português, o material vai direto ao ponto">
      <img src="img/aluno-b-{ROTULO}.webp" width="600" height="600" loading="lazy" alt="Aluno mostra o material no tablet e diz que ficou extremamente fácil estudar, material organizado">
      <img src="img/aluno-c-{ROTULO}.webp" width="600" height="600" loading="lazy" alt="Mensagem de aluna dizendo que o custo-benefício é o melhor, com bastante conteúdo e bem ilustrado">
    </div>
  </div>
</section>

<!-- ============ 6. AUTORIDADE (curta) ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Quem faz</h2>
    <div class="autor">
      <p style="color:var(--grafite);font-size:.97rem">Marcelo dos Santos, advogado. Faz material ilustrado para concurso há mais de 6 anos, publicando quase todo dia.</p>
      <div class="numeros">
        <div><b>6 anos</b><span>fazendo material</span></div>
        <div><b>95 mil</b><span>alunos atendidos</span></div>
        <div><b>52</b><span>páginas no Português</span></div>
      </div>
    </div>
  </div>
</section>

<!-- ============ 7. GARANTIA ============ -->
<section class="compacta" style="background:var(--off)">
  <div class="wrap">
    <div class="garantia">
      <h2>Garantia de satisfação</h2>
      <p>Baixe, abra as páginas e use numa revisão de verdade. Se achar que não é para você, peça o reembolso e devolvemos o seu dinheiro. O prazo legal de arrependimento é de 7 dias (art. 49 do Código de Defesa do Consumidor).</p>
    </div>
  </div>
</section>

<!-- ============ 8. FAQ ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Perguntas que sempre chegam</h2>
    <div class="faq">
      <details><summary>Como recebo o material?</summary><p>O acesso é liberado automaticamente assim que o pagamento é reconhecido. Você recebe um e-mail com o link para baixar o PDF.</p></details>
      <details><summary>Posso imprimir?</summary><p>Sim. O PDF tem download ilimitado e está liberado para impressão durante todo o período de acesso.</p></details>
      <details><summary>Serve para o meu concurso?</summary><p>Serve para qualquer prova que cobre Português. O conteúdo é a matéria em si, não um edital específico.</p></details>
      <details><summary>Posso dividir com um amigo?</summary><p>Não. O material é protegido pela Lei de Direitos Autorais (Lei nº 9.610/98). A compra é individual.</p></details>
      <details><summary>Como pago?</summary><p>Pix ou cartão, pelo checkout seguro da Kiwify. O valor é R$ 17, pagamento único.</p></details>
    </div>
  </div>
</section>

<!-- ============ 9. FECHO ============ -->
<section class="fecho">
  <div class="wrap">
    <h2>Português inteiro em mapas que você revisa numa tarde</h2>
    <p class="sub">52 páginas ilustradas, direto no seu e-mail.</p>
    <div class="oferta">
      <p class="de">De <s>R$ 117</s> por apenas</p>
      <p class="preco"><small>R$</small>17</p>
      <p class="parcela">à vista, uma vez só</p>
      <a class="cta" href="{CHECKOUT}" data-cta="fecho">Quero o Português ilustrado</a>
      <p class="selos"><span>Acesso imediato</span><span>PDF para baixar e imprimir</span><span>Garantia de satisfação</span></p>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    Marcelo Mapas &middot; MS Empreendimentos Ltda &middot; CNPJ 45.522.478/0001-10<br>
    Este material é de apoio ao estudo e não garante aprovação em concurso.<br>
    Pagamento processado pela Kiwify.
  </div>
</footer>

<!-- barra fixa mobile -->
<div class="barra" id="barra">
  <div class="txt"><b>R$ 17</b><span>à vista &middot; garantia de satisfação</span></div>
  <a class="cta" href="{CHECKOUT}" data-cta="barra">Quero agora</a>
</div>

<dialog class="zoom" id="zoom" aria-label="Página ampliada">
  <button class="fecha" type="button" id="zoomFecha">Fechar</button>
  <img id="zoomImg" alt="Página do material ampliada">
</dialog>

<script>
// barra fixa aparece depois que a oferta do topo sai da tela
(function(){{
  var oferta = document.querySelector('.dobra .oferta');
  var barra = document.getElementById('barra');
  if(!oferta || !barra || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function(e){{
    barra.classList.toggle('aparece', !e[0].isIntersecting && e[0].boundingClientRect.top < 0);
  }},{{threshold:0}}).observe(oferta);
}})();

// Pixel da Meta (mesmo id das outras páginas)
{PIXEL}

// InitiateCheckout em qualquer clique de compra, com o lugar do botão
document.querySelectorAll('a[data-cta]').forEach(function(a){{
  a.addEventListener('click',function(){{
    if(window.fbq) fbq('track','InitiateCheckout',{{content_name:'Português Ilustrado',value:17,currency:'BRL',posicao:a.dataset.cta}});
  }});
}});

// Toque na página de amostra abre a versão grande
(function(){{
  var dlg=document.getElementById('zoom'), img=document.getElementById('zoomImg');
  if(!dlg || !dlg.showModal) return;
  document.querySelectorAll('[data-zoom]').forEach(function(b){{
    b.addEventListener('click',function(){{
      img.src=b.dataset.zoom; img.alt=b.getAttribute('aria-label')||'';
      dlg.showModal();
    }});
  }});
  document.getElementById('zoomFecha').addEventListener('click',function(){{dlg.close();}});
  dlg.addEventListener('click',function(e){{ if(e.target===dlg) dlg.close(); }});
}})();
</script>

<!-- UTMify: mesma atribuição das outras páginas -->
{UTMIFY}
'''

HEAD = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Português Ilustrado: 52 páginas em mapas e quadros | Marcelo Mapas</title>
<meta name="description" content="Português para concursos, OAB e carreiras policiais em quadros ilustrados. 52 páginas para revisar rápido. R$17, acesso imediato.">
<link rel="icon" href="img/pg-ortografia-{ROTULO}.webp">
<meta property="og:title" content="Português Ilustrado: 52 páginas em mapas e quadros">
<meta property="og:description" content="Regras de Português em quadros com exemplos, para revisar rápido. R$17, acesso imediato.">
<meta property="og:image" content="https://marcelomapas.com/portugues-v2/img/foto-material-{ROTULO}.webp">
<meta property="og:type" content="website">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="image" href="img/foto-material-{ROTULO}.webp">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>{css}</style>
</head>
<body>
'''

out = HEAD + BODY + '</body>\n</html>\n'
assert out.count("fbq('init'") == 1 and out.count("fbq('track','PageView')") == 1
assert out.count('cdn.utmify.com.br') == 1
assert out.count(CHECKOUT) == 3, out.count(CHECKOUT)
assert 'pay.kiwify.com.br/fbvV7j4' not in out
assert '—' not in out and '–' not in out, 'travessão no texto'
open(f'{DEST}/index.html', 'w', encoding='utf-8').write(out)
print('ok', len(out), 'bytes')

# mesmo .htaccess das outras páginas em teste (HTML sem cache no navegador)
import shutil
shutil.copy(f'{RAIZ}/public_html/oab-v2/.htaccess', f'{DEST}/.htaccess')
