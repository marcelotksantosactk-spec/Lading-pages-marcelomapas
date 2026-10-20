"""Monta public_html/tjsp/ a partir da /oab-v2/ (mesmo modelo da /3-0/ de Carreiras).

Troca só conteúdo e imagens. Cada substituição confere quantas vezes o trecho aparece,
para o script quebrar em vez de gerar página errada se a /oab-v2/ mudar.

Fontes do conteúdo:
- Produto na Kiwify: "TJSP - Tribunal de Justica de Sao Paulo", R$ 97, checkout zRttdvv.
- Estrutura da prova: edital 2025 de Escrevente Técnico Judiciário (Vunesp), segundo
  Gran Cursos e Estratégia (consultados em 28/09/2026).
- Pós-edital (20/10/2026): Edital nº 02/2026 de Escrevente (Vunesp), DEJESP edição 4542 de 19/10/2026,
  texto em ~/clientes/marcelo-mapas/tjsp-criativos/fontes/. 2ª a 10ª RAJ (Capital fora), prova objetiva
  prevista para 14/03/2027, 70 questões (16 / 30 / 24), blocos I e II eliminam abaixo de 50%.
  Aprovado pelo André; o Marcelo confirmou que o material cobre o edital novo.
- Fotos: Wikimedia Commons, CC BY-SA 4.0 (crédito no rodapé). Logo: site do TJSP.
"""
import os, re, shutil
from PIL import Image

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = f'{RAIZ}/public_html/oab-v2'
DEST = f'{RAIZ}/public_html/tjsp'
REF = f'{RAIZ}/referencias-tjsp'
REF_OAB = f'{RAIZ}/referencias-oab-v2'
CHECKOUT = 'https://pay.kiwify.com.br/zRttdvv'

s = open(f'{BASE}/index.html', encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, n, old[:90])
    s = s.replace(old, new)


# ---------- head ----------
rep('<title>Resumos Ilustrados para a 1ª Fase da OAB | Aprenda 5x Mais Rápido</title>',
    '<title>Resumos Ilustrados para o Concurso TJSP | Aprenda 5x Mais Rápido</title>')
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="O conteúdo da prova de Escrevente do TJSP em resumos ilustrados: mapas mentais, esquemas e mnemônicos. +95 mil alunos, avaliação 4.9.">',
           s, count=1)
rep('content="Resumos Ilustrados para a 1ª Fase da OAB – Aprenda 5x Mais Rápido"',
    'content="Resumos Ilustrados para o Concurso TJSP – Aprenda 5x Mais Rápido"')
rep('content="As 16 disciplinas da 1ª fase da OAB em mapas mentais, esquemas e mnemônicos."',
    'content="O conteúdo da prova de Escrevente do TJSP em mapas mentais, esquemas e mnemônicos."', 2)
rep('content="Resumos Ilustrados para a 1ª Fase da OAB"', 'content="Resumos Ilustrados para o Concurso TJSP"')
rep('https://marcelomapas.com/oab-v2/img/og.jpg', 'https://marcelomapas.com/tjsp/img/og-tjsp.jpg')
s = s.replace('https://marcelomapas.com/oab-v2/', 'https://marcelomapas.com/tjsp/')

# ---------- dobra ----------
LOGO = ('<img src="img/logo-tjsp.png" alt="Tribunal de Justiça do Estado de São Paulo" '
        'width="60" height="32" style="height:20px;width:auto;margin-right:8px;vertical-align:middle;'
        'background:#fff;border-radius:4px;padding:2px 4px">')
rep('Foco total: 1ª fase da OAB</span>', f'{LOGO}Foco total: Escrevente TJSP</span>')
rep('<span class="gold-grad">lista dos aprovados</span> da 1ª fase da OAB.</h1>',
    '<span class="gold-grad">lista dos aprovados</span> do concurso do TJSP.</h1>')
rep('<img src="img/dobra-oab.webp" alt="Material ilustrado para a 1ª fase da OAB no computador, impresso e em livro"',
    '<img src="img/dobra-tjsp.webp" alt="Material ilustrado para o concurso do TJSP no computador, impresso e em livro"')
rep('As 16 disciplinas cobradas na 1ª fase da OAB, organizadas e simplificadas em mapas mentais, esquemas e mnemônicos &mdash; em um único pacote.',
    'O conteúdo cobrado na prova de Escrevente Técnico Judiciário do TJSP, organizado e simplificado em mapas mentais, esquemas e mnemônicos, em um único pacote.')

# ---------- contagens ----------
rep('Além das 16 disciplinas ilustradas, sem custo adicional.', 'Além do material ilustrado, sem custo adicional.')
rep('E assim são as 16 disciplinas', 'E assim é o material inteiro')
rep('O sumário do material, as 16 disciplinas do combo:', 'O que cai na prova de Escrevente, bloco por bloco:')
rep('<b>16 disciplinas ilustradas</b>. Cada revisão', '<b>Material ilustrado do TJSP</b>. Cada revisão')

# ---------- carrossel de páginas: sai Ética e Legislação Especial, entra Penal ----------
def troca_pagina(img_velha, img_nova, titulo_velho, area_velha, titulo, area):
    rep(f'aria-label="Ampliar amostra: {titulo_velho}"><img src="img/{img_velha}" alt="Amostra real do material — {titulo_velho}"',
        f'aria-label="Ampliar amostra: {titulo}"><img src="img/{img_nova}" alt="Amostra real do material — {titulo}"')
    rep(f'<figcaption class="tira-rot">{titulo_velho}<span>{area_velha}</span>',
        f'<figcaption class="tira-rot">{titulo}<span>{area}</span>')

troca_pagina('pg-etica-direitos.webp', 'pg-penal-principios.webp', 'Direitos do Advogado', 'Ética da OAB',
             'Princípios e Fontes', 'Direito Penal')
troca_pagina('pg-etica-honorarios.webp', 'pg-penal-tempo.webp', 'Honorários Advocatícios', 'Ética da OAB',
             'Tempo e Lugar do Crime', 'Direito Penal')
troca_pagina('pg-leg.webp', 'pg-penal-crime.webp', 'Lei nº 13.431/2017', 'Legislação Especial',
             'Crime Impossível', 'Direito Penal')

# ---------- sumário: os blocos do edital de Escrevente ----------
i = s.index('<div class="sm2">')
j = s.index('<p style="text-align:center;margin:24px 0 0', i)
bloco = s[i:j]
li_tpl = re.search(r'<li><svg class="sm2-ck"[\s\S]*?</svg><span>[^<]*</span></li>', bloco).group(0)


def col(titulo, itens, rotulo):
    lis = ''.join(re.sub(r'<span>[^<]*</span>', f'<span>{t}</span>', li_tpl) for t in itens)
    return (f'<div class="sm2-col"><div class="sm2-h"><span class="sm2-h-t">{titulo}</span>'
            f'<span class="sm2-h-n">{rotulo}</span></div><ul class="sm2-l">{lis}</ul></div>')


c1 = ['Direito Constitucional', 'Direito Administrativo', 'Direito Penal',
      'Direito Processual Penal', 'Direito Processual Civil', 'Normas e legislação do TJSP']
c2 = ['Língua Portuguesa', 'Raciocínio Lógico', 'Matemática', 'Informática', 'Atualidades']
# na /oab-v2/ este trecho é exatamente .sm2 com as duas colunas (montado pelo oab-v2-build.py)
assert bloco.endswith('</ul></div></div>'), bloco[-60:]
s = (s[:i] + '<div class="sm2">' + col('Conhecimentos em Direito', c1, 'Bloco II')
     + col('Português e conhecimentos gerais', c2, 'Blocos I e III') + '</div>' + s[j:])

# ---------- oferta ----------
rep('<span class="ck-badge">16 disciplinas + 500 questões + 2 bônus</span>',
    '<span class="ck-badge">Material do edital + 2 bônus</span>')
rep('Todo o edital da 1ª fase da OAB <b>', 'Todo o edital de Escrevente do TJSP <b>')
itens = re.search(r'<ul class="ck-l">[\s\S]*?</ul>', s).group(0)
lis = re.findall(r'<li>[\s\S]*?</li>', itens)
assert len(lis) == 7, len(lis)
assert 'Legislação Especial' in lis[1] and '500 questões' in lis[2]
lis[0] = lis[0].replace('<b>16 disciplinas completas em PDF</b> — todo o edital ilustrado',
                        '<b>Material completo em PDF</b> — as 11 disciplinas do edital de Escrevente')
# âncora igual à do anúncio do Marcelo ("De R$871 por apenas R$97"): 661 + 47 + 30 + 77 + 56 = 871
assert lis[0].count('<s>R$ 347</s>') == 1
lis[0] = lis[0].replace('<s>R$ 347</s>', '<s>R$ 661</s>')
assert 'Material completo em PDF' in lis[0]
novo_ul = '<ul class="ck-l">' + lis[0] + ''.join(lis[3:]) + '</ul>'
rep(itens, novo_ul)
# a âncora da /oab-v2/ já é R$ 871, igual à do anúncio do TJSP: fica como está

# ---------- checkout ----------
rep('https://pay.kiwify.com.br/TGerrqk', CHECKOUT, s.count('https://pay.kiwify.com.br/TGerrqk'))

# ---------- rodapé: crédito das fotos ----------
rep('Material didático de apoio aos estudos, sem vínculo com bancas organizadoras ou órgãos públicos.',
    'Material didático de apoio aos estudos, sem vínculo com o Tribunal de Justiça de São Paulo, bancas organizadoras ou órgãos públicos. '
    'Fotos do Palácio da Justiça (Wikimedia Commons): Catherine Gaspar e Rodrigo Tetsuo Argenton, CC BY-SA 4.0; '
    'Dornicke, CC BY 3.0. Ícones: Tabler Icons (MIT).')

# ---------- pós-edital: Edital nº 02/2026 (ver docstring) ----------
# faixa no topo: some sozinha a partir do dia da prova (o contador roda no navegador, fuso de Brasília)
FAIXA_EDITAL = (
    '<div id="pv-faixa" class="pv-faixa" hidden>Edital nº 02/2026 publicado&nbsp;· '
    'prova prevista para 14/03/2027&nbsp;· <span id="pv-falta"></span></div>'
    '<script>(function(){try{var v={};new Intl.DateTimeFormat("en-CA",{timeZone:"America/Sao_Paulo",'
    'year:"numeric",month:"2-digit",day:"2-digit"}).formatToParts(new Date()).forEach(function(x){v[x.type]=x.value});'
    'var d=Math.round((Date.UTC(2027,2,14)-Date.UTC(+v.year,v.month-1,+v.day))/864e5);if(d<1)return;'
    'document.getElementById("pv-falta").innerHTML=d===1?"falta <b>1</b> dia":"faltam <b>"+d+"</b> dias";'
    'document.getElementById("pv-faixa").hidden=false}catch(e){}})();</script>')
rep('<main><section class="relative flex items-start sm:items-center pt-30',
    '<main>' + FAIXA_EDITAL + '<section class="relative flex items-start sm:items-center pt-30')

rep('Atualizado em <span data-current-date="true" data-locale="pt-BR" data-timezone="America/Sao_Paulo" '
    'data-format="month-year">agosto de 2026</span>', 'Conferido com o Edital nº&nbsp;02/2026')

# bloco "Como a prova é cobrada": cada bloco ligado às disciplinas que o sumário já lista (c1, c2)
assert c2[0] == 'Língua Portuguesa'


def linha_bloco(n, num, titulo, disc, elimina):
    tag = ('<span class="pv-tag pv-tag--el">Elimina abaixo de 50%</span>' if elimina
           else '<span class="pv-tag">Só classifica</span>')
    sub = f'<span class="pv-disc">{"&nbsp;· ".join(disc)}</span>' if disc else ''
    return (f'<li class="pv-row"><span class="pv-num">{num}<small>questões</small></span>'
            f'<span class="pv-txt"><span class="pv-bl">Bloco {n}</span><b>{titulo}</b>{sub}{tag}</span></li>')


BLOCO_PROVA = (
    '<section id="como-cai" class="pv-sec"><div class="pv-card fade-in">'
    '<span class="el-hl-kicker">Edital nº&nbsp;02/2026</span><h2>Como a prova é cobrada</h2>'
    '<div class="pv-barra" role="img" aria-label="70 questões: 16 de Português, 30 de Direito, 24 de Conhecimentos Gerais">'
    '<span style="flex:16">16</span><span style="flex:30">30</span><span class="pv-b3" style="flex:24">24</span></div>'
    '<ul class="pv-rows">'
    + linha_bloco('I', 16, 'Língua Portuguesa', [], True)
    + linha_bloco('II', 30, 'Conhecimentos em Direito', c1, True)
    + linha_bloco('III', 24, 'Conhecimentos Gerais', c2[1:], False)
    + '</ul><p class="pv-alerta"><b>Português e Direito eliminam:</b> 46 das 70 questões exigem 50% de acerto em cada bloco.</p>'
    '<p class="pv-fonte">Prova objetiva prevista para 14/03/2027, segundo o Edital nº&nbsp;02/2026 (Vunesp).</p>'
    '</div></section>\n')
rep('<section id="depoimentos" class="tm-sec">', BLOCO_PROVA + '<section id="depoimentos" class="tm-sec">')

# FAQ: duas perguntas novas no topo, no mesmo molde das que já existem
faq_i = s.index('<div class="bg-[var(--card)] border border-[var(--border)] rounded-xl overflow-hidden card-glow hover:border-gold"><details class="faqfix-details">')
faq_j = s.index('</details></div>', faq_i) + len('</details></div>')
faq_tpl = s[faq_i:faq_j]
assert 'Como terei acesso ao material?' in faq_tpl
faq_p = re.search(r'<span class="transition-colors duration-300 ">[^<]*</span>', faq_tpl).group(0)
faq_r = re.search(r'(<div class="px-6 pb-5[^"]*">)[^<]*(</div>)', faq_tpl)


def faq(pergunta, resposta):
    return (faq_tpl.replace(faq_p, f'<span class="transition-colors duration-300 ">{pergunta}</span>')
            .replace(faq_r.group(0), faq_r.group(1) + resposta + faq_r.group(2)))


# "Serve para Oficial de Justiça?" fica de fora de propósito: não há resposta confirmada.
s = s[:faq_i] + faq('Serve para o edital novo (nº&nbsp;02/2026)?',
                    'Sim. O conteúdo de Direito do Edital nº&nbsp;02/2026 é o mesmo do edital anterior de Escrevente, '
                    'e o material segue o conteúdo programático do edital.') \
    + faq('É para a Capital?',
          'Este edital é para o interior e o litoral, nas circunscrições da 2ª à 10ª Região Administrativa '
          'Judiciária (RAJ). A Capital não está neste concurso.') + s[faq_i:]

EDITAL_CSS = '''<style id="tjsp-edital">
.pv-faixa{position:relative;z-index:30;background:var(--tj-navy);color:#F7F0E2;text-align:center;
 font-size:.78rem;font-weight:600;line-height:1.45;letter-spacing:.01em;padding:10px 18px;text-wrap:balance}
.pv-faixa[hidden]{display:none!important}
.pv-faixa b{color:var(--tj-gold-l);font-weight:800;font-variant-numeric:tabular-nums}
.pv-sec{background-color:var(--tj-creme);background-image:url(img/padrao-claro.svg);background-size:440px 440px;padding:8px 20px 72px}
.pv-card{max-width:820px;margin:0 auto;background:#fff;border-radius:22px;padding:36px 22px 30px;
 box-shadow:0 18px 50px rgba(16,24,32,.08);border:1px solid rgba(16,24,32,.07)}
.pv-card h2{font-family:"Oswald","Montserrat",sans-serif;text-transform:uppercase;font-weight:700;
 font-size:1.55rem;line-height:1.2;text-align:center;color:var(--tj-navy);margin:0;text-wrap:balance}
.pv-barra{display:flex;gap:3px;height:34px;margin:24px 0 6px;border-radius:8px;overflow:hidden}
.pv-barra span{display:flex;align-items:center;justify-content:center;background:var(--tj-navy);color:#F7F0E2;
 font-weight:800;font-size:.85rem;font-variant-numeric:tabular-nums}
.pv-barra .pv-b3{background:#E9DFC6;color:var(--tj-navy)}
.pv-rows{list-style:none;margin:6px 0 0;padding:0}
.pv-row{display:grid;grid-template-columns:64px 1fr;gap:14px;align-items:start;padding:16px 0;border-top:1px solid rgba(16,24,32,.09)}
.pv-row:first-child{border-top:0}
.pv-num{font-weight:900;font-size:2.1rem;line-height:1;color:var(--tj-navy);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.pv-num small{display:block;font-size:.62rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#6B6A60;margin-top:5px}
.pv-txt{display:flex;flex-direction:column;align-items:flex-start;gap:3px;min-width:0}
.pv-bl{font-size:.68rem;font-weight:800;letter-spacing:.16em;text-transform:uppercase;color:var(--tj-red)}
.pv-txt b{font-size:1rem;color:#141414;line-height:1.3}
.pv-disc{font-size:.84rem;line-height:1.55;color:#55544C}
.pv-tag{margin-top:6px;font-size:.68rem;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
 padding:5px 9px;border-radius:6px;background:#EFEADC;color:#55544C}
.pv-tag--el{background:rgba(179,21,27,.08);color:var(--tj-red)}
.pv-alerta{margin:14px 0 0;padding:14px 16px;border-left:4px solid var(--tj-red);background:rgba(179,21,27,.05);
 border-radius:0 10px 10px 0;font-size:.95rem;line-height:1.55;color:#141414;text-wrap:pretty}
.pv-alerta b{color:var(--tj-red)}
.pv-fonte{margin:14px 0 0;font-size:.76rem;line-height:1.5;color:#6B6A60;text-align:center}
</style>'''
MEDIA_EDITAL = ('<style>@media(min-width:640px){#tj .pv-faixa{font-size:.85rem}#tj .pv-card{padding:50px 56px 40px}'
                '#tj .pv-card h2{font-size:2.15rem}#tj .pv-row{grid-template-columns:96px 1fr}#tj .pv-num{font-size:2.6rem}}</style>')

# ---------- tema visual TJSP ----------
# Cores do brasão (referencias-tjsp/01-marca-tjsp/PALETA.md) e o jeito decorativo dos criativos da
# Gaby no Tribunal: ícones de tribunal em traço fino no fundo, faixa da bandeira de SP, fotos do
# Palácio da Justiça nas seções escuras. Só cor e decoração: texto e estrutura não mudam.
DOBRA = 'dobra-tjsp-v2.webp'   # nome novo a cada troca: o Cloudflare guarda imagem por 180 dias
rep('src="img/dobra-tjsp.webp"', f'src="img/{DOBRA}"')
rep('https://marcelomapas.com/tjsp/img/og-tjsp.jpg', 'https://marcelomapas.com/tjsp/img/og-tjsp-v2.jpg')

FAIXA_SP = '<div class="tj-faixa-sp" aria-hidden="true"></div>'
rep('<section class="relative flex items-start sm:items-center pt-30 sm:pt-20 overflow-hidden hero-bg is-light el-hero">',
    '<section class="relative flex items-start sm:items-center pt-30 sm:pt-20 overflow-hidden hero-bg is-light el-hero">' + FAIXA_SP)
rep('<section id="compre" class="ck-sec">',
    '<div class="tj-cupula" aria-hidden="true"></div><section id="compre" class="ck-sec">')

TEMA = '''<style id="tema-tjsp">
:root,.is-light{--tj-red:#B3151B;--tj-red2:#8F1015;--tj-navy:#101820;--tj-navy2:#18222D;
 --tj-gold:#C9A646;--tj-gold-l:#E3C766;--tj-gold-d:#8C7A2E;--tj-creme:#F7F0E2;
 --gold:#C9A646;--gold-light:#E3C766;--gold-dark:#8C7A2E}
/* faixa da bandeira de SP no alto da dobra */
.tj-faixa-sp{position:absolute;top:0;left:0;right:0;height:22px;z-index:20;
 background:linear-gradient(90deg,var(--tj-red) 0 70px,transparent 70px),
 repeating-linear-gradient(180deg,var(--tj-navy) 0 4.4px,#F8F8F8 4.4px 8.8px);
 box-shadow:0 2px 0 var(--tj-gold)}
/* fundo creme com ícones de tribunal em traço fino */
.el-hero,.tira-sec,.bn-sec,.ck-sec,.el-hl,.tm-sec{background-color:var(--tj-creme)!important;
 background-image:url(img/padrao-claro.svg)!important;background-size:440px 440px!important}
.el-hero{background-image:radial-gradient(ellipse at 50% 62%,rgba(201,166,70,.28),transparent 58%),url(img/padrao-claro.svg)!important;
 background-size:auto,440px 440px!important}
.hero-amostra img{filter:drop-shadow(0 18px 30px rgba(16,24,32,.18))}
/* seções escuras: fachada do Palácio sob azul-noite */
.sec-escura{background:linear-gradient(180deg,rgba(16,24,32,.84),rgba(16,24,32,.93)),url(img/palacio-fachada.webp) center/cover!important;
 border-top:3px solid var(--tj-gold);border-bottom:3px solid var(--tj-gold)}
.sec-escura article{background:rgba(255,255,255,.045)!important;border-color:rgba(227,199,102,.22)!important;border-top-color:var(--tj-gold)!important}
.sec-escura svg{color:var(--tj-gold-l)}
.sec-escura .tag,.cmp-tag{color:var(--tj-gold-l)!important;border-color:rgba(227,199,102,.4)!important;background:rgba(227,199,102,.08)!important}
/* faixa da cúpula antes da oferta */
.tj-cupula{height:190px;background:linear-gradient(180deg,rgba(16,24,32,.25),rgba(16,24,32,.45)),url(img/palacio-cupula.webp) center/cover;
 border-top:3px solid var(--tj-gold);border-bottom:3px solid var(--tj-gold)}
@media(min-width:768px){.tj-cupula{height:260px}}
/* destaques */
.gold-grad,.el-hero .gold-grad,h1 .gold-grad{background:none!important;color:var(--tj-red)!important;-webkit-text-fill-color:var(--tj-red)!important}
.sec-escura .gold-grad{color:var(--tj-gold-l)!important;-webkit-text-fill-color:var(--tj-gold-l)!important}
.el-kicker,.au-kicker{color:var(--tj-red)!important}
.tira-tag,.ck-badge,.bn-tag,.el-hl-kicker{background:linear-gradient(135deg,var(--tj-gold-l),var(--tj-gold))!important;color:#2A2208!important}
.ck-val,.ck-val small{color:var(--tj-navy)!important}
.sm2-ck,.el-hl-check,.of-chk{color:var(--tj-red)!important}
.ck-ok{background:var(--tj-navy)!important;color:var(--tj-gold-l)!important}
.tm-stars svg,.tm-nota span{color:var(--tj-gold)!important}
.tm-dot.on,.amt-dot.on{background:var(--tj-red)!important}
.el-hero .tag{border-color:rgba(179,21,27,.25)!important;background:rgba(255,255,255,.75)!important}
/* botões de compra: ficam no verde original da /3-0/ (vermelho em botão de compra gera rejeição) */
.dp-selo--data{color:var(--tj-red)!important;background:rgba(179,21,27,.07)!important;border-color:rgba(179,21,27,.3)!important}
.dp-selo--data span{color:var(--tj-red)!important}
.dp-selo--data i{background:var(--tj-red)!important;color:var(--tj-red)!important}
.rd-selo svg{color:var(--tj-red)!important}
.tm-tag svg{color:var(--tj-gold-l)!important}
.ck-card{border-color:var(--tj-gold)!important;box-shadow:0 14px 40px rgba(16,24,32,.10),0 0 0 4px rgba(201,166,70,.12)!important}
</style>'''
TEMA = TEMA.replace('.hero-amostra img{filter:drop-shadow(0 18px 30px rgba(16,24,32,.18))}',
    '.hero-amostra img{mix-blend-mode:multiply}')


def prefixa(css, pre='#tj '):
    """Prefixa cada seletor com o id do body, para o tema ganhar das ~60 folhas de estilo herdadas."""
    def um(m):
        sels = m.group(1)
        if sels.strip().startswith((':root', '@')):
            return m.group(0)
        return ','.join(pre + x.strip() for x in sels.split(',')) + '{'
    return re.sub(r'(?m)(?<=[}\n])([^{}@/]+)\{', um, css)


rep('<body', '<body id="tj"')
rep('</body>', prefixa(TEMA) + prefixa(EDITAL_CSS) + MEDIA_EDITAL + '</body>')

visivel = re.sub(r'<(script|style)[\s\S]*?</\1>', '', s).replace('quem estuda para a OAB, para concursos', '')
for resto in ('OAB', 'oab-v2', '1ª fase', '16 disciplinas', 'TGerrqk'):
    assert resto not in visivel, resto
# proibido no pós-edital (só cadastro de reserva, salário não é R$ 9 mil, sem escassez falsa)
for proibido in ('vaga', 'nomeaç', 'nomeac', '9 mil', '9.000', 'Oficial de Justiça', 'Atualizado em'):
    assert proibido.lower() not in visivel.lower(), proibido

# ---------- arquivos ----------
os.makedirs(f'{DEST}/img', exist_ok=True)
open(f'{DEST}/index.html', 'w', encoding='utf-8').write(s)
shutil.copy(f'{BASE}/.htaccess', f'{DEST}/.htaccess')
usados = set(re.findall(r'src="img/([^"]+)"', s))
for nome in usados:
    if os.path.exists(f'{BASE}/img/{nome}'):
        shutil.copy(f'{BASE}/img/{nome}', f'{DEST}/img/{nome}')


def webp(origem, nome, largura):
    im = Image.open(origem).convert('RGB')
    if im.width > largura:
        im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    im.save(f'{DEST}/img/{nome}', 'WEBP', quality=82, method=6)


webp(f'{REF}/03-dobra-atual/dobra-tjsp.png', DOBRA, 980)
webp(f'{REF}/02-fotos-tjsp/foto-14.jpg', 'palacio-fachada.webp', 1600)
cup = Image.open(f'{REF}/02-fotos-tjsp/foto-02.jpg').convert('RGB')
alt = round(cup.width * 0.36)   # só a faixa que aparece na página (proporção ~16:6)
topo = round(cup.height * 0.20)
cup.crop((0, topo, cup.width, topo + alt)).resize((1400, round(1400 * alt / cup.width)), Image.LANCZOS) \
   .save(f'{DEST}/img/palacio-cupula.webp', 'WEBP', quality=72, method=6)
shutil.copy(f'{REF}/04-icones/padrao-claro.svg', f'{DEST}/img/padrao-claro.svg')

# imagem de compartilhamento (og), na paleta do TJSP
from PIL import ImageDraw, ImageFont
og = Image.new('RGB', (1200, 630), (247, 240, 226))
padrao_bg = Image.open(f'{DEST}/img/palacio-cupula.webp').convert('RGB').resize((1200, 900)).crop((0, 135, 1200, 765))
og = Image.blend(og, padrao_bg, 0.10)
dobra = Image.open(f'{REF}/03-dobra-atual/dobra-tjsp.png').convert('RGB')
dobra = dobra.resize((round(dobra.width * 600 / dobra.height), 600), Image.LANCZOS)
og.paste(dobra, (1200 - dobra.width + 10, 15))
d = ImageDraw.Draw(og)
d.rectangle((0, 0, 1200, 14), fill=(16, 24, 32))
d.rectangle((0, 0, 90, 14), fill=(179, 21, 27))
d.rectangle((0, 14, 1200, 17), fill=(201, 166, 70))
f = ImageFont.truetype(f'{REF}/fontes/Montserrat.ttf', 60)
f.set_variation_by_axes([800])
for k, (linha, cor) in enumerate([('Revise 5x mais', (16, 24, 32)), ('rápido para o', (16, 24, 32)),
                                  ('concurso do TJSP', (179, 21, 27))]):
    d.text((62, 150 + k * 82), linha, font=f, fill=cor)
og.save(f'{DEST}/img/og-tjsp-v2.jpg', quality=86)
webp(f'{REF_OAB}/02-paginas-reais/penal-principios-e-fontes.webp', 'pg-penal-principios.webp', 707)
webp(f'{REF_OAB}/02-paginas-reais/penal-tempo-e-lugar-do-crime.webp', 'pg-penal-tempo.webp', 707)
webp(f'{REF_OAB}/02-paginas-reais/penal-crime-impossivel.webp', 'pg-penal-crime.webp', 707)
lg = Image.open(f'{REF}/01-marca-tjsp/logo-tjsp-original.png')
lg.save(f'{DEST}/img/logo-tjsp.png')
faltando = [n for n in usados if not os.path.exists(f'{DEST}/img/{n}')]
assert not faltando, faltando
print('ok', len(usados), 'imagens')
