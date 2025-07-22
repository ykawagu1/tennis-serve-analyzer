import os
import shutil
import time

print("Clean Output Batch Started")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, "static", "output")
NOW = time.time()
DAY = 60 * 60 * 24  # 1日（秒）

if not os.path.exists(OUTPUT_FOLDER):
    print("No output folder found:", OUTPUT_FOLDER)
    exit(0)

for dir_name in os.listdir(OUTPUT_FOLDER):
    dir_path = os.path.join(OUTPUT_FOLDER, dir_name)
    if os.path.isdir(dir_path):
        mtime = os.path.getmtime(dir_path)
        if NOW - mtime > DAY:
            shutil.rmtree(dir_path)
            print(f"Deleted {dir_path}")
