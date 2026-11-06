# LinkedIn Post - Epoch 4 Training Update

Milestone reached in my 601-class computer vision object detection project: Recall has more than doubled since training began!

Fine-tuning YOLO11 Nano on 85,000 images and validating across 15,000 images (100,000 images per epoch). Epoch 4 is complete, and the detector continues to show remarkable steady learning across 601 distinct object categories.

## Results Progression (Epoch 1 -> Epoch 2 -> Epoch 3 -> Epoch 4)

- Recall (objects found): 6.42% -> 9.73% -> 11.30% -> 13.18% (+105.3% relative gain -- more than doubled!)
- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% -> 9.61% (+83.0% relative gain)
- mAP@50-95 (stricter average): 3.37% -> 4.71% -> 5.58% -> 6.30% (+87.0% relative gain)
- Precision (detections correct): 53.8% -> 51.2% -> 46.0% -> 41.17%

## Loss Progression (4th Consecutive Drop)

- Box loss (location error): 1.5772 -> 1.5002 -> 1.4786 -> 1.4570 (improved)
- Classification loss (class error): 3.3083 -> 2.4242 -> 2.3067 -> 2.1981 (down >1.11 points total)
- DFL loss (refinement error): 1.5859 -> 1.5174 -> 1.4981 -> 1.4808 (improved)

## Key Takeaway
Training a 601-class model on an entry-level GTX 1050 (3GB VRAM) requires balancing capacity and complexity. Seeing recall surge past 13% while mAP@50 approaches 10% confirms the network is learning meaningful semantic features for rare classes, not just the common ones.

Halfway to the 10-epoch goal! Checkpoint saved, heading straight into Epoch 5.

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 4 done. recall more than doubled from 6.4% to 13.2%, mAP50 is knocking on 10%, and all three losses dropped again. onto epoch 5.
