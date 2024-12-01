import zipfile
from io import BytesIO


def process_zip_file(zip_data):
    """
    Извлекает и объединяет текстовые файлы из ZIP-архива, включая файлы из вложенных папок.
    """
    zip_content = BytesIO(zip_data)  # Преобразуем bytes в объект BytesIO
    extracted_content = []

    try:
        with zipfile.ZipFile(zip_content) as z:
            for file_name in z.namelist():
                # Проверяем, является ли элемент файлом (не папкой)
                if not file_name.endswith('/'):  # Пропускаем папки
                    try:
                        with z.open(file_name) as f:
                            # Попытка декодировать содержимое файла как UTF-8
                            content = f.read().decode("utf-8")
                            extracted_content.append(
                                f"=== {file_name} ===\n{content}"
                            )
                    except UnicodeDecodeError:
                        print(
                            f"Файл {file_name} не является текстовым или имеет неверную кодировку. Пропускаем."
                        )
                    except Exception as e:
                        print(f"Ошибка при обработке файла {file_name}: {e}")
    except zipfile.BadZipFile:
        raise ValueError("Ошибка: Некорректный ZIP-архив")

    return "\n\n".join(extracted_content)
