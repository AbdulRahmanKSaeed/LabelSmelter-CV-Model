"""
Prepare Open Images V5 dataset for YOLO object detection training.

Features:
1. Reads Open Images bounding box annotations (CSV format).
2. Supports selecting an initial subset of ~10-15 object categories (recommended for auto-annotation).
3. Samples a configurable, manageable number of images per category.
4. Preserves multi-object image relationships without label corruption.
5. Converts bounding boxes from Open Images format (XMin, XMax, YMin, YMax) to YOLO format (class_idx, x_center, y_center, width, height).
6. Creates training and validation splits with zero image leakage.
7. Excludes invalid, degenerate, and IsGroupOf boxes.
8. Produces a YOLO dataset configuration YAML file (dataset.yaml).
9. Generates image download lists with direct URLs for selective image fetching.
10. Produces a comprehensive dataset summary report.

Usage:
    python scripts/prepare_yolo_dataset.py --images-per-class 100 --val-ratio 0.2
    python scripts/prepare_yolo_dataset.py --classes "Person,Car,Dog,Cat" --images-per-class 50
"""

import os
import sys
import csv
import json
import random
import argparse
from collections import Counter, defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNO_DIR = os.path.join(PROJECT_ROOT, "data", "annotations")
YOLO_DIR = os.path.join(PROJECT_ROOT, "data", "yolo_dataset")

# Recommended 12 balanced, high-frequency, practical categories for auto-annotation
RECOMMENDED_12_CLASSES = [
    "Person",
    "Car",
    "Bus",
    "Bicycle",
    "Motorcycle",
    "Dog",
    "Cat",
    "Chair",
    "Table",
    "Laptop",
    "Bottle",
    "Book"
]


def load_class_descriptions(filepath):
    """Load class MID -> human-readable name and reverse mapping."""
    mid_to_name = {}
    name_to_mid = {}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                mid = row[0].strip()
                name = row[1].strip()
                mid_to_name[mid] = name
                name_to_mid[name.lower()] = mid
    return mid_to_name, name_to_mid


def load_bbox_annotations(filepath, allowed_mids=None, exclude_group_of=True,
                          exclude_depiction=True, exclude_inside=True):
    """
    Load and filter bounding box annotations from an Open Images CSV file.
    """
    annotations = defaultdict(list)
    total_read = 0
    total_kept = 0
    skipped_class = 0
    skipped_group = 0
    skipped_depiction = 0
    skipped_inside = 0
    skipped_invalid = 0

    print(f"  Reading annotations from {os.path.basename(filepath)}...")
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_read += 1
            label = row["LabelName"].strip()

            if allowed_mids is not None and label not in allowed_mids:
                skipped_class += 1
                continue

            if exclude_group_of and row.get("IsGroupOf", "0") == "1":
                skipped_group += 1
                continue

            if exclude_depiction and row.get("IsDepiction", "0") == "1":
                skipped_depiction += 1
                continue

            if exclude_inside and row.get("IsInside", "0") == "1":
                skipped_inside += 1
                continue

            try:
                xmin = float(row["XMin"])
                xmax = float(row["XMax"])
                ymin = float(row["YMin"])
                ymax = float(row["YMax"])
            except (ValueError, KeyError):
                skipped_invalid += 1
                continue

            # Verify normalized boundaries
            if not (0.0 <= xmin < xmax <= 1.0 and 0.0 <= ymin < ymax <= 1.0):
                skipped_invalid += 1
                continue

            width = xmax - xmin
            height = ymax - ymin
            if width < 0.002 or height < 0.002:  # Filter degenerate boxes
                skipped_invalid += 1
                continue

            image_id = row["ImageID"].strip()
            annotations[image_id].append((label, xmin, xmax, ymin, ymax))
            total_kept += 1

            if total_read % 1_000_000 == 0:
                print(f"    ... processed {total_read:,} rows, kept {total_kept:,}", flush=True)

    print(f"\n  Annotations load summary:")
    print(f"    Total rows read:        {total_read:,}")
    print(f"    Bounding boxes kept:    {total_kept:,}")
    print(f"    Skipped (unselected):   {skipped_class:,}")
    print(f"    Skipped (IsGroupOf):    {skipped_group:,}")
    print(f"    Skipped (IsDepiction):  {skipped_depiction:,}")
    print(f"    Skipped (IsInside):     {skipped_inside:,}")
    print(f"    Skipped (invalid/tiny): {skipped_invalid:,}")
    print(f"    Images with annotations:{len(annotations):,}")

    return annotations


def select_images_per_class(annotations, target_mids, images_per_class=100, seed=42):
    """
    Select a balanced subset of images covering target classes up to images_per_class.
    Handles multi-label images correctly without duplicates.
    """
    rng = random.Random(seed)
    mid_to_images = defaultdict(set)
    for img_id, boxes in annotations.items():
        for mid, *_ in boxes:
            if mid in target_mids:
                mid_to_images[mid].add(img_id)

    selected_images = set()
    # Sort classes by count ascending (rarest classes first) to maximize representation
    sorted_mids = sorted(target_mids, key=lambda m: len(mid_to_images[m]))

    for mid in sorted_mids:
        current_in_class = {img_id for img_id in selected_images if img_id in mid_to_images[mid]}
        needed = images_per_class - len(current_in_class)
        if needed > 0:
            available = sorted(list(mid_to_images[mid] - selected_images))
            rng.shuffle(available)
            chosen = available[:needed]
            selected_images.update(chosen)

    return selected_images


def split_train_val(selected_images, val_ratio=0.2, seed=42):
    """Split selected images into train and val sets with no leakage."""
    rng = random.Random(seed)
    all_imgs = sorted(list(selected_images))
    rng.shuffle(all_imgs)

    val_count = max(1, int(len(all_imgs) * val_ratio))
    val_set = set(all_imgs[:val_count])
    train_set = set(all_imgs[val_count:])
    return train_set, val_set


def convert_and_write_yolo(annotations, image_ids, mid_to_idx, output_labels_dir):
    """
    Convert Open Images box coordinates to YOLO format and write .txt label files.
    YOLO format: class_id x_center y_center width height (normalized)
    """
    os.makedirs(output_labels_dir, exist_ok=True)
    box_stats = Counter()
    total_boxes = 0
    total_images = 0

    for img_id in sorted(image_ids):
        boxes = annotations.get(img_id, [])
        lines = []
        for mid, xmin, xmax, ymin, ymax in boxes:
            if mid not in mid_to_idx:
                continue

            class_idx = mid_to_idx[mid]
            x_center = (xmin + xmax) / 2.0
            y_center = (ymin + ymax) / 2.0
            width = xmax - xmin
            height = ymax - ymin

            lines.append(f"{class_idx} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
            box_stats[class_idx] += 1
            total_boxes += 1

        if lines:
            label_file = os.path.join(output_labels_dir, f"{img_id}.txt")
            with open(label_file, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            total_images += 1

    return total_images, total_boxes, box_stats


def generate_dataset_yaml(class_names_list, yaml_path, train_dir, val_dir):
    """Generate YOLO dataset.yaml configuration file."""
    yaml_lines = [
        "# Open Images Subset - YOLO Dataset Configuration",
        "# Auto-generated by prepare_yolo_dataset.py",
        "",
        f"path: {os.path.abspath(os.path.dirname(yaml_path))}",
        "train: images/train",
        "val: images/val",
        "",
        f"nc: {len(class_names_list)}",
        "",
        "names:"
    ]
    for idx, name in enumerate(class_names_list):
        yaml_lines.append(f"  {idx}: '{name}'")

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines) + "\n")


def generate_download_lists(image_ids, image_metadata_files, output_path):
    """
    Generate download list CSV mapping ImageID -> OriginalURL and Thumbnail URL.
    """
    found = {}
    for meta_file in image_metadata_files:
        if not os.path.exists(meta_file):
            continue
        with open(meta_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                img_id = row.get("ImageID", "").strip()
                if img_id in image_ids and img_id not in found:
                    found[img_id] = {
                        "OriginalURL": row.get("OriginalURL", ""),
                        "Thumbnail300KURL": row.get("Thumbnail300KURL", ""),
                        "Title": row.get("Title", ""),
                        "Rotation": row.get("Rotation", "0.0")
                    }

    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ImageID", "OriginalURL", "Thumbnail300KURL", "Rotation", "Title"])
        for img_id in sorted(image_ids):
            data = found.get(img_id, {})
            writer.writerow([
                img_id,
                data.get("OriginalURL", ""),
                data.get("Thumbnail300KURL", ""),
                data.get("Rotation", "0.0"),
                data.get("Title", "")
            ])

    return len(found)


def main():
    parser = argparse.ArgumentParser(description="Prepare Open Images dataset for YOLO training")
    parser.add_argument("--anno-file", type=str, default=None,
                        help="Path to annotation CSV (default: auto-detects validation or train)")
    parser.add_argument("--classes", type=str, default=None,
                        help="Comma-separated class names (default: 12 recommended categories)")
    parser.add_argument("--images-per-class", type=int, default=100,
                        help="Number of images per category to select (default: 100)")
    parser.add_argument("--val-ratio", type=float, default=0.2,
                        help="Validation set fraction (default: 0.2)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for split reproducibility (default: 42)")
    parser.add_argument("--output-dir", type=str, default=YOLO_DIR,
                        help="Output directory for YOLO dataset")
    args = parser.parse_args()

    print("=" * 75)
    print("Open Images -> YOLO Dataset Preparation Pipeline")
    print("=" * 75)

    # 1. Load class descriptions
    class_desc_path = os.path.join(ANNO_DIR, "class-descriptions-boxable.csv")
    if not os.path.exists(class_desc_path):
        print(f"ERROR: {class_desc_path} not found. Run download_annotations.py first.")
        return 1

    mid_to_name, name_to_mid = load_class_descriptions(class_desc_path)
    print(f"Loaded {len(mid_to_name)} boxable classes from dictionary.")

    # 2. Determine target classes (10-15 recommended)
    if args.classes:
        requested = [c.strip() for c in args.classes.split(",") if c.strip()]
        target_names = []
        target_mids = set()
        for r in requested:
            mid = name_to_mid.get(r.lower())
            if mid:
                target_names.append(mid_to_name[mid])
                target_mids.add(mid)
            else:
                print(f"WARNING: Class '{r}' not found in class descriptions, skipping.")
    else:
        target_names = RECOMMENDED_12_CLASSES
        target_mids = {name_to_mid[c.lower()] for c in RECOMMENDED_12_CLASSES if c.lower() in name_to_mid}

    print(f"\nSelected {len(target_mids)} Target Object Categories:")
    sorted_classes = sorted(list(target_mids), key=lambda m: mid_to_name[m])
    for idx, mid in enumerate(sorted_classes):
        print(f"  [{idx:2d}] {mid_to_name[mid]:<20} ({mid})")

    # Mid to index mapping (0 .. N-1)
    mid_to_idx = {mid: idx for idx, mid in enumerate(sorted_classes)}
    idx_to_name = {idx: mid_to_name[mid] for mid, idx in mid_to_idx.items()}

    # 3. Locate annotation file
    anno_file = args.anno_file
    if not anno_file:
        for candidate in ["validation-annotations-bbox.csv", "train-annotations-bbox.csv", "challenge-2019-train-detection-bbox.csv"]:
            candidate_path = os.path.join(ANNO_DIR, candidate)
            if os.path.exists(candidate_path):
                anno_file = candidate_path
                break

    if not anno_file or not os.path.exists(anno_file):
        print(f"ERROR: No annotation file found in {ANNO_DIR}.")
        return 1

    print(f"\nUsing annotation file: {anno_file}")

    # 4. Load annotations for target classes
    annotations = load_bbox_annotations(anno_file, allowed_mids=target_mids)

    # 5. Balanced image selection
    selected_images = select_images_per_class(
        annotations, target_mids, images_per_class=args.images_per_class, seed=args.seed
    )
    print(f"\nSelected total unique images: {len(selected_images):,}")

    # 6. Train / Validation split without leakage
    train_set, val_set = split_train_val(selected_images, val_ratio=args.val_ratio, seed=args.seed)
    print(f"Split results:")
    print(f"  Training set:   {len(train_set):,} images ({100 - int(args.val_ratio * 100)}%)")
    print(f"  Validation set: {len(val_set):,} images ({int(args.val_ratio * 100)}%)")

    # 7. Convert and write YOLO labels
    train_labels_dir = os.path.join(args.output_dir, "labels", "train")
    val_labels_dir = os.path.join(args.output_dir, "labels", "val")
    train_images_dir = os.path.join(args.output_dir, "images", "train")
    val_images_dir = os.path.join(args.output_dir, "images", "val")

    for d in [train_labels_dir, val_labels_dir, train_images_dir, val_images_dir]:
        os.makedirs(d, exist_ok=True)

    print("\nWriting YOLO format labels...")
    train_imgs_count, train_boxes_count, train_box_stats = convert_and_write_yolo(
        annotations, train_set, mid_to_idx, train_labels_dir
    )
    val_imgs_count, val_boxes_count, val_box_stats = convert_and_write_yolo(
        annotations, val_set, mid_to_idx, val_labels_dir
    )

    print(f"  Written Train labels: {train_imgs_count:,} files, {train_boxes_count:,} boxes")
    print(f"  Written Val labels:   {val_imgs_count:,} files, {val_boxes_count:,} boxes")

    # 8. Produce dataset.yaml configuration file
    yaml_path = os.path.join(args.output_dir, "dataset.yaml")
    generate_dataset_yaml([idx_to_name[i] for i in range(len(sorted_classes))], yaml_path, train_images_dir, val_images_dir)
    print(f"  Generated YAML config: {yaml_path}")

    # 9. Produce class mapping JSON
    mapping_path = os.path.join(args.output_dir, "class_mapping.json")
    with open(mapping_path, "w", encoding="utf-8") as f:
        json.dump({
            "nc": len(sorted_classes),
            "idx_to_name": idx_to_name,
            "mid_to_idx": mid_to_idx,
            "mid_to_name": {m: mid_to_name[m] for m in sorted_classes}
        }, f, indent=2)
    print(f"  Generated class mapping: {mapping_path}")

    # 10. Generate selective download lists
    metadata_candidates = [
        os.path.join(ANNO_DIR, "validation-images-with-rotation.csv"),
        os.path.join(ANNO_DIR, "train-images-boxable-with-rotation.csv")
    ]
    train_dl_file = os.path.join(args.output_dir, "train_download_list.csv")
    val_dl_file = os.path.join(args.output_dir, "val_download_list.csv")
    dl_train_count = generate_download_lists(train_set, metadata_candidates, train_dl_file)
    dl_val_count = generate_download_lists(val_set, metadata_candidates, val_dl_file)
    print(f"  Generated download list: {train_dl_file} ({dl_train_count:,} image URLs)")
    print(f"  Generated download list: {val_dl_file} ({dl_val_count:,} image URLs)")

    # 11. Final Summary Report
    print("\n" + "=" * 75)
    print("DATASET PREPARATION SUMMARY")
    print("=" * 75)
    print(f"{'Class ID':<10} {'Class Name':<20} {'Train Boxes':<15} {'Val Boxes':<15} {'Total Boxes':<15}")
    print("-" * 75)
    for idx in range(len(sorted_classes)):
        c_name = idx_to_name[idx]
        tr_b = train_box_stats[idx]
        val_b = val_box_stats[idx]
        print(f"{idx:<10} {c_name:<20} {tr_b:<15} {val_b:<15} {tr_b + val_b:<15}")
    print("-" * 75)
    print(f"{'TOTAL':<31} {train_boxes_count:<15} {val_boxes_count:<15} {train_boxes_count + val_boxes_count:<15}")
    print(f"\nAll files saved cleanly to: {os.path.abspath(args.output_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
