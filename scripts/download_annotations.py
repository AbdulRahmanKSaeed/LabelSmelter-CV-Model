"""
Download Open Images V5 annotation CSV files from Google Cloud Storage.

These are lightweight metadata files needed before selecting and downloading images.
Total download size: approximately 500 MB.
"""

import os
import sys
import urllib.request
import time

# Annotation directory
ANNO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "annotations")

# Files to download: (filename, URL)
FILES = [
    # Class descriptions (boxable classes — 600 classes)
    ("class-descriptions-boxable.csv",
     "https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv"),

    # Bounding box annotations
    ("train-annotations-bbox.csv",
     "https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv"),
    ("validation-annotations-bbox.csv",
     "https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv"),
    ("test-annotations-bbox.csv",
     "https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv"),

    # Image IDs with URLs (for selective downloading later)
    ("train-images-boxable-with-rotation.csv",
     "https://storage.googleapis.com/openimages/2018_04/train/train-images-boxable-with-rotation.csv"),
    ("validation-images-with-rotation.csv",
     "https://storage.googleapis.com/openimages/2018_04/validation/validation-images-with-rotation.csv"),
    ("test-images-with-rotation.csv",
     "https://storage.googleapis.com/openimages/2018_04/test/test-images-with-rotation.csv"),

    # Challenge 2019 specific (500 classes used in competition)
    ("challenge-2019-classes-description-500.csv",
     "https://storage.googleapis.com/openimages/challenge_2019/challenge-2019-classes-description-500.csv"),
    ("challenge-2019-train-detection-bbox.csv",
     "https://storage.googleapis.com/openimages/challenge_2019/challenge-2019-train-detection-bbox.csv"),
]


def download_file(url, dest_path):
    """Download a file with streaming and progress reporting using requests."""
    import requests

    if os.path.exists(dest_path):
        size = os.path.getsize(dest_path)
        print(f"  [SKIP] Already exists ({size:,} bytes): {os.path.basename(dest_path)}")
        return True

    print(f"  [DOWNLOAD] {os.path.basename(dest_path)}")
    print(f"    URL: {url}")

    tmp_path = dest_path + ".tmp"
    try:
        start = time.time()
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        if total_size > 0:
            print(f"    Size: {total_size:,} bytes ({total_size / 1024 / 1024:.1f} MB)")

        downloaded = 0
        last_log = time.time()
        with open(tmp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if time.time() - last_log > 5:
                        pct = (downloaded / total_size * 100) if total_size > 0 else 0
                        speed = (downloaded / (time.time() - start)) / 1024 / 1024
                        print(f"    ... {downloaded / 1024 / 1024:.1f} MB ({pct:.1f}%) at {speed:.2f} MB/s", flush=True)
                        last_log = time.time()

        os.replace(tmp_path, dest_path)
        elapsed = time.time() - start
        final_size = os.path.getsize(dest_path)
        speed = final_size / elapsed / 1024 / 1024 if elapsed > 0 else 0
        print(f"    Done: {final_size:,} bytes in {elapsed:.1f}s ({speed:.1f} MB/s)")
        return True

    except Exception as e:
        print(f"    [ERROR] {e}")
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        return False


def main():
    os.makedirs(ANNO_DIR, exist_ok=True)

    print(f"Annotation directory: {ANNO_DIR}")
    print(f"Files to download: {len(FILES)}")
    print()

    success = 0
    failed = 0

    for filename, url in FILES:
        dest = os.path.join(ANNO_DIR, filename)
        if download_file(url, dest):
            success += 1
        else:
            failed += 1
        print()

    print(f"=== Summary ===")
    print(f"  Success: {success}/{len(FILES)}")
    print(f"  Failed:  {failed}/{len(FILES)}")

    # Report total size
    total = sum(os.path.getsize(os.path.join(ANNO_DIR, f)) for f, _ in FILES
                if os.path.exists(os.path.join(ANNO_DIR, f)))
    print(f"  Total annotation data: {total:,} bytes ({total / 1024 / 1024:.1f} MB)")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
