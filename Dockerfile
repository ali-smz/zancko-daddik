
FROM python:3.11-slim


WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt


COPY . .


RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
