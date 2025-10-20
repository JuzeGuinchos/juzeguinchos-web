FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
# Logs no stdout e timeout maior para evitar mortes prematuras
CMD ["gunicorn","-w","2","--timeout","180","--access-logfile","-","--error-logfile","-","-b","0.0.0.0:$PORT","executar:app"]
