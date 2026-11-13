# LinkedIn Post — Phase 2, Round 1 (Epochs 11–15)

Round 1 of Phase 2 is complete! 🎯

Continuing my **601-class object detection journey** with YOLO11 Nano, now with advanced training optimizations on the same edge hardware I started with.

## What changed in Phase 2?

After 10 baseline epochs in Phase 1, I didn't switch to a bigger cloud GPU. Instead, I pushed the same **GTX 1050 (3 GB VRAM)** further with smarter training:

- ⚡ **FP16 Mixed Precision** — halved VRAM usage, more room to train
- 📉 **Cosine LR Scheduler** — smooth convergence instead of linear decay
- 🔀 **Mosaic + Mixup + Copy-Paste Augmentation** — richer training signal per batch

## Round 1 Results (Epochs 11–15):

| Metric | Phase 1 Baseline | Round 1 | Change |
|--------|-----------------|---------|--------|
| mAP@50 | 13.18% | **15.53%** | +2.35 pts |
| Recall | 19.05% | **21.44%** | +2.39 pts |
| mAP@50-95 | 8.52% | **10.16%** | +1.64 pts |
| Precision | 29.24% | **32.43%** | +3.19 pts |
| Class Loss | 1.8941 | **1.9872** | +0.0931 |
| Box Loss | 1.3847 | **1.4428** | +0.0581 |

Training on **100,000 images per round** across all 601 Open Images V6 categories.
Round 2 next — Epochs 16–20!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #AI #OpenImages #EdgeAI #MachineLearning #PyTorch

---

## Short Caption

phase 2 round 1 complete! epochs 11–15 done on a 3gb gtx 1050 with fp16 + cosine lr + mosaic augmentation. recall: 21.44% (phase 1: 19.05%), map50: 15.53% (phase 1: 13.18%), across 601 classes on 100k images. onto round 2!
