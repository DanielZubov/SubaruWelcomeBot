FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код бота
COPY main.py .

# Запуск
CMD ["python", "main.py"]
