# 🎯 CV Project — Status Report

**Date:** October 22, 2026 · 5:00 PM  
**Workspace:** `C:\Users\HP\Desktop\CV Project`

---

## 1. What Has Been Completed

### ✅ Dataset Preparation (100% Done)

| Item | Detail |
|------|--------|
| **Source** | Open Images V6 (official S3 storage) |
| **Total images** | **100,000** JPEGs (85,000 train / 15,000 val) |
| **Total bounding boxes** | **1,925,557** (1,638,599 train / 286,958 val) |
| **Class coverage** | **599 of 601** classes with annotations (2 classes — *Container* and *Kitchenware* — have 0 source boxes) |
| **Format** | YOLO (one `.txt` label file per image, 1:1 alignment verified) |
| **Config** | [`data/yolo_dataset/dataset.yaml`](file:///c:/Users/HP/Desktop/CV%20Project/data/yolo_dataset/dataset.yaml) — `nc: 601`, paths to `images/train` and `images/val` |

**Key files on disk:**

```
data/
├── annotations/           # Raw Open Images CSV annotations
│   ├── train-annotations-bbox.csv (1.13 GB)
│   ├── validation-annotations-bbox.csv
│   └── class-descriptions-boxable.csv (601 classes)
├── manifests/             # Sampling manifests and coverage reports
│   ├── selected_images_manifest.csv
│   ├── class_coverage.csv
│   └── sampling_report.json
└── yolo_dataset/          # Ready-to-train YOLO dataset
    ├── dataset.yaml       # YOLO config file
    ├── class_mapping.json
    ├── images/
    │   ├── train/  (85,000 images)
    │   └── val/    (15,000 images)
    └── labels/
        ├── train/  (85,000 .txt files)
        └── val/    (15,000 .txt files)
```

### ✅ Training Script Created

[`scripts/train_detector.py`](file:///c:/Users/HP/Desktop/CV%20Project/scripts/train_detector.py) — A full-featured training pipeline with:
- Automatic GPU/CPU detection
- VRAM safety clamping for your GTX 1050 (3 GB)
- Disk space monitoring
- Configurable `--fraction` for quick smoke tests
- `--dry-run` mode (tested and passed ✅)

### ✅ Pre-trained Model Weights Downloaded

- [`yolo11n.pt`](file:///c:/Users/HP/Desktop/CV%20Project/yolo11n.pt) (5.4 MB) — YOLO11 Nano, downloaded during dry-run

### 🔄 CUDA GPU Environment (In Progress)

A Python 3.12 virtual environment is being set up at `.venv_cuda/` with CUDA-enabled PyTorch. The `torch` package (2.4 GB) was **still downloading** at the time this report was created. Once it finishes, you'll need to install `ultralytics` into the same venv (see commands below).

---

## 2. Hardware Summary

| Component | Value |
|-----------|-------|
| **CPU** | Intel Core i5-9300H @ 2.40 GHz (4 cores / 8 threads) |
| **RAM** | 16 GB |
| **GPU** | NVIDIA GeForce GTX 1050 (3072 MB VRAM) |
| **NVIDIA Driver** | 582.66 · CUDA 13.0 |
| **Free Disk** | ~35.9 GB (15 GB safety floor) |

---

## 3. Two Training Paths — Choose One

### Option A: Train on GPU (Recommended — Faster)

> [!IMPORTANT]
> This requires the CUDA PyTorch installation in `.venv_cuda` to finish first.

**Estimated speed:** ~15–25 minutes per epoch on 85k images with batch=8, imgsz=640, GTX 1050.

### Option B: Train on CPU (Works Right Now — Very Slow)

The system Python 3.14 already has `ultralytics` + `torch` (CPU) installed.

**Estimated speed:** ~3–6 hours per epoch on 85k images. Not recommended for full training, but fine for a quick smoke test.

---

## 4. Exact PowerShell Commands

Open PowerShell, then `cd` to the project:

```powershell
cd "C:\Users\HP\Desktop\CV Project"
```

### Step 1: Check if the CUDA venv install finished

```powershell
.venv_cuda\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

> If this errors with `ModuleNotFoundError` or shows `CUDA available: False`, the install hasn't finished or failed. In that case, re-run:
> ```powershell
> uv pip install --python .venv_cuda\Scripts\python.exe torch torchvision --index-url https://download.pytorch.org/whl/cu124
> ```

### Step 2: Install Ultralytics into the CUDA venv

```powershell
uv pip install --python .venv_cuda\Scripts\python.exe ultralytics
```

### Step 3: Run a quick smoke test (1% of data, 1 epoch)

```powershell
.venv_cuda\Scripts\python.exe scripts/train_detector.py --epochs 1 --fraction 0.01 --batch 8 --imgsz 640 --name smoke_test
```

> This trains on ~850 images for 1 epoch. Should complete in a few minutes on GPU and confirms everything works end-to-end.

### Step 4: Launch full training (10 epochs, all 85k train images)

```powershell
.venv_cuda\Scripts\python.exe scripts/train_detector.py --epochs 10 --batch 8 --imgsz 640 --name openimages_600_v1
```

> [!TIP]
> If you get a **CUDA out of memory** error, reduce batch size or image size:
> ```powershell
> .venv_cuda\Scripts\python.exe scripts/train_detector.py --epochs 10 --batch 4 --imgsz 416 --name openimages_600_v1
> ```

### Alternative: CPU-only training (no venv needed, but slow)

```powershell
python scripts/train_detector.py --epochs 1 --fraction 0.01 --device cpu --name cpu_smoke_test
```

---

## 5. What to Expect During Training

- **Progress bar** prints each epoch with loss metrics (box loss, cls loss, dfl loss)
- **Checkpoints saved** every epoch to `runs/detect/<name>/weights/`
  - `best.pt` — best validation mAP
  - `last.pt` — latest checkpoint
- **Validation results** printed after each epoch (mAP@50, mAP@50-95)
- **Plots** generated in `runs/detect/<name>/` (confusion matrix, loss curves, PR curves)
- You can **resume** an interrupted run with `--resume`:
  ```powershell
  .venv_cuda\Scripts\python.exe scripts/train_detector.py --resume --name openimages_600_v1
  ```

---

## 6. Summary Checklist

| Step | Status |
|------|--------|
| Download & verify 100k images | ✅ Complete |
| Convert annotations to YOLO format | ✅ Complete |
| Create `dataset.yaml` (601 classes) | ✅ Complete |
| Write training script | ✅ Complete |
| Dry-run validation | ✅ Passed |
| Create Python 3.12 CUDA venv | ✅ Created |
| Install CUDA PyTorch in venv | 🔄 Downloading (2.4 GB `torch`) |
| Install `ultralytics` in CUDA venv | ⬜ Pending (Step 2 above) |
| Smoke test training | ⬜ Pending (Step 3 above) |
| Full training run | ⬜ Pending (Step 4 above) |
