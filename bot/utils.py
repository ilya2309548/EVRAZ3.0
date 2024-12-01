import zipfile
from io import BytesIO


def process_zip_file(zip_data):
    """
    Извлекает текстовые файлы из ZIP-архива.
    Возвращает словарь {file_name: content}.
    """
    zip_content = BytesIO(zip_data)
    extracted_content = {}

    try:
        with zipfile.ZipFile(zip_content) as z:
            for file_name in z.namelist():
                if not file_name.endswith("/") and file_name.endswith(
                    (".txt", ".py", ".md")
                ):
                    with z.open(file_name) as f:
                        content = f.read().decode("utf-8")
                        extracted_content[file_name] = content
    except zipfile.BadZipFile:
        raise ValueError("Некорректный ZIP-архив")

    return extracted_content
