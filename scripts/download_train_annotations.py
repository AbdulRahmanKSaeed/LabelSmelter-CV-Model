"""
Multi-threaded segmented downloader for Open Images train bounding box annotations.
Downloads train-annotations-bbox.csv (1.13 GB) from Google Cloud Storage with resume capability.
"""

import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "https://storage.googleapis.com/openimages/2018_04/train/train-annotations-bbox.csv"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_PATH = os.path.join(PROJECT_ROOT, "data", "annotations", "train-annotations-bbox.csv")
PART_DIR = DEST_PATH + ".parts"
NUM_PARTS = 12


def get_file_size(url):
    r = requests.head(url, timeout=10)
    r.raise_for_status()
    return int(r.headers.get("content-length", 0))


def download_chunk(url, start, end, part_file):
    headers = {"Range": f"bytes={start}-{end}"}
    # Check if part file already exists and is complete
    expected_size = end - start + 1
    if os.path.exists(part_file) and os.path.getsize(part_file) == expected_size:
        return part_file, expected_size

    r = requests.get(url, headers=headers, stream=True, timeout=30)
    r.raise_for_status()
    with open(part_file, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
    return part_file, os.path.getsize(part_file)


def main():
    os.makedirs(os.path.dirname(DEST_PATH), exist_ok=True)
    if os.path.exists(DEST_PATH):
        size_mb = os.path.getsize(DEST_PATH) / (1024 * 1024)
        print(f"File already exists: {DEST_PATH} ({size_mb:.1f} MB)")
        return 0

    total_size = get_file_size(URL)
    print(f"Total file size: {total_size:,} bytes ({total_size / (1024*1024):.1f} MB)")
    os.makedirs(PART_DIR, exist_ok=True)

    part_size = (total_size + NUM_PARTS - 1) // NUM_PARTS
    chunks = []
    for i in range(NUM_PARTS):
        start = i * part_size
        end = min((i + 1) * part_size - 1, total_size - 1)
        part_file = os.path.join(PART_DIR, f"part_{i:02d}.tmp")
        chunks.append((i, start, end, part_file))

    print(f"Downloading in {NUM_PARTS} concurrent segments...")
    t0 = time.time()
    downloaded_bytes = 0

    with ThreadPoolExecutor(max_workers=NUM_PARTS) as executor:
        futures = {
            executor.submit(download_chunk, URL, start, end, part_file): (i, end - start + 1)
            for i, start, end, part_file in chunks
        }
        for future in as_completed(futures):
            i, exp_size = futures[future]
            try:
                p_file, actual_size = future.result()
                downloaded_bytes += actual_size
                elapsed = time.time() - t0
                pct = (downloaded_bytes / total_size) * 100
                speed = (downloaded_bytes / elapsed) / (1024 * 1024) if elapsed > 0 else 0
                print(f"  Segment {i+1:2d}/{NUM_PARTS} done ({actual_size/(1024*1024):.1f} MB) | Total: {pct:.1f}% @ {speed:.2f} MB/s", flush=True)
            except Exception as e:
                print(f"  Error downloading segment {i+1}: {e}", flush=True)
                raise e

    print(f"All segments downloaded in {time.time() - t0:.1f}s. Assembling final file...")
    with open(DEST_PATH + ".tmp", "wb") as f_out:
        for i in range(NUM_PARTS):
            part_file = os.path.join(PART_DIR, f"part_{i:02d}.tmp")
            with open(part_file, "rb") as f_in:
                while True:
                    data = f_in.read(1024 * 1024 * 4)
                    if not data:
                        break
                    f_out.write(data)
            os.remove(part_file)

    os.rmdir(PART_DIR)
    os.replace(DEST_PATH + ".tmp", DEST_PATH)
    final_size = os.path.getsize(DEST_PATH)
    print(f"Assembly complete! {DEST_PATH} ({final_size / (1024*1024):.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
