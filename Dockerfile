FROM python:3
ENV PYTHONUNBUFFERED 1
COPY . ./app
WORKDIR /app 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["gunicorn", "--bind","0.0.0.0:8000", "wsgi:main"]