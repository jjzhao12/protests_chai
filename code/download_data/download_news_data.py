import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode, urlparse, parse_qs



BASE_URL = "https://sid.erda.dk/cgi-sid/ls.py"
SHARE_ID = "e4uVSnvJ1k"
BASE_DOWNLOAD_URL = f"https://sid.erda.dk/share_redirect/{SHARE_ID}"


download_root = "/nfs/turbo/si-juliame/multimodal_news_data" 
# Make download root if it doesnt exist
if not os.path.exists(download_root):
    os.mkdir(download_root) 

def fetch_dir(current_dir):
    params = {
        "share_id": SHARE_ID,
        "current_dir": current_dir,
        "flags": "f"
    }

    query = urlencode(params, encoding='latin1')  # Use ISO-8859-1 encoding
    constructed_url = f"{BASE_URL}?{query}" 

    print(f"Visiting: {current_dir}")
    # print(f"Constructed URL: {constructed_url}")

    resp = requests.get(constructed_url)
    soup = BeautifulSoup(resp.text, "html.parser")


    # Make local directory
    local_dir = os.path.join(download_root, current_dir)
    os.makedirs(local_dir, exist_ok=True)


    for a in soup.find_all("a"):
        href = a.get("href")
        href = href.replace("¤","&curren")
        if not href or "share_id=" not in href:
            continue

        known_extensions = [".jpg", ".png", ".pdf", ".zip", ".csv", ".txt",".json",".jsonl",".tsv"]
        # If the link does not end with a known extension, it is likely a directory
        is_dir = href.endswith("/") or not any(href.endswith(ext) for ext in known_extensions)
        
        parsed = parse_qs(urlparse(href).query)
        target_dir = parsed.get("current_dir", [None])[0]  
        # print(target_dir)

        # If href is a file, we download it
        if not is_dir:
            # Construct the full file URL
            file_path = parsed.get("path", [None])[0]
            file_url = f"{BASE_DOWNLOAD_URL}/{file_path}"
            print(BASE_DOWNLOAD_URL)
            print(file_url)

        
            filename = os.path.basename(href)
            filepath = os.path.join(local_dir, filename)
            print(f"Downloading: {file_url} -> {filepath}")
            r = requests.get(file_url, stream=True)
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)  

        # If href is a directory, we need to fetch it recursively
        else:
            if target_dir and target_dir.startswith(current_dir) and target_dir != current_dir:
                fetch_dir(target_dir)



# Start recursion from this folder
start_dir = "images/2023-05-01_2023-05-31"
#start_dir = "images"

fetch_dir(start_dir)

