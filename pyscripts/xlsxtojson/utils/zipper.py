import os
import json
import zipfile
from tqdm import tqdm
from configuration.config import CONFIG

def read_json(file_path):
    """Чтение JSON файла"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def create_zip_archives(data):
    """Создание ZIP архивов для каждого компонента"""
    root_path = CONFIG['root_folder_path']
    force_create_zip = CONFIG.get('force_create_zip', False)
    exclusions = CONFIG.get('exclusions', {})
    exclude_files = exclusions.get('exclude_files', [])
    exclude_extensions = exclusions.get('exclude_extensions', [])

    # Инициализация счетчиков
    total_components = len(data)
    created_archives = 0
    skipped_archives = 0
    error_archives = 0

    # Создаем прогресс-бар
    with tqdm(total=total_components, desc="Создание ZIP архивов") as pbar:
        for item in data:
            site_category = item['siteCategory']
            technical_category = item['technicalCategory']
            name = item['name']
            component_id = item['id']
            version = item['version']

            folder_name = f"id{component_id}_v{version}_{name}"
            component_path = os.path.join(root_path, site_category, technical_category, folder_name)
            print_path = os.path.join(site_category, technical_category, folder_name)

            if not os.path.exists(component_path):
                print(f"Предупреждение: Папка компонента не найдена: {component_path}")
                skipped_archives += 1
                pbar.update(1)
                continue

            zip_filename = f"{folder_name}.zip"
            zip_path = f"\\\\?\\{os.path.abspath(os.path.join(component_path, zip_filename))}"
            zip_print_path = os.path.join(print_path, zip_filename)
            try:
                # Если ZIP файл уже существует и force_create_zip не установлен, пропускаем его создание
                if os.path.exists(zip_path) and not force_create_zip:
                    skipped_archives += 1
                else:
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, _, files in os.walk(component_path):
                            for file in files:
                                if file in exclude_files or any(file.endswith(ext) for ext in exclude_extensions):
                                    continue
                                arcname = os.path.relpath(os.path.join(root, file), component_path)
                                zipf.write(f"\\\\?\\{os.path.abspath(os.path.join(root, file))}", arcname)
                    
                    print(f"Создан ZIP архив: {zip_print_path}")
                    
                    created_archives += 1

            except Exception as e:
                print(f"Ошибка при создании ZIP для {folder_name}: {str(e)}")
                error_archives += 1

            pbar.update(1)

    return created_archives, skipped_archives, error_archives

def main():
    # Получаем пути из конфигурации
    json_file_path = CONFIG['input_json_file_path']

    print("Чтение данных JSON...")
    data = read_json(json_file_path)
    print(f"Найдено {len(data)} компонентов в JSON файле.")

    print("Начало создания ZIP архивов...")
    created, skipped, errors = create_zip_archives(data)
    
    print("\nПроцесс завершен.")
    print(f"Всего компонентов: {len(data)}")
    print(f"Созданных архивов: {created}")
    print(f"Пропущенных архивов: {skipped}")
    print(f"Ошибок при создании: {errors}")

if __name__ == "__main__":
    main()