from PIL import Image, ImageOps
import os
import sys
from tqdm import tqdm

#этот скрипт нужен, чтобы массово обрезать скриншоты 
# компонентов с требуемым соотношением сторон и ровненько

# Папка с исходными скриншотами компонентов Evos
to_crop_folder_name = "to_crop"
# Папка с готовыми изображениями
final_folder_name = "final"
# Положение начала обрезки
left_position = 470
top_position = 200
# Размер обрезки
width_new = 860
height_new = 660
# Процентное значение ширины белой границы вокруг компонента
border_size_percent = 5
# Соотношение сторон изображения для обрезки белого фона
width_relative = 16
height_relative = 9


def process_image(
    image_path,
    output_path,
    left_position,
    top_position,
    width_new,
    height_new,
    border_size_percent,
    width_relative,
    height_relative,
):
    # Open the image
    img = Image.open(image_path)

    # Первичная обрезка
    right = left_position + width_new
    bottom = top_position + height_new
    cropped_img = img.crop((left_position, top_position, right, bottom))

    # Вторичная обрезка белого фона
    image = cropped_img.convert("RGB")
    width, height = image.size
    left, top, right, bottom = width, height, 0, 0

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel != (255, 255, 255):
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    cropped_image = image.crop((left, top, right + 1, bottom + 1))
    padded_image = ImageOps.expand(
        cropped_image,
        border=int(border_size_percent * cropped_image.size[0] / 100),
        fill="white",
    )
    padded_width, padded_height = padded_image.size
    target_width = padded_width
    target_height = int(target_width * height_relative / width_relative)

    if target_height < padded_height:
        target_height = padded_height
        target_width = int(target_height * width_relative / height_relative)

    delta_w = target_width - padded_width
    delta_h = target_height - padded_height
    padding_left = delta_w // 2
    padding_right = delta_w - padding_left
    padding_top = delta_h // 2
    padding_bottom = delta_h - padding_top

    final_image = ImageOps.expand(
        padded_image,
        (padding_left, padding_top, padding_right, padding_bottom),
        fill="white",
    )
    final_image.save(output_path)


def process_images_in_folder(
    to_crop_folder_path,
    final_folder_path,
    left_position,
    top_position,
    width_new,
    height_new,
    border_size_percent,
    width_relative,
    height_relative,
):
    os.makedirs(final_folder_path, exist_ok=True)
    processed_count = 0
    image_files = [name for name in os.listdir(to_crop_folder_path) if name.endswith('.png') or name.endswith('.jpg')]
    print(f"Processing {len(image_files)} images...")

    for filename in tqdm(image_files, desc="Processing images"):
        input_path = os.path.join(to_crop_folder_path, filename)
        output_path = os.path.join(final_folder_path, filename)
        process_image(
            input_path,
            output_path,
            left_position,
            top_position,
            width_new,
            height_new,
            border_size_percent,
            width_relative,
            height_relative,
        )
        processed_count += 1

    print(f"{processed_count} images processed and saved to {final_folder_path}")


base_folder = os.path.dirname(os.path.abspath(__file__))
to_crop_folder_path = os.path.join(base_folder, to_crop_folder_name)
final_folder_path = os.path.join(base_folder, final_folder_name)

process_images_in_folder(
    to_crop_folder_path,
    final_folder_path,
    left_position,
    top_position,
    width_new,
    height_new,
    border_size_percent,
    width_relative,
    height_relative,
)