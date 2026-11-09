# LinkedIn Post - Epoch 10: Phase 1 Complete! (10 of 10 Epochs)

Phase 1 is officially complete! 10 out of 10 epochs finished for my 601-class object detection project.

Fine-tuning YOLO11 Nano on Open Images V6 (100,000 images per epoch: 85,000 train, 15,000 val) across 601 classes on an edge laptop GPU (NVIDIA GeForce GTX 1050 with 3 GB VRAM).

## 10-Epoch Final Milestones (Epoch 1 -> Epoch 10)

- Recall (objects detected): 6.42% -> 19.05% (+196.7% relative gain - nearly 3x increase!)
- mAP@50 (50% IoU accuracy): 5.25% -> 13.18% (+151.0% relative gain)
- mAP@50-95 (strict multi-threshold IoU): 3.37% -> 8.52% (+152.8% relative gain)
- Classification Loss: 3.3083 -> 1.8941 (-1.414 points reduction, breaking sub-1.90!)
- Box Loss: 1.5772 -> 1.3847 (Sub-1.39 milestone)
- DFL Loss: 1.5859 -> 1.4244 (Steady boundary refinement)
- Cumulative Compute: 15.455 hours across 106,250 training batches and 1,000,000 image passes

## Key Takeaways from Phase 1

1. Scalability on Constrained Edge Hardware: Proved that a modern lightweight architecture (YOLO11 Nano with 2.6M parameters) can reliably optimize over 601 disparate object categories on a 3 GB GPU without out-of-memory errors.
2. Consistent Convergence: All 10 epochs showed uninterrupted loss reduction in all three loss functions (box, class, and distribution focal loss).
3. Dramatic Sensitivity Surge: The model now identifies over 54,650 ground-truth objects in the 15,000-image validation split, up from just ~18,400 at baseline.

## What's Next for Phase 2?
Now that the 10-epoch edge baseline is established and verified, Phase 2 will transition compute to Google Colab accelerators to train higher-capacity models (YOLO11 Medium / Extra-Large) with larger batch sizes and higher resolutions.

Huge thanks to everyone who followed the epoch-by-epoch journey!

#ComputerVision #ObjectDetection #YOLO #YOLO11 #DeepLearning #MachineLearning #AI #OpenImages #EdgeAI #PyTorch

---

# Short Caption

phase 1 complete! 10 out of 10 epochs done. recall jumped from 6.4% to 19.05% (nearly 3x!), mAP50 reached 13.18%, box loss broke sub-1.39, and classification loss dipped below 1.90 to 1.894. 10 straight epochs of consistent optimization on a 3gb gtx 1050. edge baseline locked in. onto phase 2!
