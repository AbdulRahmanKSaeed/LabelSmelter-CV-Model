"""
train_detector.py - Production Training Pipeline for Open Images V6 600-Class Object Detection

Supports:
- Automatic hardware detection (NVIDIA CUDA GPU with VRAM check vs CPU)
- Ultralytics YOLO11 / YOLOv8 architecture
- Configurable dataset fraction (e.g., 0.01 for fast smoke testing / validation)
- VRAM-friendly defaults for consumer GPUs (e.g. GTX 1050 3GB)
- Disk space safety monitoring
- Progress tracking and checkpoint metrics logging
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime

def check_disk_space(min_free_gb=5.0):
    """Verify sufficient disk space is available before/during training."""
    total, used, free = shutil.disk_usage(Path.cwd())
    free_gb = free / (1024 ** 3)
    print(f"[Storage Check] Free space: {free_gb:.2f} GB (minimum required: {min_free_gb:.1f} GB)")
    if free_gb < min_free_gb:
        raise RuntimeError(f"Insufficient disk space: {free_gb:.2f} GB free, require at least {min_free_gb:.1f} GB.")
    return free_gb

def get_optimal_device():
    """Detect PyTorch device (CUDA GPU or CPU) with memory details."""
    import torch
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_total_mb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 2)
        print(f"[Device] CUDA GPU detected: {gpu_name} ({vram_total_mb:.0f} MB VRAM)")
        return "0", vram_total_mb
    else:
        print("[Device] No CUDA GPU available. Using CPU (training will be slower).")
        return "cpu", 0

def main():
    parser = argparse.ArgumentParser(description="Train YOLO Object Detector on Open Images V6 600-Class Subset")
    parser.add_argument("--data", type=str, default="data/yolo_dataset/dataset.yaml", help="Path to dataset.yaml")
    parser.add_argument("--model", type=str, default="yolo11n.pt", help="Base model weights (e.g. yolo11n.pt, yolov8n.pt)")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=8, help="Batch size (-1 for autobatch, 4 or 8 recommended for 3GB VRAM)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image resolution (640 or 416 for lower VRAM)")
    parser.add_argument("--device", type=str, default="auto", help="Compute device ('auto', '0', or 'cpu')")
    parser.add_argument("--workers", type=int, default=4, help="Dataloader worker threads")
    parser.add_argument("--fraction", type=float, default=1.0, help="Dataset fraction to use (e.g. 0.01 for 1% smoke test, 1.0 for full 100k)")
    parser.add_argument("--project", type=str, default="runs/detect", help="Output directory for training runs")
    parser.add_argument("--name", type=str, default="openimages_600_v1", help="Run name inside project directory")
    parser.add_argument("--resume", action="store_true", help="Resume training from previous checkpoint")
    parser.add_argument("--save-period", type=int, default=1, help="Save checkpoint every N epochs")
    parser.add_argument("--patience", type=int, default=10, help="Early stopping patience (epochs without improvement)")
    parser.add_argument("--dry-run", action="store_true", help="Perform setup and validation checks without starting training")

    args = parser.parse_args()

    print("=" * 70)
    print("   OPEN IMAGES V6 (600-CLASS) OBJECT DETECTION TRAINING PIPELINE   ")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {Path.cwd()}")

    # 1. Storage check
    check_disk_space(min_free_gb=5.0)

    # 2. Check dataset config
    data_path = Path(args.data).resolve()
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset config not found at: {data_path}")
    print(f"[Dataset Config] Found: {data_path}")

    # 3. Check Ultralytics and PyTorch
    import torch
    from ultralytics import YOLO

    print(f"[PyTorch Version] {torch.__version__}")

    # 4. Determine device
    if args.device == "auto":
        device, vram_mb = get_optimal_device()
    else:
        device = args.device
        vram_mb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 2) if device == "0" and torch.cuda.is_available() else 0
        print(f"[Device] User specified device: {device}")

    # Adjust batch size for small VRAM GPUs (GTX 1050 3GB)
    batch_size = args.batch
    if device != "cpu" and vram_mb > 0 and vram_mb <= 3500:
        if batch_size > 8:
            print(f"[VRAM Warning] GPU has {vram_mb:.0f} MB VRAM. Clamping batch size from {batch_size} to 8 to avoid CUDA OOM.")
            batch_size = 8

    # 5. Model instantiation
    print(f"[Model] Initializing architecture: {args.model}")
    model = YOLO(args.model)

    print("\nTraining Configuration:")
    print(f"  - Dataset Config: {data_path}")
    print(f"  - Model:          {args.model}")
    print(f"  - Device:         {device}")
    print(f"  - Epochs:         {args.epochs}")
    print(f"  - Batch Size:     {batch_size}")
    print(f"  - Image Size:     {args.imgsz}")
    print(f"  - Dataloader Workers: {args.workers}")
    print(f"  - Dataset Fraction:   {args.fraction * 100:.2f}% ({int(85000 * args.fraction):,} train images)")
    print(f"  - Output Dir:     {Path(args.project) / args.name}")
    print(f"  - Save Period:    Every {args.save_period} epoch(s)")
    print("=" * 70)

    if args.dry_run:
        print("[Dry Run] All checks passed successfully. Exiting without training.")
        return

    # 6. Launch training
    print("\nStarting training session...")
    results = model.train(
        data=str(data_path),
        epochs=args.epochs,
        batch=batch_size,
        imgsz=args.imgsz,
        device=device,
        workers=args.workers,
        fraction=args.fraction,
        project=args.project,
        name=args.name,
        resume=args.resume,
        save_period=args.save_period,
        patience=args.patience,
        cache=False,        # Memory safety: do not load all 100k images into 16GB RAM
        plots=True,
        verbose=True,
        amp=True if device != "cpu" else False,  # Automatic mixed precision for GPU
    )

    print("\n" + "=" * 70)
    print("TRAINING SESSION COMPLETE!")
    print("=" * 70)

    save_dir = Path(results.save_dir) if hasattr(results, "save_dir") else Path(args.project) / args.name
    best_weights = save_dir / "weights" / "best.pt"
    last_weights = save_dir / "weights" / "last.pt"

    print(f"Run outputs saved to: {save_dir}")
    if best_weights.exists():
        print(f"Best Model Weights: {best_weights} ({best_weights.stat().st_size / (1024**2):.2f} MB)")
    if last_weights.exists():
        print(f"Final Model Weights: {last_weights} ({last_weights.stat().st_size / (1024**2):.2f} MB)")

if __name__ == "__main__":
    main()
