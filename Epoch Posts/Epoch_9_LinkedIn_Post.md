# LinkedIn Post - Epoch 9 (90% Penultimate Milestone) Training Update

Penultimate milestone reached: 9 of 10 epochs complete for my 601-class computer vision object detection project!

Fine-tuning YOLO11 Nano on 85,000 images and validating across 15,000 images (100,000 total images per epoch). The training maintains an unbroken 9-epoch record of continuous loss drops and rising detection accuracy.

## 9-Epoch Progression Highlights (Epoch 1 -> Epoch 9)

- Recall (objects found): 6.42% -> 9.73% -> 11.30% -> 13.18% -> 14.84% -> 15.62% -> 16.37% -> 17.31% -> 18.15% (+182.7% relative gain!)
- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% -> 9.61% -> 10.49% -> 11.22% -> 11.82% -> 12.35% -> 12.84% (+144.6% relative gain)
- mAP@50-95 (strict average): 3.37% -> 4.71% -> 5.58% -> 6.30% -> 6.86% -> 7.29% -> 7.64% -> 7.99% -> 8.28% (+145.7% relative gain)
- Classification Loss: 3.3083 -> 1.9282 (Down >1.38 points total)
- Box Loss: 1.5772 -> 1.3935 (Sub-1.40 milestone unlocked!)
- DFL Loss: 1.5859 -> 1.4310 (Continuous focal refinement)

## Key Takeaway
Out of 287,000 ground-truth objects in the validation set, this lightweight edge model (2.6M parameters on a GTX 1050 3GB GPU) is now correctly locating and identifying over 52,000 instances across 601 classes. Both mAP@50 and mAP@50-95 have increased by nearly 2.5× since Epoch 1.

One single epoch remains to complete the entire 10-epoch journey! Moving into Epoch 10.

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 9 done (90% complete!). recall broke 18.1%, mAP50 reached 12.84%, box loss dropped below 1.40, and classification loss hit 1.92. 9 straight epochs of continuous improvement. just ONE epoch left to finish phase 1! onto epoch 10.
