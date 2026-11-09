# Open Images 601-Class Object Detection (YOLO11 Nano)

A deep learning project fine-tuning **YOLO11 Nano (`yolo11n`)** for 601-class object detection on an Open Images V6 subset (100,000 images per epoch), optimized for edge hardware (NVIDIA GeForce GTX 1050 with 3 GB VRAM).

---

## Current Training Status (Phase 1 Complete - 10 / 10 Epochs Finished)

- **Completed Epochs:** 10 of 10 (Phase 1 Edge Training Curriculum Complete!)
- **Total Images Processed:** 1,000,000 images (85,000 train + 15,000 val per epoch)
- **Total Training Batches:** 106,250 batches
- **Bounding Boxes Evaluated:** 286,954 instances across 601 categories per epoch
- **Cumulative Training Time:** ~15 hours 27 minutes (15.455 hours total)

### Metrics Progression (Complete 10-Epoch Curriculum)

| Metric | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Epoch 6 | Epoch 7 | Epoch 8 | Epoch 9 | Epoch 10 | Total Gain |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|
| **mAP@50 (50% IoU)** | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | 11.82% | 12.35% | 12.84% | **13.18%** | **+151.0% Gain** |
| **Recall (objects found)** | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | 16.37% | 17.31% | 18.15% | **19.05%** | **+196.7% Gain (nearly 3x!)** |
| **mAP@50-95 (strict average)** | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | 7.29% | 7.64% | 7.99% | 8.28% | **8.52%** | **+152.8% Gain** |
| **Precision** | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | 36.43% | 35.00% | 34.28% | 30.82% | **29.24%** | Expected Trade-off |
| **Box Loss** | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | 1.4267 | 1.4144 | 1.4035 | 1.3935 | **1.3847** | Sub-1.39 Milestone |
| **Classification Loss** | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | 2.0087 | 1.9660 | 1.9282 | **1.8941** | **Sub-1.90 Milestone (-1.41 pts)** |
| **DFL Loss** | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | 1.4564 | 1.4469 | 1.4385 | 1.4310 | **1.4244** | Consistent Convergence |

---

## Hardware & Environment

- **GPU:** NVIDIA GeForce GTX 1050 (3 GB VRAM, Notebook)
- **Framework:** PyTorch 2.6.0 with CUDA 12.4
- **Detection Library:** Ultralytics YOLO 8.4.183
- **Batch Size:** 8 images per batch at 640x640 image size
- **Parameters:** 2,807,403 (~2.6M backbone & head parameters)

---

## Repository Structure

```
.gitignore                           # Excludes heavy datasets and temporary caches
README.md                            # Project overview & progress
data/
    yolo_dataset/
        dataset.yaml                 # 601-class configuration & splits
        class_mapping.json           # Class ID to name mappings
        dataset_summary.json         # Dataset distribution statistics
Epoch Reports/                       # Formal .docx technical reports for each epoch
    Epoch_1_Training_Report.docx
    Epoch_2_Training_Report.docx
    Epoch_3_Training_Report.docx
    Epoch_4_Training_Report.docx
    Epoch_5_Training_Report.docx
    Epoch_6_Training_Report.docx
    Epoch_7_Training_Report.docx
    Epoch_8_Training_Report.docx
    Epoch_9_Training_Report.docx
    Epoch_10_Training_Report.docx
Epoch Posts/                         # Visual graphics & LinkedIn posts for each epoch
    Epoch_1_Training_Results.png
    Epoch_2_Training_Results.png
    Epoch_3_Training_Results.png
    Epoch_4_Training_Results.png
    Epoch_5_Training_Results.png
    Epoch_6_Training_Results.png
    Epoch_7_Training_Results.png
    Epoch_8_Training_Results.png
    Epoch_9_Training_Results.png
    Epoch_10_Training_Results.png
    Epoch_1_LinkedIn_Post.md
    Epoch_2_LinkedIn_Post.md
    Epoch_3_LinkedIn_Post.md
    Epoch_4_LinkedIn_Post.md
    Epoch_5_LinkedIn_Post.md
    Epoch_6_LinkedIn_Post.md
    Epoch_7_LinkedIn_Post.md
    Epoch_8_LinkedIn_Post.md
    Epoch_9_LinkedIn_Post.md
    Epoch_10_LinkedIn_Post.md
Project Documentation/
    PROJECT_JOURNAL.md               # Cumulative experiment log and technical journal
Training Logs/                       # Full raw terminal output per epoch
    Epoch_1_Training_Log.txt
    Epoch_2_Retry_Training_Log.txt
    Epoch_3_Training_Log.txt
    Epoch_4_Training_Log.txt
    Epoch_5_Training_Log.txt
    Epoch_6_Training_Log.txt
    Epoch_7_Training_Log.txt
    Epoch_8_Training_Log.txt
    Epoch_9_Training_Log.txt
    Epoch_10_Training_Log.txt
scripts/
    train_detector.py                # Main YOLO training pipeline script
    evaluate_model.py                # Model evaluation utilities
runs/detect/runs/detect/             # Checkpoints (best.pt/last.pt), evaluation plots & metrics CSVs
```

---

## Phase 2 Roadmap: Cloud Scale-Up

With Phase 1 edge baseline training completed on the GTX 1050 (3 GB VRAM):
- **Target Compute:** Google Colab / Cloud GPU (NVIDIA T4 / A100)
- **Model Upgrade:** Scale up to `yolo11m` (Medium) or `yolo11x` (Extra-Large)
- **Batch & Resolution Scaling:** Increase batch size to 32/64 and explore multi-scale image resolution (800–1024px)
- **Transfer Weights:** Fine-tuning from the trained Phase 1 weights or re-training higher-capacity backbones

---

## Author

- **Abdul Rahman K. Saeed**
