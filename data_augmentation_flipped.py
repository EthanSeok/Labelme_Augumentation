import os
import json
from PIL import Image
import base64
import argparse
from io import BytesIO

def read_image(data):
    base64_image_data = data['imageData']
    image_data = base64.b64decode(base64_image_data)

    image_stream = BytesIO(image_data)
    image = Image.open(image_stream)
    return image


def encode_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def flip_image(image, mode='horizontal'):
    if mode == 'horizontal':
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif mode == 'vertical':
        return image.transpose(Image.FLIP_TOP_BOTTOM)

def flip_coordinates(coords, image_width, image_height, mode='horizontal'):
    if mode == 'horizontal':
        return [[image_width - x, y] for [x, y] in coords]
    elif mode == 'vertical':
        return [[image_width - x, image_height - y] for [x, y] in coords]  # 좌우와 상하 모두 반전

def save_flipped_image(image, output_path, mode, filename):
    image.save(os.path.join(output_path, f'{mode}_{filename}'))

def process_images(input_folder, output_folder, flip_mode):
    os.makedirs(output_folder, exist_ok=True)
    images_output_folder = os.path.join(output_folder, 'images')
    labels_output_folder = os.path.join(output_folder, 'label')
    os.makedirs(images_output_folder, exist_ok=True)
    os.makedirs(labels_output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r') as f:
                label_data = json.load(f)

            image = read_image(label_data)

            modes = {
                'horizontal': 'flipped',
                'vertical': 'vertically_flipped',
                'both': ['flipped', 'vertically_flipped']
            }

            flip_actions = modes.get(flip_mode, modes['both'])

            if isinstance(flip_actions, list):
                for action in flip_actions:
                    process_flip(image, label_data, filename, images_output_folder, labels_output_folder, action)
            else:
                process_flip(image, label_data, filename, images_output_folder, labels_output_folder, flip_actions)


def process_flip(image, label_data, filename, images_output_folder, labels_output_folder, action):
    mode = 'horizontal' if 'flipped' in action else 'vertical'
    flipped_image = flip_image(image, mode)
    flipped_filename = filename.replace('.json', '.png')
    save_flipped_image(flipped_image, images_output_folder, action, flipped_filename)
    flipped_image_base64 = encode_image_to_base64(flipped_image)
    flipped_label_data = label_data.copy()
    flipped_label_data["imagePath"] = flipped_filename
    flipped_label_data["imageData"] = flipped_image_base64
    for shape in flipped_label_data["shapes"]:
        shape["points"] = flip_coordinates(shape["points"], flipped_image.width, flipped_image.height, mode)
    flipped_label_path = os.path.join(labels_output_folder, f'{action}_{filename}')
    with open(flipped_label_path, 'w') as f:
        json.dump(flipped_label_data, f, indent=4)


def parse_args():
    parser = argparse.ArgumentParser(description="Process images for flipping and annotating.")
    parser.add_argument('--input_folder', type=str, default='./Labels/',
                        help='Directory where the input JSON files are stored')
    parser.add_argument('--output_folder', type=str, default='./output/',
                        help='Directory where the flipped images and labels will be stored')
    parser.add_argument('--flip_mode', type=str, choices=['horizontal', 'vertical', 'both'], default='both',
                        help='Flip mode: horizontal, vertical, or both')
    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    process_images(args.input_folder, args.output_folder, args.flip_mode)
