from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r'C:\Users\HP\Desktop\CV Project')
REPORT = ROOT / 'Epoch Reports' / 'Epoch_5_Training_Report.docx'
POST = ROOT / 'Epoch Posts' / 'Epoch_5_LinkedIn_Post.md'
CARD = ROOT / 'Epoch Posts' / 'Epoch_5_Training_Results.png'

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
p.add_run('Epoch 5 Training Report (Halfway Milestone)')

p = d.add_paragraph('Open Images 601 Class Object Detection  |  Run epoch_5  |  November 7 2026')
p.paragraph_format.space_after = Pt(14)
for r in p.runs:
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(89, 89, 89)

p = d.add_paragraph()
p.add_run('Summary. ').bold = True
p.add_run('Epoch 5 marks the official halfway point of the 10-epoch training curriculum and crosses a major double-digit threshold: mAP@50 reached 10.49%, effectively doubling (+99.8% relative gain) from the Epoch 1 baseline (5.25%). Recall climbed to 14.84% (+131.2% total gain). For the fifth consecutive epoch, all three loss components decreased (classification loss down to 2.1201, box loss down to 1.4406, DFL loss down to 1.4672). Precision settled at 38.14%, indicating the expected plateau of the discovery phase before boundary refinement begins in Epochs 6-10.')

d.add_heading('Run summary', 1)
table(d, ['Item', 'Result'], [
    ('Status', 'Completed successfully (Halfway milestone 5/10)'),
    ('Model', 'YOLO11 Nano fine-tuned for 601 classes'),
    ('Dataset pass', '85,000 training images and 15,000 validation images (100,000 total)'),
    ('Batch and image size', '8 images per training batch at 640 pixels'),
    ('Session run time', '1.545 hours (~1 hour 33 minutes)'),
    ('Cumulative run time (5 epochs)', '7.743 hours (~7 hours 45 minutes)'),
    ('Output folder', 'runs/detect/runs/detect/epoch_5')
], [2.3, 4.6])

d.add_heading('Validation metrics progression (Epoch 1 to Epoch 5)', 1)
table(d, ['Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', 'Epoch 5', 'Change vs Ep 4', 'Total Gain vs Ep 1'], [
    ('Precision', '53.78%', '51.17%', '45.99%', '41.17%', '38.14%', '-3.03 pts', '-15.64 pts'),
    ('Recall', '6.42%', '9.73%', '11.30%', '13.18%', '14.84%', '+1.66 pts (+12.6%)', '+8.42 pts (+131.2%)'),
    ('mAP at 50', '5.25%', '7.21%', '8.49%', '9.61%', '10.49%', '+0.88 pts (+9.2%)', '+5.24 pts (+99.8% Doubled!)'),
    ('mAP at 50 to 95', '3.37%', '4.71%', '5.58%', '6.30%', '6.86%', '+0.56 pts (+8.9%)', '+3.49 pts (+103.6% Doubled!)'),
], [1.3, 0.75, 0.75, 0.75, 0.75, 0.75, 1.0, 1.25])

d.add_heading('Loss metrics progression and evaluation', 1)
table(d, ['Loss Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', 'Epoch 5', 'Change vs Ep 4', 'Direction & Interpretation'], [
    ('Box loss', '1.5772', '1.5002', '1.4786', '1.4570', '1.4406', '-0.0164', 'Improved. Coordinate regression tightening continuously.'),
    ('Classification loss', '3.3083', '2.4242', '2.3067', '2.1981', '2.1201', '-0.0780', 'Improved. Down -1.1882 points total since baseline.'),
    ('DFL loss', '1.5859', '1.5174', '1.4981', '1.4808', '1.4672', '-0.0136', 'Improved. Distribution focal loss alignment continues to sharpen.'),
], [1.2, 0.7, 0.7, 0.7, 0.7, 0.7, 1.0, 1.6])

d.add_heading('Halfway milestone assessment and trajectory', 1)
p = d.add_paragraph()
p.add_run('Doubling of detection capacity. ').bold = True
p.add_run('Both mAP@50 (5.25% to 10.49%) and mAP@50-95 (3.37% to 6.86%) have doubled compared to Epoch 1. Recall has expanded by +131%, indicating that out of nearly 287,000 ground-truth target objects, the model is successfully localizing and categorizing over 42,500 instances across 601 classes on an edge GPU.')

p = d.add_paragraph()
p.add_run('Entering the transition phase. ').bold = True
p.add_run('As expected in 601-class training, the discovery rate is transitioning. The precision drop has slowed (-3.0 pts vs -4.8 pts in Epoch 4) as the initial burst of broad discovery stabilizes around ~38%. In the second half of the schedule (Epochs 6-10), learning rate decay and refinement are expected to bottom out precision and start lifting overall confidence.')

d.add_heading('Checkpoint summary and next step', 1)
table(d, ['Checkpoint', 'Purpose', 'Location'], [
    ('best.pt', 'Best validation model after Epoch 5', r'runs/detect/runs/detect/epoch_5/weights/best.pt'),
    ('last.pt', 'Resume point after Epoch 5', r'runs/detect/runs/detect/epoch_5/weights/last.pt'),
], [1.05, 1.75, 4.1])

p = d.add_paragraph()
p.add_run('Next step. ').bold = True
p.add_run('Launch Epoch 6 from the Epoch 5 last.pt checkpoint to start the second half of the 10-epoch curriculum.')

foot = sec.footer.paragraphs[0]
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = foot.add_run('Epoch 5 checkpoint report (50% Milestone)  |  Open Images 601 Class Object Detection')
rr.font.size = Pt(8)
rr.font.color.rgb = RGBColor(100, 100, 100)

d.core_properties.title = 'Epoch 5 Training Report'
d.core_properties.author = 'CV Project'
d.save(REPORT)

# --- 2. LINKEDIN POST ---
POST.write_text('''# LinkedIn Post - Epoch 5 (50% Milestone) Training Update

Halfway milestone reached: 5 of 10 epochs completed in my 601-class computer vision object detection project!

Fine-tuning YOLO11 Nano on 85,000 training images and validating across 15,000 images (100,000 images per epoch). The model has officially crossed into double digits, with mAP@50 doubling since the start of training.

## Milestone Highlights (Epoch 1 -> Epoch 5)

- mAP@50 (50% IoU accuracy): 5.25% -> 10.49% (Doubled! +99.8% relative gain)
- mAP@50-95 (strict average): 3.37% -> 6.86% (Doubled! +103.6% relative gain)
- Recall (objects found): 6.42% -> 14.84% (+131.2% relative gain across 601 classes)
- Classification Loss: 3.3083 -> 2.1201 (Down nearly 1.20 points total)
- Box Loss: 1.5772 -> 1.4406 (Consistent coordinate convergence)
- DFL Loss: 1.5859 -> 1.4672 (Steady boundary refinement)

## 5-Epoch Progression Table

| Metric | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Total Gain |
|---|---:|---:|---:|---:|---:|:---:|
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | **14.84%** | **+131%** |
| mAP@50 | 5.25% | 7.21% | 8.49% | 9.61% | **10.49%** | **Doubled (+100%)** |
| mAP@50-95 | 3.37% | 4.71% | 5.58% | 6.30% | **6.86%** | **Doubled (+104%)** |
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | **38.14%** | Plateauing |

## Takeaway
In a massive 601-class problem on edge hardware (GTX 1050 3GB), seeing both mAP and mAP@50-95 double by epoch 5 proves consistent optimization without overfitting. The aggressive discovery phase is now beginning to stabilize around ~38% precision, setting up the second half (Epochs 6-10) for boundary refinement.

Halfway mark done. Heading into the second half with Epoch 6!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 5 done and halfway through the project! mAP50 officially crossed 10% (doubling from 5.2% at start), recall reached nearly 15%, and all 3 losses dropped for the 5th time. onto epoch 6.
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
draw.text((70, 52), 'COMPUTER VISION PROJECT  |  50% HALFWAY MILESTONE', font=F(22, True), fill='#B3D4FC')
draw.text((70, 98), 'Epoch 5: mAP Crosses 10%', font=F(54, True), fill='white')
draw.text((70, 182), 'YOLO11 Nano  |  601 classes  |  mAP & mAP@50-95 Doubled Since Start', font=F(23), fill='#D9EAF7')

# Section Title
draw.text((70, 325), 'EPOCH 5 PROGRESSION (HALFWAY POINT)', font=F(21, True), fill=blue)
draw.text((70, 365), 'Double-digit mAP & 131% Recall Gain', font=F(38, True), fill=ink)

# 4 Metric Cards with bracketed descriptions
metrics = [
    ('mAP@50 (accuracy at 50% overlap)', '9.61% -> 10.49%', 'DOUBLED VS EP 1 (+100%)', green),
    ('Recall (objects found out of all)', '13.18% -> 14.84%', 'UP +1.66 pts (+131% vs Ep 1)', green),
    ('mAP@50-95 (average across stricter overlaps)', '6.30% -> 6.86%', 'DOUBLED VS EP 1 (+104%)', green),
    ('Precision (detections that are correct)', '41.2% -> 38.1%', 'DISCOVERY PHASE (-3.0 pts)', orange)
]

for i, (lab, val, delta, col) in enumerate(metrics):
    x = 70 + (i % 2) * 545
    y = 440 + (i // 2) * 175
    draw.rounded_rectangle((x, y, x + 515, y + 145), radius=16, fill=pale, outline='#D9E2EC', width=2)
    draw.text((x + 22, y + 20), lab, font=F(16, True), fill=blue)
    draw.text((x + 22, y + 54), val, font=F(30, True), fill=ink)
    draw.text((x + 22, y + 104), delta, font=F(17, True), fill=col)

# Loss Section Title
draw.text((70, 810), 'LOSS METRICS: 5TH CONSECUTIVE IMPROVEMENT', font=F(21, True), fill=blue)

# 3 Loss Cards with bracketed descriptions
losses = [
    ('Box loss (box location error)', '1.4570 -> 1.4406', '-0.0164 improved'),
    ('Classification loss (class prediction error)', '2.1981 -> 2.1201', '-0.0780 improved (-1.19 total)'),
    ('DFL loss (box refinement error)', '1.4808 -> 1.4672', '-0.0136 improved')
]

for i, (lab, val, delta) in enumerate(losses):
    x = 70 + i * 355
    draw.rounded_rectangle((x, 855, x + 335, 995), radius=16, fill='#E4F7EA', outline='#B7E3C4', width=2)
    draw.text((x + 18, 878), lab, font=F(14, True), fill=green)
    draw.text((x + 18, 918), val, font=F(24, True), fill=ink)
    draw.text((x + 18, 958), delta, font=F(15, True), fill=green)

# Footer bar
draw.line((70, 1030, 1130, 1030), fill='#D9E2EC', width=2)
draw.text((70, 1055), 'Status: 5 of 10 epochs complete. Checkpoint saved. Heading into Epoch 6.', font=F(21, True), fill=ink)
draw.text((70, 1098), 'mAP@50 doubled (5.25% to 10.49%) and Recall climbed from 6.42% to 14.84%.', font=F(18), fill=muted)

im.save(CARD, quality=95)
print('SUCCESS: Created', REPORT)
print('SUCCESS: Created', POST)
print('SUCCESS: Created', CARD)
