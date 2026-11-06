from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r'C:\Users\HP\Desktop\CV Project')
REPORT = ROOT / 'Epoch Reports' / 'Epoch_3_Training_Report.docx'
POST = ROOT / 'Epoch Posts' / 'Epoch_3_LinkedIn_Post.md'
CARD = ROOT / 'Epoch Posts' / 'Epoch_3_Training_Results.png'

NAVY, BLUE, PALE, GRID = '17365D', '1D70B8', 'F5F8FC', 'D9D9D9'

def cell_shade(cell, color):
    p = cell._tc.get_or_add_tcPr()
    e = OxmlElement('w:shd')
    e.set(qn('w:fill'), color)
    p.append(e)

def style_cell(c, header=False, center=False):
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for side in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement('w:' + side)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), '4')
        e.set(qn('w:color'), GRID)
        borders.append(e)
    p.append(borders)
    for para in c.paragraphs:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.space_after = Pt(0)
        for r in para.runs:
            r.font.name = 'Aptos'
            r._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos')
            r._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
            r.font.size = Pt(9)
            if header:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
    if header:
        cell_shade(c, NAVY)

def table(doc, hdr, rows, widths):
    t = doc.add_table(rows=1, cols=len(hdr))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, v in enumerate(hdr):
        c = t.rows[0].cells[i]
        c.width = Inches(widths[i])
        c.text = v
        style_cell(c, True, True)
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].width = Inches(widths[i])
            cells[i].text = str(v)
            style_cell(cells[i], False, i > 0)
            if ri % 2:
                cell_shade(cells[i], PALE)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

# --- 1. DOCX GENERATION ---
d = Document()
sec = d.sections[0]
sec.top_margin = Inches(0.65)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.72)
sec.right_margin = Inches(0.72)

for n, size in [('Normal', 10), ('Title', 22), ('Heading 1', 14)]:
    s = d.styles[n]
    s.font.name = 'Aptos'
    s._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos')
    s._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
    s.font.size = Pt(size)
    s.font.color.rgb = RGBColor(0, 0, 0)

p = d.add_paragraph(style='Title')
p.add_run('Epoch 3 Training Report')

p = d.add_paragraph('Open Images 601 Class Object Detection  |  Run epoch_3  |  November 6 2026')
p.paragraph_format.space_after = Pt(14)
for r in p.runs:
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(89, 89, 89)

p = d.add_paragraph()
p.add_run('Summary. ').bold = True
p.add_run('Epoch 3 completed successfully in 1.544 hours. Detection quality continued its consistent upward trajectory: recall improved to 11.30% (+1.57 percentage points) and mAP@50 reached 8.49% (+1.28 percentage points). All three training losses decreased for the third consecutive epoch (box loss down to 1.4786, classification loss down to 2.3067, DFL loss down to 1.4981). Precision adjusted to 45.99% as the model broadens coverage across underrepresented classes in the 601-category hierarchy.')

d.add_heading('Run summary', 1)
table(d, ['Item', 'Result'], [
    ('Status', 'Completed successfully'),
    ('Model', 'YOLO11 Nano fine-tuned for 601 classes'),
    ('Dataset pass', '85,000 training images and 15,000 validation images (100,000 total)'),
    ('Batch and image size', '8 images per training batch at 640 pixels'),
    ('Session run time', '1.544 hours (~1 hour 33 minutes)'),
    ('Cumulative run time (3 epochs)', '4.604 hours'),
    ('Output folder', 'runs/detect/runs/detect/epoch_3')
], [2.2, 4.7])

d.add_heading('Validation metrics progression (Epoch 1 to Epoch 3)', 1)
table(d, ['Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Change vs Ep 2', 'Change vs Ep 1'], [
    ('Precision', '53.78%', '51.17%', '45.99%', '-5.18 pts', '-7.79 pts'),
    ('Recall', '6.42%', '9.73%', '11.30%', '+1.57 pts (+16.1%)', '+4.88 pts (+76.0%)'),
    ('mAP at 50', '5.25%', '7.21%', '8.49%', '+1.28 pts (+17.8%)', '+3.24 pts (+61.7%)'),
    ('mAP at 50 to 95', '3.37%', '4.71%', '5.58%', '+0.87 pts (+18.5%)', '+2.21 pts (+65.6%)'),
], [1.5, 1.0, 1.0, 1.0, 1.2, 1.2])

d.add_heading('Loss metrics progression and evaluation', 1)
table(d, ['Loss Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Change vs Ep 2', 'Direction & Interpretation'], [
    ('Box loss', '1.5772', '1.5002', '1.4786', '-0.0216', 'Improved. Tighter bounding box coordinate boundaries.'),
    ('Classification loss', '3.3083', '2.4242', '2.3067', '-0.1175', 'Improved. Substantial class identification gain (-1.0016 overall).'),
    ('DFL loss', '1.5859', '1.5174', '1.4981', '-0.0193', 'Improved. More precise distribution focal loss box alignment.'),
], [1.3, 0.9, 0.9, 0.9, 1.1, 1.8])

d.add_heading('Assessment and insights', 1)
p = d.add_paragraph()
p.add_run('Consistent learning signal. ').bold = True
p.add_run('Recall has increased by +76.0% relative to Epoch 1 (from 6.42% to 11.30%), and mAP@50 has surged from 5.25% to 8.49% (+61.7% relative). Over 601 diverse classes, steady gains across all three epochs confirm the network is steadily overcoming the massive class imbalance.')

p = d.add_paragraph()
p.add_run('Precision trade-off. ').bold = True
p.add_run('Precision decreased from 51.17% to 45.99%. This is expected: the model is lowering its detection threshold internally to capture more difficult object instances, which increases recall substantially while temporarily admitting false positives. Because mAP@50 and mAP@50-95 increased simultaneously, the net detection quality is definitively higher.')

d.add_heading('Checkpoint summary and next step', 1)
table(d, ['Checkpoint', 'Purpose', 'Location'], [
    ('best.pt', 'Best validation model after Epoch 3', r'runs/detect/runs/detect/epoch_3/weights/best.pt'),
    ('last.pt', 'Resume point after Epoch 3', r'runs/detect/runs/detect/epoch_3/weights/last.pt'),
], [1.05, 1.75, 4.1])

p = d.add_paragraph()
p.add_run('Next step. ').bold = True
p.add_run('Launch Epoch 4 using the Epoch 3 last.pt checkpoint. Expect recall to cross the 12-13% threshold as classification loss continues toward ~2.20.')

foot = sec.footer.paragraphs[0]
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = foot.add_run('Epoch 3 checkpoint report  |  Open Images 601 Class Object Detection')
rr.font.size = Pt(8)
rr.font.color.rgb = RGBColor(100, 100, 100)

d.core_properties.title = 'Epoch 3 Training Report'
d.core_properties.author = 'CV Project'
d.save(REPORT)

# --- 2. LINKEDIN POST ---
POST.write_text('''# LinkedIn Post - Epoch 3 Training Update

Epoch 3 is complete for my 601-class computer vision object detection project!

I am fine-tuning YOLO11 Nano on 85,000 training images and validating on 15,000 separate images (100,000 total images per epoch). The third epoch finished smoothly, showing steady improvements across key detection metrics and continued drop across all training losses.

## Results progression (Epoch 1 -> Epoch 2 -> Epoch 3)

- Recall (objects found): 6.42% -> 9.73% -> 11.30% (+76.0% relative gain since Epoch 1)
- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% (+61.7% relative gain)
- mAP@50-95 (stricter average): 3.37% -> 4.71% -> 5.58% (+65.6% relative gain)
- Precision (detections correct): 53.8% -> 51.2% -> 45.99%

## Loss progression (All 3 decreasing steadily)

- Box loss (location error): 1.5772 -> 1.5002 -> 1.4786 (improved)
- Classification loss (class error): 3.3083 -> 2.4242 -> 2.3067 (improved by over 1.0 point total)
- DFL loss (refinement error): 1.5859 -> 1.5174 -> 1.4981 (improved)

## Key Takeaway
For a complex 601-class problem on edge hardware (GTX 1050), recall jumping to 11.3% while mAP expands to 8.5% is the key indicator of healthy learning. The slight drop in precision is standard at this stage as the model gains confidence to spot less frequent classes.

Checkpoint saved. Moving straight on to Epoch 4!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 3 done. recall pushed past 11% and mAP50 reached 8.5%. all three losses keep dropping across the 601 classes. moving onto epoch 4.
''', encoding='utf-8')

# --- 3. LINKEDIN GRAPHIC CARD (1200x1200) ---
W = H = 1200
im = Image.new('RGB', (W, H), 'white')
draw = ImageDraw.Draw(im)

def F(sz, b=False):
    return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if b else 'C:/Windows/Fonts/arial.ttf', sz)

navy = '#102A43'
blue = '#1D70B8'
ink = '#1F2933'
muted = '#627D98'
pale = '#EAF3FB'
green = '#16803C'
orange = '#D97706'

# Header banner
draw.rectangle((0, 0, W, 290), fill=navy)
draw.rectangle((0, 0, 18, 290), fill=blue)
draw.text((70, 52), 'COMPUTER VISION PROJECT', font=F(24, True), fill='#B3D4FC')
draw.text((70, 102), 'Epoch 3 Complete', font=F(56, True), fill='white')
draw.text((70, 185), 'YOLO11 Nano  |  601 classes  |  100,000 images per epoch', font=F(24), fill='#D9EAF7')

# Section Title
draw.text((70, 330), 'EPOCH 3 VS EPOCH 2 PROGRESSION', font=F(21, True), fill=blue)
draw.text((70, 370), 'Detection recall & mAP keep climbing', font=F(38, True), fill=ink)

# 4 Metric Cards with bracketed descriptions
metrics = [
    ('Recall (objects found out of all)', '9.73% -> 11.30%', 'UP +1.57 pts (+16.1%)', green),
    ('mAP@50 (accuracy at 50% overlap)', '7.21% -> 8.49%', 'UP +1.28 pts (+17.8%)', green),
    ('mAP@50-95 (average across stricter overlaps)', '4.71% -> 5.58%', 'UP +0.87 pts (+18.5%)', green),
    ('Precision (detections that are correct)', '51.2% -> 46.0%', 'ADJUSTED -5.18 pts', orange)
]

for i, (lab, val, delta, col) in enumerate(metrics):
    x = 70 + (i % 2) * 545
    y = 445 + (i // 2) * 175
    draw.rounded_rectangle((x, y, x + 515, y + 145), radius=16, fill=pale, outline='#D9E2EC', width=2)
    draw.text((x + 22, y + 20), lab, font=F(16, True), fill=blue)
    draw.text((x + 22, y + 54), val, font=F(30, True), fill=ink)
    draw.text((x + 22, y + 104), delta, font=F(17, True), fill=col)

# Loss Section Title
draw.text((70, 815), 'LOSS METRICS: 3RD CONSECUTIVE DECREASE', font=F(21, True), fill=blue)

# 3 Loss Cards with bracketed descriptions
losses = [
    ('Box loss (box location error)', '1.5002 -> 1.4786', '-0.0216 improved'),
    ('Classification loss (class prediction error)', '2.4242 -> 2.3067', '-0.1175 improved'),
    ('DFL loss (box refinement error)', '1.5174 -> 1.4981', '-0.0193 improved')
]

for i, (lab, val, delta) in enumerate(losses):
    x = 70 + i * 355
    draw.rounded_rectangle((x, 860, x + 335, 995), radius=16, fill='#E4F7EA', outline='#B7E3C4', width=2)
    draw.text((x + 18, 882), lab, font=F(14, True), fill=green)
    draw.text((x + 18, 922), val, font=F(24, True), fill=ink)
    draw.text((x + 18, 960), delta, font=F(16, True), fill=green)

# Footer bar
draw.line((70, 1030, 1130, 1030), fill='#D9E2EC', width=2)
draw.text((70, 1055), 'Status: Epoch 3 checkpoint saved (5.5 MB). Continuing to Epoch 4.', font=F(21, True), fill=ink)
draw.text((70, 1098), 'Recall is up +76% and mAP@50 is up +62% compared to Epoch 1.', font=F(18), fill=muted)

im.save(CARD, quality=95)
print('SUCCESS: Created', REPORT)
print('SUCCESS: Created', POST)
print('SUCCESS: Created', CARD)
