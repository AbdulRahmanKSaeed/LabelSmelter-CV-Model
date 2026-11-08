# LinkedIn Post - Epoch 7 (70% Complete) Training Update

70% milestone reached: 7 of 10 epochs complete for my 601-class computer vision object detection project!

Fine-tuning YOLO11 Nano on 85,000 images and validating across 15,000 images (100,000 images per epoch). The training continues its unbroken record of improvement across all key metrics and loss categories.

## 7-Epoch Progression Highlights (Epoch 1 -> Epoch 7)

- mAP@50 (50% IoU accuracy): 5.25% -> 7.21% -> 8.49% -> 9.61% -> 10.49% -> 11.22% -> 11.82% (+125.1% relative gain)
- Recall (objects found): 6.42% -> 9.73% -> 11.30% -> 13.18% -> 14.84% -> 15.62% -> 16.37% (+155.0% relative gain)
- mAP@50-95 (strict average): 3.37% -> 4.71% -> 5.58% -> 6.30% -> 6.86% -> 7.29% -> 7.64% (+126.7% relative gain)
- Classification Loss: 3.3083 -> 2.4242 -> 2.3067 -> 2.1981 -> 2.1201 -> 2.0591 -> 2.0087 (Down ~1.30 points total, touching 2.0!)
- Box Loss: 1.5772 -> 1.4144 (Continuous coordinate convergence)
- DFL Loss: 1.5859 -> 1.4469 (Steady focal boundary refinement)

## Key Takeaway
Training an edge model (GTX 1050 3GB VRAM) across a massive 601-class hierarchy has demonstrated remarkable stability:
- Both mAP@50 and mAP@50-95 have more than doubled since baseline.
- Recall has jumped from finding 6% to finding over 16.3% of all objects across the vocabulary.
- Precision decline has fully plateaued around ~35%, setting up the final 3 epochs for boundary consolidation.

Just 3 epochs left to the 10-epoch finish line! Heading into Epoch 8.

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages

---

# Short Caption

epoch 7 done (70% complete!). mAP50 reached 11.8%, recall hit 16.4%, and classification loss touched 2.00 with all 3 losses dropping for the 7th straight epoch. 3 epochs to go. onto epoch 8.
