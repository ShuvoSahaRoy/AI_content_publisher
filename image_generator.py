from bing_image_downloader import downloader
import os
from PIL import Image


folder_path = 'images'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def get_image_properties(image_path):
    try:
        with Image.open(image_path) as image:
            width, height = image.size
            print(width, height)
            return width, height
    except (IOError, OSError, FileNotFoundError):
        return None

def generate_image(topic):
    output_dir = 'images/'  # Output directory
    downloader.download(topic, limit=1, output_dir=output_dir, \
                        adult_filter_off=True, force_replace=False, timeout=10, verbose=False)

    topic_folder = os.path.join(output_dir, topic)
    files = os.listdir(topic_folder)
    for file in files:
        file_path = os.path.join(topic_folder, file)
        if os.path.isfile(file_path):
            image_properties = get_image_properties(file_path)
            if image_properties and (image_properties[0] < 400 or image_properties[1] < 400):
                os.remove(file_path)
                return generate_image(topic)

    return os.path.join(topic_folder, files[0]) if files else None

