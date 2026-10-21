from PIL import Image, ImageDraw
import numpy as np, os, shutil
I='/tmp/thumbs/in/'; A='/tmp/thumbs/assets/'; os.makedirs(A+'outfit',exist_ok=True)
for w,n in [(600,'SemiBold'),(700,'Bold'),(800,'ExtraBold')]: shutil.copy(I+f'Outfit-{n}.ttf',A+f'outfit/outfit-{w}.ttf')
for f in ['ibinn_src.png','ibinn_src2.png','logo_src.png']:
    im=Image.open(I+f).convert('RGBA'); a=np.array(im)
    print(f,im.size,'alpha min/max',a[...,3].min(),a[...,3].max(),'rgb mean opaque',a[a[...,3]>128][:, :3].mean(0) if (a[...,3]>128).any() else None)
def bbox_save(im,out): im.crop(im.getbbox()).save(out)
ib=Image.open(I+'ibinn_src.png').convert('RGBA'); bbox_save(ib,A+'ibinn.png')
lg=Image.open(I+'logo_src.png').convert('RGBA'); bbox_save(lg,A+'logo.png')
# iconos de la miniatura del #16 (1080x1350)
src=Image.open(I+'ep16_45.png').convert('RGBA')
boxes={'youtube':(60,1283,121,1325),'spotify':(133,1283,175,1325),'apple':(187,1283,229,1325),'amazon':(241,1283,283,1325)}
for k,b in boxes.items():
    c=src.crop(b); w,h=c.size
    # recortar hacia dentro y máscara redondeada
    c=c.crop((2,2,w-2,h-2)); w,h=c.size
    m=Image.new('L',(w*4,h*4),0); r=min(w,h)*4//2 if k=='spotify' else 10*4
    ImageDraw.Draw(m).rounded_rectangle((0,0,w*4-1,h*4-1),radius=r,fill=255)
    c.putalpha(m.resize((w,h),Image.LANCZOS)); c=c.resize((w*3,h*3),Image.LANCZOS); c.save(A+f'ic_{k}.png')
print(os.listdir(A))
