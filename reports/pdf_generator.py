from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generate_pdf(content, output_path):
    """
    Генерация PDF-документа с использованием reportlab.
    """
    # Регистрируем шрифт, поддерживающий Unicode
    pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))

    c = canvas.Canvas(output_path)
    text = c.beginText(40, 800)  # Начальная позиция текста
    text.setFont("DejaVuSans", 12)  # Используем Unicode-шрифт

    # Добавляем строки текста
    for line in content:
        text.textLine(line)

    # Завершаем создание PDF
    c.drawText(text)
    c.save()
