import argparse
import os
from pathlib import Path
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Run 601-class object detection on an image using fine-tuned YOLO11n")
    parser.add_argument("--source", type=str, required=True, help="Path to input image or image URL")
    parser.add_argument("--model", type=str, default=r"runs\detect\runs\detect\epoch_10\weights\best.pt", help="Path to trained model weights")
    parser.add_argument("--conf", type=float, default=0.20, help="Confidence threshold (default: 0.20)")
    parser.add_argument("--show", action="store_true", help="Automatically open the annotated image upon completion")
    args = parser.parse_args()

    if not Path(args.model).exists():
        print(f"Error: Model weights not found at {args.model}")
        return

    print(f"Loading trained 601-class model from: {args.model}...")
    model = YOLO(args.model)

    print(f"Running inference on: {args.source} (conf={args.conf})...")
    results = model.predict(source=args.source, conf=args.conf, save=True)

    for r in results:
        saved_file = Path(r.save_dir) / Path(r.path).name
        print("\n" + "=" * 60)
        print(f"DETECTION COMPLETE: Found {len(r.boxes)} objects")
        print(f"Annotated image saved to: {saved_file.resolve()}")
        print("=" * 60)

        # Print detected class breakdown
        if len(r.boxes) > 0:
            counts = {}
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                counts[cls_name] = counts.get(cls_name, 0) + 1
            print("Detected objects breakdown:")
            for cls_name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {cls_name}: {count}")

        if args.show:
            print("\nOpening image...")
            os.startfile(saved_file)

if __name__ == "__main__":
    main()
