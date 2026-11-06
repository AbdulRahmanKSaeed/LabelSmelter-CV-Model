from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUT = Path(r"C:\Users\HP\.codex\visualizations\2026\11\02\01a19bb2-6b9b-7790-a118-32f25fa009d4\Epoch_1_Training_Report.docx")

NAVY = "17365D"
BLUE = "DCEAF7"
PALE = "F5F8FC"
GRID = "D9D9D9"

def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), fill)
    tc_pr.append(shd)

def border(cell):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = tc_pr.first_child_found_in('w:tcBorders')
    if borders is None:
        borders = OxmlElement('w:tcBorders')
        tc_pr.append(borders)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        tag = 'w:' + edge
        el = borders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag); borders.append(el)
        el.set(qn('w:val'), 'single'); el.set(qn('w:sz'), '4'); el.set(qn('w:color'), GRID)

def margins(cell, top=110, start=130, bottom=110, end=130):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.first_child_found_in('w:tcMar')
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar'); tcPr.append(tcMar)
    for side, value in [('top',top),('start',start),('bottom',bottom),('end',end)]:
        node = tcMar.find(qn('w:' + side))
        if node is None:
            node = OxmlElement('w:' + side); tcMar.append(node)
        node.set(qn('w:w'), str(value)); node.set(qn('w:type'), 'dxa')

def style_cell(cell, header=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    border(cell); margins(cell)
    for p in cell.paragraphs:
        p.alignment = align
        p.paragraph_format.space_after = Pt(0)
        for r in p.runs:
            r.font.name = 'Aptos'; r._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos'); r._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
            r.font.size = Pt(9)
            if header:
                r.font.bold = True; r.font.color.rgb = RGBColor(255,255,255)
    if header: shade(cell, NAVY)

def add_table(doc, headers, rows, widths):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for i, text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.width = Inches(widths[i]); cell.text = text; style_cell(cell, True, WD_ALIGN_PARAGRAPH.CENTER)
    for row_i, row in enumerate(rows):
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].width = Inches(widths[i]); cells[i].text = str(value)
            style_cell(cells[i], False, WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT)
            if row_i % 2 == 1: shade(cells[i], PALE)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65); sec.bottom_margin = Inches(0.65); sec.left_margin = Inches(0.72); sec.right_margin = Inches(0.72)

styles = doc.styles
styles['Normal'].font.name = 'Aptos'; styles['Normal']._element.rPr.rFonts.set(qn('w:ascii'), 'Aptos'); styles['Normal']._element.rPr.rFonts.set(qn('w:hAnsi'), 'Aptos')
styles['Normal'].font.size = Pt(10)
for style_name, size in [('Title', 22), ('Heading 1', 14), ('Heading 2', 11)]:
    st = styles[style_name]; st.font.name = 'Aptos Display' if style_name == 'Title' else 'Aptos'; st.font.size = Pt(size); st.font.color.rgb = RGBColor(0,0,0)
    st._element.rPr.rFonts.set(qn('w:ascii'), st.font.name); st._element.rPr.rFonts.set(qn('w:hAnsi'), st.font.name)

title = doc.add_paragraph(style='Title'); title.alignment = WD_ALIGN_PARAGRAPH.LEFT
title.add_run('Epoch 1 Training Report')
sub = doc.add_paragraph(); sub.paragraph_format.space_after = Pt(14)
r = sub.add_run('Open Images 601 Class Object Detection  |  Run epoch_by_epoch  |  November 4 2026')
r.font.size = Pt(10); r.font.color.rgb = RGBColor(89,89,89)

p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(10)
lead = p.add_run('Summary. '); lead.bold = True
p.add_run('The first full training epoch completed successfully on the GTX 1050 without a memory error. The run produced valid checkpoints and baseline validation results. The model is still at an early learning stage; continue training before making accuracy decisions.')

doc.add_heading('Run summary', level=1)
add_table(doc, ['Item', 'Result'], [
    ('Status', 'Completed successfully'),
    ('Start time', 'November 4 2026 9:05 PM'),
    ('Model', 'YOLO11 Nano yolo11n fine tuned for 601 classes'),
    ('Compute', 'NVIDIA GeForce GTX 1050 with 3072 MiB VRAM'),
    ('Training workload', '85,000 images across 10,625 batches'),
    ('Validation workload', '15,000 images with 286,954 labeled objects'),
    ('Duration', '1.611 hours approximately 1 hour 37 minutes'),
    ('Peak GPU memory', '3.07 GB'),
], [2.1, 4.8])

doc.add_heading('Validation metrics', level=1)
add_table(doc, ['Metric', 'Epoch 1 result', 'Interpretation'], [
    ('Precision', '53.8%', 'Predicted detections were often correct when made.'),
    ('Recall', '6.42%', 'Most ground truth objects are not yet being found.'),
    ('mAP at 50', '5.25%', 'Early baseline at the 0.50 IoU threshold.'),
    ('mAP at 50 to 95', '3.37%', 'Stricter overall localization baseline.'),
], [1.45, 1.25, 4.2])

doc.add_heading('Training losses', level=1)
add_table(doc, ['Loss', 'Epoch 1 value', 'Purpose'], [
    ('Box loss', '1.577', 'Bounding box location and size error.'),
    ('Classification loss', '3.308', 'Class prediction error across 601 classes.'),
    ('DFL loss', '1.586', 'Bounding box distribution refinement error.'),
], [1.45, 1.4, 4.05])

doc.add_heading('Checkpoint summary', level=1)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(5)
p.add_run('Both checkpoints were written successfully. ').bold = True
p.add_run('At epoch 1, best.pt and last.pt represent the same completed model state; future epochs may cause them to diverge if a later epoch does not improve validation performance.')
add_table(doc, ['Checkpoint', 'Purpose', 'Location'], [
    ('best.pt', 'Best validation result so far', r'C:\Users\HP\Desktop\CV Project\runs\detect\runs\detect\epoch_by_epoch\weights\best.pt'),
    ('last.pt', 'Resume point after epoch 1', r'C:\Users\HP\Desktop\CV Project\runs\detect\runs\detect\epoch_by_epoch\weights\last.pt'),
], [1.05, 1.75, 4.1])

doc.add_heading('Run health and observations', level=1)
for text in [
    'No CUDA out of memory error occurred, although observed GPU use of 3.07 GB is close to the available 3 GB capacity. Keep batch size at 8 only while runs remain stable; reduce it to 4 if memory errors appear.',
    'The training pipeline detected slower image reads at about 38 to 40 MB/s. This affects throughput but did not stop the run.',
    'Forty three duplicate training labels and four duplicate validation labels were removed automatically. No corrupt images were reported.',
    'The evaluator raised its maximum detections per image to 510 to match the densest annotated image, avoiding an artificial recall cap during validation.',
]:
    p = doc.add_paragraph(style='Normal'); p.style = styles['Normal']; p.paragraph_format.left_indent = Inches(0.18); p.paragraph_format.first_line_indent = Inches(-0.18); p.paragraph_format.space_after = Pt(4)
    p.add_run('• ').bold = True; p.add_run(text)

doc.add_heading('Assessment and next checkpoint', level=1)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(5)
p.add_run('Assessment. ').bold = True
p.add_run('The low recall and mAP values are expected after one epoch for a 601 class detector. The stable completion and saved checkpoints confirm that the training pipeline is ready to continue. Do not compare this run to a finished model yet; the useful signal will be the direction of loss and mAP across subsequent epochs.')
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(0)
p.add_run('Next checkpoint target. ').bold = True
p.add_run('After epoch 2, compare mAP, recall, precision, losses, training time, GPU memory, disk space, and whether best.pt changed. Estimated runtime for the next epoch is about 1 hour 35 to 45 minutes if system conditions remain similar.')

footer = sec.footer.paragraphs[0]; footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer.add_run('Epoch 1 checkpoint report  |  Open Images 601 Class Object Detection')
fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(100,100,100)

doc.core_properties.title = 'Epoch 1 Training Report'
doc.core_properties.subject = 'YOLO11 Nano checkpoint summary'
doc.core_properties.author = 'CV Project'
doc.save(OUT)
print(OUT)
