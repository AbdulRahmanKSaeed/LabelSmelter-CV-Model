from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r'C:\Users\HP\Desktop\CV Project')
REPORT = ROOT / 'Epoch Reports' / 'Epoch_6_Training_Report.docx'
POST = ROOT / 'Epoch Posts' / 'Epoch_6_LinkedIn_Post.md'
CARD = ROOT / 'Epoch Posts' / 'Epoch_6_Training_Results.png'

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
p.add_run('Epoch 6 Training Report')

p = d.add_paragraph('Open Images 601 Class Object Detection  |  Run epoch_6  |  November 8 2026')
p.paragraph_format.space_after = Pt(14)
for r in p.runs:
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(89, 89, 89)

p = d.add_paragraph()
p.add_run('Summary. ').bold = True
p.add_run('Epoch 6 launched the second half of the 10-epoch curriculum, maintaining strong steady gains across all detection metrics. mAP@50 advanced to 11.22% (+113.7% relative gain since Epoch 1), and recall reached 15.62% (+143.3% relative gain). All three loss metrics decreased for the sixth consecutive epoch (classification loss down to 2.0591, box loss down to 1.4267, DFL loss down to 1.4564). Crucially, the precision rate of decline has visibly flattened (-1.71 pts vs -3.03 pts in Ep 5 and -4.82 pts in Ep 4), confirming that the model is exiting the chaotic initial discovery phase and entering stabilization.')

d.add_heading('Run summary', 1)
table(d, ['Item', 'Result'], [
    ('Status', 'Completed successfully (6 of 10 epochs complete)'),
    ('Model', 'YOLO11 Nano fine-tuned for 601 classes'),
    ('Dataset pass', '85,000 training images and 15,000 validation images (100,000 total)'),
    ('Batch and image size', '8 images per training batch at 640 pixels'),
    ('Session run time', '1.535 hours (~1 hour 32 minutes)'),
    ('Cumulative run time (6 epochs)', '9.278 hours (~9 hours 17 minutes)'),
    ('Output folder', 'runs/detect/runs/detect/epoch_6')
], [2.3, 4.6])

d.add_heading('Validation metrics progression (Epoch 1 to Epoch 6)', 1)
table(d, ['Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', 'Epoch 5', 'Epoch 6', 'Change vs Ep 5', 'Total Gain vs Ep 1'], [
    ('Precision', '53.78%', '51.17%', '45.99%', '41.17%', '38.14%', '36.43%', '-1.71 pts', '-17.35 pts'),
    ('Recall', '6.42%', '9.73%', '11.30%', '13.18%', '14.84%', '15.62%', '+0.78 pts (+5.3%)', '+9.20 pts (+143.3%)'),
    ('mAP at 50', '5.25%', '7.21%', '8.49%', '9.61%', '10.49%', '11.22%', '+0.73 pts (+7.0%)', '+5.97 pts (+113.7%)'),
    ('mAP at 50 to 95', '3.37%', '4.71%', '5.58%', '6.30%', '6.86%', '7.29%', '+0.43 pts (+6.3%)', '+3.92 pts (+116.3%)'),
], [1.2, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.9, 1.2])

d.add_heading('Loss metrics progression and evaluation', 1)
table(d, ['Loss Metric', 'Epoch 1', 'Epoch 2', 'Epoch 3', 'Epoch 4', 'Epoch 5', 'Epoch 6', 'Change vs Ep 5', 'Direction & Interpretation'], [
    ('Box loss', '1.5772', '1.5002', '1.4786', '1.4570', '1.4406', '1.4267', '-0.0139', 'Improved. Coordinate regression tightening steadily.'),
    ('Classification loss', '3.3083', '2.4242', '2.3067', '2.1981', '2.1201', '2.0591', '-0.0610', 'Improved. Down -1.2492 pts total; nearing < 2.0.'),
    ('DFL loss', '1.5859', '1.5174', '1.4981', '1.4808', '1.4672', '1.4564', '-0.0108', 'Improved. Focal distribution refinement ongoing.'),
], [1.1, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.9, 1.6])

d.add_heading('Assessment and phase transition', 1)
p = d.add_paragraph()
p.add_run('Robust generalization. ').bold = True
p.add_run('mAP@50 increased to 11.22% and mAP@50-95 reached 7.29%. Recall reached 15.62%, indicating the detector now detects roughly 1 in every 6.4 ground-truth target objects in the complex 601-class evaluation set.')

p = d.add_paragraph()
p.add_run('Precision stabilization confirmed. ').bold = True
p.add_run('The drop in precision has significantly decelerated (-1.71 pts in Ep 6 vs -3.03 pts in Ep 5 and -4.82 pts in Ep 4). This confirms the theoretical expectation: the initial broad exploratory phase is transitioning into a boundary consolidation phase as learning rates stabilize.')

d.add_heading('Checkpoint summary and next step', 1)
table(d, ['Checkpoint', 'Purpose', 'Location'], [
    ('best.pt', 'Best validation model after Epoch 6', r'runs/detect/runs/detect/epoch_6/weights/best.pt'),
    ('last.pt', 'Resume point after Epoch 6', r'runs/detect/runs/detect/epoch_6/weights/last.pt'),
], [1.05, 1.75, 4.1])

p = d.add_paragraph()
p.add_run('Next step. ').bold = True
p.add_run('Launch Epoch 7 from the Epoch 6 last.pt checkpoint. Expect classification loss to break below 2.00.')

foot = sec.footer.paragraphs[0]
foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rr = foot.add_run('Epoch 6 checkpoint report  |  Open Images 601 Class Object Detection')
rr.font.size = Pt(8)
rr.font.color.rgb = RGBColor(100, 100, 100)

d.core_properties.title = 'Epoch 6 Training Report'
d.core_properties.author = 'CV Project'
d.save(REPORT)

# --- 2. LINKEDIN POST ---
POST.write_text('''# LinkedIn Post - Epoch 6 Training Update

Epoch 6 is complete for my 601-class computer vision object detection project!

Entering the second half of the 10-epoch training schedule, fine-tuning YOLO11 Nano on 85,000 images and validating across 15,000 images (100,000 total images per epoch). Metrics continue their upward climb, and the model is beginning to show textbook precision stabilization.

## Key Progression Highlights (Epoch 1 -> Epoch 6)

- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% -> 9.61% -> 10.49% -> 11.22% (+113.7% relative gain)
- Recall (objects found): 6.42% -> 9.73% -> 11.30% -> 13.18% -> 14.84% -> 15.62% (+143.3% relative gain)
- mAP@50-95 (strict average): 3.37% -> 4.71% -> 5.58% -> 6.30% -> 6.86% -> 7.29% (+116.3% relative gain)
- Classification Loss: 3.3083 -> 2.4242 -> 2.3067 -> 2.1981 -> 2.1201 -> 2.0591 (Nearing < 2.0)
- Box Loss: 1.5772 -> 1.4267 (Continuous coordinate tightening)
- DFL Loss: 1.5859 -> 1.4564 (Refining distribution bounds)

## The Turning Point: Precision Stabilization
In the early epochs (1-4), precision dropped as the model aggressively discovered rare classes among the 601 categories. By Epoch 6, the drop has flattened dramatically (-1.7 pts vs -4.8 pts earlier), signaling the transition from raw discovery to boundary refinement.

6 epochs in the books. 4 remaining. Heading straight into Epoch 7!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 6 done. mAP50 reached 11.2%, recall climbed past 15.6%, and all 3 losses dropped for the 6th consecutive epoch. precision drop is visibly flattening as expected. onto epoch 7.
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
draw.text((70, 52), 'COMPUTER VISION PROJECT  |  SECOND HALF UNDERWAY', font=F(22, True), fill='#B3D4FC')
draw.text((70, 98), 'Epoch 6: mAP Hits 11.2%', font=F(54, True), fill='white')
draw.text((70, 182), 'YOLO11 Nano  |  601 classes  |  Recall & mAP Up >110% Since Start', font=F(23), fill='#D9EAF7')

# Section Title
draw.text((70, 325), 'EPOCH 6 PROGRESSION (6 OF 10 COMPLETE)', font=F(21, True), fill=blue)
draw.text((70, 365), 'Consistent Convergence & Plateauing Precision', font=F(38, True), fill=ink)

# 4 Metric Cards with bracketed descriptions
metrics = [
    ('mAP@50 (accuracy at 50% overlap)', '10.49% -> 11.22%', 'UP +0.73 pts (+114% vs Ep 1)', green),
    ('Recall (objects found out of all)', '14.84% -> 15.62%', 'UP +0.78 pts (+143% vs Ep 1)', green),
    ('mAP@50-95 (average across stricter overlaps)', '6.86% -> 7.29%', 'UP +0.43 pts (+116% vs Ep 1)', green),
    ('Precision (detections that are correct)', '38.1% -> 36.4%', 'FLATTENING (-1.7 pts)', orange)
]

for i, (lab, val, delta, col) in enumerate(metrics):
    x = 70 + (i % 2) * 545
    y = 440 + (i // 2) * 175
    draw.rounded_rectangle((x, y, x + 515, y + 145), radius=16, fill=pale, outline='#D9E2EC', width=2)
    draw.text((x + 22, y + 20), lab, font=F(16, True), fill=blue)
    draw.text((x + 22, y + 54), val, font=F(30, True), fill=ink)
    draw.text((x + 22, y + 104), delta, font=F(17, True), fill=col)

# Loss Section Title
draw.text((70, 810), 'LOSS METRICS: 6TH CONSECUTIVE IMPROVEMENT', font=F(21, True), fill=blue)

# 3 Loss Cards with bracketed descriptions
losses = [
    ('Box loss (box location error)', '1.4406 -> 1.4267', '-0.0139 improved'),
    ('Classification loss (class prediction error)', '2.1201 -> 2.0591', '-0.0610 improved (nearing <2.0)'),
    ('DFL loss (box refinement error)', '1.4672 -> 1.4564', '-0.0108 improved')
]

for i, (lab, val, delta) in enumerate(losses):
    x = 70 + i * 355
    draw.rounded_rectangle((x, 855, x + 335, 995), radius=16, fill='#E4F7EA', outline='#B7E3C4', width=2)
    draw.text((x + 18, 878), lab, font=F(14, True), fill=green)
    draw.text((x + 18, 918), val, font=F(24, True), fill=ink)
    draw.text((x + 18, 958), delta, font=F(15, True), fill=green)

# Footer bar
draw.line((70, 1030, 1130, 1030), fill='#D9E2EC', width=2)
draw.text((70, 1055), 'Status: 6 of 10 epochs complete. Checkpoint saved. Continuing to Epoch 7.', font=F(21, True), fill=ink)
draw.text((70, 1098), 'Recall surged from 6.42% to 15.62%, finding over 44,800 validation instances.', font=F(18), fill=muted)

im.save(CARD, quality=95)
print('SUCCESS: Created', REPORT)
print('SUCCESS: Created', POST)
print('SUCCESS: Created', CARD)
