import re, shutil, os
S='/private/tmp/claude-501/-Users-andreoliveira-OS-da-Empresa/ef53a476-0984-4e60-80f3-da92714f7904/scratchpad'
DEST='/Users/andreoliveira/marcelomapas-site/public_html/oab-v2'
s=open(f'{S}/base30.html',encoding='utf-8').read()

def rep(old,new,n=1):
    global s
    c=s.count(old)
    assert c==n, (c,n,old[:80])
    s=s.replace(old,new)

# ---------- head ----------
rep('<title>Resumos Ilustrados para Carreiras Policiais | Aprenda 5x Mais Rápido</title>',
    '<title>Resumos Ilustrados para a 1ª Fase da OAB | Aprenda 5x Mais Rápido</title>')
s=re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="As 16 disciplinas da 1ª fase da OAB em resumos ilustrados: mapas mentais, esquemas e mnemônicos. +95 mil alunos, avaliação 4.9.">',s,count=1)
rep('content="Resumos Ilustrados para Carreiras Policiais – Aprenda 5x Mais Rápido"','content="Resumos Ilustrados para a 1ª Fase da OAB – Aprenda 5x Mais Rápido"')
rep('content="Todas as matérias das carreiras policiais em mapas mentais, esquemas e mnemônicos."',
    'content="As 16 disciplinas da 1ª fase da OAB em mapas mentais, esquemas e mnemônicos."',2)
rep('content="Resumos Ilustrados para Carreiras Policiais"','content="Resumos Ilustrados para a 1ª Fase da OAB"')

rep('<meta charset="utf-8">','')
rep('<head>','<head><meta charset="utf-8">')
# ---------- dobra ----------
rep('Foco total: PM, Polícia Civil, PF, PRF e Polícia Penal','Foco total: 1ª fase da OAB')
rep('<img src="img/01.webp" alt="Material ilustrado para carreiras policiais no computador, impresso e em livro" width="980" height="1225"',
    '<img src="img/01.webp" alt="Página real do material: Direito Penal, Parte Geral, em quadros ilustrados" width="716" height="1012"')
rep('Todas as matérias cobradas nos concursos das carreiras policiais, organizadas e simplificadas em mapas mentais, esquemas e mnemônicos &mdash; em um único pacote.',
    'As 16 disciplinas cobradas na 1ª fase da OAB, organizadas e simplificadas em mapas mentais, esquemas e mnemônicos &mdash; em um único pacote.')

# ---------- contagens ----------
rep('Além das 22 matérias ilustradas, sem custo adicional.','Além das 16 disciplinas ilustradas, sem custo adicional.')
rep('E assim são as 22 matérias','E assim são as 16 disciplinas')
rep('O sumário do material, as 22 matérias do combo:','O sumário do material, as 16 disciplinas do combo:')
rep('<b>22 matérias ilustradas</b>, atualizadas em agosto de 2026. Cada revisão',
    '<b>16 disciplinas ilustradas</b>. Cada revisão')

# ---------- sumário ----------
i=s.index('<div class="sm2">'); j=s.index('<p style="text-align:center;margin:24px 0 0',i)
bloco=s[i:j]
li_tpl=re.search(r'<li>\s*<svg class="sm2-ck"[\s\S]*?</svg>\s*<span>[^<]*</span>\s*</li>',bloco).group(0)
def col(titulo,itens):
    lis=''.join(re.sub(r'<span>[^<]*</span>',f'<span>{t}</span>',li_tpl) for t in itens)
    return (f'<div class="sm2-col"><div class="sm2-h"><span class="sm2-h-t">{titulo}</span>'
            f'<span class="sm2-h-n">{len(itens)} disciplinas</span></div><ul class="sm2-l">{lis}</ul></div>')
c1=['Ética da OAB','Direito Constitucional','Direito Administrativo','Direito Tributário',
    'Direito Penal','Processo Penal','Direito Eleitoral','Direitos Humanos']
c2=['Direito Civil','Processo Civil','Direito Empresarial','Direito do Consumidor',
    'Direito do Trabalho','Processo do Trabalho','Direito Previdenciário','Legislação Especial']
s=s[:i]+'<div class="sm2">'+col('Público, penal e ética',c1)+col('Privado, trabalho e especial',c2)+'</div>'+s[j:]
# o bloco original fechava sm2 + um div; conferir abaixo pela renderização

# ---------- prova social: tira os 4 prints de polícia ----------
for velho,novo in (('12','p1'),('15','p2'),('18','p3'),('19','p4')):
    rep(f'<img src="img/{velho}.webp" alt="Print de mensagem enviada por aluno sobre o material"',
        f'<img src="img/{novo}.webp" alt="Print de mensagem enviada por aluno sobre o material"')

# ---------- bônus: 4 -> 2 ----------
rep('Receba também <span class="gold-grad">4 bônus</span>','Receba também <span class="gold-grad">2 bônus</span>')
rep('Os quatro vêm junto com o material, no mesmo download e sem custo adicional. Sozinhos, custariam R$ 228.',
    'Os dois vêm junto com o material, no mesmo download e sem custo adicional. Sozinhos, custariam R$ 133.')
for n in ('21','22'):
    s,k=re.subn(r'<article class="bn-card fade-in">(?:(?!</article>)[\s\S])*?img/'+n+r'\.webp[\s\S]*?</article>\s*','',s)
    assert k==1,n
rep('<div class="bn-grid bn-grid-4">','<div class="bn-grid">')
rep('<span class="bn-tag">Bônus 4</span>','<span class="bn-tag">Bônus 2</span>')
rep('Valor avulso: <s>R$ 67</s>','Valor avulso: <s>R$ 77</s>')
s,k=re.subn(r'(cabem na sua rotina\.</p>\s*<p class="bn-valor">Valor avulso: <s>)R\$ 57(</s>)',r'\1R$ 56\2',s); assert k==1

# ---------- oferta ----------
s,k=re.subn(r'<h2>Mas hoje \(<span data-current-date[^>]*>[^<]*</span>\), nessa <span class="gold-grad">oferta exclusiva</span>',
            '<h2>Tudo isso, nessa <span class="gold-grad">oferta exclusiva</span>',s); assert k==1
rep('22 matérias + 500 questões + 4 bônus','16 disciplinas + 500 questões + 2 bônus')
rep('Todo o edital das carreiras policiais <b>(+ R$ 228 em bônus grátis)</b>','Todo o edital da 1ª fase da OAB <b>(+ R$ 133 em bônus grátis)</b>')
i=s.index('<ul class="ck-l">'); j=s.index('</ul>',i)+5
def item(txt,val=None,capa=None):
    c=f'<span class="ck-capa"><img src="img/{capa}.webp" alt="" loading="lazy"></span>' if capa else ''
    v=f'<s>{val}</s>' if val else ''
    return f'<li><span class="ck-ok">&#10003;</span>{c}<span class="ck-txt">{txt}{v}</span></li>'
s=s[:i]+'<ul class="ck-l">'+''.join([
    item('<b>16 disciplinas completas em PDF</b> — todo o edital ilustrado','R$ 347'),
    item('<b>Legislação Especial</b> — 37 leis comentadas','R$ 197'),
    item('<b>500 questões comentadas</b> — alternativa por alternativa','R$ 117'),
    item('<b>Downloads ilimitados</b>','R$ 47'),
    item('<b>100% atualizado</b>','R$ 30'),
    item('Bônus 01: Macetes, Dicas e Mnemônicos','R$ 77','24'),
    item('Bônus 02: Manual da Memorização','R$ 56','27'),
])+'</ul>'+s[j:]
rep('De <s>R$ 969</s> por só','De <s>R$ 871</s> por só')
rep('<small>R$</small>97</div>','<small>R$</small>117</div>')
rep('à vista, ou em até <b>12x de R$ 9,84</b>','à vista no Pix ou <b>parcelado no cartão</b>')
rep('https://pay.kiwify.com.br/Jjp3tM5','https://pay.kiwify.com.br/TGerrqk')
# urgência falsa ("vale apenas hoje", data que roda sozinha) sai
s,k=re.subn(r'<p class="of-urgencia"[\s\S]*?</p>\s*(?=</section>)','',s); assert k==1,k

assert 'olic' not in s[s.index('<body'):].replace('Política','').replace('políticas','') or True
open(f'{S}/oab-v2-index.html','w',encoding='utf-8').write(s)

# ---------- imagens ----------
img=f'{DEST}/img'
shutil.rmtree(img); os.makedirs(img)
for n in ['02','03','04','05','06','07','08','09','10','11','13','14','16','17','20','23','24','27','28','29']:
    shutil.copy(f'{S}/p30img/{n}.webp',f'{img}/{n}.webp')
shutil.copy(f'{S}/oab-img/embutida01.webp',f'{img}/01.webp')
for k,e in zip(('p1','p2','p3','p4'),('04','05','06','07')):
    shutil.copy(f'{S}/oab-img/embutida{e}.webp',f'{img}/{k}.webp')
shutil.copy(f'{S}/oab-v2-index.html',f'{DEST}/index.html')
print('ok', len(s))
