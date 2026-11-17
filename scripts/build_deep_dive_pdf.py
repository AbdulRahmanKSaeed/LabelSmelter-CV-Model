"""
Deep Dive Masterclass Document & PDF Generator
==============================================
Generates an exhaustive, beautifully styled HTML and PDF reference manual:
"The Deep End: A Masterclass Guide to Modern Object Detection, YOLO11, and Edge Machine Learning"
"""

import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\HP\Desktop\CV Project")
DOCS_DIR = PROJECT_ROOT / "Project Documentation"
HTML_OUT = DOCS_DIR / "The_Deep_End_YOLO11_Masterclass.html"
PDF_OUT = DOCS_DIR / "The_Deep_End_YOLO11_Masterclass.pdf"

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Deep End: A Masterclass Guide to YOLO11 & Object Detection</title>
<style>
  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {
      content: counter(page);
      font-size: 9pt;
      color: #64748b;
    }
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.65;
    font-size: 10.5pt;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
  }

  /* Cover Page */
  .cover {
    page-break-after: always;
    padding-top: 60px;
    padding-bottom: 60px;
    text-align: center;
  }
  .cover-badge {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    font-size: 10pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 9999px;
    border: 1px solid #bfdbfe;
    margin-bottom: 24px;
  }
  .cover-title {
    font-size: 32pt;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.15;
    margin: 0 0 16px 0;
    letter-spacing: -0.5px;
  }
  .cover-subtitle {
    font-size: 14pt;
    color: #475569;
    max-width: 650px;
    margin: 0 auto 36px auto;
    line-height: 1.5;
  }
  .cover-divider {
    width: 80px;
    height: 4px;
    background: #2563eb;
    margin: 0 auto 40px auto;
    border-radius: 2px;
  }
  .cover-meta {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 24px;
    max-width: 520px;
    margin: 0 auto;
    text-align: left;
    font-size: 9.5pt;
  }
  .cover-meta table {
    width: 100%;
    border-collapse: collapse;
  }
  .cover-meta td {
    padding: 6px 0;
    border-bottom: 1px solid #f1f5f9;
  }
  .cover-meta td:first-child {
    font-weight: 600;
    color: #64748b;
    width: 40%;
  }
  .cover-meta td:last-child {
    font-weight: 700;
    color: #0f172a;
  }

  /* Typography */
  h1 {
    font-size: 20pt;
    font-weight: 800;
    color: #0f172a;
    margin-top: 36px;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
    page-break-after: avoid;
  }
  .chapter-header {
    page-break-before: always;
    margin-top: 0;
    padding-top: 10px;
  }
  .chapter-tag {
    font-size: 9pt;
    font-weight: 700;
    color: #2563eb;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 4px;
  }
  h2 {
    font-size: 14pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 24px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }
  h3 {
    font-size: 11.5pt;
    font-weight: 700;
    color: #334155;
    margin-top: 18px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }
  p {
    margin-top: 0;
    margin-bottom: 12px;
    text-align: justify;
  }

  /* Callout Boxes */
  .callout {
    border-radius: 8px;
    padding: 14px 18px;
    margin: 16px 0;
    page-break-inside: avoid;
    font-size: 9.5pt;
    line-height: 1.55;
  }
  .callout-blue {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    color: #1e3a8a;
  }
  .callout-green {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    color: #14532d;
  }
  .callout-amber {
    background: #fffbeb;
    border-left: 4px solid #d97706;
    color: #78350f;
  }
  .callout-title {
    font-weight: 700;
    font-size: 10pt;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
  }

  /* Tables */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 24px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }
  table.data-table th {
    background: #0f172a;
    color: #ffffff;
    font-weight: 700;
    padding: 8px 10px;
    text-align: left;
    border: 1px solid #1e293b;
  }
  table.data-table td {
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
  }
  table.data-table tr:nth-child(even) {
    background-color: #f8fafc;
  }
  table.data-table tr:hover {
    background-color: #f1f5f9;
  }

  /* Code Blocks */
  pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 14px 16px;
    border-radius: 8px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 14px 0;
  }
  code {
    font-family: "Consolas", "Courier New", monospace;
    font-size: 9pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 5px;
    border-radius: 4px;
  }
  pre code {
    background: transparent;
    color: inherit;
    padding: 0;
  }

  /* Math Blocks */
  .math-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 18px;
    margin: 14px 0;
    text-align: center;
    font-family: "Georgia", serif;
    font-style: italic;
    font-size: 11pt;
    color: #0f172a;
    page-break-inside: avoid;
  }

  /* Two Column Layout */
  .two-col {
    display: flex;
    gap: 18px;
    margin: 16px 0;
    page-break-inside: avoid;
  }
  .col {
    flex: 1;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 14px;
  }

  /* Badge Tags */
  .tag {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 8pt;
    font-weight: 700;
  }
  .tag-green { background: #dcfce7; color: #15803d; }
  .tag-blue  { background: #dbeafe; color: #1d4ed8; }
  .tag-amber { background: #fef3c7; color: #b45309; }
</style>
</head>
<body>

<!-- ================= COVER PAGE ================= -->
<div class="cover">
  <div class="cover-badge">Complete Technical Blueprint & Masterclass Reference</div>
  <h1 class="cover-title">The Deep End</h1>
  <div class="cover-subtitle">
    An Exhaustive, Step-by-Step Technical Guide to Modern Object Detection, YOLO11 Architecture, Mathematical Loss Formulations, Edge Hardware Optimization, and Auto-Annotation
  </div>
  <div class="cover-divider"></div>

  <div class="cover-meta">
    <table>
      <tr>
        <td>Project Subject</td>
        <td>Open Images V6 (601 Classes) Object Detection</td>
      </tr>
      <tr>
        <td>Model Architecture</td>
        <td>YOLO11 Nano (<code>yolo11n</code>, 2.6M Parameters)</td>
      </tr>
      <tr>
        <td>Target Hardware</td>
        <td>NVIDIA GeForce GTX 1050 (3 GB VRAM Laptop)</td>
      </tr>
      <tr>
        <td>Total Epochs Trained</td>
        <td>30 Epochs (Phase 1: 10 Ep | Phase 2: 20 Ep)</td>
      </tr>
      <tr>
        <td>Images Evaluated</td>
        <td>3,000,000 Image Passes (100k per epoch)</td>
      </tr>
      <tr>
        <td>Peak Accuracy (mAP@50)</td>
        <td>18.47% (from baseline 5.25% & Phase 1 13.18%)</td>
      </tr>
      <tr>
        <td>Inference Speed</td>
        <td>11.7 milliseconds (~85 FPS)</td>
      </tr>
      <tr>
        <td>Author & Engineer</td>
        <td>Abdul Rahman K. Saeed</td>
      </tr>
      <tr>
        <td>Date of Publication</td>
        <td>November 2026</td>
      </tr>
    </table>
  </div>
</div>

<!-- ================= TABLE OF CONTENTS ================= -->
<h1 class="chapter-header">Table of Contents</h1>
<ol style="font-size: 10pt; line-height: 1.8; color: #334155;">
  <li><strong>Chapter 1: The Foundations of Computer Vision</strong> — From raw pixels and tensors to the four core vision tasks and why object detection is intrinsically difficult.</li>
  <li><strong>Chapter 2: The Dataset & Real-World Complexity</strong> — Open Images V6, the long-tail distribution across 601 classes, and coordinate normalization mathematics.</li>
  <li><strong>Chapter 3: Under the Hood of YOLO11 Nano</strong> — Backbone, Neck, Decoupled Anchor-Free Head, C3k2, SPPF, and parameter efficiency.</li>
  <li><strong>Chapter 4: The Mathematics of Loss Functions</strong> — Complete IoU (CIoU), Binary Cross-Entropy with Sigmoid, and Distribution Focal Loss (DFL).</li>
  <li><strong>Chapter 5: How We Measure Success</strong> — Precision, Recall, PR Curves, mAP@50, and strict mAP@50-95 explained from first principles.</li>
  <li><strong>Chapter 6: The Phase 2 Engineering Playbook</strong> — FP16 mixed precision, cosine annealing schedules, the augmentation trio, and mosaic shutoff.</li>
  <li><strong>Chapter 7: Hardware Constraints & Edge Engineering</strong> — Managing 3 GB VRAM bottlenecks, thermal dissipation at 92°C, and local vs. cloud trade-offs.</li>
  <li><strong>Chapter 8: Real-Time Inference & Auto-Annotation Suite</strong> — Non-Maximum Suppression (NMS), dual-format exports (YOLO <code>.txt</code> & JSON), and validation benchmarks.</li>
  <li><strong>Chapter 9: The Master Glossary & Interview Defense Guide</strong> — Clear definitions of all 35+ core machine learning and computer vision terms.</li>
</ol>

<!-- ================= CHAPTER 1 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 1</div>
  The Foundations of Computer Vision
</h1>

<h2>1.1 How Computers See Images</h2>
<p>
To human eyes, a photograph is a cohesive visual scene of people, vehicles, and skylines. To a computer, a digital image is nothing more than a structured 3-dimensional array of numbers called a <strong>Tensor</strong>.
</p>
<p>
A standard RGB color image of resolution 640 × 640 pixels is stored as a matrix of shape:
</p>
<div class="math-box">
  \text{Shape} = (H \times W \times C) = (640 \times 640 \times 3) = 1,228,800 \text{ integer values}
</div>
<p>
Where <strong>H</strong> is height, <strong>W</strong> is width, and <strong>C</strong> represents the 3 color channels (Red, Green, Blue). Each value is an 8-bit unsigned integer ranging from <code>0</code> (completely black) to <code>255</code> (maximum intensity). Before feeding these tensors into a neural network, they are normalized into 32-bit or 16-bit floating-point numbers between <code>0.0</code> and <code>1.0</code> by dividing every pixel by 255.0.
</p>

<h2>1.2 The 4 Core Computer Vision Tasks</h2>
<p>
To understand object detection, we must contrast it with the other fundamental computer vision paradigms:
</p>

<table class="data-table">
  <thead>
    <tr>
      <th>Task</th>
      <th>Question Answered</th>
      <th>Network Output</th>
      <th>Complexity Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Image Classification</strong></td>
      <td>"What is the single dominant subject in this image?"</td>
      <td>One probability vector across $K$ classes (e.g. <code>[Cat: 0.92, Dog: 0.08]</code>).</td>
      <td><span class="tag tag-blue">Low</span></td>
    </tr>
    <tr>
      <td><strong>2. Object Detection (Our Project)</strong></td>
      <td>"What objects exist, and <em>where</em> are they located?"</td>
      <td>List of bounding boxes $(x, y, w, h)$ + class label + confidence score for each.</td>
      <td><span class="tag tag-amber">High (Regression + Classification)</span></td>
    </tr>
    <tr>
      <td><strong>3. Semantic Segmentation</strong></td>
      <td>"Which category does each individual pixel belong to?"</td>
      <td>Pixel-wise class mask matching the input resolution (no distinction between separate instances).</td>
      <td><span class="tag tag-amber">High</span></td>
    </tr>
    <tr>
      <td><strong>4. Instance Segmentation</strong></td>
      <td>"Which specific object instance does each pixel belong to?"</td>
      <td>Individual pixel masks for "Car 1", "Car 2", "Person 1".</td>
      <td><span class="tag tag-green">Very High</span></td>
    </tr>
  </tbody>
</table>

<h2>1.3 Why Object Detection is 100× Harder than Classification</h2>
<p>
Classification is simply predicting a discrete category label from an entire image. Object detection is substantially more complex due to four mathematical and architectural hurdles:
</p>
<ol>
  <li><strong>Dual Objective (Classification + Regression):</strong> The model must simultaneously solve a continuous mathematical regression problem (predicting four spatial coordinates with sub-pixel precision) and a discrete multi-class classification problem.</li>
  <li><strong>Variable-Length Outputs:</strong> One image may contain zero objects, while another image (e.g., a packed parking lot) contains 80 objects. Standard neural networks require fixed-size output layers; handling variable numbers of predictions requires sophisticated matching algorithms.</li>
  <li><strong>Extreme Scale Variation:</strong> A "Person" walking near the camera might occupy 500 × 300 pixels, while a "Car" parked at the end of the street might occupy only 12 × 15 pixels. The network must extract features that resolve both microscopic and massive objects simultaneously.</li>
  <li><strong>Occlusion and Dense Overlap:</strong> In real-world urban images, a bicycle might be 60% occluded by a pedestrian, standing in front of a car. The detector must disentangle which pixels belong to which target.</li>
</ol>

<!-- ================= CHAPTER 2 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 2</div>
  The Dataset & The Real-World Challenge
</h1>

<h2>2.1 What is Open Images V6?</h2>
<p>
Most popular academic object detection benchmarks (such as <strong>COCO</strong>) feature only <strong>80 classes</strong>. In contrast, Google's <strong>Open Images V6</strong> is one of the most comprehensive and challenging computer vision datasets in existence, featuring <strong>601 object categories</strong> organized into a rich semantic hierarchy.
</p>

<div class="two-col">
  <div class="col">
    <h3 style="margin-top:0;">COCO Benchmark (Standard)</h3>
    <p style="font-size:9pt; margin:0;">
      • 80 Common categories<br>
      • High class frequency per image<br>
      • Broadly uniform distribution<br>
      • Pre-filtered clean bounding boxes
    </p>
  </div>
  <div class="col" style="background:#eff6ff; border-color:#bfdbfe;">
    <h3 style="margin-top:0; color:#1d4ed8;">Open Images V6 (Our Project)</h3>
    <p style="font-size:9pt; margin:0;">
      • <strong>601 Categories</strong> (7.5× larger taxonomy)<br>
      • Severe long-tail class imbalance<br>
      • Hierarchical classes (e.g. "Vehicle" → "Land Vehicle" → "Car")<br>
      • Complex real-world consumer photographs
    </p>
  </div>
</div>

<h2>2.2 The "Long-Tail" Imbalance Challenge</h2>
<p>
In Open Images, common classes such as <em>Car</em>, <em>Person</em>, and <em>Wheel</em> appear hundreds of thousands of times across the training split. Conversely, rare fine-grained categories such as <em>Artichoke</em>, <em>Harmonica</em>, <em>Harpsichord</em>, or <em>Segway</em> appear in only a few dozen images.
</p>
<p>
This severe statistical disparity is known as the <strong>Long-Tail Distribution</strong>. When training begins, the network's loss is heavily dominated by errors on the rare classes, resulting in an initial classification loss of <strong>3.3083</strong>. Over 30 epochs, the network must learn balanced feature representations without catastrophic forgetting of the rare classes.
</p>

<h2>2.3 Understanding Coordinate Normalization</h2>
<p>
Image resolutions vary widely—some training images are 1920 × 1080, while others are 640 × 480. If bounding boxes were recorded in raw pixel coordinates, the network would fail whenever image sizes changed. 
</p>
<p>
To achieve complete <strong>resolution invariance</strong>, all YOLO annotations are stored as normalized floating-point numbers between <code>0.0</code> and <code>1.0</code> relative to the image dimensions:
</p>

<div class="math-box">
  x_{\text{center}} = \frac{x_{\text{pixel\_center}}}{W_{\text{image}}}, \quad
  y_{\text{center}} = \frac{y_{\text{pixel\_center}}}{H_{\text{image}}}, \quad
  w = \frac{\text{width}_{\text{pixels}}}{W_{\text{image}}}, \quad
  h = \frac{\text{height}_{\text{pixels}}}{H_{\text{image}}}
</div>

<p>
When reading a line from our dataset label file:
<code>90 0.4872 0.6413 0.9636 0.7173</code>
It translates to:
</p>
<ul>
  <li><code>90</code> = Class ID (corresponding to <strong>Car</strong> in <code>class_mapping.json</code>).</li>
  <li><code>0.4872</code> = The center of the car is at 48.72% of the image width from the left.</li>
  <li><code>0.6413</code> = The center of the car is at 64.13% of the image height from the top.</li>
  <li><code>0.9636</code> = The car spans 96.36% of the total image width.</li>
  <li><code>0.7173</code> = The car spans 71.73% of the total image height.</li>
</ul>

<!-- ================= CHAPTER 3 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 3</div>
  Under the Hood of YOLO11 Nano (yolo11n)
</h1>

<h2>3.1 The One-Stage vs. Two-Stage Paradigm</h2>
<p>
Early deep-learning detectors (like Faster R-CNN) operated in two stages: Stage 1 proposed several thousand potential regions of interest (RoIs), and Stage 2 evaluated each region through a classification network. While accurate, two-stage detectors were computationally heavy and struggled to run in real-time.
</p>
<p>
<strong>YOLO ("You Only Look Once")</strong> revolutionized the field as a <strong>One-Stage Detector</strong>: it passes the image through a single unified convolutional neural network once, predicting bounding box locations and class probabilities across the entire image simultaneously.
</p>

<h2>3.2 The Three Structural Components of YOLO11</h2>
<p>
Modern YOLO architectures consist of three distinct functional modules:
</p>

<div class="callout callout-blue">
  <div class="callout-title">1. The Backbone (Feature Extractor)</div>
  The backbone consists of consecutive convolutional and residual blocks that progressively downsample the spatial resolution of the image (from 640×640 down to 20×20) while expanding the number of feature channels (from 3 to 256). In YOLO11, this is powered by <strong>C3k2 blocks</strong> (an optimized Cross-Stage Partial network) and <strong>SPPF (Spatial Pyramid Pooling Fast)</strong>, which pools features at multiple pooling kernels (5×5, 9×9, 13×13) to capture global context without slowing inference.
</div>

<div class="callout callout-green">
  <div class="callout-title">2. The Neck (Multi-Scale Feature Aggregator)</div>
  Small objects are best detected in high-resolution, early layers; large objects require deep, low-resolution layers with large receptive fields. The Neck uses a combination of <strong>Feature Pyramid Network (FPN)</strong> (top-down path) and <strong>Path Aggregation Network (PAN)</strong> (bottom-up path) to fuse shallow spatial textures with deep semantic context. This produces three distinct prediction grids:
  <ul style="margin: 6px 0 0 0; padding-left: 20px;">
    <li><strong>P3 (80 × 80 grid):</strong> Dedicated to tiny objects (e.g. distant signs, small sports balls).</li>
    <li><strong>P4 (40 × 40 grid):</strong> Dedicated to medium objects (e.g. pedestrians, bicycles).</li>
    <li><strong>P5 (20 × 20 grid):</strong> Dedicated to massive foreground objects (e.g. buses, buildings).</li>
  </ul>
</div>

<div class="callout callout-amber">
  <div class="callout-title">3. The Head (Decoupled Anchor-Free Detector)</div>
  In traditional older detectors (YOLOv3, YOLOv5), the head used a single shared convolutional branch to predict class, box, and objectness simultaneously. YOLO11 uses a <strong>Decoupled Head</strong>: classification and box localization are split into two independent pathways. Why? Because the features required to determine <em>"What is this?"</em> (color, texture) are fundamentally in conflict with the features required to determine <em>"Where are the exact edges?"</em> (contrast, gradients).
</div>

<h2>3.3 Anchor-Based vs. Anchor-Free Architecture</h2>
<p>
Previous generations of YOLO relied on predefined <strong>Anchor Boxes</strong>—candidate boxes of hand-crafted aspect ratios (e.g. tall for people, wide for cars) placed across every grid cell. The model had to predict small offsets from these candidate templates.
</p>
<p>
<strong>YOLO11 is completely Anchor-Free:</strong> It treats every grid cell as a point location and directly predicts the 4 continuous distances from that point to the top, bottom, left, and right boundaries $(l, r, t, b)$. This eliminates thousands of hyperparameters, reduces memory consumption on small GPUs, and generalizes significantly better across diverse aspect ratios.
</p>

<h2>3.4 The Miracle of 2.6M Parameters</h2>
<p>
Our model contains exactly <strong>2,807,403 parameters</strong>, resulting in a compiled weights file of only <strong>5.51 MB</strong>. To put this in perspective:
</p>
<ul>
  <li>Meta's LLaMA 3 8B contains 8,000,000,000 parameters (~16,000 MB).</li>
  <li>ResNet-50 contains 25,600,000 parameters (~100 MB).</li>
  <li><strong>YOLO11n</strong> manages to classify <strong>601 classes</strong> and locate multiple objects in <strong>11.7 milliseconds</strong> using only <strong>2.8M parameters</strong>!</li>
</ul>

<!-- ================= CHAPTER 4 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 4</div>
  The Mathematics of Loss Functions
</h1>

<p>
During training, the model makes thousands of predictions on each batch of images. The <strong>Loss Function</strong> is the mathematical penalty score comparing the model's guesses to the ground-truth annotations. The goal of training is to drive this score down using gradient descent. In YOLO11, the total loss is a weighted sum of three distinct components:
</p>

<div class="math-box">
  \mathcal{L}_{\text{total}} = \lambda_{\text{box}} \mathcal{L}_{\text{CIoU}} + \lambda_{\text{cls}} \mathcal{L}_{\text{cls}} + \lambda_{\text{dfl}} \mathcal{L}_{\text{DFL}}
</div>

<h2>4.1 Classification Loss ($\mathcal{L}_{\text{cls}}$)</h2>
<p>
Traditional multi-class classification uses the <strong>Softmax</strong> function, which assumes all classes are mutually exclusive (if an object is a Dog, it cannot be a Cat). However, in Open Images V6, labels are hierarchical: an object can simultaneously be a <strong>Person</strong>, a <strong>Man</strong>, and a <strong>Boy</strong>.
</p>
<p>
Therefore, YOLO11 uses <strong>Binary Cross-Entropy (BCE) with Sigmoid</strong> for each of the 601 classes independently:
</p>
<div class="math-box">
  \mathcal{L}_{\text{cls}} = -\sum_{c=1}^{601} \Big[ y_c \log(\sigma(\hat{y}_c)) + (1 - y_c) \log(1 - \sigma(\hat{y}_c)) \Big]
</div>
<p>
Where $y_c \in \{0, 1\}$ is whether the object belongs to class $c$, and $\sigma(\hat{y}_c)$ is the predicted probability. Over 30 epochs, our classification loss plunged from <strong>3.3083 down to 1.8377</strong>—a drop of nearly 1.5 points.
</p>

<h2>4.2 Box Localization Loss ($\mathcal{L}_{\text{CIoU}}$)</h2>
<p>
Why don't we use simple Mean Squared Error (MSE) like $|x_{\text{pred}} - x_{\text{true}}|^2$ to measure bounding box error? Because a 5-pixel error on a huge 500-pixel bus is virtually unnoticeable, but a 5-pixel error on a tiny 10-pixel bottle completely misses the object! Coordinate loss must be <strong>scale-invariant</strong>.
</p>
<p>
YOLO11 utilizes <strong>Complete Intersection over Union (CIoU) Loss</strong>. CIoU measures three geometric factors simultaneously:
</p>
<div class="math-box">
  \mathcal{L}_{\text{CIoU}} = 1 - \text{IoU} + \frac{\rho^2(b, b^{\text{gt}})}{c^2} + \alpha v
</div>
<ol>
  <li><strong>Overlap Area (1 - IoU):</strong> Maximizes the overlapping pixel area between prediction and truth.</li>
  <li><strong>Center Point Distance ($\frac{\rho^2}{c^2}$):</strong> Penalizes predictions whose center points are far from the ground truth, normalized by the diagonal length $c$ of the smallest enclosing box.</li>
  <li><strong>Aspect Ratio Consistency ($\alpha v$):</strong> Penalizes boxes that have the wrong width-to-height proportion compared to ground truth.</li>
</ol>
<p>
This ensures that the predicted boxes do not just overlap the object, but align tightly to its physical boundaries. Our validation box loss improved consistently from <strong>1.5772 down to 1.4248</strong>.
</p>

<h2>4.3 Distribution Focal Loss ($\mathcal{L}_{\text{DFL}}$)</h2>
<p>
This is one of the most innovative breakthroughs in modern computer vision.
</p>
<p>
In traditional regression, a neural network is forced to output a single definitive scalar for each coordinate (e.g. <em>"Left boundary = 42.4 pixels"</em>). But real-world edges in photographs are often blurry, shadowed, or occluded. Forcing a network to choose one exact number causes gradient instability.
</p>
<p>
<strong>Distribution Focal Loss (DFL)</strong> changes the problem: instead of predicting a single scalar, the network outputs a <strong>continuous probability distribution</strong> over a range of discrete bins around the boundary! The final predicted coordinate is computed as the mathematical expectation:
</p>
<div class="math-box">
  \hat{x} = \sum_{i=0}^{N} P(y_i) \cdot y_i
</div>
<p>
If a boundary is crystal clear (like the sharp outline of a billboard), the probability distribution collapses into a sharp spike. If a boundary is blurry (like hair or foliage), the distribution broadens, reflecting spatial uncertainty. Our DFL loss declined from <strong>1.5859 to 1.4157</strong>, producing noticeably sharper bounding box edges.
</p>

<!-- ================= CHAPTER 5 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 5</div>
  How We Measure Success: Evaluation Metrics
</h1>

<h2>5.1 Precision vs. Recall (The Fundamental Trade-off)</h2>
<p>
Whenever the model evaluates an image, its detections are classified into three outcomes against the ground truth:
</p>
<ul>
  <li><strong>True Positive (TP):</strong> The model predicted an object that actually exists and correctly overlapped it (IoU ≥ threshold).</li>
  <li><strong>False Positive (FP):</strong> The model predicted an object where none exists (a "hallucination" or false alarm).</li>
  <li><strong>False Negative (FN):</strong> An actual ground-truth object was missed by the model.</li>
</ul>

<div class="two-col">
  <div class="col">
    <h3 style="margin-top:0;">Precision (Accuracy of Detections)</h3>
    <div class="math-box" style="margin:8px 0; font-size:10pt;">
      \text{Precision} = \frac{TP}{TP + FP}
    </div>
    <p style="font-size:9pt; margin:0;">
      <em>"When the detector claims an object is a Car, how often is it actually a Car?"</em> High precision means very few false alarms.
    </p>
  </div>
  <div class="col">
    <h3 style="margin-top:0;">Recall (Coverage of Detections)</h3>
    <div class="math-box" style="margin:8px 0; font-size:10pt;">
      \text{Recall} = \frac{TP}{TP + FN}
    </div>
    <p style="font-size:9pt; margin:0;">
      <em>"Out of all 54,000 real objects present in the images, how many did the detector find?"</em> High recall means very few missed targets.
    </p>
  </div>
</div>

<p>
There is an unavoidable engineering trade-off:
</p>
<ul>
  <li>If you set a high confidence threshold (e.g. <code>conf=0.80</code>), the model only flags objects it is 100% sure about. <strong>Precision rises, but Recall plummets</strong> because many valid objects are ignored.</li>
  <li>If you set a low confidence threshold (e.g. <code>conf=0.05</code>), the model detects almost every object. <strong>Recall soars, but Precision plummets</strong> due to false alarms on background textures.</li>
</ul>

<h2>5.2 mAP (Mean Average Precision) Explained</h2>
<p>
Because picking a single confidence threshold is arbitrary, the computer vision community evaluates models using the <strong>Precision-Recall Curve (PR Curve)</strong>. By varying the confidence threshold from 1.0 down to 0.0, we plot Precision against Recall.
</p>
<p>
The area under this curve is the <strong>Average Precision (AP)</strong> for that class. Taking the mean across all 601 classes yields the <strong>mAP (Mean Average Precision)</strong>.
</p>

<h3>What is mAP@50?</h3>
<p>
<strong>mAP@50</strong> is the classic PASCAL VOC metric. A detection is counted as a True Positive if its bounding box overlaps the ground truth with an <strong>Intersection over Union (IoU) of at least 50%</strong> (0.50). 
</p>
<p>
Our project pushed mAP@50 from an initial baseline of <strong>5.25%</strong> up to <strong>13.18%</strong> in Phase 1, and ultimately to <strong>18.47%</strong> in Phase 2—a <strong>+251.8% cumulative improvement</strong>.
</p>

<h3>What is mAP@50-95?</h3>
<p>
<strong>mAP@50-95</strong> is the gold-standard COCO metric. Instead of testing at just 50% overlap, it computes the mAP at 10 distinct IoU thresholds:
</p>
<div class="math-box">
  \text{mAP@[0.50:0.95]} = \frac{1}{10} \Big[ \text{mAP}_{0.50} + \text{mAP}_{0.55} + \text{mAP}_{0.60} + \dots + \text{mAP}_{0.95} \Big]
</div>
<p>
At IoU 0.95, a box is only considered correct if 95% of its area perfectly matches the ground truth. This is an extremely rigorous test of boundary tightness. Our model advanced from <strong>3.37% to 12.16%</strong> (+260.8% gain), proving that the bounding boxes became remarkably sharp and well-aligned.
</p>

<!-- ================= CHAPTER 6 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 6</div>
  The Phase 2 Engineering Playbook
</h1>

<h2>6.1 Automatic Mixed Precision (AMP / FP16)</h2>
<p>
Standard deep learning calculations use 32-bit single-precision floating-point numbers (<code>FP32</code>). Each float consumes 4 bytes of memory:
</p>
<div class="math-box">
  \text{FP32: } 1 \text{ sign bit} + 8 \text{ exponent bits} + 23 \text{ mantissa bits} = 32 \text{ bits (4 bytes)}
</div>
<p>
By contrast, half-precision (<code>FP16</code>) consumes only 2 bytes:
</p>
<div class="math-box">
  \text{FP16: } 1 \text{ sign bit} + 5 \text{ exponent bits} + 10 \text{ mantissa bits} = 16 \text{ bits (2 bytes)}
</div>
<p>
<strong>Why AMP was mandatory for Phase 2:</strong><br>
Our GTX 1050 has only 3 GB of VRAM. Training in FP32 with batch size 8 caused immediate Out-of-Memory (OOM) crashes. Enabling AMP cut the memory footprint of weights and activations by ~40-50%, keeping VRAM usage at a rock-solid <strong>2.81 GB</strong>. 
</p>
<div class="callout callout-amber">
  <strong>Dynamic Loss Scaling:</strong> Because FP16 has a smaller dynamic range, extremely small gradient numbers can "underflow" to zero. AMP solves this by automatically multiplying the loss by a scaling factor during backpropagation, and scaling it back down before updating weights.
</div>

<h2>6.2 Cosine Annealing Learning Rate Scheduler</h2>
<p>
In Phase 1, the learning rate followed a simple linear decay. In Phase 2, we switched to a <strong>Cosine Annealing Scheduler</strong>:
</p>
<div class="math-box">
  \eta_t = \eta_{\text{min}} + \frac{1}{2}(\eta_{\text{max}} - \eta_{\text{min}})\left(1 + \cos\left(\frac{T_{\text{cur}}}{T_{\text{max}}}\pi\right)\right)
</div>
<p>
Rather than dropping sharply in a straight line, cosine decay decreases the learning rate slowly at first, accelerates during mid-training, and then gently glides down toward zero in the final epochs. This allows the optimizer (AdamW/SGD) to settle smoothly into the deepest, flattest minima of the loss landscape without bouncing out of optimal weights.
</p>

<h2>6.3 The Data Augmentation Trio</h2>
<p>
If a neural network sees the exact same images repeatedly, it memorizes individual pixel patterns rather than learning generalizable concepts. We deployed three complementary augmentations:
</p>
<ol>
  <li><strong>Mosaic Augmentation (1.0):</strong> Combines 4 different training images into a single 2×2 stitched canvas. This forces the model to detect objects at 4× smaller scale than usual, effectively quadrupling the apparent batch size and handling objects near boundaries.</li>
  <li><strong>Mixup Augmentation (0.1):</strong> Takes two random images and performs a linear alpha blend: $I_{\text{mix}} = \lambda I_1 + (1 - \lambda) I_2$. This softens class labels, preventing overconfident false positives.</li>
  <li><strong>Copy-Paste Augmentation (0.1):</strong> Randomly crops bounding box instances from one image and pastes them into another image, exposing the network to diverse background contexts.</li>
</ol>

<h2>6.4 The Mosaic Shutoff Secret (Last 2 Epochs)</h2>
<p>
While Mosaic is exceptional for learning general features, real-world images don't look like 4 pictures stitched together with synthetic cross-shaped seams. In the final stages, Mosaic introduces an artificial <strong>domain shift</strong> that degrades bounding box precision.
</p>
<p>
In Round 4, we configured <code>close_mosaic=2</code>. During Epochs 29 and 30, mosaic augmentation was automatically disabled. The model was trained purely on natural, uncropped images with clean borders. This single technique produced our final surge in mAP@50 (from 18.15% to <strong>18.47%</strong>) and drove validation box loss to its lowest level (<strong>1.4248</strong>).
</p>

<!-- ================= CHAPTER 7 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 7</div>
  Hardware Constraints & Edge Engineering
</h1>

<h2>7.1 The Reality of the NVIDIA GTX 1050 (3 GB VRAM)</h2>
<p>
Training deep vision models is typically conducted in industrial datacenters on clusters of NVIDIA A100 (80 GB) or H100 (80 GB) GPUs costing tens of thousands of dollars.
</p>
<p>
Our project was executed entirely on an entry-level consumer laptop equipped with an <strong>NVIDIA GeForce GTX 1050 (3 GB VRAM, Pascal GP107 architecture)</strong>. 
</p>

<table class="data-table">
  <thead>
    <tr>
      <th>Constraint</th>
      <th>The Threat</th>
      <th>Our Engineering Solution</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>3 GB VRAM Ceiling</strong></td>
      <td>Immediate CUDA Out-Of-Memory (OOM) crash during batch forward pass.</td>
      <td>FP16 mixed precision, batch size 8, lightweight 2.6M parameter Nano backbone.</td>
    </tr>
    <tr>
      <td><strong>PCIe Bandwidth Bottleneck</strong></td>
      <td>GPU sits idle waiting for CPU to read images from disk.</td>
      <td>Multithreaded PyTorch dataloaders (<code>workers=4</code>) with persistent memory pinning.</td>
    </tr>
    <tr>
      <td><strong>Thermal Limits (92°C)</strong></td>
      <td>Sustained 8-hour training blocks trigger automatic thermal downclocking.</td>
      <td>Propped chassis for ventilation; modular 5-epoch rounds preventing overnight runaway heat.</td>
    </tr>
  </tbody>
</table>

<h2>7.2 Why Local Edge Training Triumphed Over Cloud (Google Colab)</h2>
<p>
Earlier in the project, we experimented with migrating to Google Colab's cloud environment. However, free-tier cloud environments introduced crippling operational vulnerabilities:
</p>
<ul>
  <li><strong>Ephemeral Virtual Machines:</strong> Whenever a session timed out or disconnected, Colab wiped the entire <code>/content</code> filesystem, deleting 28 GB of downloaded images.</li>
  <li><strong>Mid-Epoch Quota Termination:</strong> Google Colab's usage limits frequently severed compute halfway through an epoch without saving checkpoints.</li>
  <li><strong>Deterministic Local Stability:</strong> By returning to the local GTX 1050, every epoch was saved deterministically to local NVMe storage. Interrupted runs could be resumed in 2 seconds with <code>--resume</code> without losing a single batch.</li>
</ul>

<!-- ================= CHAPTER 8 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 8</div>
  Real-Time Inference & Auto-Annotation Suite
</h1>

<h2>8.1 What Happens During Inference (11.7 Milliseconds)?</h2>
<p>
When an image (like <code>1.jpg</code>) is passed to <code>scripts/test_model.py</code>, the system completes three distinct stages in just <strong>11.7 milliseconds</strong> (~85 frames per second):
</p>
<ol>
  <li><strong>Pre-processing (47.8 ms):</strong> The image is resized to 640px while maintaining aspect ratio (letterboxing), normalized to $[0.0, 1.0]$, converted to tensor format, and loaded into GPU memory.</li>
  <li><strong>Neural Network Forward Pass (11.7 ms):</strong> The tensor passes through the 181 layers of YOLO11n. The network produces thousands of candidate bounding box predictions across the P3, P4, and P5 feature maps.</li>
  <li><strong>Non-Maximum Suppression / NMS (10.0 ms):</strong> Because adjacent grid cells often detect the same object, the raw output contains dozens of overlapping boxes for a single car. <strong>NMS</strong> sorts all boxes by confidence score, takes the highest-confidence box, and discards all other boxes that overlap it with an IoU above a threshold (typically 0.70).</li>
</ol>

<h2>8.2 The Dual Auto-Annotation Pipeline</h2>
<p>
Our test script (<code>scripts/test_model.py</code>) does not just draw colorful boxes on pictures—it functions as an <strong>Automated Machine Learning Annotation Engine</strong>. Passing <code>--save-txt</code> and <code>--save-json</code> generates two enterprise-standard formats:
</p>

<h3>1. Normalized YOLO Format (<code>labels/1.txt</code>)</h3>
<p>
Directly ingestible by CVAT, Label Studio, Roboflow, and PyTorch dataloaders for continuous active learning:
</p>
<pre><code>44 0.174400 0.856322 0.223507 0.287357 0.6492
582 0.171387 0.856792 0.226135 0.285731 0.6024
90 0.487245 0.641338 0.963691 0.717324 0.5417
381 0.559805 0.475330 0.199795 0.900450 0.3447</code></pre>

<h3>2. Structured JSON Format (<code>1_annotations.json</code>)</h3>
<p>
Clean, parseable metadata containing exact pixel coordinates, human-readable class names, and confidence probabilities for web APIs and robotics controllers:
</p>
<pre><code>{
  "image": "1.jpg",
  "num_detections": 12,
  "detections": [
    {
      "class_id": 90,
      "class_name": "Car",
      "confidence": 0.5417,
      "bbox_pixels_xyxy": [3.51, 116.75, 629.91, 413.0],
      "bbox_yolo_normalized_xywh": [0.487245, 0.641338, 0.963691, 0.717324]
    },
    {
      "class_id": 381,
      "class_name": "Person",
      "confidence": 0.3447,
      "bbox_pixels_xyxy": [298.94, 10.37, 428.81, 382.25],
      "bbox_yolo_normalized_xywh": [0.559805, 0.475330, 0.199795, 0.900450]
    }
  ]
}</code></pre>

<!-- ================= CHAPTER 9 ================= -->
<h1 class="chapter-header">
  <div class="chapter-tag">Chapter 9</div>
  The Master Glossary & Interview Defense Guide
</h1>

<p>
Use this authoritative glossary to explain any concept with absolute technical fluency in engineering discussions, technical presentations, or portfolio reviews:
</p>

<table class="data-table">
  <thead>
    <tr>
      <th style="width:25%;">Term / Acronym</th>
      <th>Plain-English Definition & Context in Our Project</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>AMP (Automatic Mixed Precision)</strong></td>
      <td>A PyTorch training technique that executes specific operations in 16-bit half-precision (FP16) while keeping critical weights in 32-bit (FP32). Cuts VRAM consumption by ~40-50% to prevent GPU memory crashes.</td>
    </tr>
    <tr>
      <td><strong>Anchor-Free</strong></td>
      <td>Modern object detection architecture that directly predicts bounding box edge offsets from feature grid centers, avoiding predefined template shapes (anchor boxes). Used in YOLO11.</td>
    </tr>
    <tr>
      <td><strong>Backbone</strong></td>
      <td>The initial feature-extraction convolutional layers of a network (e.g. C3k2 blocks in YOLO11) that transform raw image pixels into dense abstract visual embeddings.</td>
    </tr>
    <tr>
      <td><strong>BCE Loss (Binary Cross-Entropy)</strong></td>
      <td>Loss function used for classification across independent binary outputs. In our 601-class hierarchy, it allows an object to belong to multiple classes at once (e.g. "Man" and "Person").</td>
    </tr>
    <tr>
      <td><strong>CIoU (Complete IoU)</strong></td>
      <td>An advanced bounding box loss function that penalizes lack of overlap, center-point displacement, and aspect ratio discrepancy simultaneously.</td>
    </tr>
    <tr>
      <td><strong>Cosine Annealing</strong></td>
      <td>A learning rate schedule that decreases the learning rate along a smooth cosine curve, enabling gentle convergence into optimal parameter minima.</td>
    </tr>
    <tr>
      <td><strong>DFL (Distribution Focal Loss)</strong></td>
      <td>A regression loss that models bounding box coordinates as probability distributions over discrete bins rather than fixed scalars, handling blurry or occluded edges.</td>
    </tr>
    <tr>
      <td><strong>Epoch</strong></td>
      <td>One complete pass through the entire training dataset (85,000 images in our curriculum). 30 epochs = 2,550,000 training image evaluations.</td>
    </tr>
    <tr>
      <td><strong>FP16 vs. FP32</strong></td>
      <td>16-bit vs 32-bit floating point representations. FP16 uses 2 bytes per number; FP32 uses 4 bytes. Half-precision doubles tensor processing throughput on modern GPUs.</td>
    </tr>
    <tr>
      <td><strong>IoU (Intersection over Union)</strong></td>
      <td>The ratio of the area of overlap between two boxes to their total combined area. 0.0 means no contact; 1.0 means identical alignment.</td>
    </tr>
    <tr>
      <td><strong>Long-Tail Distribution</strong></td>
      <td>A dataset phenomenon where a few common classes have abundant examples, while hundreds of rare classes have very few, skewing the learning signal.</td>
    </tr>
    <tr>
      <td><strong>mAP@50</strong></td>
      <td>Mean Average Precision evaluated at an IoU threshold of 0.50. Measures how accurately the model detects objects when 50% overlap is required. Our model reached 18.47%.</td>
    </tr>
    <tr>
      <td><strong>mAP@50-95</strong></td>
      <td>The average mAP across 10 increasing IoU thresholds (0.50 to 0.95). The definitive benchmark of boundary tightness. Our model achieved 12.16%.</td>
    </tr>
    <tr>
      <td><strong>Mosaic Augmentation</strong></td>
      <td>Stitching 4 random images into one canvas during training. Forces the model to locate objects at 4× smaller scale and handles edge-boundary cutoffs.</td>
    </tr>
    <tr>
      <td><strong>Neck</strong></td>
      <td>The intermediate feature pyramid network (FPN + PAN) connecting the backbone to the head, fusing multi-scale feature maps so the model detects small and large objects.</td>
    </tr>
    <tr>
      <td><strong>NMS (Non-Maximum Suppression)</strong></td>
      <td>A post-processing clustering algorithm that eliminates duplicate, redundant bounding boxes around the same object by keeping only the highest-confidence prediction.</td>
    </tr>
    <tr>
      <td><strong>Precision</strong></td>
      <td>The fraction of predicted objects that were actually correct ($TP / (TP + FP)$). Measures the quality and confidence of detections (35.13% in our final model).</td>
    </tr>
    <tr>
      <td><strong>Recall</strong></td>
      <td>The fraction of all real ground-truth objects that the detector succeeded in finding ($TP / (TP + FN)$). Reached 23.94% across 601 classes in our final model.</td>
    </tr>
    <tr>
      <td><strong>VRAM (Video RAM)</strong></td>
      <td>Dedicated ultra-high-speed memory on the graphics card holding model weights, activations, and gradient tensors during training.</td>
    </tr>
  </tbody>
</table>

</body>
</html>
"""

def generate_pdf():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Write HTML
    print(f"Writing Masterclass HTML to: {HTML_OUT}")
    HTML_OUT.write_text(HTML_CONTENT, encoding="utf-8")
    
    # 2. Compile to PDF using Microsoft Edge headless
    print(f"Compiling PDF via Microsoft Edge Headless...")
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={PDF_OUT}",
        str(HTML_OUT)
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and PDF_OUT.exists():
        size_kb = PDF_OUT.stat().st_size / 1024
        print(f"SUCCESS: Generated PDF at {PDF_OUT} ({size_kb:.1f} KB)")
    else:
        print(f"ERROR generating PDF: {res.stderr}")

if __name__ == "__main__":
    generate_pdf()
