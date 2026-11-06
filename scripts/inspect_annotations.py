"""
Inspect Open Images V5 annotations and produce a detailed dataset report.

This script analyzes the downloaded annotation CSVs to determine:
- Number of boxable classes and their names
- Distribution of bounding boxes across classes
- Training/validation/test split sizes
- Image counts per class
- Recommended subset selection strategy

Run AFTER download_annotations.py has completed.
"""

import os
import csv
import sys
from collections import Counter, defaultdict

ANNO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "annotations")


def load_class_descriptions(filepath):
    """Load class MID -> human-readable name mapping."""
    mapping = {}
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                mapping[row[0]] = row[1]
    return mapping


def analyze_bbox_file(filepath, class_names=None):
    """Analyze a bounding box annotation CSV file."""
    print(f"\nAnalyzing: {os.path.basename(filepath)}")
    file_size = os.path.getsize(filepath)
    print(f"  File size: {file_size:,} bytes ({file_size / 1024 / 1024:.1f} MB)")

    class_counts = Counter()       # class -> number of bounding boxes
    image_ids = set()              # unique image IDs
    images_per_class = defaultdict(set)  # class -> set of image IDs
    group_of_count = 0
    depiction_count = 0
    occluded_count = 0
    truncated_count = 0
    inside_count = 0
    total_boxes = 0

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_boxes += 1
            label = row["LabelName"]
            image_id = row["ImageID"]

            class_counts[label] += 1
            image_ids.add(image_id)
            images_per_class[label].add(image_id)

            # Count attributes
            if row.get("IsGroupOf") == "1":
                group_of_count += 1
            if row.get("IsDepiction") == "1":
                depiction_count += 1
            if row.get("IsOccluded") == "1":
                occluded_count += 1
            if row.get("IsTruncated") == "1":
                truncated_count += 1
            if row.get("IsInside") == "1":
                inside_count += 1

            if total_boxes % 1_000_000 == 0:
                print(f"  ... processed {total_boxes:,} boxes", flush=True)

    print(f"\n  === Results ===")
    print(f"  Total bounding boxes: {total_boxes:,}")
    print(f"  Unique images: {len(image_ids):,}")
    print(f"  Unique classes: {len(class_counts):,}")
    print(f"  Avg boxes per image: {total_boxes / len(image_ids):.1f}")
    print(f"  Avg images per class: {len(image_ids) / len(class_counts):.0f}")

    print(f"\n  Attribute counts:")
    print(f"    IsGroupOf:   {group_of_count:,} ({group_of_count / total_boxes * 100:.1f}%)")
    print(f"    IsDepiction: {depiction_count:,} ({depiction_count / total_boxes * 100:.1f}%)")
    print(f"    IsOccluded:  {occluded_count:,} ({occluded_count / total_boxes * 100:.1f}%)")
    print(f"    IsTruncated: {truncated_count:,} ({truncated_count / total_boxes * 100:.1f}%)")
    print(f"    IsInside:    {inside_count:,} ({inside_count / total_boxes * 100:.1f}%)")

    # Top 30 classes by box count
    print(f"\n  Top 30 classes by bounding box count:")
    for i, (label, count) in enumerate(class_counts.most_common(30)):
        name = class_names.get(label, "???") if class_names else label
        num_images = len(images_per_class[label])
        print(f"    {i + 1:3d}. {label:15s} {name:30s} {count:>10,} boxes in {num_images:>8,} images")

    # Bottom 10 classes
    print(f"\n  Bottom 10 classes by bounding box count:")
    for label, count in class_counts.most_common()[-10:]:
        name = class_names.get(label, "???") if class_names else label
        num_images = len(images_per_class[label])
        print(f"    {label:15s} {name:30s} {count:>10,} boxes in {num_images:>8,} images")

    return {
        "total_boxes": total_boxes,
        "unique_images": len(image_ids),
        "unique_classes": len(class_counts),
        "class_counts": class_counts,
        "images_per_class": {k: len(v) for k, v in images_per_class.items()},
        "image_ids": image_ids,
    }


def analyze_image_ids_file(filepath):
    """Check image ID file for download URLs."""
    print(f"\nAnalyzing image IDs: {os.path.basename(filepath)}")
    file_size = os.path.getsize(filepath)
    print(f"  File size: {file_size:,} bytes ({file_size / 1024 / 1024:.1f} MB)")

    count = 0
    has_url = False
    sample_row = None

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            count += 1
            if count == 1:
                sample_row = row
                has_url = "OriginalURL" in row or "Thumbnail300KURL" in row
            if count >= 5:
                break

    # Count total
    with open(filepath, "r", encoding="utf-8") as f:
        total = sum(1 for _ in f) - 1  # subtract header

    print(f"  Total images: {total:,}")
    print(f"  Has download URLs: {has_url}")
    if sample_row:
        print(f"  Columns: {list(sample_row.keys())}")

    return {"total": total, "has_url": has_url, "columns": list(sample_row.keys()) if sample_row else []}


def main():
    print("=" * 70)
    print("Open Images V5 — Annotation Dataset Inspection")
    print("=" * 70)

    # Check class descriptions file exists
    class_desc_path = os.path.join(ANNO_DIR, "class-descriptions-boxable.csv")
    if not os.path.exists(class_desc_path):
        print(f"ERROR: Missing required file: {class_desc_path}")
        print("Run download_annotations.py first.")
        return 1

    # Load class descriptions
    class_names = load_class_descriptions(class_desc_path)
    print(f"\nLoaded {len(class_names)} boxable class descriptions")

    # Also load challenge 2019 500-class description if available
    challenge_classes_path = os.path.join(ANNO_DIR, "challenge-2019-classes-description-500.csv")
    challenge_classes = {}
    if os.path.exists(challenge_classes_path):
        challenge_classes = load_class_descriptions(challenge_classes_path)
        print(f"Loaded {len(challenge_classes)} challenge 2019 class descriptions")

    # Analyze each bbox file
    results = {}

    for split_name, filename in [
        ("train", "train-annotations-bbox.csv"),
        ("validation", "validation-annotations-bbox.csv"),
        ("test", "test-annotations-bbox.csv"),
    ]:
        path = os.path.join(ANNO_DIR, filename)
        if os.path.exists(path):
            results[split_name] = analyze_bbox_file(path, class_names)
        else:
            print(f"\n[SKIP] {filename} not found")

    # Analyze image ID files
    for split_name, filename in [
        ("train", "train-images-boxable-with-rotation.csv"),
        ("validation", "validation-images-with-rotation.csv"),
        ("test", "test-images-with-rotation.csv"),
    ]:
        path = os.path.join(ANNO_DIR, filename)
        if os.path.exists(path):
            analyze_image_ids_file(path)
        else:
            print(f"\n[SKIP] {filename} not found")

    # Overall summary
    print("\n" + "=" * 70)
    print("OVERALL SUMMARY")
    print("=" * 70)

    for split_name, data in results.items():
        print(f"\n  {split_name.upper():12s}: {data['unique_images']:>10,} images, "
              f"{data['total_boxes']:>12,} boxes, {data['unique_classes']:>5,} classes")

    # Storage estimate for ~200K images
    if "train" in results:
        avg_image_size_kb = 100  # conservative estimate: ~100 KB per JPEG
        target_images = 200_000
        estimated_gb = target_images * avg_image_size_kb / 1024 / 1024
        print(f"\n  Estimated storage for {target_images:,} training images:")
        print(f"    At ~100 KB/image: {estimated_gb:.1f} GB")
        print(f"    At ~150 KB/image: {estimated_gb * 1.5:.1f} GB")
        print(f"    At ~200 KB/image: {estimated_gb * 2:.1f} GB")

    return 0


if __name__ == "__main__":
    sys.exit(main())
