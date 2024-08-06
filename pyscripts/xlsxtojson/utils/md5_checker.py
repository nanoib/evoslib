import os
import csv
from tqdm import tqdm
import hashlib
from configuration.config import CONFIG
from utils.hashcalc import create_md5_file



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

def check_md5_sums(data):
    root_folder_path = CONFIG['root_folder_path']
    output_csv_path = CONFIG['output_csv_path']

    total_checked = 0
    total_equal = 0
    total_not_equal = 0

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['name', 'version', 'hash-sum'])

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
                
                if file_md5 is None:
                    print("\n","+"*25)
                    print(f"ВОПРОС! MD5-сумма для {name} (ID: {component_id}, Version: {version}) не найдена.")
                    user_input = input("Создать md5 файл? Нажмите 1 чтобы создать, 0 чтобы пропустить: ")
                    if user_input == '1':
                        if create_md5_file(full_path):
                            file_md5 = read_md5_from_file(md5_file_path)
                            print(f"MD5 файл успешно создан для {name}")
                        else:
                            print(f"Не удалось создать MD5 файл для {name}")
                    print("+" * 25, "\n")

                
                csv_writer.writerow([name, version, calc_md5])
                
                total_checked += 1
                if json_md5 == calc_md5 == file_md5:
                    total_equal += 1
                else:
                    total_not_equal += 1
                    print("\n\n", "+" * 25)
                    print(f"ОШИБКА! MD5 не сходится для {name} (ID: {component_id}, Version: {version})")
                    print(f"JSON MD5: {json_md5}")
                    print(f"File MD5: {file_md5}")
                    print(f"Рассчитанная MD5: {calc_md5}")
                    print("+" * 25, "\n")
            else:
                print(f"Папка не найдена: {full_path}")

    return total_checked, total_equal, total_not_equal