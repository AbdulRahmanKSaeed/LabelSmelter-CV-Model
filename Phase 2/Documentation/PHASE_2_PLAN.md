# Phase 2 Plan: Cloud Scale-Up with High-Capacity YOLO11 on Google Colab

**Project:** Open Images V6 (601-Class) Object Detection  
**Author:** Abdul Rahman K. Saeed  
**Date:** November 2026  
**Status:** In Preparation (Transitioning from Phase 1 Edge Baseline)  

---

## 1. Executive Summary & Why Phase 2

In Phase 1, we successfully completed a 10-epoch fine-tuning curriculum using **YOLO11 Nano (`yolo11n`)** on local edge hardware (NVIDIA GeForce GTX 1050 with 3 GB VRAM). 

### Key Lessons from Phase 1:
- The end-to-end pipeline was 100% verified (data ingestion, label mapping, loss convergence from 3.30 down to 1.89, weights management).
- However, **YOLO Nano (2.8M parameters)** across **601 classes** reached its physical capacity ceiling:
  - Bounding boxes were loose on complex scenes.
  - Distant and partially occluded objects (such as cars in street parking) received low confidence scores (0.01 – 0.09) due to feature downsampling and parameter dilution across 601 competing heads.
  - 10 epochs is only the initial discovery phase for a 601-class problem.

**Phase 2 Goal:** Scale up to **YOLO11 Medium (`yolo11m`)** or **Large (`yolo11l`)** using cloud GPUs (NVIDIA T4 with 16 GB VRAM or A100 with 40 GB VRAM) on Google Colab, targeting 30 to 50 epochs of training with high confidence, tight bounding boxes, and comprehensive object detection.

---

## 2. Hardware & Model Comparison

| Feature | Phase 1 (Local Edge Baseline) | Phase 2 (Google Colab Scale-Up) | Impact on Performance |
|---|---|---|---|
| **Hardware** | NVIDIA GTX 1050 (3 GB VRAM) | NVIDIA T4 / A100 (16 GB - 40 GB VRAM) | 5× to 13× more memory headroom |
| **Model** | YOLO11 Nano (`yolo11n`) | **YOLO11 Medium (`yolo11m`)** | **7.5× more parameters (20.1M vs 2.8M)** |
| **Batch Size** | 8 | **32 to 64** | Much more stable gradient updates |
| **Input Resolution** | 640 × 640 | **800 × 800** | Small & distant objects remain crisp |
| **Target Epochs** | 10 epochs (completed) | **30 to 50 epochs** | Deep convergence and high confidence |
| **Confidence Output** | Low (0.05 – 0.20 on hard objects) | **High (0.60 – 0.90+)** | Crisp, tight detections without false negatives |

---

## 3. Project Directory Architecture for Phase 2

To maintain clean separation between Phase 1 and Phase 2, all new documentation, reports, and graphics are housed under the dedicated `Phase 2/` directory:

```
CV Project/
├── Epoch Reports/                     # Phase 1 Technical Reports (Epochs 1-10)
├── Epoch Posts/                       # Phase 1 LinkedIn Posts & PNGs (Epochs 1-10)
├── Project Documentation/             # Phase 1 Journal & Docs
├── Phase 2/
│   ├── Documentation/
│   │   ├── PHASE_2_PLAN.md            # Architecture & strategy blueprint (this file)
│   │   └── PROJECT_JOURNAL_PHASE_2.md # Running log for Phase 2 cloud training
│   ├── Reports/                       # Formal .docx technical reports for Phase 2
│   ├── Posts/                         # 1200x1200 graphics & LinkedIn copy for Phase 2
│   └── Colab/
│       ├── Phase_2_YOLO11_Training.ipynb # Ready-to-run Google Colab Notebook
│       ├── labels.zip                 # Pre-compressed 601-class annotations
│       └── colab_train.py             # Headless cloud training script
```

---

## 4. Operational Execution Steps for Colab

### Step 1: Set Up Persistent Storage (Google Drive)
All checkpoints (`best.pt`, `last.pt`) and evaluation outputs will be written directly to a designated Google Drive folder (`/content/drive/MyDrive/CV_Project_Phase2`), ensuring that even if a Colab session disconnects, no progress is ever lost.

### Step 2: Dataset Loading in Colab
Because Colab instances possess ultra-high-speed network connectivity (500–1000 Mbps):
- Unzip the lightweight pre-generated labels archive (`labels.zip`, ~40 MB).
- Stream or batch-download images via the multithreaded downloader script, or mount an image zip from Drive.

### Step 3: Training Launch
Launch training with YOLO11 Medium:
```python
from ultralytics import YOLO

model = YOLO("yolo11m.pt")
model.train(
    data="dataset.yaml",
    epochs=30,
    batch=32,
    imgsz=640,
    device=0,
    project="/content/drive/MyDrive/CV_Project_Phase2/runs",
    name="yolo11m_601class",
    save=True,
    save_period=1
)
```

### Step 4: Tracking & Reporting
For each completed milestone in Colab, sync metrics down to update:
1. `Phase 2/Reports/` (.docx technical reports)
2. `Phase 2/Posts/` (1200×1200 graphics and LinkedIn posts)
3. `Phase 2/Documentation/PROJECT_JOURNAL_PHASE_2.md`
