import json
import os

from configuration.config import CONFIG
from utils.excel_to_json import excel_to_json
from utils.consistency_checker import check_consistency
from utils.md5_checker import check_md5_sums
from utils.zipper import create_zip_archives  # Импортируем функцию создания архивов

def main():
    # Конвертируем Excel в JSON
    print("Начинаем конвертацию Excel в JSON...")
    json_data_list = excel_to_json()
    print(f"Конвертация завершена. Получено {len(json_data_list)} записей.")

    # Проверяем консистентность (интегрированность, целостность) базы данных
    print("-" * 50)
    print("Начинаем проверку консистентности базы данных...")
    missing_folders, missing_internal_structure, missing_images, unexpected_files_or_folders = check_consistency(json_data_list)
    
    # Выводим результаты проверки консистентности
    print(f"Проверка завершена:")
    print(f"- Отсутствующие папки: {missing_folders}")
    print(f"- Отсутствующая внутренняя структура: {missing_internal_structure}")
    print(f"- Отсутствующие изображения: {missing_images}")
    print(f"- Неожиданные файлы или папки: {unexpected_files_or_folders}")
    print("-" * 50)
    
    # Проверяем MD5 суммы
    print("Начинаем проверку MD5 сумм...")
    total_checked, total_equal, total_not_equal = check_md5_sums(json_data_list)
    
    # Выводим результаты проверки MD5 сумм
    print(f"Проверка MD5 сумм завершена:")
    print(f"- Всего проверено: {total_checked}")
    print(f"- Совпадающих сумм: {total_equal}")
    print(f"- Несовпадающих сумм: {total_not_equal}")
    print("-" * 50)

    # Создаем ZIP архивы
    print("Начинаем создание ZIP архивов...")
    zip_created, zip_skipped, zip_errors = create_zip_archives(json_data_list)
    
    # Выводим результаты создания архивов
    print(f"Создание ZIP архивов завершено:")
    print(f"- Создано архивов: {zip_created}")
    print(f"- Пропущено: {zip_skipped}")
    print(f"- Ошибок: {zip_errors}")
    print("-" * 50)

    force_create_json = CONFIG.get('force_create_json', False)

    if not (missing_folders or missing_internal_structure or missing_images or unexpected_files_or_folders or total_not_equal or zip_errors) or force_create_json:
        # Сохраняем обновленные данные в JSON файл
        output_path = CONFIG['output_json_file_path']
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data_list, f, ensure_ascii=False, indent=4)
        print(f"Обновленная база данных сохранена в файл: {os.path.abspath(output_path)}")
        print("-" * 50)
        print("OK")
        input("\nНажмите Enter для завершения...")
    else:
        print("\nERROR: Обнаружены проблемы в базе данных или при создании архивов. JSON файл не был создан.")
        print("Пожалуйста, проверьте выше указанные детали.")
        input("\nНажмите Enter для завершения...")

if __name__ == '__main__':
    main()