# LinkedIn Post — Phase 2, Round 3 (Epochs 21–25)

Round 3 of Phase 2 is complete! 🎯

Continuing my **601-class object detection journey** with YOLO11 Nano, now with advanced training optimizations on the same edge hardware I started with.

## What changed in Phase 2?

After 10 baseline epochs in Phase 1, I didn't switch to a bigger cloud GPU. Instead, I pushed the same **GTX 1050 (3 GB VRAM)** further with smarter training:

- ⚡ **FP16 Mixed Precision** — halved VRAM usage, more room to train
- 📉 **Cosine LR Scheduler** — smooth convergence instead of linear decay
- 🔀 **Mosaic + Mixup + Copy-Paste Augmentation** — richer training signal per batch

## Round 3 Results (Epochs 21–25):

| Metric | Phase 1 Baseline | Round 3 | Change |
|--------|-----------------|---------|--------|
| mAP@50 | 13.18% | **17.78%** | +4.60 pts |
| Recall | 19.05% | **23.46%** | +4.41 pts |
| mAP@50-95 | 8.52% | **11.72%** | +3.20 pts |
| Precision | 29.24% | **34.15%** | +4.91 pts |
| Class Loss | 1.8941 | **1.9268** | +0.0327 |
| Box Loss | 1.3847 | **1.4311** | +0.0464 |

Training on **100,000 images per round** across all 601 Open Images V6 categories.
Round 4 next — Epochs 26–30!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #AI #OpenImages #EdgeAI #MachineLearning #PyTorch

---

## Short Caption

phase 2 round 3 complete! epochs 21–25 done on a 3gb gtx 1050 with fp16 + cosine lr + mosaic augmentation. recall: 23.46% (phase 1: 19.05%), map50: 17.78% (phase 1: 13.18%), across 601 classes on 100k images. onto round 4!
