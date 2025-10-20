FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Gunicorn process (Render expõe a env PORT)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:$PORT", "executar:app"]
