import cv2, numpy as np
from PIL import Image
m=np.array(Image.open('/Users/andreoliveira/marcelomapas-site/public_html/oab-v2/img/dobra-oab.webp').convert('RGB'))[:,:,::-1].copy()
old=cv2.imread('/Users/andreoliveira/marcelomapas-site/referencias-oab-v2/01-mockup/capa-livro-oab.png')
new=cv2.imread('capa-tjsp.png')
H=np.load('homografia-capa.npy')
sz=(m.shape[1],m.shape[0])
wo=cv2.warpPerspective(old,H,sz,flags=cv2.INTER_CUBIC)
wn=cv2.warpPerspective(new,H,sz,flags=cv2.INTER_CUBIC)
area=cv2.warpPerspective(np.full(old.shape[:2],255,np.uint8),H,sz)
area=cv2.erode(area,np.ones((3,3),np.uint8))
# oclusão: onde o mockup difere muito da capa antiga warpada (folha na frente)
diff=np.abs(cv2.GaussianBlur(wo,(9,9),0).astype(int)-cv2.GaussianBlur(m,(9,9),0).astype(int)).sum(2)
occ=((diff>150)&(area>0)).astype(np.uint8)*255
occ=cv2.morphologyEx(occ,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
# mantém só componentes grandes (a folha), descarta ruído
n,lab,st,_=cv2.connectedComponentsWithStats(occ)
keep=np.zeros_like(occ)
for i in range(1,n):
    if st[i,cv2.CC_STAT_AREA]>3000: keep[lab==i]=255
keep=cv2.dilate(keep,np.ones((5,5),np.uint8))
# iluminação: razão entre mockup e capa antiga, bem suavizada
lo=cv2.GaussianBlur(cv2.cvtColor(wo,cv2.COLOR_BGR2GRAY).astype(float)+8,(61,61),0)
lm=cv2.GaussianBlur(cv2.cvtColor(m,cv2.COLOR_BGR2GRAY).astype(float)+8,(61,61),0)
ratio=np.clip(lm/lo,0.7,1.3)[...,None]
lit=np.clip(wn.astype(float)*ratio,0,255)
alpha=(area.astype(float)/255)*(1-keep.astype(float)/255)
alpha=cv2.GaussianBlur(alpha,(3,3),0)[...,None]
out=(m*(1-alpha)+lit*alpha).astype(np.uint8)
cv2.imwrite('occ.png',keep)
Image.fromarray(out[:,:,::-1]).save('dobra-tjsp.png')
Image.fromarray(out[:,:,::-1]).save('x') if False else None
print('ok', keep.sum()//255)
