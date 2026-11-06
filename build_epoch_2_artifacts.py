from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r'C:\Users\HP\Desktop\CV Project')
REPORT = ROOT / 'Epoch Reports' / 'Epoch_2_Training_Report.docx'
POST = ROOT / 'Epoch Posts' / 'Epoch_2_LinkedIn_Post.md'
CARD = ROOT / 'Epoch Posts' / 'Epoch_2_Training_Results.png'

NAVY, BLUE, PALE, GRID = '17365D','1D70B8','F5F8FC','D9D9D9'

def cell_shade(cell, color):
    p = cell._tc.get_or_add_tcPr(); e = OxmlElement('w:shd'); e.set(qn('w:fill'), color); p.append(e)
def style_cell(c, header=False, center=False):
    c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p=c._tc.get_or_add_tcPr(); borders=OxmlElement('w:tcBorders')
    for side in ('top','left','bottom','right'):
        e=OxmlElement('w:'+side); e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),GRID);borders.append(e)
    p.append(borders)
    for para in c.paragraphs:
        para.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
        para.paragraph_format.space_after=Pt(0)
        for r in para.runs:
            r.font.name='Aptos';r._element.rPr.rFonts.set(qn('w:ascii'),'Aptos');r._element.rPr.rFonts.set(qn('w:hAnsi'),'Aptos');r.font.size=Pt(9)
            if header:r.font.bold=True;r.font.color.rgb=RGBColor(255,255,255)
    if header:cell_shade(c,NAVY)
def table(doc, hdr, rows, widths):
    t=doc.add_table(rows=1,cols=len(hdr));t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.autofit=False
    for i,v in enumerate(hdr):
        c=t.rows[0].cells[i];c.width=Inches(widths[i]);c.text=v;style_cell(c,True,True)
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for i,v in enumerate(row):
            cells[i].width=Inches(widths[i]);cells[i].text=str(v);style_cell(cells[i],False,i>0)
            if ri%2:cell_shade(cells[i],PALE)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)

# DOCX
d=Document();sec=d.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.72);sec.right_margin=Inches(.72)
for n,size in [('Normal',10),('Title',22),('Heading 1',14)]:
    s=d.styles[n];s.font.name='Aptos';s._element.rPr.rFonts.set(qn('w:ascii'),'Aptos');s._element.rPr.rFonts.set(qn('w:hAnsi'),'Aptos');s.font.size=Pt(size);s.font.color.rgb=RGBColor(0,0,0)
p=d.add_paragraph(style='Title');p.add_run('Epoch 2 Training Report')
p=d.add_paragraph('Open Images 601 Class Object Detection  |  Run epoch_by_epoch-3  |  November 5 2026');p.paragraph_format.space_after=Pt(14)
for r in p.runs:r.font.size=Pt(10);r.font.color.rgb=RGBColor(89,89,89)
p=d.add_paragraph();p.add_run('Summary. ').bold=True;p.add_run('Epoch 2 completed successfully and improved recall and both mAP measures over Epoch 1. All three training losses also decreased, indicating continued learning. Precision reduced slightly, which is common while the model starts making more detections.')
d.add_heading('Run summary',1)
table(d,['Item','Result'],[
 ('Status','Completed successfully'),('Model','YOLO11 Nano fine tuned for 601 classes'),('Dataset pass','85,000 training images and 15,000 validation images'),('Batch and image size','8 images per training batch at 640 pixels'),('Total two epoch run time','3.060 hours'),('Output folder','runs/detect/runs/detect/epoch_by_epoch-3')],[2.0,4.9])
d.add_heading('Validation metrics compared with Epoch 1',1)
table(d,['Metric','Epoch 1','Epoch 2','Change'],[
 ('Precision','53.78%','51.17%','-2.61 percentage points'),('Recall','6.42%','9.73%','+3.32 percentage points'),('mAP at 50','5.25%','7.21%','+1.96 percentage points'),('mAP at 50 to 95','3.37%','4.71%','+1.35 percentage points'),
],[1.55,1.3,1.3,2.75])
d.add_heading('Loss metrics compared with Epoch 1',1)
table(d,['Loss','Epoch 1','Epoch 2','Change','Meaning'],[
 ('Box loss','1.5772','1.5002','-0.0770','Improved bounding box localization.'),('Classification loss','3.3083','2.4242','-0.8841','Large improvement in class prediction.'),('DFL loss','1.5859','1.5174','-0.0685','Improved box refinement.'),
],[1.25,1.15,1.15,1.25,2.1])
d.add_heading('Assessment',1)
p=d.add_paragraph();p.add_run('What improved. ').bold=True;p.add_run('Recall increased by 51.7% relative to Epoch 1, mAP at 50 increased by 37.3%, and mAP at 50 to 95 increased by 39.9%. The declining losses reinforce that the model is learning more accurate classes and locations.')
p=d.add_paragraph();p.add_run('Precision note. ').bold=True;p.add_run('Precision moved down from 53.8% to 51.2%. This is not concerning after only two epochs: the rising recall suggests the model is attempting more detections, and the mAP gains show overall detection quality improved.')
d.add_heading('Checkpoint summary and next step',1)
table(d,['Checkpoint','Purpose','Location'],[
 ('best.pt','Best validation model after Epoch 2',r'runs/detect/runs/detect/epoch_by_epoch-3/weights/best.pt'),('last.pt','Resume point after Epoch 2',r'runs/detect/runs/detect/epoch_by_epoch-3/weights/last.pt'),
],[1.05,1.75,4.1])
p=d.add_paragraph();p.add_run('Next step. ').bold=True;p.add_run('Continue from the Epoch 2 last.pt checkpoint for Epoch 3. Track whether mAP and recall continue upward and whether losses continue downward; those are the key near term trends.')
foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.CENTER;rr=foot.add_run('Epoch 2 checkpoint report  |  Open Images 601 Class Object Detection');rr.font.size=Pt(8);rr.font.color.rgb=RGBColor(100,100,100)
d.core_properties.title='Epoch 2 Training Report';d.core_properties.author='CV Project';d.save(REPORT)

# LinkedIn copy
POST.write_text('''# LinkedIn Post - Epoch 2 Training Update\n\nEpoch 2 is complete for my 601 class computer vision object detection project.\n\nI am fine tuning YOLO11 Nano on 85,000 training images and validating on 15,000 separate images. The second epoch completed successfully, and the model is already showing a better overall ability to find objects.\n\n## Results compared with Epoch 1\n\n- Recall: 6.42% to 9.73%\n- mAP@50: 5.25% to 7.21%\n- mAP@50-95: 3.37% to 4.71%\n- Precision: 53.8% to 51.2%\n\n## Loss improvement\n\n- Box loss: 1.5772 to 1.5002\n- Classification loss: 3.3083 to 2.4242\n- DFL loss: 1.5859 to 1.5174\n\nThe biggest early signal is the recall and mAP improvement. The slight precision drop is expected while the model begins making more detections; the rising mAP and falling losses show that the overall learning direction is positive.\n\nNext up: Epoch 3, continuing from the new saved checkpoint.\n\n#ComputerVision #ObjectDetection #YOLO #DeepLearning #MachineLearning #AI\n\n---\n\n# Short Caption\n\nepoch 2 done. recall and mAP are up, all three losses are down, and the model is learning better from the full 601 class dataset. moving onto epoch 3.\n''',encoding='utf-8')

# LinkedIn image
W=H=1200;im=Image.new('RGB',(W,H),'white');draw=ImageDraw.Draw(im)
def F(sz,b=False):return ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if b else 'C:/Windows/Fonts/arial.ttf',sz)
navy='#102A43';blue='#1D70B8';ink='#1F2933';muted='#627D98';pale='#EAF3FB';green='#16803C';orange='#F59E0B'
draw.rectangle((0,0,W,300),fill=navy);draw.rectangle((0,0,18,300),fill=blue)
draw.text((70,58),'COMPUTER VISION PROJECT',font=F(24,True),fill='#B3D4FC');draw.text((70,112),'Epoch 2 Complete',font=F(58,True),fill='white');draw.text((70,195),'YOLO11 Nano  |  601 classes  |  100,000 image dataset',font=F(25),fill='#D9EAF7')
draw.text((70,350),'EPOCH 2 VS EPOCH 1',font=F(22,True),fill=blue);draw.text((70,393),'Learning trend is positive',font=F(42,True),fill=ink)
metrics=[('Recall (objects found out of all)','6.42% → 9.73%','UP +3.32 pts',green),('mAP@50 (accuracy at 50% overlap)','5.25% → 7.21%','UP +1.96 pts',green),('mAP@50-95 (average across stricter overlaps)','3.37% → 4.71%','UP +1.35 pts',green),('Precision (detections that are correct)','53.8% → 51.2%','DOWN -2.61 pts',orange)]
for i,(lab,val,delta,col) in enumerate(metrics):
 x=70+(i%2)*545;y=485+(i//2)*180;draw.rounded_rectangle((x,y,x+515,y+145),radius=18,fill=pale,outline='#D9E2EC',width=2);draw.text((x+25,y+22),lab,font=F(17,True),fill=blue);draw.text((x+25,y+58),val,font=F(31,True),fill=ink);draw.text((x+25,y+108),delta,font=F(18,True),fill=col)
draw.text((70,855),'LOSS METRICS ALL DECREASED',font=F(22,True),fill=blue)
losses=[('Box loss (box location error)','1.5772 → 1.5002'),('Classification loss (class prediction error)','3.3083 → 2.4242'),('DFL loss (box refinement error)','1.5859 → 1.5174')]
for i,(lab,val) in enumerate(losses):
 x=70+i*355;draw.rounded_rectangle((x,905,x+325,1032),radius=16,fill='#E4F7EA',outline='#B7E3C4',width=2);draw.text((x+22,928),lab,font=F(15,True),fill=green);draw.text((x+22,971),val,font=F(25,True),fill=ink);draw.text((x+22,1007),'improved',font=F(16),fill=green)
draw.line((70,1080,1130,1080),fill='#D9E2EC',width=2);draw.text((70,1110),'Status: Epoch 2 checkpoint saved. Continuing to Epoch 3.',font=F(22,True),fill=ink);draw.text((70,1153),'Rising recall and mAP with falling losses is the key early result.',font=F(18),fill=muted)
im.save(CARD,quality=95)
print(REPORT);print(POST);print(CARD)
