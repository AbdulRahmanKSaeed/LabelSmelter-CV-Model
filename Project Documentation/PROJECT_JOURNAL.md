# CV Project Journal

## Project purpose

Fine tune YOLO11 Nano for 601 class object detection using a prepared Open Images dataset. This journal records completed epochs, the exact training context, measured results, checkpoints, and the decision for the next epoch.

## Project baseline

| Item | Value |
|---|---|
| Model | YOLO11 Nano `yolo11n.pt` |
| Dataset | Open Images subset in YOLO format |
| Training set | 85,000 images |
| Validation set | 15,000 images |
| Classes | 601 |
| GPU | NVIDIA GeForce GTX 1050 with 3 GB VRAM |
| Default configuration | Batch 8, image size 640, 4 workers |

## Epoch 1

**Status:** Completed successfully  
**Date and start time:** November 4 2026, 9:05 PM  
**Run name:** `epoch_by_epoch`  
**Model:** YOLO11 Nano fine tuned for 601 classes

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --epochs 1 --batch 8 --imgsz 640 --name epoch_by_epoch
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.611 hours (about 1 hour 37 minutes) |
| Peak GPU memory | 3.07 GB |
| Corrupt images | 0 |
| Duplicate labels removed | 43 train, 4 validation |

### Validation metrics

| Metric | Result |
|---|---:|
| Precision | 53.8% |
| Recall | 6.42% |
| mAP at 50 | 5.25% |
| mAP at 50 to 95 | 3.37% |
| Box loss | 1.577 |
| Classification loss | 3.308 |
| DFL loss | 1.586 |

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_by_epoch/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_by_epoch/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_1_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_1_Training_Report.docx`
- LinkedIn graphic: `Epoch Posts/Epoch_1_Training_Results.png`

### Interpretation and next step

The first full epoch completed without a CUDA memory error and validates the end to end training workflow. Low recall and mAP are expected at this early stage for a 601 class detector. Continue through Epoch 2 and compare the direction of mAP, recall, losses, runtime, memory usage, and disk space before drawing conclusions about final model quality.

## Epoch 2

**Status:** Completed successfully  
**Date:** November 5 2026  
**Run folder:** `runs/detect/runs/detect/epoch_by_epoch-3`

### Results and losses compared with Epoch 1

| Measure | Epoch 1 | Epoch 2 | Change |
|---|---:|---:|---:|
| Precision | 53.78% | 51.17% | -2.61 percentage points |
| Recall | 6.42% | 9.73% | +3.32 percentage points |
| mAP at 50 | 5.25% | 7.21% | +1.96 percentage points |
| mAP at 50 to 95 | 3.37% | 4.71% | +1.35 percentage points |
| Box loss | 1.5772 | 1.5002 | -0.0770 |
| Classification loss | 3.3083 | 2.4242 | -0.8841 |
| DFL loss | 1.5859 | 1.5174 | -0.0685 |

All three loss measures decreased. Recall and both mAP measures improved, which is the primary positive trend. Precision declined slightly as the model began making more detections, but the rising mAP and falling losses indicate that overall learning is progressing.

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_by_epoch-3/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_by_epoch-3/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_2_Retry_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_2_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_2_Training_Results.png` and `Epoch Posts/Epoch_2_LinkedIn_Post.md`

## Epoch 3

**Status:** Completed successfully  
**Date:** November 6 2026  
**Run folder:** `runs/detect/runs/detect/epoch_3`

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_by_epoch-3\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_3
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.544 hours (about 1 hour 33 minutes) |
| Cumulative 3-epoch runtime | 4.604 hours |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses compared with previous epochs

| Measure | Epoch 1 | Epoch 2 | Epoch 3 | Change vs Epoch 2 | Change vs Epoch 1 |
|---|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | -5.18 percentage points | -7.79 percentage points |
| Recall | 6.42% | 9.73% | 11.30% | +1.57 percentage points (+16.1%) | +4.88 percentage points (+76.0%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | +1.28 percentage points (+17.8%) | +3.24 percentage points (+61.7%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | +0.87 percentage points (+18.5%) | +2.21 percentage points (+65.6%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | -0.0216 (improved) | -0.0986 |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | -0.1175 (improved) | -1.0016 |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | -0.0193 (improved) | -0.0878 |

All three loss measures decreased for the third consecutive epoch. Classification loss has dropped by more than 1.0 point overall since training began. Recall jumped past 11% and mAP@50 reached 8.49%, demonstrating consistent learning across the 601-class space. Precision decreased slightly to 45.99%, reflecting increased object proposal coverage by the detector.

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_3/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_3/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_3_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_3_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_3_Training_Results.png` and `Epoch Posts/Epoch_3_LinkedIn_Post.md`

## Epoch 4

**Status:** Completed successfully  
**Date:** November 6 2026  
**Run folder:** `runs/detect/runs/detect/epoch_4`

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_3\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_4
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.594 hours (about 1 hour 36 minutes) |
| Cumulative 4-epoch runtime | 6.198 hours (~6 hours 12 minutes) |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses compared with previous epochs

| Measure | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Change vs Epoch 3 | Total Change vs Epoch 1 |
|---|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | -4.82 percentage points | -12.61 percentage points |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | +1.88 percentage points (+16.6%) | +6.76 percentage points (+105.3%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | +1.12 percentage points (+13.2%) | +4.36 percentage points (+83.0%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | +0.72 percentage points (+12.9%) | +2.93 percentage points (+87.0%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | -0.0216 (improved) | -0.1202 |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | -0.1086 (improved) | -1.1102 |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | -0.0173 (improved) | -0.1051 |

For the fourth consecutive epoch, all three loss measures decreased. Classification loss dropped below 2.20 (-1.11 points total since baseline). Crucially, recall reached 13.18%, more than doubling (+105.3% relative increase) from Epoch 1 (6.42%). mAP@50 reached 9.61% (+83% gain vs Epoch 1), demonstrating that the detector is successfully learning to recognize objects across diverse categories. Precision moved to 41.17% as detection coverage expanded.

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_4/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_4/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_4_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_4_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_4_Training_Results.png` and `Epoch Posts/Epoch_4_LinkedIn_Post.md`

## Epoch 5 (50% Milestone)

**Status:** Completed successfully  
**Date:** November 6-7 2026  
**Run folder:** `runs/detect/runs/detect/epoch_5`

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_4\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_5
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.545 hours (about 1 hour 33 minutes) |
| Cumulative 5-epoch runtime | 7.743 hours (~7 hours 45 minutes) |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses compared with previous epochs

| Measure | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Change vs Epoch 4 | Total Change vs Epoch 1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | -3.03 percentage points | -15.64 percentage points |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | +1.66 percentage points (+12.6%) | +8.42 percentage points (+131.2%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | +0.88 percentage points (+9.2%) | +5.24 percentage points (+99.8% Doubled!) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | +0.56 percentage points (+8.9%) | +3.49 percentage points (+103.6% Doubled!) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | -0.0164 (improved) | -0.1366 |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | -0.0780 (improved) | -1.1882 |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | -0.0136 (improved) | -0.1187 |

Epoch 5 brings the project to its official halfway mark (50% of the 10 planned epochs) with a double-digit breakthrough: mAP@50 reached 10.49%, effectively doubling from the start of training (+99.8% gain). mAP@50-95 likewise doubled (3.37% to 6.86%), and recall reached 14.84% (+131% gain). For the fifth consecutive epoch, all three loss metrics decreased. Precision settled at 38.14%, indicating the expected plateauing of the initial discovery phase before boundary refinement begins in Epochs 6-10.

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_5/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_5/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_5_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_5_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_5_Training_Results.png` and `Epoch Posts/Epoch_5_LinkedIn_Post.md`

## Epoch 6

**Status:** Completed successfully  
**Date:** November 8 2026  
**Run folder:** `runs/detect/runs/detect/epoch_6`

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_5\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_6
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.535 hours (about 1 hour 32 minutes) |
| Cumulative 6-epoch runtime | 9.278 hours (~9 hours 17 minutes) |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses compared with previous epochs

| Measure | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Epoch 6 | Change vs Epoch 5 | Total Change vs Epoch 1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | 36.43% | -1.71 percentage points | -17.35 percentage points |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | +0.78 percentage points (+5.3%) | +9.20 percentage points (+143.3%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | +0.73 percentage points (+7.0%) | +5.97 percentage points (+113.7%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | 7.29% | +0.43 percentage points (+6.3%) | +3.92 percentage points (+116.3%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | 1.4267 | -0.0139 (improved) | -0.1505 |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | -0.0610 (improved) | -1.2492 |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | 1.4564 | -0.0108 (improved) | -0.1295 |

Epoch 6 initiates the second half of training with steady convergence. mAP@50 reached 11.22% (+113.7% gain since Epoch 1) and recall climbed to 15.62% (+143.3% gain). All three loss metrics decreased for the sixth consecutive epoch, with classification loss approaching the sub-2.0 boundary (2.0591). Notably, precision decline has flattened (-1.71 pts vs -3.03 pts in Ep 5 and -4.82 pts in Ep 4), marking the transition into boundary stabilization.

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_6/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_6/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_6_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_6_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_6_Training_Results.png` and `Epoch Posts/Epoch_6_LinkedIn_Post.md`




