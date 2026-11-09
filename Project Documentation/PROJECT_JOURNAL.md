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

## Epoch 7 (70% Milestone)

**Status:** Completed successfully  
**Date:** November 8 2026  
**Run folder:** `runs/detect/runs/detect/epoch_7`

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_6\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_7
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.564 hours (about 1 hour 34 minutes) |
| Cumulative 7-epoch runtime | 10.842 hours (~10 hours 51 minutes) |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses compared with previous epochs

| Measure | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Epoch 6 | Epoch 7 | Change vs Epoch 6 | Total Change vs Epoch 1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | 36.43% | 35.00% | -1.43 percentage points | -18.78 percentage points |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | 16.37% | +0.75 percentage points (+4.8%) | +9.95 percentage points (+155.0%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | 11.82% | +0.60 percentage points (+5.4%) | +6.57 percentage points (+125.1%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | 7.29% | 7.64% | +0.35 percentage points (+4.8%) | +4.27 percentage points (+126.7%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | 1.4267 | 1.4144 | -0.0123 (improved) | -0.1628 |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | 2.0087 | -0.0504 (improved) | -1.2996 |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | 1.4564 | 1.4469 | -0.0095 (improved) | -0.1390 |

Epoch 7 brings the project to 70% completion with unbroken progress. mAP@50 reached 11.82% (+125.1% relative gain since baseline) and recall expanded to 16.37% (+155.0% gain). All three loss metrics decreased for the seventh consecutive epoch, with classification loss touching the 2.00 threshold (2.0087). Precision settled firmly around 35.0% (-1.43 pts), preparing the detector for boundary consolidation over the final 3 epochs.

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_7/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_7/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_7_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_7_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_7_Training_Results.png` and `Epoch Posts/Epoch_7_LinkedIn_Post.md`

## Epoch 8 (80% Milestone - Sub-2.0 Loss Breakthrough)

**Status:** Completed successfully  
**Date:** November 8 2026  
**Run folder:** `runs/detect/runs/detect/epoch_8`

### Command used

```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_7\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_8
```

### Execution record

| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.539 hours (about 1 hour 32 minutes) |
| Cumulative 8-epoch runtime | 12.381 hours (~12 hours 23 minutes) |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses compared with previous epochs

| Measure | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Epoch 6 | Epoch 7 | Epoch 8 | Change vs Epoch 7 | Total Change vs Epoch 1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | 36.43% | 35.00% | 34.28% | -0.72 percentage points | -19.50 percentage points |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | 16.37% | 17.31% | +0.94 percentage points (+5.7%) | +10.89 percentage points (+169.6%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | 11.82% | 12.35% | +0.53 percentage points (+4.5%) | +7.10 percentage points (+135.2%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | 7.29% | 7.64% | 7.99% | +0.35 percentage points (+4.6%) | +4.62 percentage points (+137.1%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | 1.4267 | 1.4144 | 1.4035 | -0.0109 (improved) | -0.1737 |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | 2.0087 | 1.9660 | -0.0427 (improved) | -1.3423 (Sub-2.0 milestone!) |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | 1.4564 | 1.4469 | 1.4385 | -0.0084 (improved) | -0.1474 |

Epoch 8 brings the project to 80% completion with a key optimization breakthrough: classification loss officially dropped below the 2.00 barrier to 1.9660 (-1.34 pts total since baseline). mAP@50 reached 12.35% (+135.2% relative gain) and recall climbed to 17.31% (+169.6% gain, finding nearly 50,000 target objects). All three loss metrics decreased for the eighth consecutive epoch. Precision change flattened to just -0.72 percentage points, demonstrating complete stabilization as the project enters the final two epochs (Epochs 9 & 10).

### Checkpoints and artifacts

- Best checkpoint: `runs/detect/runs/detect/epoch_8/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_8/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_8_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_8_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_8_Training_Results.png` and `Epoch Posts/Epoch_8_LinkedIn_Post.md`








## Epoch 9 (90% Penultimate Milestone)

**Status:** Completed successfully  
**Date:** November 8-9 2026  
**Run folder:** `runs/detect/runs/detect/epoch_9`

### Command used
```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model runs\detect\runs\detect\epoch_8\weights\last.pt --epochs 1 --batch 8 --imgsz 640 --name epoch_9
```

### Execution record
| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.534 hours (about 1 hour 32 minutes) |
| Cumulative 9-epoch runtime | 13.915 hours (~13 hours 55 minutes) |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses
| Measure | Ep1 | Ep2 | Ep3 | Ep4 | Ep5 | Ep6 | Ep7 | Ep8 | Ep9 | Change vs Ep8 | Total vs Ep1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | 36.43% | 35.00% | 34.28% | 30.82% | -3.46 pts | -22.96 pts |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | 16.37% | 17.31% | 18.15% | +0.84 pts | +11.73 pts (+182.7%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | 11.82% | 12.35% | 12.84% | +0.49 pts | +7.59 pts (+144.6%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | 7.29% | 7.64% | 7.99% | 8.28% | +0.29 pts | +4.91 pts (+145.7%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | 1.4267 | 1.4144 | 1.4035 | 1.3935 | -0.0100 | -0.1837 (sub-1.40 milestone!) |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | 2.0087 | 1.9660 | 1.9282 | -0.0378 | -1.3801 |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | 1.4564 | 1.4469 | 1.4385 | 1.4310 | -0.0075 | -0.1549 |

Epoch 9 brings the project to 90% completion with a new milestone: box loss broke below the 1.40 barrier to 1.3935. mAP@50 reached 12.84% (+144.6% relative gain since Epoch 1) and recall climbed to 18.15%, meaning the model now finds roughly 52,000 ground-truth objects per validation run. All three loss metrics decreased for the ninth consecutive epoch. The precision decline continues as expected during the discovery phase of training for a 601-class detection task.

### Checkpoints and artifacts
- Best checkpoint: `runs/detect/runs/detect/epoch_9/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_9/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_9_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_9_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_9_Training_Results.png` and `Epoch Posts/Epoch_9_LinkedIn_Post.md`


## Epoch 10 (Phase 1 Complete - 100% Milestone)

**Status:** Completed successfully (Phase 1 Finished)  
**Date:** November 9 2026  
**Run folder:** `runs/detect/runs/detect/epoch_10`

### Command used
```powershell
.venv_cuda\Scripts\python.exe scripts\train_detector.py --model "runs\detect\runs\detect\epoch_9\weights\last.pt" --epochs 1 --batch 8 --imgsz 640 --name epoch_10 2>&1 | Tee-Object -FilePath "Training Logs\Epoch_10_Training_Log.txt"
```

### Execution record
| Item | Result |
|---|---:|
| Training batches | 10,625 |
| Training images | 85,000 |
| Validation images | 15,000 |
| Validation objects | 286,954 |
| Total duration | 1.540 hours (about 1 hour 32 minutes 25 seconds) |
| Cumulative 10-epoch runtime | 15.455 hours (~15 hours 27 minutes) |
| Total images processed (10 epochs) | 1,000,000 images |
| Total batches trained (10 epochs) | 106,250 batches |
| Final weights size | 5.51 MB (`best.pt` & `last.pt`) |

### Results and losses across the full 10 epochs
| Measure | Ep1 | Ep2 | Ep3 | Ep4 | Ep5 | Ep6 | Ep7 | Ep8 | Ep9 | Ep10 | Change vs Ep9 | Total vs Ep1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | 38.14% | 36.43% | 35.00% | 34.28% | 30.82% | 29.24% | -1.58 pts | -24.54 pts |
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | 14.84% | 15.62% | 16.37% | 17.31% | 18.15% | 19.05% | +0.90 pts | +12.63 pts (+196.7%) |
| mAP at 50 | 5.25% | 7.21% | 8.49% | 9.61% | 10.49% | 11.22% | 11.82% | 12.35% | 12.84% | 13.18% | +0.34 pts | +7.93 pts (+151.0%) |
| mAP at 50 to 95 | 3.37% | 4.71% | 5.58% | 6.30% | 6.86% | 7.29% | 7.64% | 7.99% | 8.28% | 8.52% | +0.24 pts | +5.15 pts (+152.8%) |
| Box loss | 1.5772 | 1.5002 | 1.4786 | 1.4570 | 1.4406 | 1.4267 | 1.4144 | 1.4035 | 1.3935 | 1.3847 | -0.0088 | -0.1925 (sub-1.39 milestone) |
| Classification loss | 3.3083 | 2.4242 | 2.3067 | 2.1981 | 2.1201 | 2.0591 | 2.0087 | 1.9660 | 1.9282 | 1.8941 | -0.0341 | -1.4142 (sub-1.90 milestone!) |
| DFL loss | 1.5859 | 1.5174 | 1.4981 | 1.4808 | 1.4672 | 1.4564 | 1.4469 | 1.4385 | 1.4310 | 1.4244 | -0.0066 | -0.1615 |

Epoch 10 successfully marks the completion of Phase 1! The entire 10-epoch curriculum finished with flawless loss convergence, never encountering an increase in any loss metric across all 10 epochs. Classification loss broke below 1.90 to 1.8941 (-1.41 pts total reduction). Detection recall reached 19.05% (nearly tripling from the initial 6.42%), and mAP@50 reached 13.18% (+151.0% relative improvement). The final model weights are safely persisted in `runs/detect/runs/detect/epoch_10/weights/best.pt`.

### Checkpoints and artifacts
- Best checkpoint: `runs/detect/runs/detect/epoch_10/weights/best.pt`
- Resume checkpoint: `runs/detect/runs/detect/epoch_10/weights/last.pt`
- Raw terminal log: `Training Logs/Epoch_10_Training_Log.txt`
- Detailed report: `Epoch Reports/Epoch_10_Training_Report.docx`
- LinkedIn graphic and copy: `Epoch Posts/Epoch_10_Training_Results.png` and `Epoch Posts/Epoch_10_LinkedIn_Post.md`
