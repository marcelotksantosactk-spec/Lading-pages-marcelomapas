"""Monta public_html/tjpb/ a partir da /tjsp/ pronta (pedido do André em 29/10/2026: "cria a página com base no TJSP").

Troca só o que é do TJSP: edital, cargo, banca, data, blocos da prova, FAQ, rodapé e tema (sai a foto do
Palácio da Justiça de SP e a faixa da bandeira de SP). Cada substituição confere quantas vezes o trecho
aparece, para quebrar em vez de gerar página errada se a /tjsp/ mudar.

Fonte do edital: Edital nº 01/2026 do TJPB (FGV), lido na fonte em 29/10/2026,
~/clientes/marcelo-mapas/tjpb/PESQUISA-EDITAL-TJPB-2026.md. Cargo de Direito: Analista Judiciário,
área Judiciária (25 das 50 vagas). Prova objetiva e discursiva em 24/01/2027; objetiva com 60 questões
(10 Português, 5 Ética e Gestão, 5 Informática e Proteção de Dados, 40 específicas), aprovação com 60%.

RASCUNHO: o produto do TJ-PB ainda não existe na Kiwify (busca de 29/10). Ficam marcados com PENDENTE,
e o script não deixa publicar enquanto houver PENDENTE: checkout, preço, conteúdo do material, bônus e
a arte da dobra (por enquanto o monitor e as páginas impressas, sem o livro com "TJSP" na capa).
"""
import os, re, shutil
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.abspath(__file__))
BASE = f'{RAIZ}/public_html/tjsp'
DEST = f'{RAIZ}/public_html/tjpb'
REF = f'{RAIZ}/referencias-tjpb'
REF_TJSP = f'{RAIZ}/referencias-tjsp'
CHECKOUT = 'PENDENTE-CHECKOUT'   # trocar pelo https://pay.kiwify.com.br/<id> quando o Marcelo criar o produto
PEND = '<mark style="background:#FFE58A;color:#000;padding:0 4px">PENDENTE: {}</mark>'

s = open(f'{BASE}/index.html', encoding='utf-8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, n, old[:90])
    s = s.replace(old, new)


# ---------- head e endereços ----------
rep('Resumos Ilustrados para o Concurso TJSP', 'Resumos Ilustrados para o Concurso TJPB', s.count('Resumos Ilustrados para o Concurso TJSP'))
s = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="O conteúdo da prova de Analista Judiciário do TJPB em resumos ilustrados: mapas mentais, esquemas e mnemônicos.">',
           s, count=1)
rep('O conteúdo da prova de Escrevente do TJSP em mapas mentais, esquemas e mnemônicos.',
    'O conteúdo da prova de Analista Judiciário do TJPB em mapas mentais, esquemas e mnemônicos.',
    s.count('O conteúdo da prova de Escrevente do TJSP em mapas mentais, esquemas e mnemônicos.'))
s = s.replace('https://marcelomapas.com/tjsp/img/og-tjsp-v2.jpg', 'https://marcelomapas.com/tjpb/img/og-tjpb.jpg')
s = s.replace('https://marcelomapas.com/tjsp/', 'https://marcelomapas.com/tjpb/')

# ---------- faixa do edital no topo (contador some no dia da prova) ----------
rep('Edital nº 02/2026 publicado&nbsp;· prova prevista para 14/03/2027&nbsp;·',
    'Edital nº 01/2026 publicado&nbsp;· prova em 24/01/2027&nbsp;·')
rep('Date.UTC(2027,2,14)', 'Date.UTC(2027,0,24)')

# ---------- dobra ----------
s = re.sub(r'<img src="img/logo-tjsp\.png"[^>]*>', '', s)
rep('Foco total: Escrevente TJSP</span>', 'Foco total: Analista Judiciário TJPB</span>')
rep('do concurso do TJSP.</h1>', 'do concurso do TJPB.</h1>')
rep('alt="Material ilustrado para o concurso do TJSP no computador, impresso e em livro"',
    'alt="Material ilustrado para o concurso do TJPB no computador e impresso"')
rep('src="img/dobra-tjsp-v2.webp"', 'src="img/dobra-tjpb.webp"')
rep('O conteúdo cobrado na prova de Escrevente Técnico Judiciário do TJSP, organizado e simplificado em mapas mentais, esquemas e mnemônicos, em um único pacote.',
    'O conteúdo cobrado na prova de Analista Judiciário do TJPB, organizado e simplificado em mapas mentais, esquemas e mnemônicos, em um único pacote.')

# ---------- sumário: o que cai na prova (edital, não o conteúdo do material) ----------
rep('O que cai na prova de Escrevente, bloco por bloco:', 'O que cai na prova de Analista Judiciário, módulo por módulo:')
rep('Conferido com o Edital nº&nbsp;02/2026', 'Conferido com o Edital nº&nbsp;01/2026')
rep('<b>Material ilustrado do TJSP</b>', '<b>Material ilustrado do TJPB</b>')
ESPEC = ['Direito Constitucional', 'Direito Administrativo', 'Direito Civil e do Consumidor',
         'Direito Processual Civil', 'Direito Penal', 'Direito Processual Penal', 'Direitos Humanos e Tutela Coletiva']
GERAIS = ['Língua Portuguesa', 'Ética e Gestão no Serviço Público', 'Noções de Informática e Proteção de Dados']
i = s.index('<div class="sm2">')
j = s.index('<p style="text-align:center;margin:24px 0 0', i)
bloco = s[i:j]
li_tpl = re.search(r'<li><svg class="sm2-ck"[\s\S]*?</svg><span>[^<]*</span></li>', bloco).group(0)


def col(titulo, itens, rotulo):
    lis = ''.join(re.sub(r'<span>[^<]*</span>', f'<span>{t}</span>', li_tpl) for t in itens)
    return (f'<div class="sm2-col"><div class="sm2-h"><span class="sm2-h-t">{titulo}</span>'
            f'<span class="sm2-h-n">{rotulo}</span></div><ul class="sm2-l">{lis}</ul></div>')


s = (s[:i] + '<div class="sm2">' + col('Conhecimentos Específicos', ESPEC, '40 questões')
     + col('Conhecimentos Gerais', GERAIS, '20 questões') + '</div>' + s[j:])

# ---------- bloco "Como a prova é cobrada" ----------
a = s.index('<section id="como-cai" class="pv-sec">')
b = s.index('</section>', a) + len('</section>')


def linha(num, rotulo, titulo, disc):
    sub = f'<span class="pv-disc">{"&nbsp;· ".join(disc)}</span>' if disc else ''
    return (f'<li class="pv-row"><span class="pv-num">{num}<small>questões</small></span>'
            f'<span class="pv-txt"><span class="pv-bl">{rotulo}</span><b>{titulo}</b>{sub}</span></li>')


BLOCO = (
    '<section id="como-cai" class="pv-sec"><div class="pv-card fade-in">'
    '<span class="el-hl-kicker">Edital nº&nbsp;01/2026</span><h2>Como a prova é cobrada</h2>'
    '<div class="pv-barra" role="img" aria-label="60 questões: 40 de Conhecimentos Específicos e 20 de Conhecimentos Gerais">'
    '<span style="flex:40">40</span><span class="pv-b3" style="flex:20">20</span></div>'
    '<ul class="pv-rows">'
    + linha(40, 'Módulo II', 'Conhecimentos Específicos', ESPEC)
    + linha(10, 'Módulo I', 'Língua Portuguesa', [])
    + linha(5, 'Módulo I', 'Ética e Gestão no Serviço Público', [])
    + linha(5, 'Módulo I', 'Noções de Informática e Proteção de Dados', [])
    + '</ul><p class="pv-alerta"><b>Para passar na objetiva:</b> 60% de acerto nas 60 questões. '
      'No mesmo dia vem a discursiva, com 1 questão de 30 linhas valendo 40 pontos.</p>'
    '<p class="pv-fonte">Prova objetiva e discursiva em 24/01/2027, segundo o Edital nº&nbsp;01/2026 (FGV).</p>'
    '</div></section>')
s = s[:a] + BLOCO + s[b:]

# ---------- FAQ: troca as duas perguntas do edital do TJSP ----------
s = re.sub(r'<span class="transition-colors duration-300 ">Serve para o edital novo \(nº&nbsp;02/2026\)\?</span>',
           '<span class="transition-colors duration-300 ">Serve para o Edital nº&nbsp;01/2026?</span>', s, count=1)
rep('O conteúdo de Direito do Edital nº&nbsp;02/2026 é o mesmo do edital anterior de Escrevente, '
    'e o material segue o conteúdo programático do edital.',
    PEND.format('o Marcelo confirmar que o material cobre o conteúdo programático do Edital nº 01/2026'))
rep('<span class="transition-colors duration-300 ">É para a Capital?</span>',
    '<span class="transition-colors duration-300 ">Para qual cargo é?</span>')
rep('Este edital é para o interior e o litoral, nas circunscrições da 2ª à 10ª Região Administrativa '
    'Judiciária (RAJ). A Capital não está neste concurso.',
    'Analista Judiciário, área Judiciária, que exige formação em Direito. A prova é em 24/01/2027, '
    'pela FGV.')

# ---------- oferta (tudo que depende do produto fica marcado) ----------
rep('Material do edital + 2 bônus</span>', PEND.format('selo da oferta (conteúdo e bônus)') + '</span>')
rep('Todo o edital de Escrevente do TJSP <b>', 'Todo o edital de Analista Judiciário do TJPB <b>')
rep('<b>Material completo em PDF</b> — as 11 disciplinas do edital de Escrevente',
    '<b>Material completo em PDF</b> — ' + PEND.format('disciplinas e páginas do material'))
rep('<span class="ck-badge">', '<span class="ck-badge">', s.count('<span class="ck-badge">'))
rep('https://pay.kiwify.com.br/zRttdvv', CHECKOUT, s.count('https://pay.kiwify.com.br/zRttdvv'))

# ---------- rodapé ----------
rep('sem vínculo com o Tribunal de Justiça de São Paulo, bancas organizadoras ou órgãos públicos. '
    'Fotos do Palácio da Justiça (Wikimedia Commons): Catherine Gaspar e Rodrigo Tetsuo Argenton, CC BY-SA 4.0; '
    'Dornicke, CC BY 3.0. Ícones: Tabler Icons (MIT).',
    'sem vínculo com o Tribunal de Justiça da Paraíba, a FGV ou órgãos públicos. Ícones: Tabler Icons (MIT).')

# ---------- tema: sai SP (faixa da bandeira e fotos do Palácio), ficam as cores ----------
rep('<div class="tj-faixa-sp" aria-hidden="true"></div>', '<div class="tj-faixa-pb" aria-hidden="true"></div>')
rep('<div class="tj-cupula" aria-hidden="true"></div>', '')
s = re.sub(r'#tj \.tj-faixa-sp\{[^}]*\}', '#tj .tj-faixa-pb{position:absolute;top:0;left:0;right:0;height:10px;z-index:20;'
           'background:var(--tj-red);box-shadow:0 2px 0 var(--tj-gold)}', s, count=1)
s = s.replace(',url(img/palacio-fachada.webp) center/cover', '')
assert 'palacio-' not in re.sub(r'#tj \.tj-cupula[^}]*\}', '', s), 'foto do Palácio de SP ficou na página'
s = re.sub(r'#tj \.tj-cupula[^}]*\}', '', s)

# ---------- conferência ----------
visivel = re.sub(r'<(script|style)[\s\S]*?</\1>', '', s)
for resto in ('TJSP', 'Escrevente', 'São Paulo', 'Vunesp', '14/03', '02/2026', 'RAJ', 'Palácio', 'Capital',
              'zRttdvv', '70 questões', '11 disciplinas', 'logo-tjsp'):
    assert resto not in visivel, resto
for proibido in ('nomeaç', '9 mil', 'Oficial de Justiça', 'Atualizado em'):
    assert proibido.lower() not in visivel.lower(), proibido

# ---------- arquivos ----------
os.makedirs(f'{DEST}/img', exist_ok=True)
open(f'{DEST}/index.html', 'w', encoding='utf-8').write(s)
shutil.copy(f'{BASE}/.htaccess', f'{DEST}/.htaccess')
usados = set(re.findall(r'src="img/([^"]+)"', s)) | set(re.findall(r'url\(img/([^)]+)\)', s))
for nome in usados:
    if os.path.exists(f'{BASE}/img/{nome}'):
        shutil.copy(f'{BASE}/img/{nome}', f'{DEST}/img/{nome}')

dobra = Image.open(f'{REF}/dobra-sem-capa.png').convert('RGB')   # recorte da dobra do TJSP sem o livro
dobra.save(f'{DEST}/img/dobra-tjpb.webp', 'WEBP', quality=82, method=6)

og = Image.new('RGB', (1200, 630), (247, 240, 226))
d2 = dobra.resize((round(dobra.width * 600 / dobra.height), 600), Image.LANCZOS)
og.paste(d2, (1200 - d2.width + 10, 15))
d = ImageDraw.Draw(og)
d.rectangle((0, 0, 1200, 10), fill=(179, 21, 27))
d.rectangle((0, 10, 1200, 13), fill=(201, 166, 70))
f = ImageFont.truetype(f'{REF_TJSP}/fontes/Montserrat.ttf', 60)
f.set_variation_by_axes([800])
for k, (txt, cor) in enumerate([('Revise 5x mais', (16, 24, 32)), ('rápido para o', (16, 24, 32)),
                                ('concurso do TJPB', (179, 21, 27))]):
    d.text((62, 150 + k * 82), txt, font=f, fill=cor)
og.save(f'{DEST}/img/og-tjpb.jpg', quality=86)

faltando = [n for n in usados if not os.path.exists(f'{DEST}/img/{n}')]
assert not faltando, faltando
pend = s.count('PENDENTE')
print('ok', len(usados), 'imagens;', pend, 'marcas PENDENTE (não publicar enquanto houver)')
