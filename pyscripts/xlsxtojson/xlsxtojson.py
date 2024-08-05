#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import pandas as pd
import warnings
import hashlib
from tqdm import tqdm
import csv

# Отключение FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

def calculate_hash(directory):
    """
    Calculate the hash-sum of all files in the given directory.
    """
    hash_md5 = hashlib.md5()
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            with open(f"\\\\?\\{file_path}", "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
    return hash_md5.hexdigest()

def read_md5_from_file(file_path):
    """
    Read the md5 sum from a file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

def check_md5_sums(data, root_folder_path):
    """
    Check the MD5 sums of the files and compare them with the values in the JSON data.

    :param json_file_path: Path to the JSON file containing the expected MD5 sums.
    :param root_folder_path: Root folder path where the files are located.
    :return: total_checked, total_equal, total_not_equal
    """

    output_csv_path = os.path.join(os.path.dirname(__file__), 'hashsums.csv')

    # Prepare CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['name', 'version', 'hash-sum'])

        total_checked = 0
        total_equal = 0
        total_not_equal = 0

        # Process each component
        for item in tqdm(data, desc="Расчет хеш-сумм..."):
            site_category = item['siteCategory']
            technical_category = item['technicalCategory']
            name = item['name']
            component_id = item['id']
            version = item['version']
            json_md5 = item.get('md5', '')

            folder_name = f"id{component_id}_v{version}_{name}"
            full_path = os.path.abspath(os.path.join(root_folder_path, site_category, technical_category, folder_name, name))
            md5_file_path = os.path.abspath(os.path.join(root_folder_path, site_category, technical_category, folder_name, 'md5'))

            if os.path.exists(f"\\\\?\\{full_path}"):
                calc_md5 = calculate_hash(full_path)
                file_md5 = read_md5_from_file(md5_file_path)
                csv_writer.writerow([name, version, calc_md5])
                
                total_checked += 1
                if json_md5 == calc_md5 == file_md5:
                    total_equal += 1
                else:
                    total_not_equal += 1
                    print("\n\n","+" * 25)
                    print(f"ОШИБКА! MD5 не сходится для {name} (ID: {component_id}, Version: {version})")
                    print(f"JSON MD5: {json_md5}")
                    print(f"File MD5: {file_md5}")
                    print(f"Рассчитанная MD5: {calc_md5}")
                    print("+" * 25,"\n")
            else:
                print(f"Folder not found: {full_path}")

    return total_checked, total_equal, total_not_equal

def read_excel_to_dataframe(file_path, sheet_name, start_cell, end_col):
    """
    Читает данные из Excel файла и возвращает их в виде DataFrame.

    :param file_path: Путь к Excel файлу.
    :param sheet_name: Имя листа, с которого нужно считать данные.
    :param start_cell: Левая верхняя ячейка таблицы (например, 'B4').
    :param end_col: Последний столбец для чтения (например, 'I').
    :return: DataFrame с данными из Excel файла.
    """
    print("-" * 50)
    print(f"Чтение данных из файла: {os.path.abspath(file_path)},\nЛист: {sheet_name},\nНачиная с ячейки: {start_cell},\nДо столбца: {end_col}")
    print("-" * 50)
    # Читаем данные из Excel файла, начиная с указанной ячейки
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    start_row, start_col = start_cell
    end_col_index = ord(end_col.upper()) - ord('A') + 1
    df = df.iloc[start_row - 1 :, start_col - 1 : end_col_index]

    # Устанавливаем первую строку как заголовки столбцов
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)

    return df


def dataframe_to_json(df):
    """
    Преобразует DataFrame в JSON формат, заменяя NaN на пустые строки.

    :param df: DataFrame для преобразования.
    :return: JSON строка.
    """
    print("Преобразование данных в JSON формат")
    print("-" * 50)
    # Заменяем NaN на пустые строки
    df = df.fillna("")

    # Преобразуем DataFrame в список словарей
    data_list = df.to_dict(orient='records')

    # Преобразуем список словарей в JSON строку
    json_data = json.dumps(data_list, ensure_ascii=False, indent=4)

    return json_data

def save_json_to_file(json_data, output_file_path):
    """
    Сохраняет JSON данные в файл.

    :param json_data: JSON строка для сохранения.
    :param output_file_path: Путь к выходному файлу.
    """
    print(f"Сохранение JSON данных в файл: {os.path.abspath(output_file_path)}")
    print("-" * 50)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(json_data)


def check_consistency(json_data, root_folder_path, image_folder_path):
    print("Проверка консистентности базы данных")
    print("-" * 50)
    missing_folders = 0
    missing_internal_structure = 0
    missing_images = 0
    unexpected_files_or_folders = 0

    # Создаем словарь ожидаемых папок для каждой категории
    expected_folders = {}
    for item in json_data:
        site_category = item['siteCategory']
        technical_category = item['technicalCategory']
        name = item['name']
        component_id = item['id']
        version = item['version']

        folder_name = f"id{component_id}_v{version}_{name}"
        if site_category not in expected_folders:
            expected_folders[site_category] = {}
        if technical_category not in expected_folders[site_category]:
            expected_folders[site_category][technical_category] = set()
        expected_folders[site_category][technical_category].add(folder_name)

    for item in json_data:
        site_category = item['siteCategory']
        technical_category = item['technicalCategory']
        name = item['name']
        component_id = item['id']
        version = item['version']

        folder_name = f"id{component_id}_v{version}_{name}"
        full_path = os.path.join(root_folder_path, site_category, technical_category, folder_name)
        print_path = os.path.join(site_category, technical_category, folder_name)

        if not os.path.exists(full_path):
            print(f"ЭТОГО КОМПОНЕНТА НЕТ!: {print_path}")
            missing_folders += 1
        else:
            # Check internal structure
            internal_folder_path = os.path.join(full_path, name)
            repository_file_path = os.path.join(internal_folder_path, f"{name}.repository")

            if not os.path.exists(internal_folder_path) or not os.path.exists(repository_file_path):
                print(f"Нарушена структура внутри папки: {print_path}")
                missing_internal_structure += 1

        # Check for the presence of the image file
        image_file_path = os.path.join(image_folder_path, f"{component_id}.png")
        if not os.path.exists(image_file_path):
            print(f"ОТСУТСТВУЕТ ИЗОБРАЖЕНИЕ: {image_file_path}")
            missing_images += 1

    # Check for unexpected files or folders
    for site_category in os.listdir(root_folder_path):
        site_category_path = os.path.join(root_folder_path, site_category)
        if os.path.isdir(site_category_path):
            if site_category not in expected_folders:
                print(f"Неожиданная категория: {site_category}")
                unexpected_files_or_folders += 1
            else:
                for item in os.listdir(site_category_path):
                    item_path = os.path.join(site_category_path, item)
                    if os.path.isdir(item_path):
                        if item not in expected_folders[site_category]:
                            print("\n", "+" * 25)
                            print(f"ВНИМАНИЕ! Неожиданная техническая категория: {os.path.join(site_category, item)}")
                            print("+" * 25,"\n")

                            unexpected_files_or_folders += 1
                        else:
                            for sub_item in os.listdir(item_path):
                                if sub_item not in expected_folders[site_category][item]:
                                    print("\n", "+" * 25)
                                    print(f"ВНИМАНИЕ! Неожиданная папка или файл: {os.path.join(site_category, item, sub_item)}")
                                    print("+" * 25,"\n")
                                    unexpected_files_or_folders += 1
                    else:
                        print("\n", "+" * 25)
                        print(f"ВНИМАНИЕ! Неожиданный файл в категории: {os.path.join(site_category, item)}")
                        print("+" * 25,"\n")

                        unexpected_files_or_folders += 1
        else:
            print("\n", "+" * 25)
            print(f"ВНИМАНИЕ! Неожиданный файл в корневой папке: {site_category}")
            print("+" * 25,"\n")
            unexpected_files_or_folders += 1

    print(f"Итого отсусутвующих директорий: {missing_folders}")
    print(f"Итого нарушений структуры внутри папок: {missing_internal_structure}")
    print(f"Итого отсутствующих изображений: {missing_images}")
    print(f"Итого неожиданных файлов или папок: {unexpected_files_or_folders}")
    print("-" * 50)

    return missing_folders, missing_internal_structure, missing_images, unexpected_files_or_folders


def main():
    """
    Main function to read data from an Excel file, convert it to JSON format, save it to a file, and check consistency.

    This function performs the following steps:
    1. Reads data from a specified Excel file and sheet.
    2. Converts the data to a JSON format.
    3. Saves the JSON data to a specified output file.
    4. Checks the consistency of the database by ensuring corresponding folders exist and have the correct internal structure.

    Parameters:
    None

    Returns:
    None
    """
    # Параметры, которые могут изменяться пользователем
    excel_file_path = os.path.join(os.path.dirname(__file__), '../../db/Base.xlsx')
    output_json_file_path = os.path.join(os.path.dirname(__file__), '../../db/Base.json')
    root_folder_path = os.path.join(os.path.dirname(__file__), '../../components')
    image_folder_path = os.path.join(os.path.dirname(__file__), '../../im')
    sheet_name = 'Экспорт'
    start_cell = (4, 2)  # Ячейка B4
    end_col = 'N'  # Последний столбец для чтения

    # Чтение данных из Excel файла
    df = read_excel_to_dataframe(excel_file_path, sheet_name, start_cell, end_col)

    # Преобразование данных в JSON формат
    json_data = dataframe_to_json(df)

    # Сохранение JSON данных в файл
    save_json_to_file(json_data, output_json_file_path)
    print(f"Данные успешно экспортированы: {os.path.abspath(output_json_file_path)}")
    print("-" * 50)

    # Проверка консистентности базы данных
    json_data_list = json.loads(json_data)
    missing_folders, missing_internal_structure, missing_images, unexpected_files_or_folders = check_consistency(json_data_list, root_folder_path, image_folder_path)
    total_checked, total_equal, total_not_equal = check_md5_sums(json_data_list, root_folder_path)

    print("-" * 50)
    print(f"Всего MD5 посчитано: {total_checked}")
    print(f"Совпало MD5 сумм: {total_equal}")
    print(f"НЕ совпало MD5 сумм: {total_not_equal}")
    print("-" * 50)

    # Check for errors and print the appropriate message
    if missing_folders == 0 and missing_internal_structure == 0 and missing_images == 0 and total_not_equal == 0 and unexpected_files_or_folders == 0:
        print("ОК")
    else:
        print("ERROR")

    input("Нажмите Enter...")

if __name__ == '__main__':
    main()