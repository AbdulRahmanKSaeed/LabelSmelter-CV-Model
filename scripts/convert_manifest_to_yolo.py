"""
Convert approved subset annotations to YOLO format for model training.

Reads:
- data/manifests/selected_images_manifest.csv
- data/annotations/train-annotations-bbox.csv
- data/annotations/class-descriptions-boxable.csv

Generates:
- data/yolo_dataset/labels/train/*.txt
- data/yolo_dataset/labels/val/*.txt
- data/yolo_dataset/dataset.yaml
- data/yolo_dataset/class_mapping.json
- data/yolo_dataset/dataset_summary.json
"""

import os
import sys
import csv
import json
import argparse
from collections import Counter, defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNO_DIR = os.path.join(PROJECT_ROOT, "data", "annotations")
MANIFEST_DIR = os.path.join(PROJECT_ROOT, "data", "manifests")
YOLO_DIR = os.path.join(PROJECT_ROOT, "data", "yolo_dataset")


def load_classes(class_desc_path):
    mid_to_name = {}
    with open(class_desc_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                mid_to_name[row[0].strip()] = row[1].strip()

    # Sort alphabetically by class name for deterministic index assignment (0..599)
    sorted_mids = sorted(list(mid_to_name.keys()), key=lambda m: mid_to_name[m].lower())
    mid_to_idx = {mid: idx for idx, mid in enumerate(sorted_mids)}
    idx_to_name = {idx: mid_to_name[mid] for mid, idx in mid_to_idx.items()}
    return mid_to_name, mid_to_idx, idx_to_name, sorted_mids


def main():
    parser = argparse.ArgumentParser(description="Convert approved manifest annotations to YOLO format")
    parser.add_argument("--manifest", type=str, default=os.path.join(MANIFEST_DIR, "selected_images_manifest.csv"))
    parser.add_argument("--anno-file", type=str, default=os.path.join(ANNO_DIR, "train-annotations-bbox.csv"))
    parser.add_argument("--output-dir", type=str, default=YOLO_DIR)
    args = parser.parse_args()

    print("=" * 75)
    print("Open Images Subset -> YOLO Annotation Converter")
    print("=" * 75)

    class_desc_path = os.path.join(ANNO_DIR, "class-descriptions-boxable.csv")
    mid_to_name, mid_to_idx, idx_to_name, sorted_mids = load_classes(class_desc_path)
    print(f"Loaded {len(mid_to_name)} boxable classes.")

    # Read selected manifest
    target_images = {}  # img_id -> split ('train' or 'val')
    with open(args.manifest, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_id = row["ImageID"].strip()
            split = row.get("Split", "train").strip()
            target_images[img_id] = split

    print(f"Loaded manifest with {len(target_images):,} selected images.")
    train_ids = {k for k, v in target_images.items() if v == "train"}
    val_ids = {k for k, v in target_images.items() if v == "val"}
    print(f"  Training:   {len(train_ids):,} images")
    print(f"  Validation: {len(val_ids):,} images")

    # Output directories
    train_label_dir = os.path.join(args.output_dir, "labels", "train")
    val_label_dir = os.path.join(args.output_dir, "labels", "val")
    train_img_dir = os.path.join(args.output_dir, "images", "train")
    val_img_dir = os.path.join(args.output_dir, "images", "val")

    for d in [train_label_dir, val_label_dir, train_img_dir, val_img_dir]:
        os.makedirs(d, exist_ok=True)

    # Accumulate boxes for selected images only
    print(f"\nReading annotations from {os.path.basename(args.anno_file)}...")
    image_boxes = defaultdict(list)
    total_rows = 0
    skipped_group = 0
    skipped_invalid = 0

    with open(args.anno_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            img_id = row["ImageID"].strip()
            if img_id not in target_images:
                continue

            if row.get("IsGroupOf", "0") == "1":
                skipped_group += 1
                continue

            mid = row["LabelName"].strip()
            if mid not in mid_to_idx:
                continue

            try:
                xmin = float(row["XMin"])
                xmax = float(row["XMax"])
                ymin = float(row["YMin"])
                ymax = float(row["YMax"])
            except (ValueError, KeyError):
                skipped_invalid += 1
                continue

            if not (0.0 <= xmin < xmax <= 1.0 and 0.0 <= ymin < ymax <= 1.0):
                skipped_invalid += 1
                continue

            width = xmax - xmin
            height = ymax - ymin
            if width < 0.002 or height < 0.002:
                skipped_invalid += 1
                continue

            # Convert to YOLO format
            class_id = mid_to_idx[mid]
            x_center = (xmin + xmax) / 2.0
            y_center = (ymin + ymax) / 2.0
            image_boxes[img_id].append((class_id, x_center, y_center, width, height))

            if total_rows % 3_000_000 == 0:
                print(f"  ... scanned {total_rows:,} rows", flush=True)

    print(f"Finished scanning. Matched {sum(len(b) for b in image_boxes.values()):,} boxes across {len(image_boxes):,} images.")

    # Write YOLO .txt label files
    print("\nWriting YOLO label files...")
    train_class_counts = Counter()
    val_class_counts = Counter()
    written_train = 0
    written_val = 0

    for img_id, split in target_images.items():
        boxes = image_boxes.get(img_id, [])
        dest_dir = val_label_dir if split == "val" else train_label_dir
        counter = val_class_counts if split == "val" else train_class_counts

        if boxes:
            lines = []
            for cid, xc, yc, w, h in boxes:
                lines.append(f"{cid} {xc:.6f} {yc:.6f} {w:.6f} {h:.6f}")
                counter[cid] += 1
            out_file = os.path.join(dest_dir, f"{img_id}.txt")
            with open(out_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

            if split == "val":
                written_val += 1
            else:
                written_train += 1

    print(f"  Written training label files:   {written_train:,} ({sum(train_class_counts.values()):,} boxes)")
    print(f"  Written validation label files: {written_val:,} ({sum(val_class_counts.values()):,} boxes)")

    # Generate dataset.yaml
    yaml_path = os.path.join(args.output_dir, "dataset.yaml")
    yaml_lines = [
        "# Open Images V6 Full 600-Class Subset - YOLO Configuration",
        f"path: {os.path.abspath(args.output_dir)}",
        "train: images/train",
        "val: images/val",
        "",
        f"nc: {len(sorted_mids)}",
        "",
        "names:"
    ]
    for cid in range(len(sorted_mids)):
        name = idx_to_name[cid].replace("'", "\\'")
        yaml_lines.append(f"  {cid}: '{name}'")

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines) + "\n")
    print(f"Generated YAML config: {yaml_path}")

    # Generate class_mapping.json
    mapping_path = os.path.join(args.output_dir, "class_mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump({
            "nc": len(sorted_mids),
            "idx_to_name": idx_to_name,
            "mid_to_idx": mid_to_idx,
            "mid_to_name": {m: mid_to_name[m] for m in sorted_mids}
        }, f, indent=2)
    print(f"Generated class mapping: {mapping_path}")

    # Generate dataset_summary.json
    summary_path = os.path.join(args.output_dir, "dataset_summary.json")
    summary = {
        "total_images": len(target_images),
        "train_images": len(train_ids),
        "val_images": len(val_ids),
        "total_boxes": sum(train_class_counts.values()) + sum(val_class_counts.values()),
        "train_boxes": sum(train_class_counts.values()),
        "val_boxes": sum(val_class_counts.values()),
        "nc": len(sorted_mids),
        "classes_with_zero_instances": [idx_to_name[i] for i in range(len(sorted_mids)) if (train_class_counts[i] + val_class_counts[i]) == 0]
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Generated dataset summary: {summary_path}")

    print("\nConversion ready. When images are downloaded, place them in:")
    print(f"  Train images: {train_img_dir}")
    print(f"  Val images:   {val_img_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
