#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import hashlib

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

def create_md5_file(target_directory):
    """
    Calculate MD5 hash for the given directory and create an 'md5' file.
    
    :param target_directory: Path to the directory for which to calculate MD5.
    :return: True if 'md5' file was created successfully, False otherwise.
    """
    if not os.path.isdir(target_directory):
        print(f"Ошибка: Указанная директория не существует: {target_directory}")
        return False

    md5_file_path = os.path.join(os.path.dirname(target_directory), 'md5')

    if os.path.exists(md5_file_path):
        print(f"Ошибка: Файл 'md5' уже существует в {os.path.dirname(target_directory)}")
        return False

    try:
        hash_sum = calculate_hash(target_directory)

        with open(md5_file_path, 'w', encoding='utf-8') as f:
            f.write(hash_sum)

        print(f"MD5-сумма успешно рассчитана и сохранена в файл 'md5': {hash_sum}")
        return True
    except Exception as e:
        print(f"Произошла ошибка при создании файла 'md5': {str(e)}")
        return False

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directories = [d for d in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, d))]

    if len(directories) == 0:
        print("Ошибка: В текущей директории нет поддиректорий.")
    elif len(directories) > 1:
        print("Ошибка: В текущей директории больше одной поддиректории.")
    else:
        target_directory = os.path.join(script_dir, directories[0])
        result = create_md5_file(target_directory)
        if result:
            print("Файл 'md5' успешно создан.")
        else:
            print("Не удалось создать файл 'md5'.")

    input("Нажмите Enter для выхода...")