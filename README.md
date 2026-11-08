# Open Images 601-Class Object Detection (YOLO11 Nano)

A deep learning project fine-tuning **YOLO11 Nano (`yolo11n`)** for 601-class object detection on an Open Images V6 subset (100,000 images total), optimized for edge hardware (NVIDIA GeForce GTX 1050 with 3 GB VRAM).

---

## 📊 Current Training Status (Epoch 6 / 10)

- **Completed Epochs:** 6 of 10 (Second half underway)
- **Total Images Processed per Epoch:** 85,000 training images + 15,000 validation images (100,000 images)
- **Bounding Boxes Evaluated:** 286,954 instances across 601 categories
- **Cumulative Training Time:** ~9 hours 17 minutes (average ~1.55 hours per epoch)

### 📈 Metrics Progression

| Metric | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Epoch 6 | Trend |
|---|---:|---:|---:|---:|---:|---:|:---:|
| **mAP@50 (50% IoU)** | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | **11.22%** | 🚀 **+113.7% Gain** |
| **Recall (objects found)** | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | **15.62%** | 🚀 **+143.3% Gain** |
| **mAP@50–95 (strict average)** | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | **7.29%** | 🚀 **+116.3% Gain** |
| **Precision** | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | **36.43%** | ⚖️ Stabilizing (-1.7 pts) |
| **Box Loss** | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | **1.4267** | 📉 Improved |
| **Classification Loss** | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | **2.0591** | 📉 Down ~1.25 pts total |
| **DFL Loss** | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | **1.4564** | 📉 Improved |

---

## 🛠️ Hardware & Environment

- **GPU:** NVIDIA GeForce GTX 1050 (3 GB VRAM, Notebook)
- **Framework:** PyTorch 2.6.0 with CUDA 12.4
- **Detection Library:** Ultralytics YOLO 8.4.183
- **Batch Size:** 8 images per batch at 640×640 image size

---

## 📁 Repository Structure

```
├── .gitignore                           # Excludes heavy datasets and temporary caches
├── README.md                            # Project overview & progress
├── data/
│   └── yolo_dataset/
│       ├── dataset.yaml                 # 601-class configuration & splits
│       ├── class_mapping.json           # Class ID to name mappings
│       └── dataset_summary.json         # Dataset distribution statistics
├── Epoch Reports/                       # Formal .docx technical reports for each epoch
│   ├── Epoch_1_Training_Report.docx
│   ├── Epoch_2_Training_Report.docx
│   ├── Epoch_3_Training_Report.docx
│   ├── Epoch_4_Training_Report.docx
│   ├── Epoch_5_Training_Report.docx
│   └── Epoch_6_Training_Report.docx
├── Epoch Posts/                         # Visual graphics & LinkedIn posts for each epoch
│   ├── Epoch_1_Training_Results.png
│   ├── Epoch_2_Training_Results.png
│   ├── Epoch_3_Training_Results.png
│   ├── Epoch_4_Training_Results.png
│   ├── Epoch_5_Training_Results.png
│   └── Epoch_6_Training_Results.png
├── Project Documentation/
│   └── PROJECT_JOURNAL.md               # Cumulative experiment log and technical journal
├── Training Logs/                       # Full raw terminal output per epoch
│   ├── Epoch_1_Training_Log.txt
│   ├── Epoch_2_Retry_Training_Log.txt
│   ├── Epoch_3_Training_Log.txt
│   ├── Epoch_4_Training_Log.txt
│   ├── Epoch_5_Training_Log.txt
│   └── Epoch_6_Training_Log.txt
├── scripts/
│   ├── train_detector.py                # Main YOLO training pipeline script
│   └── evaluate_model.py                # Model evaluation utilities
└── runs/detect/runs/detect/             # Checkpoints (best.pt/last.pt), evaluation plots & metrics CSVs
```

---

## 🚀 Running Training Epoch-by-Epoch

To train the next epoch continuing from the latest saved model weights:

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py `
  --model "runs\detect\runs\detect\epoch_6\weights\last.pt" `
  --epochs 1 `
  --batch 8 `
  --imgsz 640 `
  --name epoch_7 2>&1 | Tee-Object -FilePath "Training Logs\Epoch_7_Training_Log.txt"
```

---

## 👤 Author

- **Abdul Rahman K. Saeed**
