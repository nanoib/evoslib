import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = {
    # где размещается итоговый json файл
    'output_json_file_path': os.path.join(BASE_DIR, '../../db/Base.json'),

    # создавать json при наличии проблем?
    'force_create_json': False,

    # создавать zip-файл при его наличии?
    'force_create_zip': False,

    # исключения для zip-архивации...
    'exclusions': {
        'exclude_files': ['md5'],
        'exclude_extensions': ['.zip']
    },

    # параметры экспорта Excel
    'excel_file_path': os.path.join(BASE_DIR, '../../db/Base.xlsx'),
    'sheet_name': 'Экспорт',
    'start_cell': (4, 2),
    'end_col': 'N',

    # где размещается корневая папка с компонентами
    'root_folder_path': os.path.join(BASE_DIR, '../../components'),

    # где размещается папка с изображениями
    'image_folder_path': os.path.join(BASE_DIR, '../../im'),

    # куда сохранять md5-суммы (для справки)
    'output_csv_path': os.path.join(BASE_DIR, 'output/hashsums.csv'),
}