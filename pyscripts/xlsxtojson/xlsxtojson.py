#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import pandas as pd
import warnings

# Отключение FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)


def read_excel_to_dataframe(file_path, sheet_name, start_cell, end_col):
    """
    Читает данные из Excel файла и возвращает их в виде DataFrame.

    :param file_path: Путь к Excel файлу.
    :param sheet_name: Имя листа, с которого нужно считать данные.
    :param start_cell: Левая верхняя ячейка таблицы (например, 'B4').
    :param end_col: Последний столбец для чтения (например, 'I').
    :return: DataFrame с данными из Excel файла.
    """
    print(f"Чтение данных из файла: {file_path}, лист: {sheet_name}, начиная с ячейки: {start_cell}, до столбца: {end_col}")
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
    print(f"Сохранение JSON данных в файл: {output_file_path}")
    print("-" * 50)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(json_data)


def main():
    """
    Main function to read data from an Excel file, convert it to JSON format, and save it to a file.

    This function performs the following steps:
    1. Reads data from a specified Excel file and sheet.
    2. Converts the data to a JSON format.
    3. Saves the JSON data to a specified output file.

    Parameters:
    None

    Returns:
    None
    """
    # Параметры, которые могут изменяться пользователем
    excel_file_path = os.path.join(os.path.dirname(__file__), '../../db/Base.xlsx')
    output_json_file_path = os.path.join(os.path.dirname(__file__), '../../db/Base.json')
    sheet_name = 'Экспорт'
    start_cell = (4, 2)  # Ячейка B4
    end_col = 'M'  # Последний столбец для чтения

    # Чтение данных из Excel файла
    df = read_excel_to_dataframe(excel_file_path, sheet_name, start_cell, end_col)

    # Преобразование данных в JSON формат
    json_data = dataframe_to_json(df)

    # Сохранение JSON данных в файл
    save_json_to_file(json_data, output_json_file_path)
    print("Данные успешно экспортированы в", {output_json_file_path})
    print("-" * 50)

    # Ожидание нажатия клавиши пользователем перед закрытием
    input("Нажмите Enter для завершения...")


if __name__ == '__main__':
    main()