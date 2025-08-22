FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir chainlit requests

COPY app.py ./app.py

ENV PORT=8000
EXPOSE 8000

CMD ["chainlit", "run", "app.py", "-h", "0.0.0.0", "-p", "8000"]

