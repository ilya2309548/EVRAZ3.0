import sys
from db.vector_store import VectorStore
from api.client import get_embedding
from bot.utils import process_zip_file


def add_entries_from_zip(zip_path):
    with open(zip_path, "rb") as zip_file:
        zip_data = zip_file.read()

    files_content = process_zip_file(zip_data)
    vector_store = VectorStore()

    for file_name, content in files_content.items():
        vector = get_embedding(content)
        vector_store.add_entry(
            id=file_name,
            vector=vector,
            metadata={"title": file_name, "content": content},
        )
    print(f"Данные из {zip_path} успешно добавлены в базу знаний.")


if __name__ == "__main__":
    zip_path = sys.argv[1]
    add_entries_from_zip(zip_path)
