from transformers import AutoTokenizer, AutoModel
import torch

# Загрузка модели для генерации эмбеддингов
tokenizer = AutoTokenizer.from_pretrained(
    "sentence-transformers/all-MiniLM-L6-v2"
)
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Генерация эмбеддинга для текста.

    :param text: Текст, для которого требуется сгенерировать эмбеддинг.
    :return: Векторное представление текста (эмбеддинг).
    """
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**tokens)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
