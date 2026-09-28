from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import numpy as np
W,H=600,900
F='../fontes/Montserrat.ttf'
def font(sz,w):
    f=ImageFont.truetype(F,sz); f.set_variation_by_axes([w]); return f
bg=Image.new('RGB',(W,H),(10,10,10))
ph=Image.open('../02-fotos-tjsp/foto-05.jpg').convert('L')
# recorte vertical centrado no pórtico
pw,phh=ph.size
cw=int(phh*0.62); x0=int(pw*0.5-cw*0.5)
ph=ph.crop((x0,0,x0+cw,phh)).resize((W+40,int(phh*(W+40)/cw)))
ph=ImageEnhance.Contrast(ph).enhance(1.25); ph=ImageEnhance.Brightness(ph).enhance(0.85)
ph=ph.crop((0,0,W,H)) if ph.height>=H else ph.resize((W,H))
ph=ImageOps.colorize(ph,black=(12,18,26),white=(236,214,160)).convert('RGB')
# máscara: escurece topo e esquerda como na capa original
y=np.linspace(0,1,H)[:,None]; x=np.linspace(0,1,W)[None,:]
m=np.clip((y-0.18)/0.35,0,1)*np.clip((x+0.15)/0.7,0,1)
m=np.clip(m,0,1)*0.95
bgA=np.array(bg).astype(float); phA=np.array(ph).astype(float)
out=bgA*(1-m[...,None])+phA*m[...,None]
im=Image.fromarray(out.astype(np.uint8))
d=ImageDraw.Draw(im)
# caixa branca do topo
d.rectangle((50,70,568,140),fill=(179,21,27))
d.rectangle((50,140,568,146),fill=(201,166,70))
t='CONCURSO TJSP'; f=font(40,800)
bb=d.textbbox((0,0),t,font=f); d.text((309-(bb[2]-bb[0])/2-bb[0],105-(bb[3]-bb[1])/2-bb[1]),t,font=f,fill=(250,250,250))
# RESUMOS amarelo
f=font(58,900); t='RESUMOS'
bb=d.textbbox((0,0),t,font=f); w=bb[2]-bb[0]
d.rectangle((45,242,45+w+26,304),fill=(201,166,70))
d.text((58-bb[0],273-(bb[3]-bb[1])/2-bb[1]),t,font=f,fill=(12,12,12))
f=font(40,800); d.text((75,312),'MAPEADOS',font=f,fill=(250,250,250))
# subtítulo do cargo
f=font(24,700); d.text((78,365),'Escrevente Técnico Judiciário',font=f,fill=(230,230,230))
# bullets
f=font(21,700)
for i,t in enumerate(['Mapas mentais','Esquemas visuais','Mnemônicos','Questões comentadas'][:3]):
    d.text((178,600+i*34),t,font=f,fill=(245,245,245))
# rodapé @marcelomapas
g=Image.new('L',(360,56)); gd=ImageDraw.Draw(g)
for xx in range(360): gd.line([(xx,0),(xx,56)],fill=int(150*min(1,xx/120)))
grad=Image.new('RGB',(360,56),(70,70,70)); im.paste(grad,(240,795),g)
f=font(34,700); d=ImageDraw.Draw(im); d.text((258,800),'@marcelomapas',font=f,fill=(235,235,235))
im.save('capa-tjsp.png')
