"""
Phase 2 Round-Based Training Script
=====================================
Trains 5 epochs per round, resuming from previous checkpoint.

Rounds:
  Round 1: Epochs 11-15  (resume from Phase 1 best.pt)
  Round 2: Epochs 16-20  (resume from Round 1 last.pt)
  Round 3: Epochs 21-25  (resume from Round 2 last.pt)
  Round 4: Epochs 26-30  (resume from Round 3 last.pt)

Usage:
  Round 1:  python scripts\train_phase2_local.py --round 1
  Round 2:  python scripts\train_phase2_local.py --round 2
  Resume:   python scripts\train_phase2_local.py --round 1 --resume
"""

import argparse
import os
import sys
import shutil
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_YAML  = PROJECT_ROOT / "data/yolo_dataset/dataset.yaml"
PHASE1_BEST   = PROJECT_ROOT / "runs/detect/runs/detect/epoch_10/weights/best.pt"
PHASE2_BASE   = PROJECT_ROOT / "runs/detect/phase2"

ROUND_CONFIG = {
    1: {"start": 11, "end": 15, "name": "round_1_epochs_11_15", "prev": None},
    2: {"start": 16, "end": 20, "name": "round_2_epochs_16_20", "prev": "round_1_epochs_11_15"},
    3: {"start": 21, "end": 25, "name": "round_3_epochs_21_25", "prev": "round_2_epochs_16_20"},
    4: {"start": 26, "end": 30, "name": "round_4_epochs_26_30", "prev": "round_3_epochs_21_25"},
}

def get_start_checkpoint(round_num, resume):
    cfg = ROUND_CONFIG[round_num]
    run_dir = PHASE2_BASE / cfg["name"]
    last_pt  = run_dir / "weights/last.pt"

    # Resume mid-round
    if resume and last_pt.exists():
        print(f"[RESUME] Resuming from {last_pt}")
        return str(last_pt), True

    # Round 1 starts from Phase 1 best
    if cfg["prev"] is None:
        if not PHASE1_BEST.exists():
            print(f"ERROR: Phase 1 checkpoint not found at {PHASE1_BEST}")
            sys.exit(1)
        print(f"[ROUND {round_num}] Starting from Phase 1 best.pt")
        return str(PHASE1_BEST), False

    # Subsequent rounds start from previous round's last.pt
    prev_last = PHASE2_BASE / cfg["prev"] / "weights/last.pt"
    if not prev_last.exists():
        print(f"ERROR: Previous round checkpoint not found: {prev_last}")
        print(f"       Complete Round {round_num - 1} first.")
        sys.exit(1)
    print(f"[ROUND {round_num}] Starting from Round {round_num-1}: {prev_last}")
    return str(prev_last), False


def main():
    parser = argparse.ArgumentParser(description="Phase 2 Round-Based Training")
    parser.add_argument("--round",  type=int, required=True, choices=[1,2,3,4],
                        help="Round number (1–4)")
    parser.add_argument("--resume", action="store_true",
                        help="Resume from last.pt if training was interrupted")
    parser.add_argument("--batch",  type=int, default=8,
                        help="Batch size (reduce to 4 if OOM)")
    parser.add_argument("--imgsz",  type=int, default=640)
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    cfg = ROUND_CONFIG[args.round]
    model_path, is_resume = get_start_checkpoint(args.round, args.resume)

    try:
        from ultralytics import YOLO
    except ImportError:
        os.system(f"{sys.executable} -m pip install -q ultralytics")
        from ultralytics import YOLO

    import torch
    if torch.cuda.is_available():
        gpu  = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"GPU: {gpu}  ({vram:.1f} GB VRAM)")
        device = 0
    else:
        print("WARNING: No GPU — training on CPU (very slow)")
        device = "cpu"

    epochs_in_round = cfg["end"] - cfg["start"] + 1   # always 5

    print(f"\n{'='*60}")
    print(f"  PHASE 2 — Round {args.round}  (Epochs {cfg['start']}–{cfg['end']})")
    print(f"  Epochs this run : {epochs_in_round}")
    print(f"  Batch / ImgSz   : {args.batch} / {args.imgsz}")
    print(f"  FP16            : ON")
    print(f"  Augmentation    : Mosaic + Mixup + CopyPaste")
    print(f"  LR Scheduler    : Cosine")
    print(f"{'='*60}\n")

    model = YOLO(model_path)

    train_kwargs = dict(
        data        = str(DATASET_YAML),
        epochs      = epochs_in_round,
        batch       = args.batch,
        imgsz       = args.imgsz,
        device      = device,
        workers     = 4,
        half        = True,          # FP16
        cos_lr      = True,          # Cosine LR
        mosaic      = 1.0,
        mixup       = 0.1,
        copy_paste  = 0.1,
        close_mosaic= 2,             # Disable mosaic last 2 epochs of round
        patience    = 0,             # No early stopping — run full 5 epochs
        save_period = 5,             # Save checkpoint at end of round
        project     = str(PHASE2_BASE),
        name        = cfg["name"],
        exist_ok    = True,
        plots       = True,
        verbose     = True,
    )
    if is_resume:
        train_kwargs["resume"] = True

    try:
        model.train(**train_kwargs)
        print(f"\n{'='*60}")
        print(f"  Round {args.round} COMPLETE — Epochs {cfg['start']}–{cfg['end']} done!")
        print(f"  Weights : {PHASE2_BASE / cfg['name'] / 'weights'}")
        print(f"  Results : {PHASE2_BASE / cfg['name'] / 'results.csv'}")
        print(f"\n  Next: generate artifacts then start Round {args.round + 1}" if args.round < 4 else
              f"\n  Phase 2 training COMPLETE (30 total epochs)!")
        print(f"{'='*60}\n")

    except RuntimeError as e:
        if "out of memory" in str(e).lower():
            print(f"\n{'!'*60}")
            print(f"  GPU OUT OF MEMORY! Try:")
            print(f"    python scripts\\train_phase2_local.py --round {args.round} --batch 4")
            print(f"{'!'*60}")
        else:
            raise


if __name__ == "__main__":
    main()
