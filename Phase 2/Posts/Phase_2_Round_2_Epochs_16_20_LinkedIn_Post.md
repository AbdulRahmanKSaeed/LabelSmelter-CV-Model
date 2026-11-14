# LinkedIn Post — Phase 2, Round 2 (Epochs 16–20)

Round 2 of Phase 2 is complete! 🎯

Continuing my **601-class object detection journey** with YOLO11 Nano, now with advanced training optimizations on the same edge hardware I started with.

## What changed in Phase 2?

After 10 baseline epochs in Phase 1, I didn't switch to a bigger cloud GPU. Instead, I pushed the same **GTX 1050 (3 GB VRAM)** further with smarter training:

- ⚡ **FP16 Mixed Precision** — halved VRAM usage, more room to train
- 📉 **Cosine LR Scheduler** — smooth convergence instead of linear decay
- 🔀 **Mosaic + Mixup + Copy-Paste Augmentation** — richer training signal per batch

## Round 2 Results (Epochs 16–20):

| Metric | Phase 1 Baseline | Round 2 | Change |
|--------|-----------------|---------|--------|
| mAP@50 | 13.18% | **16.75%** | +3.57 pts |
| Recall | 19.05% | **22.47%** | +3.42 pts |
| mAP@50-95 | 8.52% | **11.02%** | +2.50 pts |
| Precision | 29.24% | **33.40%** | +4.16 pts |
| Class Loss | 1.8941 | **1.9563** | +0.0622 |
| Box Loss | 1.3847 | **1.4353** | +0.0506 |

Training on **100,000 images per round** across all 601 Open Images V6 categories.
Round 3 next — Epochs 21–25!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #AI #OpenImages #EdgeAI #MachineLearning #PyTorch

---

## Short Caption

phase 2 round 2 complete! epochs 16–20 done on a 3gb gtx 1050 with fp16 + cosine lr + mosaic augmentation. recall: 22.47% (phase 1: 19.05%), map50: 16.75% (phase 1: 13.18%), across 601 classes on 100k images. onto round 3!
