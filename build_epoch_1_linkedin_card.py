from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
OUT = Path(r"C:\Users\HP\Desktop\CV Project\Epoch Posts\Epoch_1_Training_Results.png")

NAVY = '#102A43'
BLUE = '#1D70B8'
PALE_BLUE = '#EAF3FB'
INK = '#1F2933'
MUTED = '#627D98'
WHITE = '#FFFFFF'
LINE = '#D9E2EC'
GREEN = '#16803C'

def font(size, bold=False):
    name = 'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf'
    return ImageFont.truetype(name, size)

img = Image.new('RGB', (W, H), WHITE)
d = ImageDraw.Draw(img)

# Header
d.rectangle((0, 0, W, 335), fill=NAVY)
d.rectangle((0, 0, 18, 335), fill=BLUE)
d.text((70, 66), 'COMPUTER VISION PROJECT', font=font(25, True), fill='#B3D4FC')
d.text((70, 118), 'Epoch 1 Complete', font=font(62, True), fill=WHITE)
d.text((70, 202), 'YOLO11 Nano  |  Open Images  |  601 Classes', font=font(28), fill='#D9EAF7')

# Success band
d.rounded_rectangle((70, 290, 635, 373), radius=18, fill='#D8F3DC')
d.ellipse((94, 314, 132, 352), fill=GREEN)
d.text((104, 316), '1', font=font(22, True), fill=WHITE)
d.text((151, 314), 'Full training run completed successfully', font=font(23, True), fill='#155724')

# Intro
d.text((70, 418), 'FIRST EPOCH TRAINING RESULTS', font=font(21, True), fill=BLUE)
d.text((70, 457), 'Baseline validation metrics', font=font(39, True), fill=INK)
d.text((70, 510), 'A first full run confirms the end to end training pipeline is working.', font=font(23), fill=MUTED)

# metric cards
cards = [
    ('Precision', '53.8%', 'Correctness when detected'),
    ('Recall', '6.42%', 'Objects found so far'),
    ('mAP@50', '5.25%', 'Detection baseline'),
    ('mAP@50–95', '3.37%', 'Strict localization'),
]
card_y = 575
card_w, card_h, gap = 255, 210, 20
for i, (label, value, sub) in enumerate(cards):
    x = 70 + i * (card_w + gap)
    d.rounded_rectangle((x, card_y, x+card_w, card_y+card_h), radius=18, fill=PALE_BLUE, outline=LINE, width=2)
    d.text((x+24, card_y+25), label, font=font(22, True), fill=BLUE)
    d.text((x+24, card_y+75), value, font=font(43, True), fill=INK)
    d.text((x+24, card_y+145), sub, font=font(17), fill=MUTED)

# run stats
d.text((70, 855), 'RUN DETAILS', font=font(20, True), fill=BLUE)
stats = [
    ('85,000', 'training images'), ('15,000', 'validation images'), ('10,625', 'training batches'), ('1h 37m', 'run duration')
]
for i, (num, lab) in enumerate(stats):
    x = 70 + i * 278
    d.text((x, 898), num, font=font(34, True), fill=INK)
    d.text((x, 946), lab, font=font(19), fill=MUTED)

# Footer
d.line((70, 1015, 1130, 1015), fill=LINE, width=2)
d.text((70, 1050), 'Status: Epoch 1 baseline captured. Checkpoints saved. Continuing to Epoch 2.', font=font(22, True), fill=INK)
d.text((70, 1100), 'Low recall and mAP are expected at this early stage across 601 classes.', font=font(18), fill=MUTED)

img.save(OUT, quality=95)
print(OUT)
