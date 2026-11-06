# LinkedIn Post - Epoch 2 Training Update

Epoch 2 is complete for my 601 class computer vision object detection project.

I am fine tuning YOLO11 Nano on 85,000 training images and validating on 15,000 separate images. The second epoch completed successfully, and the model is already showing a better overall ability to find objects.

## Results compared with Epoch 1

- Recall: 6.42% to 9.73%
- mAP@50: 5.25% to 7.21%
- mAP@50-95: 3.37% to 4.71%
- Precision: 53.8% to 51.2%

## Loss improvement

- Box loss: 1.5772 to 1.5002
- Classification loss: 3.3083 to 2.4242
- DFL loss: 1.5859 to 1.5174

The biggest early signal is the recall and mAP improvement. The slight precision drop is expected while the model begins making more detections; the rising mAP and falling losses show that the overall learning direction is positive.

Next up: Epoch 3, continuing from the new saved checkpoint.

#ComputerVision #ObjectDetection #YOLO #DeepLearning #MachineLearning #AI

---

# Short Caption

epoch 2 done. recall and mAP are up, all three losses are down, and the model is learning better from the full 601 class dataset. moving onto epoch 3.
