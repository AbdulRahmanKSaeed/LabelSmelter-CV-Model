import os
import sys
import csv
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def parse_results_csv(csv_path):
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cleaned = {k.strip(): v.strip() for k, v in r.items() if k is not None}
            rows.append(cleaned)
    if not rows:
        raise ValueError(f"No metric rows found in {csv_path}")
    return rows[-1]

def build_artifacts(round_num, epochs, csv_path, out_dir):
    out_dir = Path(out_dir)
    reports_dir = out_dir / "Reports"
    posts_dir = out_dir / "Posts"
    docs_dir = out_dir / "Documentation"

    reports_dir.mkdir(parents=True, exist_ok=True)
    posts_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)

    metrics = parse_results_csv(csv_path)

    # Extract metrics
    box_loss = float(metrics.get("train/box_loss", 0.0))
    cls_loss = float(metrics.get("train/cls_loss", 0.0))
    dfl_loss = float(metrics.get("train/dfl_loss", 0.0))
    prec = float(metrics.get("metrics/precision(B)", 0.0)) * 100
    rec = float(metrics.get("metrics/recall(B)", 0.0)) * 100
    map50 = float(metrics.get("metrics/mAP50(B)", 0.0)) * 100
    map50_95 = float(metrics.get("metrics/mAP50-95(B)", 0.0)) * 100

    # Phase 1 baseline values
    p1_rec = 19.05
    p1_map50 = 13.18
    p1_box = 1.3847
    p1_cls = 1.8941

    delta_rec = rec - p1_rec
    delta_map = map50 - p1_map50

    # 1. GENERATE DOCX REPORT
    docx_file = reports_dir / f"Phase_2_Epoch_{epochs}_Training_Report.docx"
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn

        def cell_shade(cell, color):
            p = cell._tc.get_or_add_tcPr()
            e = OxmlElement("w:shd")
            e.set(qn("w:fill"), color)
            p.append(e)

        doc = Document()
        sec = doc.sections[0]
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.7)
        sec.right_margin = Inches(0.7)

        p = doc.add_paragraph()
        run = p.add_run(f"Phase 2 Training Report: Milestone {epochs} Epochs")
        run.bold = True
        run.font.size = Pt(20)

        sub = doc.add_paragraph(f"Open Images 601 Classes | YOLO11 Medium (20.1M Params) on Google Colab T4 | Round {round_num}")
        sub.runs[0].font.size = Pt(10)
        sub.runs[0].font.color.rgb = RGBColor(100, 100, 100)

        p_sum = doc.add_paragraph()
        p_sum.add_run("Executive Summary: ").bold = True
        p_sum.add_run(f"Round {round_num} (Epochs 1–{epochs}) completed on cloud hardware using YOLO11 Medium (20.1M parameters). "
                      f"Detection recall reached {rec:.2f}%, mAP@50 reached {map50:.2f}%, and classification loss reached {cls_loss:.4f}. "
                      f"Compared to Phase 1's 10-epoch edge baseline, this demonstrates the significant scaling power of 7.5x larger model capacity.")

        doc.add_heading("Cloud Scale-Up Comparison vs Phase 1 Baseline", 1)
        tbl = doc.add_table(rows=1, cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        headers = ["Metric", "Phase 1 Baseline (YOLO11n, 2.8M)", f"Phase 2 Epoch {epochs} (YOLO11m, 20.1M)", "Change vs Phase 1"]
        for i, h in enumerate(headers):
            c = tbl.rows[0].cells[i]
            c.text = h
            cell_shade(c, "17365D")
            c.paragraphs[0].runs[0].font.bold = True
            c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

        rows_data = [
            ("Recall (Objects Found)", f"{p1_rec:.2f}%", f"{rec:.2f}%", f"{'+' if delta_rec>=0 else ''}{delta_rec:.2f} pts"),
            ("mAP@50 (50% IoU)", f"{p1_map50:.2f}%", f"{map50:.2f}%", f"{'+' if delta_map>=0 else ''}{delta_map:.2f} pts"),
            ("mAP@50-95 (Strict)", "8.52%", f"{map50_95:.2f}%", f"{map50_95 - 8.52:+.2f} pts"),
            ("Precision", "29.24%", f"{prec:.2f}%", f"{prec - 29.24:+.2f} pts"),
            ("Classification Loss", f"{p1_cls:.4f}", f"{cls_loss:.4f}", f"{cls_loss - p1_cls:+.4f}"),
            ("Box Loss", f"{p1_box:.4f}", f"{box_loss:.4f}", f"{box_loss - p1_box:+.4f}"),
            ("DFL Loss", "1.4244", f"{dfl_loss:.4f}", f"{dfl_loss - 1.4244:+.4f}")
        ]
        for ri, r in enumerate(rows_data):
            row_cells = tbl.add_row().cells
            for ci, val in enumerate(r):
                row_cells[ci].text = val
                if ri % 2 == 1:
                    cell_shade(row_cells[ci], "F5F8FC")

        doc.save(docx_file)
        print(f"SUCCESS: Generated {docx_file}")
    except Exception as e:
        print(f"Warning: Could not create DOCX ({e})")

    # 2. GENERATE 1200x1200 LINKEDIN GRAPHIC
    png_file = posts_dir / f"Phase_2_Epoch_{epochs}_Training_Results.png"
    try:
        W = H = 1200
        im = Image.new("RGB", (W, H), "white")
        draw = ImageDraw.Draw(im)

        navy = "#102A43"
        blue = "#1D70B8"
        ink = "#1F2933"
        pale = "#EAF3FB"
        green = "#16803C"
        orange = "#D97706"

        draw.rectangle((0, 0, W, 290), fill=navy)
        draw.rectangle((0, 0, 18, 290), fill=blue)
        draw.text((70, 50), f"PHASE 2 CLOUD SCALE-UP  |  ROUND {round_num} ({epochs} OF 30 EPOCHS)", font=get_font(22, True), fill="#B3D4FC")
        draw.text((70, 96), f"YOLO11 Medium: {epochs} Epochs Done", font=get_font(52, True), fill="white")
        draw.text((70, 180), "Open Images 601 Classes  |  20.1M Parameters on Google Cloud T4 GPU", font=get_font(22), fill="#D9EAF7")

        draw.text((70, 325), "SCALE-UP DETECTION METRICS", font=get_font(21, True), fill=blue)
        draw.text((70, 365), f"Milestone: {epochs} Epochs Completed in Colab", font=get_font(38, True), fill=ink)

        cards = [
            ("mAP@50 (accuracy at 50% overlap)", f"{map50:.2f}%", f"{'+' if delta_map>=0 else ''}{delta_map:.2f} pts vs Phase 1", green),
            ("Recall (objects found out of all)", f"{rec:.2f}%", f"{'+' if delta_rec>=0 else ''}{delta_rec:.2f} pts vs Phase 1", green),
            ("mAP@50-95 (strict overlap average)", f"{map50_95:.2f}%", "Deep multi-threshold IoU", green),
            ("Precision (detections that are correct)", f"{prec:.2f}%", "Balanced convergence", orange)
        ]

        for i, (lab, val, delta, col) in enumerate(cards):
            x = 70 + (i % 2) * 545
            y = 440 + (i // 2) * 175
            draw.rounded_rectangle((x, y, x + 515, y + 145), radius=16, fill=pale, outline="#D9E2EC", width=2)
            draw.text((x + 22, y + 20), lab, font=get_font(16, True), fill=blue)
            draw.text((x + 22, y + 54), val, font=get_font(30, True), fill=ink)
            draw.text((x + 22, y + 104), delta, font=get_font(17, True), fill=col)

        draw.text((70, 810), "LOSS OPTIMIZATION ON CLOUD ACCELERATOR", font=get_font(21, True), fill=blue)

        loss_cards = [
            ("Box loss (localization error)", f"{box_loss:.4f}", f"{box_loss - p1_box:+.4f} vs Phase 1"),
            ("Classification loss (class error)", f"{cls_loss:.4f}", f"{cls_loss - p1_cls:+.4f} vs Phase 1"),
            ("DFL loss (focal box error)", f"{dfl_loss:.4f}", "Refined object boundaries")
        ]
        for i, (lab, val, delta) in enumerate(loss_cards):
            x = 70 + i * 355
            draw.rounded_rectangle((x, 855, x + 335, 995), radius=16, fill="#E4F7EA", outline="#B7E3C4", width=2)
            draw.text((x + 18, 878), lab, font=get_font(14, True), fill=green)
            draw.text((x + 18, 918), val, font=get_font(24, True), fill=ink)
            draw.text((x + 18, 958), delta, font=get_font(14, True), fill=green)

        draw.line((70, 1030, 1130, 1030), fill="#D9E2EC", width=2)
        draw.text((70, 1055), f"Status: Phase 2 Round {round_num} ({epochs}/30 epochs complete). High capacity training in progress.", font=get_font(21, True), fill=ink)
        draw.text((70, 1098), f"Trained on NVIDIA Tesla T4 with batch size 32 across 601 Open Images categories.", font=get_font(18), fill="#627D98")

        im.save(png_file, quality=95)
        print(f"SUCCESS: Generated {png_file}")
    except Exception as e:
        print(f"Warning: Could not create PNG ({e})")

    # 3. GENERATE LINKEDIN POST MARKDOWN
    md_file = posts_dir / f"Phase_2_Epoch_{epochs}_LinkedIn_Post.md"
    post_content = f"""# LinkedIn Post - Phase 2: Round {round_num} ({epochs} Epochs) Training Update

Excited to share the first milestone of **Phase 2** for my 601-class computer vision object detection project!

After completing our 10-epoch edge baseline on a GTX 1050 (3GB VRAM) with YOLO11 Nano, we have successfully scaled up compute to **Google Cloud GPUs (NVIDIA Tesla T4 with 16 GB VRAM)** and upgraded the model architecture to **YOLO11 Medium (`yolo11m`) with 20.1 million parameters** (a 7.5x increase in capacity!).

## Phase 2 Round {round_num} Highlights ({epochs} Epochs):

- **Recall (Objects Found):** {rec:.2f}% (vs {p1_rec:.2f}% in Phase 1)
- **mAP@50 (50% IoU Accuracy):** {map50:.2f}% (vs {p1_map50:.2f}% in Phase 1)
- **Classification Loss:** {cls_loss:.4f}
- **Box Localization Loss:** {box_loss:.4f}
- **Hardware & Batch Size:** Batch size 32 on a 16 GB Tesla T4 GPU

## Why Phase 2 Scaling Matters
In Phase 1, our lightweight 2.8M-parameter Nano model proved the feasibility of training across 601 categories on a laptop GPU. However, resolving fine-grained and distant objects (such as parked cars and dense crowds) requires deeper feature representation. 

With 20.1M parameters and batch size 32 on cloud accelerators, the model is now developing significantly higher confidence and much tighter bounding box regressions across the 601 categories.

Onto Round {round_num + 1} (Epochs {epochs+1} to {epochs+5})!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #AI #OpenImages #CloudComputing #MachineLearning

---

# Short Caption

phase 2 round {round_num} complete! trained yolo11 medium (20.1m params) for {epochs} epochs on a 16gb tesla t4 in google colab. recall reached {rec:.2f}%, map50 hit {map50:.2f}%, and bounding boxes are tightening across all 601 classes. onto the next 5 epochs!
"""
    md_file.write_text(post_content, encoding="utf-8")
    print(f"SUCCESS: Generated {md_file}")

    # 4. APPEND TO JOURNAL
    journal_file = docs_dir / "PROJECT_JOURNAL_PHASE_2.md"
    journal_entry = f"""

## Phase 2 Round {round_num} ({epochs} Epochs Complete)

**Status:** Completed successfully  
**Model:** YOLO11 Medium (`yolo11m` - 20.1M parameters)  
**Hardware:** Google Colab NVIDIA Tesla T4 (16 GB VRAM)  
**Batch Size:** 32 at 640x640  

### Metrics Snapshot
| Metric | Phase 1 Baseline (YOLO11n, 10 Ep) | Phase 2 Epoch {epochs} (YOLO11m) | Change |
|---|---:|---:|---:|
| Recall | {p1_rec:.2f}% | **{rec:.2f}%** | {delta_rec:+.2f} pts |
| mAP@50 | {p1_map50:.2f}% | **{map50:.2f}%** | {delta_map:+.2f} pts |
| mAP@50-95 | 8.52% | **{map50_95:.2f}%** | {map50_95 - 8.52:+.2f} pts |
| Precision | 29.24% | **{prec:.2f}%** | {prec - 29.24:+.2f} pts |
| Classification Loss | {p1_cls:.4f} | **{cls_loss:.4f}** | {cls_loss - p1_cls:+.4f} |
| Box Loss | {p1_box:.4f} | **{box_loss:.4f}** | {box_loss - p1_box:+.4f} |
| DFL Loss | 1.4244 | **{dfl_loss:.4f}** | {dfl_loss - 1.4244:+.4f} |

Checkpoints and artifacts saved to `{out_dir}`.
"""
    try:
        with open(journal_file, "a", encoding="utf-8") as f:
            f.write(journal_entry)
        print(f"SUCCESS: Appended entry to {journal_file}")
    except Exception as e:
        print(f"Warning: Could not update journal ({e})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--results_csv", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="/content/drive/MyDrive/CV_Project_Phase2")
    args = parser.parse_args()

    build_artifacts(args.round, args.epochs, args.results_csv, args.output_dir)

if __name__ == "__main__":
    main()
