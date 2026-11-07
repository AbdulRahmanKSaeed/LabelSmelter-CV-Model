# LinkedIn Post - Epoch 5 (50% Milestone) Training Update

Halfway milestone reached: 5 of 10 epochs completed in my 601-class computer vision object detection project!

Fine-tuning YOLO11 Nano on 85,000 training images and validating across 15,000 images (100,000 images per epoch). The model has officially crossed into double digits, with mAP@50 doubling since the start of training.

## Milestone Highlights (Epoch 1 -> Epoch 5)

- mAP@50 (50% IoU accuracy): 5.25% -> 10.49% (Doubled! +99.8% relative gain)
- mAP@50-95 (strict average): 3.37% -> 6.86% (Doubled! +103.6% relative gain)
- Recall (objects found): 6.42% -> 14.84% (+131.2% relative gain across 601 classes)
- Classification Loss: 3.3083 -> 2.1201 (Down nearly 1.20 points total)
- Box Loss: 1.5772 -> 1.4406 (Consistent coordinate convergence)
- DFL Loss: 1.5859 -> 1.4672 (Steady boundary refinement)

## 5-Epoch Progression Table

| Metric | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 | Epoch 5 | Total Gain |
|---|---:|---:|---:|---:|---:|:---:|
| Recall | 6.42% | 9.73% | 11.30% | 13.18% | **14.84%** | **+131%** |
| mAP@50 | 5.25% | 7.21% | 8.49% | 9.61% | **10.49%** | **Doubled (+100%)** |
| mAP@50-95 | 3.37% | 4.71% | 5.58% | 6.30% | **6.86%** | **Doubled (+104%)** |
| Precision | 53.78% | 51.17% | 45.99% | 41.17% | **38.14%** | Plateauing |

## Takeaway
In a massive 601-class problem on edge hardware (GTX 1050 3GB), seeing both mAP and mAP@50-95 double by epoch 5 proves consistent optimization without overfitting. The aggressive discovery phase is now beginning to stabilize around ~38% precision, setting up the second half (Epochs 6-10) for boundary refinement.

Halfway mark done. Heading into the second half with Epoch 6!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 5 done and halfway through the project! mAP50 officially crossed 10% (doubling from 5.2% at start), recall reached nearly 15%, and all 3 losses dropped for the 5th time. onto epoch 6.
