import os
from PIL import Image
import numpy as np


def adjust_color(color, background, foreground, alpha=1.0):
    # Interpolate between background and foreground based on original color and alpha
    return tuple(
        int(bg + (fg - bg) * (c / 255) * alpha)
        for c, bg, fg in zip(color, background, foreground)
    )


def process_image(file_path):
    # Open the image
    img = Image.open(file_path).convert('RGBA')
    data = np.array(img)

    # Define the new background color and a foreground color
    background_color = [16, 18, 20, 255]
    foreground_color = [200, 200, 200, 255]

    # Create a mask for the white background (assuming white is [255, 255, 255, 255])
    white_bg_mask = np.all(data == [255, 255, 255, 255], axis=-1)

    # Adjust colors
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if white_bg_mask[i, j]:
                data[i, j] = background_color
            else:
                original_color = data[i, j]
                if np.all(
                    original_color[:3] == original_color[0]
                ):  # Check if it's a shade of gray
                    # Calculate distance from edge
                    distance = min(i, j, data.shape[0] - i - 1, data.shape[1] - j - 1)
                    # Adjust alpha based on distance (max distance for gradient effect = 5 pixels)
                    alpha = min(1.0, distance / 5)
                    data[i, j] = adjust_color(
                        original_color, background_color, foreground_color, alpha
                    )

    # Create a new image with the modified data
    new_img = Image.fromarray(data)

    # Generate the new file name with _dark suffix
    file_name, file_ext = os.path.splitext(file_path)
    new_file_path = f"{file_name}_dark{file_ext}"

    # Save the new image
    new_img.save(new_file_path)


# Walk through all subdirectories in ./public/
for root, dirs, files in os.walk('./public/'):
    for file in files:
        if file.lower().endswith('.png'):
            file_path = os.path.join(root, file)
            process_image(file_path)
