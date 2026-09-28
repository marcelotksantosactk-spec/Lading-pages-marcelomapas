"""Baixa fotos do TJSP do Wikimedia Commons e escreve CREDITOS.md (autor, licença, link)."""
import json, re, ssl, urllib.parse, urllib.request, html
import certifi
CTX=ssl.create_default_context(cafile=certifi.where())
UA={'User-Agent':'TAOS-site/1.0 (taosmidia@gmail.com)'}
TITULOS=[
 ("foto-01.jpg","File:Palácio da Justiça de São Paulo por Rodrigo Tetsuo Argenton (01).jpg"),
 ("foto-02.jpg","File:Palácio da Justiça de São Paulo por Rodrigo Tetsuo Argenton (03).jpg"),
 ("foto-05.jpg","File:Palácio da Justiça de São Paulo 01.jpg"),
 ("foto-07.jpg","File:Palácio da Justiça de São Paulo por Rodrigo Tetsuo Argenton (06).jpg"),
 ("foto-08.jpg","File:Palácio da Justiça de São Paulo por Rodrigo Tetsuo Argenton (09).jpg"),
 ("foto-09.jpg","File:Palácio da Justiça de São Paulo por Rodrigo Tetsuo Argenton (12).jpg"),
 ("foto-10.jpg","File:Museu do Tribunal de Justiça 01.jpg"),
 ("foto-11.jpg","File:Museu do Tribunal de Justiça 05.jpg"),
 ("foto-13.jpg","File:Lateral do Palacio da Justiça do São Paulo.jpg"),
 ("foto-14.jpg","File:Palácio da Justiça, São Paulo 01.JPG"),
]
linhas=["# Créditos das fotos (Wikimedia Commons)","",
"Todas exigem crédito ao autor. As CC BY-SA exigem também que a imagem derivada (capa, mockup)",
"saia sob a mesma licença. O crédito vai no rodapé da página.","",
"| Arquivo | Autor | Licença | Original |","|---|---|---|---|"]
for arq,t in TITULOS:
    q=urllib.parse.urlencode({'action':'query','titles':t,'prop':'imageinfo','iiprop':'url|extmetadata|size','iiurlwidth':1920,'format':'json'})
    d=json.load(urllib.request.urlopen(urllib.request.Request('https://commons.wikimedia.org/w/api.php?'+q,headers=UA),context=CTX))
    p=list(d['query']['pages'].values())[0]
    if 'imageinfo' not in p: print('sem',t); continue
    ii=p['imageinfo'][0]; m=ii['extmetadata']
    autor=html.unescape(re.sub('<[^>]+>','',m.get('Artist',{}).get('value',''))).strip()
    lic=m.get('LicenseShortName',{}).get('value','')
    url=ii.get('thumburl') or ii['url']
    open(arq,'wb').write(urllib.request.urlopen(urllib.request.Request(url,headers=UA),context=CTX).read())
    linhas.append(f"| {arq} | {autor} | {lic} | {ii['descriptionurl']} |")
    print(arq,lic,autor)
open('CREDITOS.md','w').write('\n'.join(linhas)+'\n')
