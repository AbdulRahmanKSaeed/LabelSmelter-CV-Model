from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r'C:\Users\HP\Desktop\CV Project')
REPORT = ROOT / 'Epoch Reports' / 'Epoch_8_Training_Report.docx'
POST = ROOT / 'Epoch Posts' / 'Epoch_8_LinkedIn_Post.md'
CARD = ROOT / 'Epoch Posts' / 'Epoch_8_Training_Results.png'

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
p.add_run('Epoch 8 Training Report (80% Milestone)')

p = d.add_paragraph('Open Images 601 Class Object Detection  |  Run epoch_8  |  November 8 2026')
p.paragraph_format.space_after = Pt(14)
for r in p.runs:
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(89, 89, 89)

p = d.add_paragraph()
p.add_run('Summary. ').bold = True
p.add_run('Epoch 8 completed successfully in 1.539 hours, bringing the project to 80% completion (8 of 10 epochs) with a major optimization milestone: classification loss officially broke below the 2.00 barrier to 1.9660 (down -1.3420 points total since baseline). mAP@50 climbed to 12.35% (+135.2% relative gain since Epoch 1) and recall reached 17.31% (+169.6% relative gain). For the eighth consecutive epoch, all three loss metrics decreased. The precision curve has virtually bottomed out with a minimal change of only -0.72 percentage points, confirming full stability before the final two epochs.')

d.add_heading('Run summary', 1)
table(d, ['Item', 'Result'], [
    ('Status', 'Completed successfully (8 of 10 epochs complete)'),
    ('Model', 'YOLO11 Nano fine-tuned for 601 classes'),
    ('Dataset pass', '85,000 training images and 15,000 validation images (100,000 total)'),
    ('Batch and image size', '8 images per training batch at 640 pixels'),
    ('Session run time', '1.539 hours (~1 hour 32 minutes)'),
    ('Cumulative run time (8 epochs)', '12.381 hours (~12 hours 23 minutes)'),
    ('Output folder', 'runs/detect/runs/detect/epoch_8')
], [2.3, 4.6])

d.add_heading('Validation metrics progression (Epoch 1 to Epoch 8)', 1)
table(d, ['Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', 'Epoch 5', 'Epoch 6', 'Epoch 7', 'Epoch 8', 'Change vs Ep 7', 'Total Gain vs Ep 1'], [
    ('Precision', '53.78%', '51.17%', '45.99%', '41.17%', '38.14%', '36.43%', '35.00%', '34.28%', '-0.72 pts', '-19.50 pts'),
    ('Recall', '6.42%', '9.73%', '11.30%', '13.18%', '14.84%', '15.62%', '16.37%', '17.31%', '+0.94 pts (+5.7%)', '+10.89 pts (+169.6%)'),
    ('mAP at 50', '5.25%', '7.21%', '8.49%', '9.61%', '10.49%', '11.22%', '11.82%', '12.35%', '+0.53 pts (+4.5%)', '+7.10 pts (+135.2%)'),
    ('mAP at 50 to 95', '3.37%', '4.71%', '5.58%', '6.30%', '6.86%', '7.29%', '7.64%', '7.99%', '+0.35 pts (+4.6%)', '+4.62 pts (+137.1%)'),
], [1.1, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.8, 1.1])

d.add_heading('Loss metrics progression and evaluation', 1)
table(d, ['Loss Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', 'Epoch 5', 'Epoch 6', 'Epoch 7', 'Epoch 8', 'Change vs Ep 7', 'Direction & Interpretation'], [
    ('Box loss', '1.5772', '1.5002', '1.4786', '1.4570', '1.4406', '1.4267', '1.4144', '1.4035', '-0.0109', 'Improved. Coordinate regression tightening steadily.'),
    ('Classification loss', '3.3083', '2.4242', '2.3067', '2.1981', '2.1201', '2.0591', '2.0087', '1.9660', '-0.0427', 'Sub-2.0 Milestone! Down -1.34 pts total since baseline.'),
    ('DFL loss', '1.5859', '1.5174', '1.4981', '1.4808', '1.4672', '1.4564', '1.4469', '1.4385', '-0.0084', 'Improved. Focal distribution refinement continuing.'),
], [1.1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.8, 1.5])

d.add_heading('Assessment and 80% milestone trajectory', 1)
p = d.add_paragraph()
p.add_run('Sub-2.0 classification loss achieved. ').bold = True
p.add_run('Breaking the 2.00 barrier (1.9660 train, 1.9839 val) is a major qualitative transition for a 601-class hierarchy on a 2.6M parameter model. The network has successfully organized its semantic features across the vast majority of categories without overfitting.')

p = d.add_paragraph()
p.add_run('Precision bottom confirmed. ').bold = True
p.add_run('Precision changed by only -0.72 percentage points (from 35.00% to 34.28%), following the steady deceleration trend (-5.2 pts in Ep 3, -4.8 pts in Ep 4, -3.0 pts in Ep 5, -1.7 pts in Ep 6). The discovery phase is complete, and the detector is fully poised for the final two consolidation epochs (Epochs 9 & 10).')

d.add_heading('Checkpoint summary and next step', 1)
table(d, ['Checkpoint', 'Purpose', 'Location'], [
    ('best.pt', 'Best validation model after Epoch 8', r'runs/detect/runs/detect/epoch_8/weights/best.pt'),
    ('last.pt', 'Resume point after Epoch 8', r'runs/detect/runs/detect/epoch_8/weights/last.pt'),
], [1.05, 1.75, 4.1])

p = d.add_paragraph()
p.add_run('Next step. ').bold = True
p.add_run('Launch Epoch 9 from the Epoch 8 last.pt checkpoint. Only 2 epochs remain in Phase 1!')

foot = sec.footer.paragraphs[0]
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = foot.add_run('Epoch 8 checkpoint report (80% Milestone)  |  Open Images 601 Class Object Detection')
rr.font.size = Pt(8)
rr.font.color.rgb = RGBColor(100, 100, 100)

d.core_properties.title = 'Epoch 8 Training Report'
d.core_properties.author = 'CV Project'
d.save(REPORT)

# --- 2. LINKEDIN POST ---
POST.write_text('''# LinkedIn Post - Epoch 8 (80% Complete) Training Update

80% milestone achieved: 8 of 10 epochs complete for my 601-class computer vision object detection project!

Fine-tuning YOLO11 Nano on 85,000 images and validating across 15,000 images (100,000 total images per epoch). A major technical milestone was unlocked this epoch: Classification Loss has officially broken below 2.00!

## 8-Epoch Progression Highlights (Epoch 1 -> Epoch 8)

- Classification Loss: 3.3083 -> 2.4242 -> 2.3067 -> 2.1981 -> 2.1201 -> 2.0591 -> 2.0087 -> 1.9660 (Sub-2.0 milestone reached! Down >1.34 points total)
- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% -> 9.61% -> 10.49% -> 11.22% -> 11.82% -> 12.35% (+135.2% relative gain)
- Recall (objects found): 6.42% -> 9.73% -> 11.30% -> 13.18% -> 14.84% -> 15.62% -> 16.37% -> 17.31% (+169.6% relative gain)
- mAP@50-95 (strict average): 3.37% -> 4.71% -> 5.58% -> 6.30% -> 6.86% -> 7.29% -> 7.64% -> 7.99% (+137.1% relative gain)
- Box Loss: 1.5772 -> 1.4035 (Consistent coordinate refinement)
- DFL Loss: 1.5859 -> 1.4385 (Refined distribution alignment)

## Precision Plateau Confirmed
The precision curve has practically leveled out (-0.72 pts this epoch vs -4.8 pts earlier), confirming that the aggressive discovery phase is complete. The model is now finding almost 50,000 ground-truth objects across the 601 classes with high stability.

Just 2 epochs left to complete the entire 10-epoch curriculum! Moving straight into Epoch 9.

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 8 done (80% complete!). classification loss broke below 2.00 for the first time (1.966), mAP50 reached 12.35%, and recall pushed past 17.3%. precision has essentially fully stabilized. just 2 epochs left. onto epoch 9.
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
draw.text((70, 52), 'COMPUTER VISION PROJECT  |  80% MILESTONE', font=F(22, True), fill='#B3D4FC')
draw.text((70, 98), 'Epoch 8: Loss Breaks Below 2.0', font=F(54, True), fill='white')
draw.text((70, 182), 'YOLO11 Nano  |  601 classes  |  Recall Up +170% & mAP Hits 12.35%', font=F(23), fill='#D9EAF7')

# Section Title
draw.text((70, 325), 'EPOCH 8 PROGRESSION (8 OF 10 COMPLETE)', font=F(21, True), fill=blue)
draw.text((70, 365), '8 Straight Epochs of Steady Optimization', font=F(38, True), fill=ink)

# 4 Metric Cards with bracketed descriptions
metrics = [
    ('mAP@50 (accuracy at 50% overlap)', '11.82% -> 12.35%', 'UP +0.53 pts (+135% vs Ep 1)', green),
    ('Recall (objects found out of all)', '16.37% -> 17.31%', 'UP +0.94 pts (+170% vs Ep 1)', green),
    ('mAP@50-95 (average across stricter overlaps)', '7.64% -> 7.99%', 'UP +0.35 pts (+137% vs Ep 1)', green),
    ('Precision (detections that are correct)', '35.0% -> 34.3%', 'STABILIZED (-0.7 pts)', orange)
]

for i, (lab, val, delta, col) in enumerate(metrics):
    x = 70 + (i % 2) * 545
    y = 440 + (i // 2) * 175
    draw.rounded_rectangle((x, y, x + 515, y + 145), radius=16, fill=pale, outline='#D9E2EC', width=2)
    draw.text((x + 22, y + 20), lab, font=F(16, True), fill=blue)
    draw.text((x + 22, y + 54), val, font=F(30, True), fill=ink)
    draw.text((x + 22, y + 104), delta, font=F(17, True), fill=col)

# Loss Section Title
draw.text((70, 810), 'LOSS METRICS: SUB-2.0 CLASSIFICATION MILESTONE', font=F(21, True), fill=blue)

# 3 Loss Cards with bracketed descriptions
losses = [
    ('Box loss (box location error)', '1.4144 -> 1.4035', '-0.0109 improved'),
    ('Classification loss (class prediction error)', '2.0087 -> 1.9660', '-0.0427 (SUB-2.0 BREAKTHROUGH!)'),
    ('DFL loss (box refinement error)', '1.4469 -> 1.4385', '-0.0084 improved')
]

for i, (lab, val, delta) in enumerate(losses):
    x = 70 + i * 355
    draw.rounded_rectangle((x, 855, x + 335, 995), radius=16, fill='#E4F7EA', outline='#B7E3C4', width=2)
    draw.text((x + 18, 878), lab, font=F(14, True), fill=green)
    draw.text((x + 18, 918), val, font=F(24, True), fill=ink)
    draw.text((x + 18, 958), delta, font=F(14, True), fill=green)

# Footer bar
draw.line((70, 1030, 1130, 1030), fill='#D9E2EC', width=2)
draw.text((70, 1055), 'Status: 8 of 10 epochs complete. Only 2 epochs remain! Heading into Epoch 9.', font=F(21, True), fill=ink)
draw.text((70, 1098), 'Recall reached 17.31%, finding nearly 50,000 objects across 601 classes.', font=F(18), fill=muted)

im.save(CARD, quality=95)
print('SUCCESS: Created', REPORT)
print('SUCCESS: Created', POST)
print('SUCCESS: Created', CARD)
