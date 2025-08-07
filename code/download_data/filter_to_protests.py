import ujson as json
import os
from pathlib import Path 
import re
from PIL import Image
"""
This script creates a new folder with only the protest-related articles from the original dataset. 
Original file: /nfs/turbo/si-juliame/multimodal_news_data/processed/combined_annotations.jsonl

"""
def process_file(input_file, output_file):
    num_relevant = 0
    with open(input_file, 'r') as f_in:
        with open(output_file,'w') as f_out:
            for i,line in enumerate(f_in):
                news_obj = json.loads(line)
                all_text = get_all_text_from_news_obj(news_obj)
                if contains_protest_keyword(all_text):
                    news_obj['month'] = get_month_dir_from_image_path(news_obj)
                    # print(f"Found related article: {news_obj['title']}")
                    # print(f"Text: {all_text}")
                    f_out.write(json.dumps(news_obj) + '\n')
                    num_relevant += 1
                if i % 1000 == 0:
                    print(f"Processed {i} lines, found {num_relevant} relevant articles so far.")
    

def get_all_text_from_news_obj(news_obj):
    title = news_obj.get('title', '')
    maintext = news_obj.get('maintext', '')
    description = news_obj.get('description', '')
    all_text = f"{title} {maintext} {description}"
    return all_text.lower()

def get_month_dir_from_image_path(news_obj):
    image_path = news_obj.get('image-url', '')
    if image_path and image_path != '':
        month = image_path.split('/')[-2]
        return month
    return None

def contains_protest_keyword(text):
    protest_keywords = [
        'protest.*?', 'strikes?', 'boycott.*?', 'walkouts?', 'walk-outs?', 'sitins?', 'sit-ins?','rally',
        'unrest', 'uprisings?', 'rebellions?', 'civil disobedience', 'riot.*?', 'marches',
        'demonstrations?', 'demonstrators?', 'curfews?', 'picket.*?','mobs?'
    ]
    
    protest_keywords = [r'\b' + keyword + r'\b' for keyword in protest_keywords]  # Add word boundaries
    combined_pattern = r'|'.join(protest_keywords)
    regex = re.compile(combined_pattern, re.IGNORECASE)
    return bool(regex.search(text))


def copy_images(input_file, old_image_dir, new_image_dir):
    with open(input_file, 'r') as f_in:
            for i,line in enumerate(f_in):
                news_obj = json.loads(line)
                image_path = news_obj.get('image-url', '')
                if image_path and image_path != '':
                    path_ending = image_path.split('/')[-2:]
                    month, uuid_jpg = path_ending
                    original_image_path = os.path.join(old_image_dir,month,uuid_jpg)
                    new_image_path = os.path.join(new_image_dir, month, uuid_jpg)
                    Path(os.path.dirname(new_image_path)).mkdir(parents=True, exist_ok=True)
                    if os.path.exists(original_image_path):
                        os.system(f'cp {original_image_path} {new_image_path}')
                if i % 1000 == 0:
                    print(f"Processed {i} lines, copied images for relevant articles.")


def resize_image(input_path,output_path,max_size):
    with Image.open(input_path) as img:
        img.thumbnail((max_size, max_size), Image.LANCZOS)
        img.save(output_path, quality=85, optimize=True)

def get_image_size(input_path):
    with Image.open(input_path) as img:
        print(img.size)  # Returns (width, height)

def resize_all_images(input_path,output_path,max_size):
    for month_dir in os.listdir(input_path):
        print(month_dir)
        month_path = os.path.join(input_path, month_dir)
        for image_file in os.listdir(month_path):
            image_path = os.path.join(month_path, image_file)
            output_image_path = os.path.join(output_path, month_dir, image_file)
            Path(os.path.dirname(output_image_path)).mkdir(parents=True, exist_ok=True)
            # get_image_size(image_path)  # Print original size
            resize_image(image_path, output_image_path, max_size)

def main():
    input_file = '/nfs/turbo/si-juliame/multimodal_news_data/processed/combined_annotations.jsonl'
    output_dir = '/nfs/turbo/si-juliame/protest_news/data/'
    # Ensure the output directory exists
    # Path(output_dir).mkdir(parents=True, exist_ok=True)
    # output_file = os.path.join(output_dir, 'arora_data_filtered_by_protest_keywords.jsonl')

    # Test reading the first lines
    # process_file(input_file, output_file)

    # Copy images
    # old_image_dir = '/nfs/turbo/si-juliame/multimodal_news_data/images/'
    # new_image_dir = '/nfs/turbo/si-juliame/protest_news/data/images/'
    #copy_images(output_file, old_image_dir, new_image_dir)

    # Resize images
    max_size = 512
    raw_image_dir = '/nfs/turbo/si-juliame/protest_news/data/images/'
    scaled_image_dir = '/nfs/turbo/si-juliame/protest_news/data/images_scaled/'
    Path(scaled_image_dir).mkdir(parents=True, exist_ok=True)
    resize_all_images(raw_image_dir, scaled_image_dir, max_size)



if __name__ == "__main__":
    main()