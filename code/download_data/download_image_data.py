import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode, urlparse, parse_qs
import json
from multiprocessing import Pool, cpu_count


# Get csv files that have uuid information
BASE_DATA_DIR = "/nfs/turbo/si-juliame/multimodal_news_data/"
PROCESSED_DIR = os.path.join(BASE_DATA_DIR, "processed","json")
IMAGE_BASE_URL = "https://sid.erda.dk/share_redirect/e4uVSnvJ1k/images"
IMAGE_OUTPUT_DIR = os.path.join(BASE_DATA_DIR, "images")
COMPLETED_MONTHS = ['2024-02-01_2024-02-29','2023-07-01_2023-07-31','2024-01-01_2024-01-31','2023-05-01_2023-05-31']
os.makedirs(IMAGE_OUTPUT_DIR, exist_ok=True)




# Function to download images for a given month
def download_images_for_month(file_path):
    month = os.path.basename(file_path).replace('merged_anno_', '').replace('.jsonl', '')
    print(f"Processing month: {month}")
    month_dir = os.path.join(IMAGE_OUTPUT_DIR, month)
    print(file_path)
    print(month)
    os.makedirs(month_dir, exist_ok=True)
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            uuid = data.get('uuid')
            if uuid:
                image_url = f"{IMAGE_BASE_URL}/{month}/{uuid}.jpg"
                try:
                    r = requests.get(image_url)
                    filepath = os.path.join(month_dir, f"{uuid}.jpg")
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                except:
                    print(f"Failed to download image for UUID: {uuid} from {image_url}")
                    continue


def get_all_jsonl_files():
    files = []
    for filename in os.listdir(PROCESSED_DIR):
        if filename.endswith('.jsonl'):
            month = filename.replace('merged_anno_', '').replace('.jsonl', '')
            if month not in COMPLETED_MONTHS:
                files.append(os.path.join(PROCESSED_DIR, filename))
    return files

 


if __name__ == "__main__":
    jsonl_files = get_all_jsonl_files()
    print(f"Launching {len(jsonl_files)} workers (one per month)")
    with Pool(processes=len(jsonl_files)) as pool:
        pool.map(download_images_for_month, jsonl_files)