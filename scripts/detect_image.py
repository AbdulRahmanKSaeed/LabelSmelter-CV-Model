import argparse
import os
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Run 601-class object detection on an image using fine-tuned YOLO11n")
    parser.add_argument("--source", type=str, default="images.jfif", help="Path to input image (default: images.jfif)")
    parser.add_argument("--model", type=str, default=r"runs\detect\runs\detect\epoch_10\weights\best.pt", help="Path to trained model weights")
    parser.add_argument("--conf", type=float, default=0.15, help="Confidence threshold (default: 0.15)")
    parser.add_argument("--show", action="store_true", help="Automatically open the annotated image upon completion")
    args = parser.parse_args()

    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Error: Model weights not found at {model_path}")
        return

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Image source not found at {source_path}")
        return

    print(f"Loading trained 601-class model from: {model_path}...")
    model = YOLO(str(model_path))

    # Pre-open image with PIL to guarantee compatibility with .jfif, .webp, .png, etc.
    try:
        input_data = Image.open(source_path)
    except Exception:
        input_data = str(source_path)

    print(f"Running inference on '{source_path.name}' (conf={args.conf})...")
    results = model.predict(source=input_data, conf=args.conf, save=True)

    for r in results:
        save_dir = Path(r.save_dir)
        # Find the saved annotated image in save_dir
        candidates = list(save_dir.glob(f"{source_path.stem}.*"))
        if candidates:
            saved_file = candidates[0]
        else:
            files = sorted(save_dir.glob("*.*"), key=lambda p: p.stat().st_mtime, reverse=True)
            saved_file = files[0] if files else save_dir

        print("\n" + "=" * 60)
        print(f"DETECTION COMPLETE: Found {len(r.boxes)} objects")
        print(f"Annotated output saved to: {saved_file.resolve()}")
        print("=" * 60)

        if len(r.boxes) > 0:
            counts = {}
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                counts[cls_name] = counts.get(cls_name, 0) + 1
            print("Detected objects breakdown:")
            for cls_name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {cls_name}: {count}")

        if args.show and saved_file.is_file():
            print("\nOpening image...")
            os.startfile(saved_file)

if __name__ == "__main__":
    main()
