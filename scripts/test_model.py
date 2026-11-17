"""
Test & Auto-Annotation Script for Phase 2 YOLO11 Model
======================================================
Runs object detection inference and can export annotations in:
  - Standard YOLO format (.txt)
  - Human-readable JSON format (.json)

Usage:
  # Test with annotated image + standard YOLO .txt label file:
  python scripts/test_model.py --source 1.jpg --save-txt

  # Test and export human-readable JSON annotations (with class names & pixel boxes):
  python scripts/test_model.py --source 1.jpg --save-json

  # Both formats:
  python scripts/test_model.py --source 1.jpg --save-txt --save-json
"""

import argparse
import json
import sys
from pathlib import Path
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Test and Auto-Annotate with Phase 2 YOLO")
    parser.add_argument("--source", type=str, default="1.jpg", help="Path to image, video, or folder")
    parser.add_argument("--weights", type=str,
                        default="runs/detect/phase2/round_4_epochs_26_30/weights/best.pt",
                        help="Path to trained model weights")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold (default 0.25)")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference resolution")
    parser.add_argument("--save-txt", action="store_true", help="Save standard YOLO format .txt annotations")
    parser.add_argument("--save-json", action="store_true", help="Save human-readable .json annotations")
    parser.add_argument("--device", default=0, help="CUDA device (0) or cpu")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    weights_path = project_root / args.weights
    source_path = Path(args.source)
    if not source_path.is_absolute():
        source_path = project_root / source_path

    if not weights_path.exists():
        print(f"ERROR: Weights not found at {weights_path}")
        sys.exit(1)
    if not source_path.exists():
        print(f"ERROR: Source not found at {source_path}")
        sys.exit(1)

    print(f"\n{'='*65}")
    print(f"  PHASE 2 MODEL INFERENCE & AUTO-ANNOTATION")
    print(f"  Weights   : {weights_path.relative_to(project_root)}")
    print(f"  Source    : {source_path.name}")
    print(f"  Conf      : {args.conf}")
    print(f"  Save TXT  : {args.save_txt}")
    print(f"  Save JSON : {args.save_json}")
    print(f"{'='*65}\n")

    model = YOLO(str(weights_path))
    results = model.predict(
        source=str(source_path),
        conf=args.conf,
        imgsz=args.imgsz,
        device=args.device,
        save=True,
        save_txt=args.save_txt,
        save_conf=True
    )

    r = results[0]
    boxes = r.boxes
    print(f"Detected {len(boxes)} objects in {source_path.name}:")

    detections = []
    for b in boxes:
        cls_id = int(b.cls[0])
        name = model.names[cls_id]
        conf = float(b.conf[0])
        xyxy = [round(float(coord), 2) for coord in b.xyxy[0]]
        xywh_norm = [round(float(coord), 6) for coord in b.xywhn[0]]

        detections.append({
            "class_id": cls_id,
            "class_name": name,
            "confidence": round(conf, 4),
            "bbox_pixels_xyxy": xyxy,
            "bbox_yolo_normalized_xywh": xywh_norm
        })
        print(f"  - {name:<22} conf: {conf:.2f}  box: {xyxy}")

    save_dir = Path(r.save_dir)
    print(f"\nOutputs:")
    print(f"  - Annotated Image : {save_dir / source_path.name}")

    if args.save_txt:
        txt_path = save_dir / "labels" / f"{source_path.stem}.txt"
        print(f"  - YOLO .txt File  : {txt_path}")

    if args.save_json:
        json_path = save_dir / f"{source_path.stem}_annotations.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "image": source_path.name,
                "num_detections": len(detections),
                "detections": detections
            }, f, indent=2)
        print(f"  - JSON Annotations: {json_path}")
    print()

if __name__ == "__main__":
    main()
