# Project Journal: Phase 2 (Cloud Scale-Up on Google Colab)

**Project:** Open Images V6 (601-Class) Object Detection  
**Author:** Abdul Rahman K. Saeed  
**Architecture:** YOLO11 Medium (`yolo11m`) & YOLO11 Large (`yolo11l`)  
**Hardware:** Google Colab Cloud GPU (NVIDIA Tesla T4 16GB / A100 40GB)  
**Baseline Reference:** Phase 1 Edge Model (YOLO11 Nano, 10 Epochs, Recall 19.05%, mAP@50 13.18%)  

---

## Phase 2 Objectives & Milestones

| Target | Phase 1 Baseline (YOLO11n, Edge) | Phase 2 Goal (YOLO11m, Cloud) |
|---|---:|---:|
| Model Parameters | 2.8M (Nano) | **20.1M (Medium)** |
| GPU VRAM | 3 GB (GTX 1050) | **16 GB to 40 GB (Colab T4/A100)** |
| Training Batch Size | 8 | **32 to 64** |
| Target Training Epochs | 10 epochs (Done) | **30 to 50 epochs** |
| Target Recall | 19.05% | **55% - 75%+** |
| Target mAP@50 | 13.18% | **45% - 60%+** |
| Bounding Box Tightness | Loose (Box loss 1.385) | **Sharp / High Precision (Box loss < 1.0)** |
| Car / Object Detection Confidence | 0.02 – 0.09 (Uncertain) | **0.65 – 0.90+ (High Confidence)** |

---

## Phase 2 Training Log

*(Entries will be added as each milestone/epoch block completes on Google Colab)*

### Preparation & Setup (November 11, 2026)
- Created dedicated Phase 2 workspace structure (`Documentation/`, `Reports/`, `Posts/`, `Colab/`).
- Built Google Colab standalone notebook: `Phase 2/Colab/Phase_2_YOLO11_Colab_Training.ipynb`.
- Formulated data ingestion strategy for cloud instances: packaged annotations and direct S3 cloud streaming.
- Selected `yolo11m` (20.1M parameters) as primary scale-up candidate for 601-class generalization.
