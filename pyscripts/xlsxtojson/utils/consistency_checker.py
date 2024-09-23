import os
from configuration.config import CONFIG

def check_consistency(json_data):
    """
    Проверяет консистентность базы данных.

    :param json_data: Список словарей с данными компонентов.
    :return: Кортеж с количеством обнаруженных проблем.
    """
    missing_folders = 0
    missing_internal_structure = 0
    missing_images = 0
    unexpected_files_or_folders = 0

    # Получаем пути из конфигурации
    root_folder_path = CONFIG['root_folder_path']

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

    # Проверяем наличие папок и внутренней структуры для каждого компонента
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
            # Проверяем внутреннюю структуру
            internal_folder_path = os.path.join(full_path, name)
            repository_file_path = os.path.join(internal_folder_path, f"{name}.repository")

            if not os.path.exists(internal_folder_path) or not os.path.exists(repository_file_path):
                print(f"Нарушена структура внутри папки: {print_path}")
                missing_internal_structure += 1

        # Проверяем наличие файла изображения
        image_file_path = os.path.join(full_path, f"{component_id}.png")
        if not os.path.exists(image_file_path):
            print(f"ОТСУТСТВУЕТ ИЗОБРАЖЕНИЕ: {image_file_path}")
            missing_images += 1

    # Проверяем наличие неожиданных файлов или папок
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
                        if item.endswith('_old'):
                            continue  # Skip folders with '_old' suffix
                        if item not in expected_folders[site_category]:
                            print("\n", "+" * 25)
                            print(f"ВНИМАНИЕ! Неожиданная техническая категория: {os.path.join(site_category, item)}")
                            print("+" * 25,"\n")
                            unexpected_files_or_folders += 1
                        else:
                            for sub_item in os.listdir(item_path):
                                if sub_item.endswith('_old'):
                                    continue  # Skip folders with '_old' suffix
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

    # Выводим итоговую статистику
    if __name__ == '__main__':
        print(f"Итого отсутствующих директорий: {missing_folders}")
        print(f"Итого нарушений структуры внутри папок: {missing_internal_structure}")
        print(f"Итого отсутствующих изображений: {missing_images}")
        print(f"Итого неожиданных файлов или папок: {unexpected_files_or_folders}")
        print("-" * 50)

    return missing_folders, missing_internal_structure, missing_images, unexpected_files_or_folders