# Project Journal: Phase 2 — Optimized Local Training

**Project:** Open Images V6 (601-Class) Object Detection  
**Author:** Abdul Rahman K. Saeed  
**Architecture:** YOLO11 Nano (`yolo11n`) — Optimized Fine-Tuning  
**Hardware:** NVIDIA GeForce GTX 1050 (3 GB VRAM) — Local Edge Training  
**Phase 1 Baseline Reference:** YOLO11 Nano, 10 Epochs complete

---

## Phase 1 Baseline Summary (Epochs 1–10)

| Metric | Phase 1 Final (Epoch 10) |
|--------|--------------------------|
| Recall | 19.05% |
| Precision | 29.24% |
| mAP@50 | 13.18% |
| mAP@50-95 | 8.52% |
| Box Loss | 1.3847 |
| Classification Loss | 1.8941 |
| DFL Loss | 1.4244 |
| Total Training Time | ~15.5 hours (10 epochs) |

---

## Phase 2 Objectives

| Target | Phase 1 Baseline | Phase 2 Goal |
|--------|-----------------|--------------|
| Total Epochs | 10 (done) | **30 (20 more)** |
| Recall | 19.05% | **30–40%** |
| mAP@50 | 13.18% | **25–35%** |
| Augmentation | Default | **Mosaic + Mixup + Copy-Paste** |
| LR Scheduler | Linear | **Cosine Annealing** |
| Precision Mode | FP32 | **FP16 (half precision)** |

---

## Setup & Strategy (November 12, 2026)

- Transitioned Phase 2 to **local round-based training** (5 epochs per round)
- Created `scripts/train_phase2_local.py` — round-aware training script
- Created `scripts/generate_phase2_round_artifacts.py` — consolidated artifact generator
- Updated `Phase 2/Documentation/PHASE_2_PLAN.md` with local training strategy
- Removed Colab infrastructure (notebook, labels.zip) — no longer needed
- Each round produces: DOCX report, 1200×1200 PNG graphic, LinkedIn post, journal entry

---

*(Round entries will be appended below as each round completes)*


---

## Phase 2 — Round 1 (Epochs 11–15) · November 13, 2026

**Status:** Complete  
**Hardware:** NVIDIA GTX 1050 (3 GB VRAM) — local training  
**Technique:** FP16 · Cosine LR · Mosaic 1.0 · Mixup 0.1 · Copy-Paste 0.1  
**Checkpoint in:** Phase 1 best.pt (epoch_10)  

### Round 1 Final Metrics

| Metric | Phase 1 Baseline (Ep 10) | Round 1 (Ep 15) | Change |
|--------|--------------------------|--------------------------------|--------|
| Recall | 19.05% | **21.44%** | +2.39 pts |
| mAP@50 | 13.18% | **15.53%** | +2.35 pts |
| mAP@50-95 | 8.52% | **10.16%** | +1.64 pts |
| Precision | 29.24% | **32.43%** | +3.19 pts |
| Box Loss | 1.3847 | **1.4428** | +0.0581 |
| Class Loss | 1.8941 | **1.9872** | +0.0931 |
| DFL Loss | 1.4244 | **1.4594** | +0.0350 |

### Epoch Progression

| Epoch | mAP@50 | Recall | Box Loss | Cls Loss |
|-------|--------|--------|----------|----------|
| 11 | 13.27% | 18.18% | 1.5602 | 2.3735 |
| 12 | 13.99% | 19.01% | 1.5219 | 2.2795 |
| 13 | 14.66% | 19.97% | 1.5078 | 2.2405 |
| 14 | 15.28% | 21.07% | 1.4492 | 2.0190 |
| 15 | 15.53% | 21.44% | 1.4428 | 1.9872 |

Artifacts saved to `Phase 2/Reports/` and `Phase 2/Posts/`.  
Weights: `runs/detect/phase2/round_1_epochs_11_15/weights/`
