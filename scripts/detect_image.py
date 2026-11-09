import argparse
import os
import re
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

def resolve_target_classes(query_str, model_names):
    """
    Parses user query (e.g., 'man, building, car') and maps to model class IDs.
    Uses whole-word matching first, falling back to substring matching.
    """
    if not query_str or query_str.strip().lower() in ("all", "*", ""):
        return None, []

    terms = [t.strip().lower() for t in query_str.split(",") if t.strip()]
    matched_ids = set()
    matched_names = []

    for term in terms:
        # 1. Whole word match (e.g. 'man' -> 'Man', not 'Human')
        word_matches = [
            (idx, name) for idx, name in model_names.items()
            if re.search(rf"\b{re.escape(term)}\b", name.lower())
        ]
        # 2. Substring match fallback if no whole word match
        if not word_matches:
            word_matches = [
                (idx, name) for idx, name in model_names.items()
                if term in name.lower()
            ]

        for idx, name in word_matches:
            matched_ids.add(idx)
            if name not in matched_names:
                matched_names.append(name)

    return list(matched_ids), matched_names

def main():
    parser = argparse.ArgumentParser(description="Targeted 601-class object detection using fine-tuned YOLO11n")
    parser.add_argument("--source", type=str, default=None, help="Path to input image (e.g. images.jfif)")
    parser.add_argument("--targets", type=str, default=None, help="Comma-separated classes to look for (e.g. 'man, building')")
    parser.add_argument("--model", type=str, default=r"runs\detect\runs\detect\epoch_10\weights\best.pt", help="Path to model weights")
    parser.add_argument("--conf", type=float, default=0.15, help="Confidence threshold (default: 0.15)")
    parser.add_argument("--show", action="store_true", help="Automatically open the annotated image")
    parser.add_argument("--interactive", action="store_true", help="Prompt interactively for image and target classes")
    args = parser.parse_args()

    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Error: Model weights not found at {model_path}")
        return

    print(f"Loading trained 601-class model from: {model_path}...")
    model = YOLO(str(model_path))

    source_input = args.source
    targets_query = args.targets

    # If interactive mode or no arguments provided, prompt user
    if args.interactive or (args.source is None and args.targets is None):
        print("\n" + "=" * 60)
        print(" INTERACTIVE DETECTION SETUP ")
        print("=" * 60)
        user_src = input("1. Enter image path [default: images.jfif]: ").strip()
        source_input = user_src if user_src else "images.jfif"

        print("\n2. What do you want to find?")
        print("   (Enter comma-separated targets like 'man, building' or press Enter to find everything)")
        targets_query = input("   Target(s): ").strip()

    if not source_input:
        source_input = "images.jfif"

    source_path = Path(source_input)
    if not source_path.exists():
        print(f"Error: Image source not found at '{source_path}'")
        return

    # Filter target classes
    class_ids, matched_names = resolve_target_classes(targets_query, model.names)

    if class_ids is not None:
        if len(class_ids) == 0:
            print(f"\n[Warning] No matching classes found for query: '{targets_query}'. Scanning all 601 classes instead.")
            class_ids = None
        else:
            print(f"\n[Target Filter Active] Looking ONLY for: {', '.join(matched_names)} (IDs: {class_ids})")
    else:
        print("\n[Scanning All] No filter specified. Scanning across all 601 classes.")

    # Load image safely
    try:
        input_data = Image.open(source_path)
    except Exception:
        input_data = str(source_path)

    print(f"Running inference on '{source_path.name}' (conf={args.conf})...")
    results = model.predict(source=input_data, classes=class_ids, conf=args.conf, save=True)

    for r in results:
        save_dir = Path(r.save_dir)
        candidates = list(save_dir.glob(f"{source_path.stem}.*"))
        saved_file = candidates[0] if candidates else sorted(save_dir.glob("*.*"), key=lambda p: p.stat().st_mtime, reverse=True)[0]

        print("\n" + "=" * 60)
        print(f"DETECTION COMPLETE: Found {len(r.boxes)} target objects")
        print(f"Annotated output saved to: {saved_file.resolve()}")
        print("=" * 60)

        if len(r.boxes) > 0:
            counts = {}
            for box in r.boxes:
                cls_id = int(box.cls[0])
                cls_name = model.names[cls_id]
                counts[cls_name] = counts.get(cls_name, 0) + 1
            print("Detected target breakdown:")
            for cls_name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {cls_name}: {count}")
        else:
            print("No matching objects detected above confidence threshold.")

        # In interactive mode, default show to True if on Windows
        if args.show or args.interactive:
            print("\nOpening annotated result...")
            os.startfile(saved_file)

if __name__ == "__main__":
    main()
