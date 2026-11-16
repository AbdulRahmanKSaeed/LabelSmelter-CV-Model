# LinkedIn Post — Phase 2, Round 4 (Epochs 26–30)

Round 4 of Phase 2 is complete! 🎯

Continuing my **601-class object detection journey** with YOLO11 Nano, now with advanced training optimizations on the same edge hardware I started with.

## What changed in Phase 2?

After 10 baseline epochs in Phase 1, I didn't switch to a bigger cloud GPU. Instead, I pushed the same **GTX 1050 (3 GB VRAM)** further with smarter training:

- ⚡ **FP16 Mixed Precision** — halved VRAM usage, more room to train
- 📉 **Cosine LR Scheduler** — smooth convergence instead of linear decay
- 🔀 **Mosaic + Mixup + Copy-Paste Augmentation** — richer training signal per batch

## Round 4 Results (Epochs 26–30):

| Metric | Phase 1 Baseline | Round 4 | Change |
|--------|-----------------|---------|--------|
| mAP@50 | 13.18% | **18.47%** | +5.29 pts |
| Recall | 19.05% | **23.94%** | +4.89 pts |
| mAP@50-95 | 8.52% | **12.16%** | +3.64 pts |
| Precision | 29.24% | **35.13%** | +5.89 pts |
| Class Loss | 1.8941 | **1.9070** | +0.0129 |
| Box Loss | 1.3847 | **1.4266** | +0.0419 |

Training on **100,000 images per round** across all 601 Open Images V6 categories.
Phase 2 training complete — 30 total epochs achieved!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #AI #OpenImages #EdgeAI #MachineLearning #PyTorch

---

## Short Caption

phase 2 round 4 complete! epochs 26–30 done on a 3gb gtx 1050 with fp16 + cosine lr + mosaic augmentation. recall: 23.94% (phase 1: 19.05%), map50: 18.47% (phase 1: 13.18%), across 601 classes on 100k images. phase 2 complete!
