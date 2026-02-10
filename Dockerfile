FROM python:3.9-slim

WORKDIR /app

# Server endi yengil, og'ir kutubxonalar va tizim kutubxonalari shart emas.
# Faqat python kutubxonalarini o'rnatamiz.

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5000"]
