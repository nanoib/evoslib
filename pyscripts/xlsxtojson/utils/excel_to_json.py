import pandas as pd
import os
import json
import warnings

# Отключение FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

def read_excel_to_dataframe(file_path, sheet_name, start_cell, end_col):
    """
    Читает данные из Excel файла и возвращает их в виде DataFrame.

    :param file_path: Путь к Excel файлу.
    :param sheet_name: Имя листа, с которого нужно считать данные.
    :param start_cell: Левая верхняя ячейка таблицы (например, (4, 2) для 'B4').
    :param end_col: Последний столбец для чтения (например, 'N').
    :return: DataFrame с данными из Excel файла.
    """
    print("-" * 50)
    print(f"Чтение данных из файла: {os.path.abspath(file_path)},\nЛист: {sheet_name},\nНачиная с ячейки: {start_cell},\nДо столбца: {end_col}")
    print("-" * 50)
    
    # Читаем данные из Excel файла, начиная с указанной ячейки
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    start_row, start_col = start_cell
    end_col_index = ord(end_col.upper()) - ord('A') + 1
    df = df.iloc[start_row - 1:, start_col - 1: end_col_index]

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
    print(f"Сохранение JSON данных в файл...")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(json_data)

def excel_to_json():
    """
    Основная функция для чтения данных из Excel файла и преобразования их в JSON формат.

    :return: Список словарей с данными компонентов.
    """
    from configuration.config import CONFIG

    # Получаем параметры из конфигурации
    excel_file_path = CONFIG['excel_file_path']
    sheet_name = CONFIG['sheet_name']
    start_cell = CONFIG['start_cell']
    end_col = CONFIG['end_col']

    # Чтение данных из Excel файла
    df = read_excel_to_dataframe(excel_file_path, sheet_name, start_cell, end_col)

    # Преобразование данных в JSON формат
    json_data = dataframe_to_json(df)

    # Возвращаем список словарей с данными компонентов
    return json.loads(json_data)

if __name__ == '__main__':
    excel_to_json()