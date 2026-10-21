# Borra el micro del invitado y reconstruye la camisa (LaMa) + limpia el borde del recorte.
# Uso: python borrar_micro.py frame.png "x,y x,y ..."   (polígono amplio alrededor del micro, brazo y cable)
# Salida: <frame>_nomic.png (frame sin micro). Después: rembg (isnet-general-use) -> raw.png y
#         python borrar_micro.py --borde raw.png   -> raw_fix.png (alfa suave y sin filo rojo/morado).
import sys, cv2, numpy as np, torch
from PIL import Image
if sys.argv[1]!='--borde':
    from simple_lama_inpainting import SimpleLama
    _l=torch.jit.load; torch.jit.load=lambda f,*a,**k:_l(f,map_location='cpu')   # sin esto busca CUDA
    src=sys.argv[1]; pts=[tuple(map(int,p.split(','))) for p in sys.argv[2].split()]
    im=cv2.imread(src); H,W=im.shape[:2]
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV); h,s,v=[hsv[...,i].astype(int) for i in range(3)]
    env=np.zeros((H,W),np.uint8); cv2.fillPoly(env,[np.array(pts)],255)
    shirt=(h>=95)&(h<=135)&(s>=45)                          # camisa azul; ajustar si la ropa es de otro color
    red=((h<=10)|(h>=165))&(s>=110)&(v>=90)                 # fondo rojo del plató
    m=((~shirt)&(~red)&(env>0)).astype(np.uint8)*255
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
    cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    big=np.zeros_like(m); [cv2.drawContours(big,[c],-1,255,-1) for c in cnts if cv2.contourArea(c)>400]
    m=cv2.dilate(big,np.ones((13,13),np.uint8)); cv2.imwrite(src[:-4]+'_mask.png',m)
    out=SimpleLama(device=torch.device('cpu'))(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)),Image.fromarray(m))
    out.crop((0,0,W,H)).save(src[:-4]+'_nomic.png')
else:
    raw=sys.argv[2]; mask=sys.argv[3] if len(sys.argv)>3 else raw.replace('raw','frame')[:-4]+'_mask.png'
    o=np.array(Image.open(raw)).astype(np.float32); rgb=o[...,:3]; a=o[...,3]/255
    R=cv2.dilate(cv2.imread(mask,0),np.ones((41,41),np.uint8))>0
    ab=cv2.GaussianBlur(a,(0,0),6); t=np.clip((ab-0.3)/0.4,0,1); t=t*t*(3-2*t); a2=np.where(R,t,a)
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    blue=((b>r+15)&(a>0.9)).astype(np.float32)
    shirt=np.stack([cv2.GaussianBlur(rgb[...,i]*blue,(0,0),14) for i in range(3)],-1)/(cv2.GaussianBlur(blue,(0,0),14)[...,None]+1e-6)
    tex=shirt*(rgb.mean(-1,keepdims=True)/(shirt.mean(-1,keepdims=True)+1e-6))
    w=cv2.GaussianBlur((np.clip((r-b+14)/22,0,1)*R).astype(np.float32),(0,0),2)[...,None]
    Image.fromarray(np.dstack([rgb*(1-w)+tex*w,a2*255]).clip(0,255).astype(np.uint8)).save(raw[:-4]+'_fix.png')
