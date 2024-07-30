#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import pandas as pd


def read_excel_to_dataframe(file_path, sheet_name, start_cell):
    """
    Читает данные из Excel файла и возвращает их в виде DataFrame.

    :param file_path: Путь к Excel файлу.
    :param sheet_name: Имя листа, с которого нужно считать данные.
    :param start_cell: Левая верхняя ячейка таблицы (например, 'B4').
    :return: DataFrame с данными из Excel файла.
    """
    # Читаем данные из Excel файла, начиная с указанной ячейки
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    start_row, start_col = start_cell
    df = df.iloc[start_row - 1 :, start_col - 1 :]

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
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(json_data)


def main():
    # Параметры, которые могут изменяться пользователем
    excel_file_path = os.path.join(os.path.dirname(__file__), '../../db/Base_plain.xlsx')
    output_json_file_path = os.path.join(os.path.dirname(__file__), '../../db/Base.json')
    sheet_name = 'Компоненты'
    start_cell = (4, 2)  # Ячейка B4

    # Чтение данных из Excel файла
    df = read_excel_to_dataframe(excel_file_path, sheet_name, start_cell)

    # Преобразование данных в JSON формат
    json_data = dataframe_to_json(df)

    # Сохранение JSON данных в файл
    save_json_to_file(json_data, output_json_file_path)
    print("Данные успешно экспортированы в", {output_json_file_path})


if __name__ == '__main__':
    main()
