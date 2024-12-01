import os
import json
import numpy as np
import faiss
from utils.embeddings import get_embedding  # Импорт функции из нового модуля


class KnowledgeBase:
    def __init__(
        self, index_path="knowledge_base.faiss", data_path="knowledge_data.json"
    ):
        self.index_path = index_path
        self.data_path = data_path
        self.index = self._load_or_create_index()
        self.data = self._load_or_create_data()

    def _load_or_create_index(self):
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        return faiss.IndexFlatL2(384)  # Размерность эмбеддингов

    def _load_or_create_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def add_rule(self, rule_text, metadata=None):
        """Добавляет правило в базу знаний."""
        if metadata is None:
            metadata = {}
        vector = get_embedding(
            rule_text
        )  # Используем функцию из utils.embeddings
        self.index.add(vector.reshape(1, -1))
        self.data[len(self.data)] = {"rule": rule_text, **metadata}
        self._save_index()
        self._save_data()

    def search_rules(self, text, k=5):
        """Ищет релевантные правила для текста."""
        vector = get_embedding(text)  # Используем функцию из utils.embeddings
        distances, indices = self.index.search(vector.reshape(1, -1), k)
        results = [self.data[idx] for idx in indices[0] if idx != -1]
        return results

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)

    def _save_data(self):
        with open(self.data_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)
