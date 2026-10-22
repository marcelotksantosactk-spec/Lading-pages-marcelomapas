"""Monta public_html/constitucional-v2/ a partir da /penal-v2/, na ORDEM e na DENSIDADE da página de Penal do Marcelo.

Por que existe (21/10/2026): no dash, a página atual de Constitucional (/CT1 e resumosmapasdireito.com/constitucional/)
leva 22% das visitas ao checkout; as de Penal e Processo Civil do WordPress do Marcelo (resumosmapasdireito.com/direito-penal/
e /processo-civil/) levam 34-36%, com o mesmo preço e o mesmo checkout. O teste é Constitucional no molde da de Penal.
Análise: ~/clientes/marcelo-mapas/funil-por-produto-2026-10-21.md.

O que vem de onde:
- Código, CSS, identidade visual, pixel, InitiateCheckout, UTMify, rodapé: /penal-v2/ (conferidos por contagem abaixo).
- Ordem dos blocos (no celular): página de Penal do Marcelo. Lista "todo o conteúdo organizado e simplificado" ->
  ideal para quem -> 1 botão que desce até a oferta -> 3 páginas de amostra -> dentro do pacote (6) -> números ->
  prints de aluno -> sumário aberto -> 2 bônus -> oferta com os itens somados e o preço -> FAQ.
- Todo o conteúdo de Constitucional: /CT1 (sumário de 25 temas e 163 páginas, páginas de amostra 04, 05 e 09,
  bônus com valor avulso R$ 67 e R$ 57, material R$ 57, soma R$ 181, garantia de 7 dias, +95 mil alunos,
  4,9 de avaliação, +50 mil downloads, os 10 prints de aluno, FAQ, imagens).
- "Ideal para quem" e as quatro disciplinas do bônus 1: páginas de Penal/Processo Civil do Marcelo (texto dele).
Fora de propósito: data de "só hoje" e "75% de desconto hoje" (escassez com data automática), "Atualizado em <mês>"
(a CT1 troca o mês sozinha no navegador), barra fixa de compra, comparador, bloco de autoridade e bloco de garantia
(a página de Penal não tem; a garantia está na oferta e no FAQ).
Imagens com nome novo: o Cloudflare guarda imagem por 180 dias.
"""
import os
import re
import shutil

import rastreamento  # rastreamento da TAOS + reserva da UTMify (rastreamento.py)

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = f'{RAIZ}/public_html/penal-v2'
FONTE = f'{RAIZ}/public_html'          # imagens da /CT1 ficam na raiz (/01.webp ... /23.webp)
DEST = f'{RAIZ}/public_html/constitucional-v2'
IMG = f'{DEST}/img'
CHECKOUT = 'https://pay.kiwify.com.br/Gi2NvFT'
CHECKOUT_PENAL = 'https://pay.kiwify.com.br/fbvV7j4'
ROTULO = 'c1'  # nome novo a cada troca de imagem

os.makedirs(IMG, exist_ok=True)

# ---------------------------------------------------------------- imagens (as mesmas da /CT1, nome novo)
ct1 = open(f'{FONTE}/CT1', encoding='utf-8').read()
imagens = {  # nome novo: (arquivo da CT1, alt que a CT1 usa, para conferir que é a imagem certa)
    'amostra-capa': ('01', 'Páginas de amostra dos resumos ilustrados de Direito Constitucional'),
    'pg04-conceito': ('04', 'Amostra real do material — Conceito de Constituição'),
    'pg05-sentidos': ('05', 'Amostra real do material — Sentidos da Constituição'),
    'pg09-classificacao': ('07', 'Amostra real do material — Classificação das Constituições'),
    'bonus-mnemonicos': ('19', 'Capa do e-book Mnemônicos'),
    'bonus-memorizacao': ('20', 'Capa do e-book Manual da Memorização'),
    'pagamento': ('21', 'Formas de pagamento aceitas'),
}
for i in range(9, 19):
    imagens[f'aluno-{i - 8:02d}'] = (f'{i:02d}', 'Print de mensagem enviada por aluno sobre o material')

from PIL import Image

dim = {}
for nome, (arq, alt) in imagens.items():
    assert re.search(rf'<img[^>]*src="/{arq}\.webp"[^>]*alt="{re.escape(alt)}"', ct1) or \
        re.search(rf'<img[^>]*alt="{re.escape(alt)}"[^>]*src="/{arq}\.webp"', ct1), (arq, alt)
    destino = f'{IMG}/{nome}-{ROTULO}.webp'
    shutil.copyfile(f'{FONTE}/{arq}.webp', destino)
    dim[nome] = Image.open(destino).size

# ---------------------------------------------------------------- HTML
s = open(f'{BASE}/index.html', encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, n, old[:90])
    s = s.replace(old, new)


# partes que ficam como estão: pixel e UTMify (o rastreamento da TAOS e a reserva entram de novo pelo instalar())
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
rep(CHECKOUT_PENAL, CHECKOUT, 3)  # os três botões da penal-v2 apontavam para o Penal
rep("content_name:'Direito Penal Ilustrado'", "content_name:'Direito Constitucional Ilustrado'")

# CSS do molde, sem o comparador e sem a barra fixa (a página de Penal do Marcelo não tem nenhum dos dois)
css = re.search(r'<style>([\s\S]*?)</style>', s).group(1)
css = re.sub(r'/\* ---- comparador arrastável ---- \*/[\s\S]*?(?=/\* ---- sumário recolhível ---- \*/)', '', css)
assert 'cmp-box' not in css
css = re.sub(r'/\* ---- barra fixa mobile ---- \*/[\s\S]*?(?=footer\{)', '', css)
assert '.barra' not in css
for trecho in ('/* ---- dobra ---- */', '/* ---- oferta ---- */', '/* ---- bônus ---- */', '/* ---- prova ---- */',
               '/* ---- autoridade ---- */', '/* ---- faq ---- */', '/* ---- fecho ---- */', '.numeros{'):
    assert css.count(trecho) == 1, trecho

EXTRA_CSS = '''
/* ---- botão que desce até a oferta ---- */
.cta.desce{background:var(--branco);color:var(--verde);border:2px solid var(--verde);box-shadow:none}
.cta.desce:hover{background:#eaf6ef;box-shadow:none}

/* ---- páginas de amostra empilhadas (toque amplia) ---- */
.paginas{display:grid;gap:16px;margin-top:20px}
.paginas button{display:block;width:100%;padding:0;border:1px solid var(--borda);border-radius:var(--raio-sm);
  overflow:hidden;background:var(--branco);cursor:zoom-in;box-shadow:0 12px 28px -18px rgba(13,13,13,.55)}
.paginas button:focus-visible{outline:3px solid var(--verde);outline-offset:2px}
.paginas figcaption{margin-top:8px;font-size:.82rem;font-weight:600;color:var(--grafite)}
.paginas figcaption span{color:var(--cinza-claro);font-weight:500}
.dica{font-size:.82rem;color:var(--cinza);margin-top:12px}
dialog.zoom{border:0;padding:0;background:transparent;max-width:100vw;max-height:100dvh;width:100%;height:100%;
  margin:0;overflow:auto}
dialog.zoom::backdrop{background:rgba(13,13,13,.88)}
dialog.zoom .fecha{position:fixed;top:12px;right:12px;z-index:2;background:var(--branco);color:var(--preto);
  border:0;border-radius:999px;font:700 .9rem Montserrat,sans-serif;padding:10px 16px;cursor:pointer}
dialog.zoom img{display:block;width:min(100%,900px);height:auto;margin:56px auto 24px}

/* ---- dentro do pacote ---- */
.seis{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}
.seis div{background:var(--branco);border:1px solid var(--borda);border-radius:var(--raio-sm);padding:14px 14px 15px}
.seis b{display:block;font-size:.95rem;font-weight:800;letter-spacing:-.01em}
.seis b:before{content:"";display:block;width:18px;height:3px;border-radius:2px;background:var(--laranja);margin-bottom:9px}
.seis span{display:block;margin-top:4px;font-size:.84rem;color:var(--cinza);line-height:1.4}
.numeros.solto{margin-top:22px}

/* ---- prova social em tira ---- */
.tira{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;margin:20px -20px 0;padding:0 20px 12px;
  scrollbar-width:thin;-webkit-overflow-scrolling:touch}
.tira img{flex:0 0 78%;max-width:300px;scroll-snap-align:center;border-radius:var(--raio-sm);border:1px solid var(--borda)}

/* ---- bônus com capa ---- */
.bonus article.capa{display:grid;grid-template-columns:84px 1fr;gap:14px;align-items:center}
.bonus article.capa img{border-radius:6px;box-shadow:0 8px 18px -10px rgba(13,13,13,.6)}

/* ---- oferta com os itens somados ---- */
.fecho .mostra{margin:20px auto 0;width:100%;max-width:min(100%,420px);border-radius:var(--raio-sm);overflow:hidden}
.itens-oferta{list-style:none;margin:16px 0 4px;text-align:left;display:grid;gap:0}
.itens-oferta li{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid #333;
  font-size:.92rem;color:#e6e6e6}
.itens-oferta li span:last-child{white-space:nowrap;font-variant-numeric:tabular-nums;color:#bdbdbd}
.itens-oferta li.soma{border-bottom:0;font-weight:700;color:var(--branco)}
.itens-oferta li.soma span:last-child{color:#bdbdbd}
.fecho .pagamento{margin:14px auto 0;max-width:min(100%,300px);opacity:.9}
.fecho .seguro{margin-top:10px;font-size:.8rem;color:#999}
'''
css = css.replace('/* ---- fecho ---- */', EXTRA_CSS + '\n/* ---- fecho ---- */')
assert css.count(EXTRA_CSS) == 1


def img(nome, alt, extra='loading="lazy" decoding="async"'):
    w, h = dim[nome]
    return f'<img src="img/{nome}-{ROTULO}.webp" width="{w}" height="{h}" {extra} alt="{alt}">'


def pagina(nome, tema, pag):
    w, h = dim[nome]
    return (f'<figure><button type="button" data-zoom="img/{nome}-{ROTULO}.webp" aria-label="Ampliar: {tema}, página {pag}">'
            f'<img src="img/{nome}-{ROTULO}.webp" width="{w}" height="{h}" loading="lazy" decoding="async" '
            f'alt="Página real do material: {tema}"></button>'
            f'<figcaption>{tema} <span>· Teoria da Constituição, pág. {pag}</span></figcaption></figure>')


# sumário da /CT1, na ordem dela (25 temas)
TEORIA = ['Teoria da Constituição', 'Classificação da Constituição', 'Supremacia da Constituição',
          'Papel da Constituição', 'Ativismo Judicial', 'Aplicabilidade das Normas', 'Interpretação das Normas',
          'Constituições no Brasil', 'Dinâmica Constitucional', 'Poder Constituinte', 'Princípios Constitucionais']
DIREITOS = ['Direitos e Garantias Fundamentais', 'Direitos Sociais', 'Nacionalidade', 'Direitos Políticos',
            'Remédios Constitucionais', 'Organização Político-Administrativa', 'Intervenção', 'Poder Legislativo',
            'Processo Legislativo', 'Poder Executivo', 'Poder Judiciário', 'Funções Essenciais à Justiça',
            'Sistema Constitucional de Crises', 'Segurança Pública']
for t in TEORIA + DIREITOS:
    assert t in ct1, t  # cada tema existe na CT1
assert len(TEORIA) == 11 and len(DIREITOS) == 14
SUMARIO = (f'<h4>Teoria da Constituição · {len(TEORIA)} temas</h4><ul>' + ''.join(f'<li>{t}</li>' for t in TEORIA) +
           f'</ul><h4>Direitos e Organização do Estado · {len(DIREITOS)} temas</h4><ul>' +
           ''.join(f'<li>{t}</li>' for t in DIREITOS) + '</ul>')

# fatos numéricos da /CT1: conferir que ela diz exatamente isso antes de usar
for fato in ('+95 mil alunos', 'Avaliação 4.9', '+50 mil downloads', '163 páginas', 'R$ 67', 'R$ 57', 'R$ 181',
             'garantia de 7 dias', 'Macetes, Dicas e Mnemônicos', 'Manual da Memorização'):
    assert fato in ct1, fato

ALUNOS = ''.join(img(f'aluno-{i:02d}', 'Print de mensagem enviada por aluno sobre o material') for i in range(1, 11))

BODY = f'''
<!-- ============ 1. TODO O CONTEÚDO, ORGANIZADO (como abre a página de Penal no celular) ============ -->
<header class="dobra">
  <div class="wrap">
    <span class="rotulo">Direito Constitucional · OAB e concursos</span>
    <h1>Todo o Direito Constitucional que você precisa, <span class="destaque">organizado e simplificado.</span></h1>
    <p class="sub">Mapas mentais, esquemas e mnemônicos em 163 páginas ilustradas, da Teoria da Constituição à Segurança Pública.</p>
    <ul class="itens">
      <li><i class="ok">✓</i><span class="txt"><b>Mapas mentais, esquemas e mnemônicos</b> para facilitar a memorização.</span></li>
      <li><i class="ok">✓</i><span class="txt"><b>Quadros e organização visual</b> para fixação acelerada.</span></li>
      <li><i class="ok">✓</i><span class="txt">Melhore sua <b>concentração e produtividade</b> nos estudos.</span></li>
      <li><i class="ok">✓</i><span class="txt">Aumente suas <b>chances de aprovação</b> com as melhores técnicas.</span></li>
    </ul>
  </div>
</header>

<!-- ============ 2. IDEAL PARA QUEM + botão ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Ideal para quem</h2>
    <ul class="itens">
      <li><i class="ok">✓</i><span class="txt">Precisa de um material <b>organizado e ilustrado</b>.</span></li>
      <li><i class="ok">✓</i><span class="txt"><b>Erra questões</b> de conteúdo já estudado.</span></li>
      <li><i class="ok">✓</i><span class="txt">Não dispõe de <b>muito tempo</b> para revisar conteúdos importantes.</span></li>
      <li><i class="ok">✓</i><span class="txt">Tem dificuldade de estudar por <b>livros e apostilas gigantes</b>.</span></li>
    </ul>
    <a class="cta desce" href="#oferta">Quero meus resumos ilustrados</a>
  </div>
</section>

<!-- ============ 3. AMOSTRA ============ -->
<section class="compacta" style="background:var(--off)">
  <div class="wrap">
    <h2>Veja uma amostra do material</h2>
    <p class="sub">Páginas reais, exatamente como você recebe. Toque para ampliar.</p>
    <div class="paginas">
      {pagina('pg04-conceito', 'Conceito de Constituição', '04')}
      {pagina('pg05-sentidos', 'Sentidos da Constituição', '05')}
      {pagina('pg09-classificacao', 'Classificação das Constituições', '09')}
    </div>
    <p class="dica">3 das 163 páginas.</p>
  </div>
</section>

<!-- ============ 4. DENTRO DO PACOTE + NÚMEROS ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Dentro do pacote, você vai receber…</h2>
    <div class="seis">
      <div><b>Facilidade</b><span>Para revisar conteúdos com clareza e sem esforço excessivo.</span></div>
      <div><b>Velocidade</b><span>Para acelerar sua compreensão e memorização do conteúdo.</span></div>
      <div><b>Estímulos</b><span>Setas, imagens, símbolos e mapas que causam diferentes estímulos cerebrais.</span></div>
      <div><b>Conexão</b><span>Ajuda o cérebro a criar conexões entre as informações com mais eficiência.</span></div>
      <div><b>Fixação</b><span>Economia de tempo nas revisões: fixe mais em menos sessões.</span></div>
      <div><b>Revisão</b><span>Ideias organizadas em um só lugar para revisões rápidas e eficazes.</span></div>
    </div>
    <div class="numeros solto">
      <div><b>+95 mil</b><span>alunos</span></div>
      <div><b>4,9</b><span>avaliação média</span></div>
      <div><b>+50 mil</b><span>downloads</span></div>
    </div>
  </div>
</section>

<!-- ============ 5. PROVA SOCIAL ============ -->
<section class="compacta" style="background:var(--off)">
  <div class="wrap">
    <h2>O que dizem os alunos</h2>
    <p class="sub">Prints reais de mensagens recebidas, sem edição. Deslize para o lado.</p>
  </div>
  <div class="wrap">
    <div class="tira" tabindex="0" aria-label="Mensagens de alunos, deslize para os lados">{ALUNOS}</div>
  </div>
</section>

<!-- ============ 6. SUMÁRIO ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Direito Constitucional: o sumário</h2>
    <p class="sub">163 páginas ilustradas em 25 temas, da Teoria da Constituição à Segurança Pública.</p>
    <details class="sumario" open>
      <summary>Sumário completo: 25 temas</summary>
      <div class="conteudo">{SUMARIO}</div>
    </details>
  </div>
</section>

<!-- ============ 7. BÔNUS ============ -->
<section class="compacta" style="background:var(--off)">
  <div class="wrap">
    <h2>Receba também 2 bônus</h2>
    <p class="sub">Os dois vêm junto com o material, no mesmo download e sem custo adicional.</p>
    <div class="bonus">
      <article class="capa">
        {img('bonus-mnemonicos', 'Capa do e-book Mnemônicos')}
        <div><span class="tag">Bônus 1</span><h3>Macetes, Dicas e Mnemônicos</h3>
        <p>Direito Penal, Direito Constitucional, Processo Penal e Direito Administrativo.</p></div>
      </article>
      <article class="capa">
        {img('bonus-memorizacao', 'Capa do e-book Manual da Memorização')}
        <div><span class="tag">Bônus 2</span><h3>Manual da Memorização</h3>
        <p>O passo a passo para estudar de um jeito que o conteúdo realmente fique na cabeça.</p></div>
      </article>
    </div>
  </div>
</section>

<!-- ============ 8. OFERTA ============ -->
<section class="fecho" id="oferta">
  <div class="wrap">
    <h2>Tudo o que você leva</h2>
    {img('amostra-capa', 'Páginas de amostra dos resumos ilustrados de Direito Constitucional', 'loading="lazy" decoding="async" class="mostra"')}
    <div class="oferta">
      <ul class="itens-oferta">
        <li><span>Direito Constitucional completo (163 páginas)</span><span>R$ 57</span></li>
        <li><span>Bônus 1: Macetes, Dicas e Mnemônicos</span><span>R$ 67</span></li>
        <li><span>Bônus 2: Manual da Memorização</span><span>R$ 57</span></li>
        <li class="soma"><span>Valor somado</span><span><s>R$ 181</s></span></li>
      </ul>
      <p class="de">tudo isso por</p>
      <p class="preco"><small>R$</small>17</p>
      <p class="parcela">pagamento único</p>
      <a class="cta" href="{CHECKOUT}" data-cta="oferta">Quero o Constitucional ilustrado</a>
      <p class="selos"><span>Acesso imediato</span><span>PDF para baixar e imprimir</span><span>Garantia de 7 dias</span></p>
      {img('pagamento', 'Formas de pagamento aceitas', 'loading="lazy" decoding="async" class="pagamento"')}
      <p class="seguro">Pagamento seguro via Kiwify, Pix ou cartão de crédito.</p>
    </div>
  </div>
</section>

<!-- ============ 9. FAQ ============ -->
<section class="compacta">
  <div class="wrap">
    <h2>Perguntas frequentes</h2>
    <div class="faq">
      <details><summary>Como terei acesso ao material?</summary><p>O acesso é liberado automaticamente pela plataforma assim que o pagamento for reconhecido. Você receberá um e-mail com link para download em formato PDF.</p></details>
      <details><summary>Quantas vezes posso acessar meus resumos?</summary><p>Você pode acessar e baixar os materiais de forma ilimitada.</p></details>
      <details><summary>Posso fazer download e imprimir?</summary><p>Sim. Os materiais são liberados em formato PDF, com download ilimitado e liberados para impressão durante todo o período de acesso.</p></details>
      <details><summary>O material é atualizado?</summary><p>Sim, 100% atualizado com a legislação vigente.</p></details>
      <details><summary>E se eu não gostar?</summary><p>Baixe o material, abra todos os mapas e teste nas suas revisões. Se em até 7 dias você achar que não é para você, basta pedir o reembolso e devolvemos 100% do valor. Direito garantido pelo art. 49 do Código de Defesa do Consumidor; o pedido é feito direto pela Kiwify ou pelo nosso e-mail de suporte.</p></details>
      <details><summary>Posso dividir com um amigo?</summary><p>Não. Nossos materiais são protegidos pela Lei de Direitos Autorais (Lei nº 9.610/98). Qualquer violação é considerada pirataria, com responsabilização penal e civil para quem compartilha e para quem recebe, mesmo que gratuitamente.</p></details>
      <details><summary>Quais são as formas de pagamento?</summary><p>Trabalhamos com a Kiwify, plataforma segura e confiável para produtos digitais. São aceitos cartão de crédito e Pix.</p></details>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    Marcelo Mapas · MS Empreendimentos Ltda · CNPJ 45.522.478/0001-10<br>
    Este material é de apoio ao estudo e não garante aprovação em concurso.<br>
    Pagamento processado pela Kiwify.
  </div>
</footer>

<dialog class="zoom" id="zoom" aria-label="Página ampliada">
  <button class="fecha" type="button" id="zoomFecha">Fechar</button>
  <img id="zoomImg" alt="Página do material ampliada">
</dialog>

<script>
// Pixel da Meta (mesmo id e mesmo jeito da /penal-v2/)
{PIXEL}

// InitiateCheckout no clique de compra (o botão do topo só desce até a oferta e não conta)
document.querySelectorAll('a[data-cta]').forEach(function(a){{
  a.addEventListener('click',function(){{
    if(window.fbq) fbq('track','InitiateCheckout',{{content_name:'Direito Constitucional Ilustrado',value:17,currency:'BRL',posicao:a.dataset.cta}});
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
<title>Direito Constitucional Ilustrado: 163 páginas em mapas mentais | Marcelo Mapas</title>
<meta name="description" content="Todo o Direito Constitucional para OAB e concursos em mapas mentais, esquemas e mnemônicos. 163 páginas ilustradas. R$17, acesso imediato, garantia de 7 dias.">
<link rel="icon" href="img/pg04-conceito-{ROTULO}.webp">
<meta property="og:title" content="Direito Constitucional Ilustrado: 163 páginas em mapas mentais">
<meta property="og:description" content="Todo o Direito Constitucional organizado e simplificado em mapas mentais, esquemas e mnemônicos. R$17, acesso imediato.">
<meta property="og:image" content="https://marcelomapas.com/constitucional-v2/img/amostra-capa-{ROTULO}.webp">
<meta property="og:type" content="website">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

<style>{css}</style>
</head>
<body>
'''

out = rastreamento.instalar(HEAD + BODY + '</body>\n</html>\n')
assert out.count("fbq('init'") == 1 and out.count("fbq('track','PageView')") == 1
assert out.count('cdn.utmify.com.br') == 1 and out.count('window.__taos=') == 1
assert out.count(CHECKOUT) == 1, out.count(CHECKOUT)
assert out.count('href="#oferta"') == 1 and out.count('id="oferta"') == 1
assert 'fbvV7j4' not in out and 'Penal Ilustrado' not in out
assert '—' not in out and '–' not in out, 'travessão no texto'
assert not re.search(r'\bhoje\b', re.sub(r'<script[\s\S]*?</script>', '', out), re.I), 'escassez/data no texto'
assert 'data-current-date' not in out
for nome in dim:
    assert f'img/{nome}-{ROTULO}.webp' in out, nome
open(f'{DEST}/index.html', 'w', encoding='utf-8').write(out)
print('ok', len(out), 'bytes,', len(dim), 'imagens')

# mesmo .htaccess das outras páginas em teste (HTML sem cache no navegador)
shutil.copy(f'{RAIZ}/public_html/oab-v2/.htaccess', f'{DEST}/.htaccess')
