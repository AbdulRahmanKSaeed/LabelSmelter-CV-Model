"""
Download images specified in the sampling manifest.

Features:
1. Reads selected_images_manifest.csv.
2. Concurrent multi-threaded downloads from official Open Images S3 repository.
3. Automatically skips existing valid images (resumable).
4. Verifies JPEG integrity on download using PIL.
5. Safety monitor: halts immediately if free disk space drops below 15 GB reserve.
6. Progress tracking and real-time disk consumption reporting.

Usage:
    python scripts/download_manifest_images.py [--workers 10] [--split all|train|val]
"""

import os
import sys
import csv
import time
import shutil
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_FILE = os.path.join(PROJECT_ROOT, "data", "manifests", "selected_images_manifest.csv")
DEFAULT_IMAGES_DIR = os.path.join(PROJECT_ROOT, "data", "yolo_dataset", "images")
MIN_FREE_DISK_GB = 15.0  # Emergency safety margin


def check_free_space_gb():
    """Returns free space on project drive in GB."""
    total, used, free = shutil.disk_usage(PROJECT_ROOT)
    return free / (1024 ** 3)


def download_single_image(img_id, split, url, dest_dir, timeout=20, max_retries=3):
    """Download and verify a single image file with automatic retries."""
    dest_path = os.path.join(dest_dir, f"{img_id}.jpg")
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1024:
        return True, "exists", os.path.getsize(dest_path)

    tmp_path = dest_path + f".{os.getpid()}_{int(time.time()*1000)%100000}.tmp"
    last_err = ""

    for attempt in range(max_retries):
        try:
            r = requests.get(url, stream=True, timeout=timeout)
            if r.status_code == 404:
                return False, "http_404", 0
            if r.status_code != 200:
                last_err = f"http_{r.status_code}"
                time.sleep(1.0 * (attempt + 1))
                continue

            with open(tmp_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        f.write(chunk)

            with Image.open(tmp_path) as img:
                img.verify()

            os.replace(tmp_path, dest_path)
            return True, "downloaded", os.path.getsize(dest_path)
        except Exception as e:
            last_err = str(e)
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
            time.sleep(1.0 * (attempt + 1))

    return False, last_err, 0


def main():
    parser = argparse.ArgumentParser(description="Download images from approved Open Images manifest")
    parser.add_argument("--manifest", type=str, default=MANIFEST_FILE, help="Path to selected_images_manifest.csv")
    parser.add_argument("--dest-dir", type=str, default=DEFAULT_IMAGES_DIR, help="Directory to save downloaded images")
    parser.add_argument("--workers", type=int, default=10, help="Number of download threads (default: 10)")
    parser.add_argument("--split", type=str, default="all", choices=["train", "val", "all"], help="Split to download")
    parser.add_argument("--max-images", type=int, default=None, help="Optional cap for testing")
    args = parser.parse_args()

    if not os.path.exists(args.manifest):
        print(f"Error: Manifest file {args.manifest} not found.")
        return 1

    free_gb = check_free_space_gb()
    print("=" * 75)
    print(f"Open Images Approved Subset Downloader")
    print(f"  Target Destination:     {args.dest_dir}")
    print(f"  Current Free Disk Space: {free_gb:.2f} GB")
    print(f"  Safety Margin Threshold: {MIN_FREE_DISK_GB:.1f} GB")
    print("=" * 75)

    if free_gb < MIN_FREE_DISK_GB:
        print(f"ERROR: Available disk space ({free_gb:.2f} GB) is below the safety threshold ({MIN_FREE_DISK_GB} GB). Aborting.")
        return 1

    train_dir = os.path.join(args.dest_dir, "train")
    val_dir = os.path.join(args.dest_dir, "val")
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)

    items = []
    with open(args.manifest, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            split = row.get("Split", "train").strip()
            if args.split != "all" and split != args.split:
                continue
            img_id = row.get("ImageID", "").strip()
            url = row.get("ImageURL", "").strip()
            dest_dir = val_dir if split == "val" else train_dir
            if img_id and url:
                items.append((img_id, split, url, dest_dir))

    if args.max_images:
        items = items[:args.max_images]

    total = len(items)
    print(f"Queued {total:,} images for download across {args.workers} workers.")

    success = 0
    failed = 0
    skipped = 0
    downloaded_bytes = 0
    t0 = time.time()
    last_check_time = time.time()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(download_single_image, img_id, split, url, dest_dir): img_id
            for img_id, split, url, dest_dir in items
        }

        for idx, future in enumerate(as_completed(futures), 1):
            ok, status, b_size = future.result()
            if ok:
                success += 1
                if status == "exists":
                    skipped += 1
                else:
                    downloaded_bytes += b_size
            else:
                failed += 1

            # Disk space check every 250 images or 15 seconds
            if idx % 250 == 0 or (time.time() - last_check_time > 15) or idx == total:
                current_free = check_free_space_gb()
                last_check_time = time.time()
                elapsed = time.time() - t0
                speed_mb = (downloaded_bytes / elapsed) / (1024 * 1024) if elapsed > 0 else 0
                pct = (idx / total) * 100
                print(f"  [{idx:6d}/{total:6d}] ({pct:5.1f}%) | Success: {success:,} (New: {success-skipped:,}, Skip: {skipped:,}) | Failed: {failed} | Free: {current_free:.1f} GB @ {speed_mb:.2f} MB/s", flush=True)

                if current_free < MIN_FREE_DISK_GB:
                    print(f"\n[ALERT] Free space ({current_free:.2f} GB) reached safety threshold ({MIN_FREE_DISK_GB} GB). Stopping gracefully.")
                    break

    print("\n" + "=" * 75)
    print("DOWNLOAD COMPLETE")
    print("=" * 75)
    print(f"Total Processed:  {success + failed:,}")
    print(f"Successfully Got: {success:,} (Downloaded: {success - skipped:,}, Skipped existing: {skipped:,})")
    print(f"Failed:           {failed:,}")
    print(f"Total Data Added: {downloaded_bytes / (1024 * 1024 * 1024):.2f} GB")
    print(f"Remaining Free:   {check_free_space_gb():.2f} GB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
