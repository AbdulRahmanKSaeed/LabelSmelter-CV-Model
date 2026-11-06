from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1350
OUT = Path(r"C:\Users\HP\Desktop\CV Project\Epoch Posts\Dataset_and_Batch_Composition.png")

NAVY, BLUE, PALE, INK, MUTED, WHITE, ORANGE, GREEN = '#102A43','#1D70B8','#EAF3FB','#1F2933','#627D98','#FFFFFF','#F59E0B','#16803C'

def f(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf', size)

def card(draw, box, fill=WHITE, outline='#D9E2EC'):
    draw.rounded_rectangle(box, radius=20, fill=fill, outline=outline, width=2)

im = Image.new('RGB', (W,H), WHITE)
d = ImageDraw.Draw(im)

# Header
d.rectangle((0,0,W,258),fill=NAVY)
d.rectangle((0,0,18,258),fill=BLUE)
d.text((70,55),'CV PROJECT EXPLAINER',font=f(24,True),fill='#B3D4FC')
d.text((70,105),'What one epoch processes',font=f(51,True),fill=WHITE)
d.text((70,175),'Dataset split + the exact composition of each batch',font=f(25),fill='#D9EAF7')

# Dataset split
d.text((70,305),'1. DATASET ALLOCATION',font=f(22,True),fill=BLUE)
d.text((70,345),'100,000 prepared images',font=f(37,True),fill=INK)
bar=(70,410,1130,476)
d.rounded_rectangle(bar,radius=15,fill='#E9EEF4')
d.rounded_rectangle((70,410,971,476),radius=15,fill=BLUE)
d.rectangle((956,410,971,476),fill=BLUE)
d.rounded_rectangle((971,410,1130,476),radius=15,fill=ORANGE)
d.text((95,429),'Training  85,000  |  85%',font=f(21,True),fill=WHITE)
d.text((987,429),'Val  15,000  |  15%',font=f(16,True),fill=INK)
d.text((70,506),'Test set: 0 images right now. A separate untouched test set will be created after Epoch 10.',font=f(20),fill=MUTED)

# per epoch graphic
d.text((70,580),'2. ONE EPOCH HAS TWO PARTS',font=f(22,True),fill=BLUE)
card(d,(70,625,570,870),PALE)
d.text((100,658),'TRAINING',font=f(24,True),fill=BLUE)
d.text((100,700),'85,000 images',font=f(38,True),fill=INK)
d.text((100,752),'Batch size: 8 images',font=f(22,True),fill=INK)
d.text((100,791),'85,000 ÷ 8 = 10,625 batches',font=f(20),fill=MUTED)
d.text((100,827),'Updates model weights',font=f(20,True),fill=GREEN)
card(d,(630,625,1130,870),'#FFF5DD')
d.text((660,658),'VALIDATION',font=f(24,True),fill='#A65C00')
d.text((660,700),'15,000 images',font=f(38,True),fill=INK)
d.text((660,752),'About 16 images per batch',font=f(22,True),fill=INK)
d.text((660,791),'15,000 ÷ 16 ≈ 938 batches',font=f(20),fill=MUTED)
d.text((660,827),'Measures metrics only',font=f(20,True),fill='#A65C00')

# batch closeup
d.text((70,935),'3. WHAT IS IN A TRAINING BATCH?',font=f(22,True),fill=BLUE)
d.text((70,976),'Your current training batch contains 8 images, each resized to 640 × 640 pixels.',font=f(22),fill=INK)

# eight image tiles
tile_y=1035
for i in range(8):
    x=70+i*132
    d.rounded_rectangle((x,tile_y,x+108,tile_y+108),radius=12,fill='#D9EAF7',outline='#A9C5DD',width=2)
    d.rectangle((x+18,tile_y+22,x+88,tile_y+82),outline=BLUE,width=3)
    d.rectangle((x+35,tile_y+40,x+70,tile_y+68),outline=ORANGE,width=3)
    d.text((x+41,tile_y+87),str(i+1),font=f(14,True),fill=BLUE)

d.rounded_rectangle((70,1175,1130,1285),radius=18,fill='#F5F8FC',outline='#D9E2EC',width=2)
d.text((97,1200),'Each image brings its YOLO bounding box labels. Training also applies augmentation; validation does not.',font=f(19,True),fill=INK)
d.text((97,1242),'Batch → model prediction → loss calculation → one weight update. Repeat 10,625 times to complete the training portion of an epoch.',font=f(17),fill=MUTED)

d.text((70,1310),'Current flow: Train 85,000 images → Validate 15,000 images → Save checkpoint → Next epoch',font=f(18,True),fill=MUTED)
im.save(OUT,quality=95)
print(OUT)
