# LinkedIn Post - Epoch 3 Training Update

Epoch 3 is complete for my 601-class computer vision object detection project!

I am fine-tuning YOLO11 Nano on 85,000 training images and validating on 15,000 separate images (100,000 total images per epoch). The third epoch finished smoothly, showing steady improvements across key detection metrics and continued drop across all training losses.

## Results progression (Epoch 1 -> Epoch 2 -> Epoch 3)

- Recall (objects found): 6.42% -> 9.73% -> 11.30% (+76.0% relative gain since Epoch 1)
- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% (+61.7% relative gain)
- mAP@50-95 (stricter average): 3.37% -> 4.71% -> 5.58% (+65.6% relative gain)
- Precision (detections correct): 53.8% -> 51.2% -> 45.99%

## Loss progression (All 3 decreasing steadily)

- Box loss (location error): 1.5772 -> 1.5002 -> 1.4786 (improved)
- Classification loss (class error): 3.3083 -> 2.4242 -> 2.3067 (improved by over 1.0 point total)
- DFL loss (refinement error): 1.5859 -> 1.5174 -> 1.4981 (improved)

## Key Takeaway
For a complex 601-class problem on edge hardware (GTX 1050), recall jumping to 11.3% while mAP expands to 8.5% is the key indicator of healthy learning. The slight drop in precision is standard at this stage as the model gains confidence to spot less frequent classes.

Checkpoint saved. Moving straight on to Epoch 4!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 3 done. recall pushed past 11% and mAP50 reached 8.5%. all three losses keep dropping across the 601 classes. moving onto epoch 4.
