"""
Phase 2 Round Artifact Generator
==================================
Generates per-round consolidated artifacts:
  1. DOCX Technical Report  -> Phase 2/Reports/
  2. 1200x1200 LinkedIn PNG -> Phase 2/Posts/  (dark premium theme)
  3. LinkedIn Post Markdown -> Phase 2/Posts/
  4. Journal Entry          -> Phase 2/Documentation/PROJECT_JOURNAL_PHASE_2.md

Usage:
  python scripts/generate_phase2_round_artifacts.py --round 1 --start_epoch 11 --end_epoch 15
      --results_csv "runs/detect/phase2/round_1_epochs_11_15/results.csv"
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Phase 1 baseline metrics ────────────────────────────────────────────────
P1_RECALL    = 19.05
P1_PREC      = 29.24
P1_MAP50     = 13.18
P1_MAP5095   = 8.52
P1_BOX_LOSS  = 1.3847
P1_CLS_LOSS  = 1.8941
P1_DFL_LOSS  = 1.4244

# ── Colour palette — dark premium ───────────────────────────────────────────
BG_MAIN   = "#0D1117"
BG_CARD   = "#161B22"
BG_CARD2  = "#1C2128"
BORDER    = "#30363D"
TEXT_PRI  = "#F0F6FC"
TEXT_MUT  = "#8B949E"
CYAN      = "#58A6FF"
GREEN     = "#3FB950"
RED_SOFT  = "#F78166"
ORANGE    = "#D29922"
PURPLE    = "#BC8CFF"
WHITE     = "#FFFFFF"


# ── Helpers ──────────────────────────────────────────────────────────────────
def _font(size, bold=False):
    from PIL import ImageFont
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def parse_csv(csv_path):
    """Return list of metric dicts (one per epoch row) + last-row summary."""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k.strip(): v.strip() for k, v in r.items() if k})
    if not rows:
        raise ValueError(f"No data in {csv_path}")
    return rows


def extract(row, key, default=0.0):
    return float(row.get(key, default) or default)


# ── 1. PNG Graphic ───────────────────────────────────────────────────────────
def build_png(round_num, start_ep, end_ep, rows, out_path):
    from PIL import Image, ImageDraw

    W = H = 1200
    im = Image.new("RGB", (W, H), hex_to_rgb(BG_MAIN))
    draw = ImageDraw.Draw(im)

    last = rows[-1]
    rec      = extract(last, "metrics/recall(B)") * 100
    prec     = extract(last, "metrics/precision(B)") * 100
    map50    = extract(last, "metrics/mAP50(B)") * 100
    map5095  = extract(last, "metrics/mAP50-95(B)") * 100
    box_loss = extract(last, "train/box_loss")
    cls_loss = extract(last, "train/cls_loss")
    dfl_loss = extract(last, "train/dfl_loss")

    d_rec   = rec   - P1_RECALL
    d_map50 = map50 - P1_MAP50
    d_map95 = map5095 - P1_MAP5095
    d_prec  = prec  - P1_PREC

    def delta_col(v):
        return GREEN if v >= 0 else RED_SOFT

    def signed(v, pct=False):
        s = f"{v:+.2f}{'%' if pct else ''}"
        return s

    # ── Header banner ────────────────────────────────────────────────────────
    draw.rectangle((0, 0, W, 270), fill=hex_to_rgb(BG_CARD))
    # Cyan left accent bar
    draw.rectangle((0, 0, 6, 270), fill=hex_to_rgb(CYAN))
    # Dot-grid texture suggestion: subtle horizontal rule
    draw.line((6, 270, W, 270), fill=hex_to_rgb(BORDER), width=2)

    draw.text((40, 38),
              f"PHASE 2  ·  ROUND {round_num}  ·  EPOCHS {start_ep}–{end_ep}",
              font=_font(20, True), fill=hex_to_rgb(CYAN))
    draw.text((40, 80),
              f"YOLO11 Nano — Optimized Training",
              font=_font(54, True), fill=hex_to_rgb(TEXT_PRI))
    draw.text((40, 162),
              f"Open Images V6  ·  601 Classes  ·  GTX 1050 3 GB  ·  FP16 + Cosine LR + Mosaic Augmentation",
              font=_font(19), fill=hex_to_rgb(TEXT_MUT))
    draw.text((40, 210),
              f"Phase 1 Baseline → Epoch 10:  Recall {P1_RECALL}%  |  mAP@50 {P1_MAP50}%  |  Box Loss {P1_BOX_LOSS}",
              font=_font(18), fill=hex_to_rgb(TEXT_MUT))

    # ── Section label ────────────────────────────────────────────────────────
    draw.text((40, 296), "DETECTION METRICS — ROUND FINAL vs PHASE 1 BASELINE",
              font=_font(18, True), fill=hex_to_rgb(CYAN))

    # ── 4 Metric cards ───────────────────────────────────────────────────────
    metric_cards = [
        ("mAP@50", f"{map50:.2f}%", signed(d_map50, True), delta_col(d_map50), "Accuracy at 50% IoU overlap"),
        ("Recall",  f"{rec:.2f}%",  signed(d_rec,   True), delta_col(d_rec),   "Objects detected / all ground truth"),
        ("mAP@50-95", f"{map5095:.2f}%", signed(d_map95, True), delta_col(d_map95), "Strict multi-threshold average"),
        ("Precision", f"{prec:.2f}%", signed(d_prec, True), delta_col(d_prec),  "Correct detections / all detections"),
    ]

    for i, (title, val, delta, dcol, sub) in enumerate(metric_cards):
        col = i % 2
        row = i // 2
        x = 40  + col * 592
        y = 330 + row * 185
        # Card background
        draw.rounded_rectangle((x, y, x + 562, y + 162), radius=14,
                                fill=hex_to_rgb(BG_CARD), outline=hex_to_rgb(BORDER), width=1)
        # Cyan top micro-bar
        draw.rounded_rectangle((x + 1, y + 1, x + 561, y + 5), radius=4, fill=hex_to_rgb(CYAN))
        draw.text((x + 22, y + 20), title, font=_font(20, True), fill=hex_to_rgb(CYAN))
        draw.text((x + 22, y + 52), val,   font=_font(44, True), fill=hex_to_rgb(TEXT_PRI))
        draw.text((x + 22, y + 110), delta, font=_font(20, True), fill=hex_to_rgb(dcol))
        draw.text((x + 22, y + 138), sub,  font=_font(15),        fill=hex_to_rgb(TEXT_MUT))

    # ── Loss cards section ───────────────────────────────────────────────────
    draw.line((40, 710, W - 40, 710), fill=hex_to_rgb(BORDER), width=1)
    draw.text((40, 724), "LOSS METRICS — CONTINUOUS CONVERGENCE FROM PHASE 1",
              font=_font(18, True), fill=hex_to_rgb(CYAN))

    loss_cards = [
        ("Box Loss",   f"{box_loss:.4f}", f"{box_loss - P1_BOX_LOSS:+.4f} vs Phase 1",  "Localization error",   delta_col(-(box_loss - P1_BOX_LOSS))),
        ("Class Loss", f"{cls_loss:.4f}", f"{cls_loss - P1_CLS_LOSS:+.4f} vs Phase 1",  "Classification error", delta_col(-(cls_loss - P1_CLS_LOSS))),
        ("DFL Loss",   f"{dfl_loss:.4f}", f"{dfl_loss - P1_DFL_LOSS:+.4f} vs Phase 1",  "Box focal refinement", delta_col(-(dfl_loss - P1_DFL_LOSS))),
    ]

    for i, (title, val, delta, sub, dcol) in enumerate(loss_cards):
        x = 40 + i * 382
        y = 758
        draw.rounded_rectangle((x, y, x + 362, y + 148), radius=14,
                                fill=hex_to_rgb(BG_CARD2), outline=hex_to_rgb(BORDER), width=1)
        draw.rounded_rectangle((x + 1, y + 1, x + 361, y + 5), radius=4, fill=hex_to_rgb(GREEN))
        draw.text((x + 20, y + 18),  title, font=_font(18, True), fill=hex_to_rgb(GREEN))
        draw.text((x + 20, y + 50),  val,   font=_font(36, True), fill=hex_to_rgb(TEXT_PRI))
        draw.text((x + 20, y + 98),  delta, font=_font(17, True), fill=hex_to_rgb(dcol))
        draw.text((x + 20, y + 124), sub,   font=_font(14),       fill=hex_to_rgb(TEXT_MUT))

    # ── Per-epoch mini table ─────────────────────────────────────────────────
    draw.line((40, 920, W - 40, 920), fill=hex_to_rgb(BORDER), width=1)
    draw.text((40, 932), "EPOCH-BY-EPOCH BREAKDOWN (THIS ROUND)",
              font=_font(16, True), fill=hex_to_rgb(CYAN))

    ep_start_idx = max(0, len(rows) - 5)
    ep_rows = rows[ep_start_idx:]
    col_w   = [100, 155, 155, 155, 155, 155, 155]
    headers = ["Epoch", "mAP@50", "Recall", "Precision", "Box Loss", "Cls Loss", "DFL Loss"]
    hx = 40
    hy = 962
    for ci, (hdr, cw) in enumerate(zip(headers, col_w)):
        draw.text((hx + 8, hy), hdr, font=_font(13, True), fill=hex_to_rgb(CYAN))
        hx += cw

    for ri, row in enumerate(ep_rows):
        ry   = hy + 26 + ri * 26
        bg   = BG_CARD if ri % 2 == 0 else BG_CARD2
        draw.rectangle((40, ry - 2, W - 40, ry + 22), fill=hex_to_rgb(bg))
        ep_num = start_ep + ri
        vals = [
            str(ep_num),
            f"{extract(row, 'metrics/mAP50(B)') * 100:.2f}%",
            f"{extract(row, 'metrics/recall(B)') * 100:.2f}%",
            f"{extract(row, 'metrics/precision(B)') * 100:.2f}%",
            f"{extract(row, 'train/box_loss'):.4f}",
            f"{extract(row, 'train/cls_loss'):.4f}",
            f"{extract(row, 'train/dfl_loss'):.4f}",
        ]
        rx = 40
        for ci, (v, cw) in enumerate(zip(vals, col_w)):
            draw.text((rx + 8, ry), v, font=_font(13), fill=hex_to_rgb(TEXT_PRI))
            rx += cw

    # ── Footer ───────────────────────────────────────────────────────────────
    draw.line((40, 1148, W - 40, 1148), fill=hex_to_rgb(BORDER), width=1)
    draw.text((40, 1158),
              f"Phase 2 · Round {round_num} complete ({end_ep}/30 epochs)  ·  GTX 1050 3 GB  ·  601 Classes",
              font=_font(17, True), fill=hex_to_rgb(TEXT_MUT))
    draw.text((40, 1182),
              "Open Images V6 Object Detection  ·  YOLO11 Nano Optimized",
              font=_font(15), fill=hex_to_rgb(TEXT_MUT))

    im.save(str(out_path), quality=96)
    print(f"  PNG  → {out_path}")


# ── 2. DOCX Report ───────────────────────────────────────────────────────────
def build_docx(round_num, start_ep, end_ep, rows, out_path):
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn
    except ImportError:
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "python-docx"], check=True)
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn

    last    = rows[-1]
    rec     = extract(last, "metrics/recall(B)") * 100
    prec    = extract(last, "metrics/precision(B)") * 100
    map50   = extract(last, "metrics/mAP50(B)") * 100
    map5095 = extract(last, "metrics/mAP50-95(B)") * 100
    box_l   = extract(last, "train/box_loss")
    cls_l   = extract(last, "train/cls_loss")
    dfl_l   = extract(last, "train/dfl_loss")

    NAVY = "17365D"
    PALE = "F5F8FC"
    GRID = "D9D9D9"

    def shade(cell, color):
        p = cell._tc.get_or_add_tcPr()
        e = OxmlElement("w:shd")
        e.set(qn("w:fill"), color)
        p.append(e)

    def style_cell(c, header=False, center=False):
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c._tc.get_or_add_tcPr()
        borders = OxmlElement("w:tcBorders")
        for side in ("top", "left", "bottom", "right"):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), "4")
            e.set(qn("w:color"), GRID)
            borders.append(e)
        p.append(borders)
        for para in c.paragraphs:
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
            para.paragraph_format.space_after = Pt(0)
            for r in para.runs:
                r.font.name = "Aptos"
                r.font.size = Pt(8.5)
                if header:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)
        if header:
            shade(c, NAVY)

    def add_table(doc, hdr, data, widths):
        t = doc.add_table(rows=1, cols=len(hdr))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for i, h in enumerate(hdr):
            c = t.rows[0].cells[i]
            c.width = Inches(widths[i])
            c.text = h
            style_cell(c, True, True)
        for ri, row in enumerate(data):
            cells = t.add_row().cells
            for ci, v in enumerate(row):
                cells[ci].width = Inches(widths[ci])
                cells[ci].text = str(v)
                style_cell(cells[ci], False, ci > 0)
                if ri % 2:
                    shade(cells[ci], PALE)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Inches(0.65)
    sec.left_margin = sec.right_margin = Inches(0.72)

    for n, sz in [("Normal", 10), ("Title", 22), ("Heading 1", 14)]:
        s = doc.styles[n]
        s.font.name = "Aptos"
        s.font.size = Pt(sz)
        s.font.color.rgb = RGBColor(0, 0, 0)

    # Title
    t = doc.add_paragraph(style="Title")
    t.add_run(f"Phase 2 Training Report — Round {round_num} (Epochs {start_ep}–{end_ep})")

    sub = doc.add_paragraph(
        f"Open Images 601 Classes  |  YOLO11 Nano Optimized  |  GTX 1050 (3 GB VRAM)  |  "
        f"{datetime.now().strftime('%B %d, %Y')}")
    sub.paragraph_format.space_after = Pt(14)
    for r in sub.runs:
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(89, 89, 89)

    # Summary paragraph
    p = doc.add_paragraph()
    p.add_run("Summary. ").bold = True
    p.add_run(
        f"Phase 2 Round {round_num} (Epochs {start_ep}–{end_ep}) completed on local edge hardware "
        f"using YOLO11 Nano with optimized training (FP16 mixed precision, cosine LR scheduler, "
        f"mosaic + mixup + copy-paste augmentation). "
        f"Detection recall reached {rec:.2f}%, mAP@50 reached {map50:.2f}%, and classification loss "
        f"reached {cls_l:.4f}. Compared to the Phase 1 baseline (Epoch 10), recall changed by "
        f"{rec - P1_RECALL:+.2f} pts and mAP@50 changed by {map50 - P1_MAP50:+.2f} pts."
    )

    # Run summary table
    doc.add_heading("Round Summary", 1)
    add_table(doc, ["Item", "Value"], [
        ("Status",          f"Round {round_num} complete ({end_ep}/30 total epochs)"),
        ("Model",           "YOLO11 Nano fine-tuned for 601 classes (2.6M parameters)"),
        ("Resumed from",    "Phase 1 best.pt (epoch 10)" if round_num == 1 else f"Round {round_num-1} last.pt"),
        ("Dataset",         "85,000 training images, 15,000 val images (100,000 total)"),
        ("Batch / ImgSz",   "8 images per batch at 640×640 px"),
        ("Precision",       "FP16 (half precision) — enabled"),
        ("LR Scheduler",    "Cosine annealing"),
        ("Augmentation",    "Mosaic 1.0, Mixup 0.1, Copy-Paste 0.1"),
        ("Epochs this run", str(end_ep - start_ep + 1)),
        ("Output folder",   f"runs/detect/phase2/round_{round_num}_epochs_{start_ep}_{end_ep}"),
    ], [2.3, 4.6])

    # Comparison vs Phase 1
    doc.add_heading("Validation Metrics vs Phase 1 Baseline", 1)
    add_table(doc,
        ["Metric", "Phase 1 Baseline (Ep 10)", f"Phase 2 Round {round_num} (Ep {end_ep})", "Change"],
        [
            ("Recall",        f"{P1_RECALL:.2f}%",   f"{rec:.2f}%",    f"{rec - P1_RECALL:+.2f} pts"),
            ("mAP@50",        f"{P1_MAP50:.2f}%",    f"{map50:.2f}%",  f"{map50 - P1_MAP50:+.2f} pts"),
            ("mAP@50-95",     f"{P1_MAP5095:.2f}%",  f"{map5095:.2f}%",f"{map5095 - P1_MAP5095:+.2f} pts"),
            ("Precision",     f"{P1_PREC:.2f}%",     f"{prec:.2f}%",  f"{prec - P1_PREC:+.2f} pts"),
            ("Box Loss",      f"{P1_BOX_LOSS:.4f}",  f"{box_l:.4f}",  f"{box_l - P1_BOX_LOSS:+.4f}"),
            ("Class Loss",    f"{P1_CLS_LOSS:.4f}",  f"{cls_l:.4f}",  f"{cls_l - P1_CLS_LOSS:+.4f}"),
            ("DFL Loss",      f"{P1_DFL_LOSS:.4f}",  f"{dfl_l:.4f}",  f"{dfl_l - P1_DFL_LOSS:+.4f}"),
        ], [1.8, 1.65, 1.95, 1.5])

    # Per-epoch breakdown
    doc.add_heading(f"Epoch-by-Epoch Breakdown (Round {round_num})", 1)
    ep_rows_data = []
    for i, row in enumerate(rows):
        ep_num = start_ep + i
        ep_rows_data.append((
            str(ep_num),
            f"{extract(row, 'metrics/mAP50(B)') * 100:.2f}%",
            f"{extract(row, 'metrics/recall(B)') * 100:.2f}%",
            f"{extract(row, 'metrics/precision(B)') * 100:.2f}%",
            f"{extract(row, 'train/box_loss'):.4f}",
            f"{extract(row, 'train/cls_loss'):.4f}",
            f"{extract(row, 'train/dfl_loss'):.4f}",
        ))
    add_table(doc,
        ["Epoch", "mAP@50", "Recall", "Precision", "Box Loss", "Cls Loss", "DFL Loss"],
        ep_rows_data,
        [0.55, 0.75, 0.75, 0.9, 0.75, 0.75, 0.75])

    # Checkpoints
    doc.add_heading("Saved Checkpoints", 1)
    run_name = f"round_{round_num}_epochs_{start_ep}_{end_ep}"
    add_table(doc, ["File", "Description", "Path"], [
        ("best.pt", "Best checkpoint by mAP@50 in this round", f"runs/detect/phase2/{run_name}/weights/best.pt"),
        ("last.pt", "Final checkpoint (use as next round's start)", f"runs/detect/phase2/{run_name}/weights/last.pt"),
    ], [0.8, 2.3, 3.8])

    # Footer
    foot = sec.footer.paragraphs[0]
    foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = foot.add_run(f"Phase 2 Round {round_num} Report (Epochs {start_ep}–{end_ep})  |  Open Images 601 Class Object Detection")
    fr.font.size = Pt(8)
    fr.font.color.rgb = RGBColor(100, 100, 100)

    doc.core_properties.title = f"Phase 2 Round {round_num} Training Report"
    doc.core_properties.author = "Abdul Rahman K. Saeed"
    doc.save(str(out_path))
    print(f"  DOCX → {out_path}")


# ── 3. LinkedIn Post ─────────────────────────────────────────────────────────
def build_post(round_num, start_ep, end_ep, rows, out_path):
    last    = rows[-1]
    rec     = extract(last, "metrics/recall(B)") * 100
    prec    = extract(last, "metrics/precision(B)") * 100
    map50   = extract(last, "metrics/mAP50(B)") * 100
    map5095 = extract(last, "metrics/mAP50-95(B)") * 100
    box_l   = extract(last, "train/box_loss")
    cls_l   = extract(last, "train/cls_loss")

    d_rec  = rec   - P1_RECALL
    d_map  = map50 - P1_MAP50
    sign   = lambda v: f"+{v:.2f}" if v >= 0 else f"{v:.2f}"

    next_round = round_num + 1
    next_start = end_ep + 1
    next_end   = end_ep + 5

    content = f"""# LinkedIn Post — Phase 2, Round {round_num} (Epochs {start_ep}–{end_ep})

Round {round_num} of Phase 2 is complete! 🎯

Continuing my **601-class object detection journey** with YOLO11 Nano, now with advanced training optimizations on the same edge hardware I started with.

## What changed in Phase 2?

After 10 baseline epochs in Phase 1, I didn't switch to a bigger cloud GPU. Instead, I pushed the same **GTX 1050 (3 GB VRAM)** further with smarter training:

- ⚡ **FP16 Mixed Precision** — halved VRAM usage, more room to train
- 📉 **Cosine LR Scheduler** — smooth convergence instead of linear decay
- 🔀 **Mosaic + Mixup + Copy-Paste Augmentation** — richer training signal per batch

## Round {round_num} Results (Epochs {start_ep}–{end_ep}):

| Metric | Phase 1 Baseline | Round {round_num} | Change |
|--------|-----------------|---------|--------|
| mAP@50 | {P1_MAP50:.2f}% | **{map50:.2f}%** | {sign(d_map)} pts |
| Recall | {P1_RECALL:.2f}% | **{rec:.2f}%** | {sign(d_rec)} pts |
| mAP@50-95 | {P1_MAP5095:.2f}% | **{map5095:.2f}%** | {sign(map5095 - P1_MAP5095)} pts |
| Precision | {P1_PREC:.2f}% | **{prec:.2f}%** | {sign(prec - P1_PREC)} pts |
| Class Loss | {P1_CLS_LOSS:.4f} | **{cls_l:.4f}** | {cls_l - P1_CLS_LOSS:+.4f} |
| Box Loss | {P1_BOX_LOSS:.4f} | **{box_l:.4f}** | {box_l - P1_BOX_LOSS:+.4f} |

Training on **100,000 images per round** across all 601 Open Images V6 categories.
{f"Round {next_round} next — Epochs {next_start}–{next_end}!" if round_num < 4 else "Phase 2 training complete — 30 total epochs achieved!"}

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #AI #OpenImages #EdgeAI #MachineLearning #PyTorch

---

## Short Caption

phase 2 round {round_num} complete! epochs {start_ep}–{end_ep} done on a 3gb gtx 1050 with fp16 + cosine lr + mosaic augmentation. recall: {rec:.2f}% (phase 1: {P1_RECALL}%), map50: {map50:.2f}% (phase 1: {P1_MAP50}%), across 601 classes on 100k images. {"onto round " + str(next_round) + "!" if round_num < 4 else "phase 2 complete!"}
"""
    out_path.write_text(content, encoding="utf-8")
    print(f"  MD   → {out_path}")


# ── 4. Journal Entry ─────────────────────────────────────────────────────────
def append_journal(round_num, start_ep, end_ep, rows, journal_path):
    last    = rows[-1]
    rec     = extract(last, "metrics/recall(B)") * 100
    prec    = extract(last, "metrics/precision(B)") * 100
    map50   = extract(last, "metrics/mAP50(B)") * 100
    map5095 = extract(last, "metrics/mAP50-95(B)") * 100
    box_l   = extract(last, "train/box_loss")
    cls_l   = extract(last, "train/cls_loss")
    dfl_l   = extract(last, "train/dfl_loss")

    entry = f"""

---

## Phase 2 — Round {round_num} (Epochs {start_ep}–{end_ep}) · {datetime.now().strftime('%B %d, %Y')}

**Status:** Complete  
**Hardware:** NVIDIA GTX 1050 (3 GB VRAM) — local training  
**Technique:** FP16 · Cosine LR · Mosaic 1.0 · Mixup 0.1 · Copy-Paste 0.1  
**Checkpoint in:** {"Phase 1 best.pt (epoch_10)" if round_num == 1 else f"Round {round_num-1} last.pt"}  

### Round {round_num} Final Metrics

| Metric | Phase 1 Baseline (Ep 10) | Round {round_num} (Ep {end_ep}) | Change |
|--------|--------------------------|--------------------------------|--------|
| Recall | {P1_RECALL:.2f}% | **{rec:.2f}%** | {rec - P1_RECALL:+.2f} pts |
| mAP@50 | {P1_MAP50:.2f}% | **{map50:.2f}%** | {map50 - P1_MAP50:+.2f} pts |
| mAP@50-95 | {P1_MAP5095:.2f}% | **{map5095:.2f}%** | {map5095 - P1_MAP5095:+.2f} pts |
| Precision | {P1_PREC:.2f}% | **{prec:.2f}%** | {prec - P1_PREC:+.2f} pts |
| Box Loss | {P1_BOX_LOSS:.4f} | **{box_l:.4f}** | {box_l - P1_BOX_LOSS:+.4f} |
| Class Loss | {P1_CLS_LOSS:.4f} | **{cls_l:.4f}** | {cls_l - P1_CLS_LOSS:+.4f} |
| DFL Loss | {P1_DFL_LOSS:.4f} | **{dfl_l:.4f}** | {dfl_l - P1_DFL_LOSS:+.4f} |

### Epoch Progression

| Epoch | mAP@50 | Recall | Box Loss | Cls Loss |
|-------|--------|--------|----------|----------|
"""
    for i, row in enumerate(rows):
        ep  = start_ep + i
        m50 = extract(row, "metrics/mAP50(B)") * 100
        rcl = extract(row, "metrics/recall(B)") * 100
        bl  = extract(row, "train/box_loss")
        cl  = extract(row, "train/cls_loss")
        entry += f"| {ep} | {m50:.2f}% | {rcl:.2f}% | {bl:.4f} | {cl:.4f} |\n"

    run_name = f"round_{round_num}_epochs_{start_ep}_{end_ep}"
    entry += f"\nArtifacts saved to `Phase 2/Reports/` and `Phase 2/Posts/`.  \n"
    entry += f"Weights: `runs/detect/phase2/{run_name}/weights/`\n"

    with open(journal_path, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"  JRNL → {journal_path}")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Phase 2 Round Artifact Generator")
    parser.add_argument("--round",       type=int, required=True,  help="Round number (1–4)")
    parser.add_argument("--start_epoch", type=int, required=True,  help="First epoch of round (e.g. 11)")
    parser.add_argument("--end_epoch",   type=int, required=True,  help="Last epoch of round (e.g. 15)")
    parser.add_argument("--results_csv", type=str, required=True,  help="Path to results.csv")
    parser.add_argument("--output_dir",  type=str,
                        default=r"C:\Users\HP\Desktop\CV Project\Phase 2",
                        help="Phase 2 base directory")
    args = parser.parse_args()

    out      = Path(args.output_dir)
    reports  = out / "Reports";       reports.mkdir(parents=True, exist_ok=True)
    posts    = out / "Posts";         posts.mkdir(parents=True, exist_ok=True)
    docs     = out / "Documentation"; docs.mkdir(parents=True, exist_ok=True)

    csv_path = Path(args.results_csv)
    if not csv_path.exists():
        print(f"ERROR: results.csv not found at {csv_path}")
        sys.exit(1)

    rows = parse_csv(csv_path)
    # Slice to only the epochs in this round (last N rows where N = end-start+1)
    n_epochs = args.end_epoch - args.start_epoch + 1
    rows = rows[-n_epochs:]

    r  = args.round
    s  = args.start_epoch
    e  = args.end_epoch

    print(f"\nGenerating Phase 2 Round {r} artifacts (Epochs {s}–{e})...")

    build_png(r, s, e, rows,
              posts / f"Phase_2_Round_{r}_Epochs_{s}_{e}_Training_Results.png")

    build_docx(r, s, e, rows,
               reports / f"Phase_2_Round_{r}_Epochs_{s}_{e}_Training_Report.docx")

    build_post(r, s, e, rows,
               posts / f"Phase_2_Round_{r}_Epochs_{s}_{e}_LinkedIn_Post.md")

    append_journal(r, s, e, rows,
                   docs / "PROJECT_JOURNAL_PHASE_2.md")

    print(f"\nDone! All Round {r} artifacts saved to:")
    print(f"  {reports}")
    print(f"  {posts}")
    print(f"  {docs}\n")


if __name__ == "__main__":
    main()
