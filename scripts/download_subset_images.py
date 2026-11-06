"""
Download image subset for YOLO training using the generated download lists.

Downloads images concurrently from Flickr / Open Images URLs with progress tracking,
retries, and automatic file verification.

Usage:
    python scripts/download_subset_images.py [--workers 8] [--split train|val|all]
"""

import os
import sys
import csv
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YOLO_DIR = os.path.join(PROJECT_ROOT, "data", "yolo_dataset")


def download_single_image(img_id, url, dest_dir, timeout=15):
    """Download and verify a single image."""
    dest_path = os.path.join(dest_dir, f"{img_id}.jpg")
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1024:
        return True, "exists"

    if not url:
        return False, "no_url"

    tmp_path = dest_path + ".tmp"
    try:
        r = requests.get(url, stream=True, timeout=timeout)
        if r.status_code != 200:
            return False, f"http_{r.status_code}"

        with open(tmp_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=32 * 1024):
                if chunk:
                    f.write(chunk)

        # Verify image integrity
        with Image.open(tmp_path) as img:
            img.verify()

        os.replace(tmp_path, dest_path)
        return True, "downloaded"
    except Exception as e:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        return False, str(e)


def download_split(list_csv_path, dest_dir, max_workers=8):
    """Download all images from a download list CSV."""
    if not os.path.exists(list_csv_path):
        print(f"Error: Download list {list_csv_path} not found.")
        return 0, 0

    os.makedirs(dest_dir, exist_ok=True)

    items = []
    with open(list_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            img_id = row.get("ImageID", "").strip()
            # Try Thumbnail URL first (faster, ~300K, ideal for YOLO 640x640), fallback to OriginalURL
            url = row.get("Thumbnail300KURL") or row.get("OriginalURL")
            if img_id and url:
                items.append((img_id, url))

    total = len(items)
    print(f"Downloading {total:,} images to {dest_dir} (concurrency: {max_workers})...")

    success = 0
    failed = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_single_image, img_id, url, dest_dir): img_id for img_id, url in items}
        for idx, future in enumerate(as_completed(futures), 1):
            ok, status = future.result()
            if ok:
                success += 1
            else:
                failed += 1

            if idx % 50 == 0 or idx == total:
                pct = (idx / total) * 100
                print(f"  [{idx:4d}/{total:4d}] ({pct:5.1f}%) | Success: {success} | Failed: {failed}", flush=True)

    return success, failed


def main():
    parser = argparse.ArgumentParser(description="Download subset images for YOLO training")
    parser.add_argument("--workers", type=int, default=8, help="Number of concurrent download threads (default: 8)")
    parser.add_argument("--split", type=str, default="all", choices=["train", "val", "all"],
                        help="Which split to download (default: all)")
    args = parser.parse_args()

    train_csv = os.path.join(YOLO_DIR, "train_download_list.csv")
    val_csv = os.path.join(YOLO_DIR, "val_download_list.csv")
    train_dest = os.path.join(YOLO_DIR, "images", "train")
    val_dest = os.path.join(YOLO_DIR, "images", "val")

    if args.split in ["train", "all"]:
        print("\n--- Downloading Training Split ---")
        download_split(train_csv, train_dest, max_workers=args.workers)

    if args.split in ["val", "all"]:
        print("\n--- Downloading Validation Split ---")
        download_split(val_csv, val_dest, max_workers=args.workers)

    print("\nImage download process complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
