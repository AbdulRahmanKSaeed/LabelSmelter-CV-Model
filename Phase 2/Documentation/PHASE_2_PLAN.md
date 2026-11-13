# Phase 2 Plan: Optimized Local Training with YOLO11 Nano

**Project:** Open Images V6 (601-Class) Object Detection  
**Author:** Abdul Rahman K. Saeed  
**Date:** November 2026  
**Status:** Active — Round-Based Local Training  

---

## 1. Executive Summary & Why Phase 2

In Phase 1, we completed a 10-epoch fine-tuning curriculum using **YOLO11 Nano (`yolo11n`)** on local edge hardware (NVIDIA GeForce GTX 1050 with 3 GB VRAM). The model achieved:
- **Recall:** 19.05% (detecting 54,650+ objects across 601 classes)
- **mAP@50:** 13.18% (+151% relative gain over Epoch 1)
- **Classification Loss:** 1.8941 (sub-1.90 milestone)
- **Unbroken convergence** across all 10 epochs

**Phase 2 Goal:** Continue training the same YOLO11 Nano architecture locally with **advanced training optimizations** to push accuracy significantly higher without requiring more powerful hardware:
- **FP16 Mixed Precision** — halves VRAM usage, enables more headroom
- **Cosine Learning Rate Scheduler** — smoother convergence in later epochs
- **Mosaic + Mixup + Copy-Paste Augmentation** — richer training signal per batch
- **20 more epochs** (4 rounds × 5 epochs), targeting mAP@50 25–35%+

---

## 2. Training Configuration

| Feature | Phase 1 (Baseline) | Phase 2 (Optimized) | Benefit |
|---|---|---|---|
| **Hardware** | GTX 1050 (3 GB VRAM) | GTX 1050 (3 GB VRAM) | Same edge hardware |
| **Model** | YOLO11 Nano (2.6M params) | YOLO11 Nano (2.6M params) | Resume from Phase 1 best |
| **Batch Size** | 8 | 8 | Fits in 3 GB with FP16 |
| **Precision** | FP32 | **FP16 (half precision)** | ~40% VRAM savings |
| **LR Scheduler** | Linear | **Cosine annealing** | Better late-stage convergence |
| **Augmentation** | Default | **Mosaic 1.0 + Mixup 0.1 + Copy-paste 0.1** | Richer gradients per batch |
| **Target Epochs** | 10 (done) | **+20 more (30 total)** | Deep convergence |
| **Round Structure** | 1 epoch per run | **5 epochs per round** | Efficient batching |
| **Checkpoint** | Every epoch | **Every 5 epochs** | Clean round boundaries |

---

## 3. Round Schedule

| Round | Epochs | Starting Checkpoint | Expected Duration |
|---|---|---|---|
| Round 1 | 11–15 | Phase 1 best.pt (epoch 10) | ~7.5 hours |
| Round 2 | 16–20 | Round 1 last.pt | ~7.5 hours |
| Round 3 | 21–25 | Round 2 last.pt | ~7.5 hours |
| Round 4 | 26–30 | Round 3 last.pt | ~7.5 hours |

---

## 4. Directory Structure

```
CV Project/
├── Epoch Reports/                     # Phase 1 Reports (Epochs 1-10)
├── Epoch Posts/                       # Phase 1 LinkedIn Posts (Epochs 1-10)
├── Project Documentation/             # Phase 1 Journal & Docs
├── Phase 2/
│   ├── Documentation/
│   │   ├── PHASE_2_PLAN.md            # This file
│   │   └── PROJECT_JOURNAL_PHASE_2.md # Running log for Phase 2
│   ├── Reports/                       # DOCX reports per round
│   └── Posts/                         # 1200x1200 PNGs & LinkedIn posts per round
├── runs/detect/phase2/
│   └── nano_optimized/                # Training outputs, weights, results.csv
└── scripts/
    ├── train_phase2_local.py          # Round-based training script
    └── generate_phase2_round_artifacts.py  # Artifact generator
```

---

## 5. Execution

### Start a round:
```powershell
cd "C:\Users\HP\Desktop\CV Project"
.venv_cuda\Scripts\python.exe scripts\train_phase2_local.py --round 1
```

### Generate artifacts after a round:
```powershell
.venv_cuda\Scripts\python.exe scripts\generate_phase2_round_artifacts.py --round 1 --start_epoch 11 --end_epoch 15 --results_csv "runs/detect/phase2/nano_optimized/results.csv"
```

### Resume if interrupted:
```powershell
.venv_cuda\Scripts\python.exe scripts\train_phase2_local.py --round 1 --resume
```
