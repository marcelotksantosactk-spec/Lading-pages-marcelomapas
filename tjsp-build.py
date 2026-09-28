"""Monta public_html/tjsp/ a partir da /oab-v2/ (mesmo modelo da /3-0/ de Carreiras).

Troca só conteúdo e imagens. Cada substituição confere quantas vezes o trecho aparece,
para o script quebrar em vez de gerar página errada se a /oab-v2/ mudar.

Fontes do conteúdo:
- Produto na Kiwify: "TJSP - Tribunal de Justica de Sao Paulo", R$ 97, checkout zRttdvv.
- Estrutura da prova: edital 2025 de Escrevente Técnico Judiciário (Vunesp), segundo
  Gran Cursos e Estratégia (consultados em 28/09/2026). Novo edital: em estudo.
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
                        '<b>Material completo em PDF</b> — o edital de Escrevente ilustrado')
assert 'Material completo em PDF' in lis[0]
novo_ul = '<ul class="ck-l">' + lis[0] + ''.join(lis[3:]) + '</ul>'
rep(itens, novo_ul)
rep('De <s>R$ 871</s> por só', 'De <s>R$ 557</s> por só')

# ---------- checkout ----------
rep('https://pay.kiwify.com.br/TGerrqk', CHECKOUT, s.count('https://pay.kiwify.com.br/TGerrqk'))

# ---------- rodapé: crédito das fotos ----------
rep('Material didático de apoio aos estudos, sem vínculo com bancas organizadoras ou órgãos públicos.',
    'Material didático de apoio aos estudos, sem vínculo com o Tribunal de Justiça de São Paulo, bancas organizadoras ou órgãos públicos. '
    'Foto do Palácio da Justiça: Catherine Gaspar, Wikimedia Commons, CC BY-SA 4.0.')

visivel = re.sub(r'<(script|style)[\s\S]*?</\1>', '', s).replace('quem estuda para a OAB, para concursos', '')
for resto in ('OAB', 'oab-v2', '1ª fase', '16 disciplinas', 'TGerrqk'):
    assert resto not in visivel, resto

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


webp(f'{REF}/dobra-tjsp.png', 'dobra-tjsp.webp', 980)
webp(f'{REF_OAB}/02-paginas-reais/penal-principios-e-fontes.webp', 'pg-penal-principios.webp', 707)
webp(f'{REF_OAB}/02-paginas-reais/penal-tempo-e-lugar-do-crime.webp', 'pg-penal-tempo.webp', 707)
webp(f'{REF_OAB}/02-paginas-reais/penal-crime-impossivel.webp', 'pg-penal-crime.webp', 707)
lg = Image.open(f'{REF}/logo-tjsp-original.png')
lg.save(f'{DEST}/img/logo-tjsp.png')
faltando = [n for n in usados if not os.path.exists(f'{DEST}/img/{n}')]
assert not faltando, faltando
print('ok', len(usados), 'imagens')
