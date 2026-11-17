# Open Images 601-Class Object Detection (YOLO11 Nano)

A deep learning project fine-tuning **YOLO11 Nano (`yolo11n`)** for comprehensive 601-class object detection on an Open Images V6 dataset (100,000 images per epoch), fully trained and evaluated on edge consumer hardware (**NVIDIA GeForce GTX 1050 with 3 GB VRAM**).

The project successfully executed an end-to-end **30-Epoch Curriculum** across two major phases:
1. **Phase 1 (Epochs 1–10):** Feasibility & baseline establishment on edge hardware.
2. **Phase 2 (Epochs 11–30):** Advanced optimization using FP16 mixed precision, Cosine LR scheduling, Mosaic/Mixup/Copy-Paste augmentation, and dynamic mosaic shutoff.

---

## 🚀 Executive Project Summary (30 / 30 Epochs Complete)

- **Total Images Processed:** **3,000,000 image passes** (85,000 train + 15,000 val per epoch across 30 epochs)
- **Total Training Batches:** **318,750 batches**
- **Categories:** **601 distinct classes** from Open Images V6
- **Cumulative Training Time:** **~45 hours** of edge GPU computation
- **Final Model Size:** **5.51 MB** (`best.pt` / `last.pt` — 2.6M parameters)
- **Real-Time Inference Speed:** **11.7 ms per image** (~85 FPS) on a laptop GTX 1050

---

## 📊 Milestone Progression: Phase 1 vs. Phase 2

| Metric | Phase 1 Baseline (Ep 10) | Phase 2 Round 1 (Ep 15) | Phase 2 Round 2 (Ep 20) | Phase 2 Round 3 (Ep 25) | **Phase 2 Round 4 (Ep 30 - Final)** | Total Project Gain (vs Ep 1) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **mAP@50 (50% IoU)** | 13.18% | 15.53% | 16.75% | 17.78% | **18.47%** | **+251.8% Gain** (5.25% → 18.47%) |
| **Recall (objects found)** | 19.05% | 21.44% | 22.47% | 23.47% | **23.94%** | **+272.9% Gain** (6.42% → 23.94%) |
| **Precision** | 29.24% | 32.43% | 33.40% | 34.15% | **35.13%** | Balanced high-confidence convergence |
| **mAP@50-95 (strict)** | 8.52% | 10.16% | 11.02% | 11.72% | **12.16%** | **+260.8% Gain** (3.37% → 12.16%) |
| **Validation Box Loss** | 1.4688 | 1.4363 | 1.4314 | 1.4290 | **1.4248** | Uninterrupted boundary refinement |
| **Validation Class Loss** | 1.9601 | 1.9062 | 1.8798 | 1.8556 | **1.8377** | **New all-time project low (-1.47 pts)** |
| **Validation DFL Loss** | 1.4525 | 1.4264 | 1.4216 | 1.4181 | **1.4157** | Sub-1.42 focal milestone |

---

## 📈 Phase-by-Phase Breakdown

### Phase 2: Advanced Edge Optimization (Epochs 11–30)
In Phase 2, the model was fine-tuned locally in modular 5-epoch rounds using advanced training techniques:
- **FP16 Half-Precision (AMP):** Enabled zero out-of-memory errors on 3 GB VRAM while accelerating tensor throughput.
- **Cosine Annealing Scheduler:** Smoothed learning rate decay in late-stage training for tighter gradient convergence.
- **Richer Augmentations:** Mosaic (1.0), Mixup (0.1), and Copy-Paste (0.1) exposed the detector to complex occlusion and multi-scale combinations.
- **Mosaic Shutoff (Epochs 29–30):** Disabling mosaic in the final 2 epochs allowed the model to fine-tune bounding box regressions on clean, unaugmented scenes, driving final mAP@50 to a peak of **18.47%**.

| Round | Epoch Range | mAP@50 | Recall | Precision | mAP@50-95 | Key Optimization |
|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Round 1** | Ep 11–15 | 15.53% | 21.44% | 32.43% | 10.16% | FP16 + Cosine LR + Augmentation warm-up |
| **Round 2** | Ep 16–20 | 16.75% | 22.47% | 33.40% | 11.02% | Continued adaptation to rich augmentations |
| **Round 3** | Ep 21–25 | 17.78% | 23.47% | 34.15% | 11.72% | Sub-1.86 class loss breakthrough |
| **Round 4** | Ep 26–30 | **18.47%** | **23.94%** | **35.13%** | **12.16%** | Mosaic shutoff in final 2 epochs |

---

### Phase 1: Baseline Edge Feasibility (Epochs 1–10)
Phase 1 established that fine-tuning a 601-class model on constrained 3 GB hardware was viable.

| Metric | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Epoch 6 | Epoch 7 | Epoch 8 | Epoch 9 | Epoch 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **mAP@50** | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | 11.82% | 12.35% | 12.84% | **13.18%** |
| **Recall** | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | 16.37% | 17.31% | 18.15% | **19.05%** |
| **Classification Loss** | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | 2.0087 | 1.9660 | 1.9282 | **1.8941** |

---

## 🔍 Model Inference & Auto-Annotation Suite

The repository includes a standalone inference script (`scripts/test_model.py`) capable of running real-time object detection and auto-generating annotation files.

### 1. Test Inference
```powershell
# Run inference on any image with the final Phase 2 model
python scripts/test_model.py --source "path/to/image.jpg" --conf 0.25
```

### 2. Auto-Annotate in Standard Formats
The model can output detections in two distinct formats:
- **YOLO Label Format (`.txt`):** Generates normalized `<class_id> <x_center> <y_center> <width> <height> <confidence>` format for retraining or uploading to CVAT / Roboflow.
- **Human-Readable JSON (`.json`):** Exports class names, confidence percentages, and bounding box pixel coordinates for APIs and downstream software.

```powershell
# Export both YOLO .txt and structured JSON annotations
python scripts/test_model.py --source 1.jpg --save-txt --save-json
```

**Benchmark Performance on GTX 1050:**
- Preprocessing: 47.8 ms
- **Inference Speed:** **11.7 ms per image (~85 FPS)**
- Postprocessing: 10.0 ms
- Example detection: In complex urban scenes (`1.jpg`), the model accurately localized 12 distinct objects (Cars, Wheels, Tires, Persons, Footwear) with confidence scores reaching **0.60 – 0.65** (up from 0.02 – 0.09 at Phase 1 baseline).

---

## 🛠️ Hardware & Environment

- **GPU:** NVIDIA GeForce GTX 1050 (3 GB VRAM, Notebook)
- **CPU:** Intel Core i5-9300H @ 2.40 GHz (4 Cores / 8 Threads)
- **RAM:** 16 GB DDR4
- **OS:** Windows 10
- **Frameworks:** PyTorch 2.6.0 with CUDA 12.4
- **Detection Architecture:** Ultralytics YOLO11 Nano (`yolo11n`) — 2.6M parameters
- **Batch Size:** 8 images per batch at 640×640 px
- **Precision:** FP16 Automatic Mixed Precision (AMP)

---

## 📁 Repository Structure

```
LabelSmelter-CV-Model/
├── .gitignore                           # Excludes raw images, intermediate checkpoints & caches
├── README.md                            # Comprehensive project overview & documentation
├── data/
│   └── yolo_dataset/
│       ├── dataset.yaml                 # 601-class Open Images V6 YAML configuration
│       ├── class_mapping.json           # Class ID to name mappings
│       └── dataset_summary.json         # Dataset distribution metadata
│
├── Phase 2/                             # Phase 2 Optimized Curriculum (Epochs 11–30)
│   ├── Documentation/
│   │   ├── PHASE_2_PLAN.md              # Technical design and optimization roadmap
│   │   └── PROJECT_JOURNAL_PHASE_2.md   # Round-by-round engineering journal
│   ├── Reports/                         # Formal .docx technical reports (Rounds 1–4)
│   │   ├── Phase_2_Round_1_Epochs_11_15_Training_Report.docx
│   │   ├── Phase_2_Round_2_Epochs_16_20_Training_Report.docx
│   │   ├── Phase_2_Round_3_Epochs_21_25_Training_Report.docx
│   │   └── Phase_2_Round_4_Epochs_26_30_Training_Report.docx
│   └── Posts/                           # High-res 1200x1200 dark premium graphics & LinkedIn posts
│       ├── Phase_2_Round_1_Epochs_11_15_Training_Results.png
│       ├── Phase_2_Round_2_Epochs_16_20_Training_Results.png
│       ├── Phase_2_Round_3_Epochs_21_25_Training_Results.png
│       └── Phase_2_Round_4_Epochs_26_30_Training_Results.png
│
├── Epoch Reports/                       # Phase 1 Technical Reports (Epochs 1–10)
├── Epoch Posts/                         # Phase 1 Visuals & LinkedIn Posts (Epochs 1–10)
├── Project Documentation/               # Phase 1 Project Journal & Architecture Specs
│
├── scripts/
│   ├── train_phase2_local.py            # Phase 2 round-based training automation script
│   ├── generate_phase2_round_artifacts.py # Automated report, graphic & post generator
│   ├── test_model.py                    # Inference & dual-format auto-annotation tool
│   ├── train_detector.py                # Phase 1 baseline training pipeline
│   └── download_manifest_images.py      # Multithreaded S3 dataset downloader
│
└── runs/detect/
    └── phase2/                          # Model checkpoints (best.pt/last.pt), curves & CSVs
        ├── round_1_epochs_11_15/
        ├── round_2_epochs_16_20/
        ├── round_3_epochs_21_25/
        └── round_4_epochs_26_30/
```

---

## 👤 Author

- **Abdul Rahman K. Saeed**  
  [LinkedIn](https://www.linkedin.com) | [GitHub](https://github.com/AbdulRahmanKSaeed)
