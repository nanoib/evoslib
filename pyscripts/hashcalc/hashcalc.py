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

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directories = [d for d in os.listdir(script_dir) if os.path.isdir(os.path.join(script_dir, d))]

    if len(directories) == 0:
        print("Ошибка: В текущей директории нет поддиректорий.")
        input("Нажмите Enter для выхода...")
        return
    elif len(directories) > 1:
        print("Ошибка: В текущей директории больше одной поддиректории.")
        input("Нажмите Enter для выхода...")
        return

    target_directory = os.path.join(script_dir, directories[0])
    md5_file_path = os.path.join(script_dir, 'md5')

    if os.path.exists(md5_file_path):
        print("Ошибка: Файл 'md5' уже существует.")
        input("Нажмите Enter для выхода...")
        return

    hash_sum = calculate_hash(target_directory)

    with open(md5_file_path, 'w', encoding='utf-8') as f:
        f.write(hash_sum)

    print(f"MD5-сумма успешно рассчитана и сохранена в файл 'md5': {hash_sum}")
    input("Нажмите Enter для выхода...")


if __name__ == '__main__':
    main()