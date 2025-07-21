import os
import shutil
import time

OUTPUT_FOLDER = 'static/output'
NOW = time.time()
DAY = 60 * 60 * 24  # 1日（秒）

for dir_name in os.listdir(OUTPUT_FOLDER):
    dir_path = os.path.join(OUTPUT_FOLDER, dir_name)
    if os.path.isdir(dir_path):
        mtime = os.path.getmtime(dir_path)
        if NOW - mtime > DAY:
            shutil.rmtree(dir_path)
            print(f"Deleted {dir_path}")
