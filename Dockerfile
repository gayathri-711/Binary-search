# Minimal Dockerfile for the Flask-based DS mini project
FROM python:3.11-slim

# set workdir
WORKDIR /app

# avoid generation of .pyc files and enable stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy app sources
COPY . /app

# ensure a directory for persistent data
RUN mkdir -p /data
ENV STUDENT_DATA_FILE=/data/student_data.json

# expose port used by Flask
EXPOSE 5000

# runtime - using builtin server for simplicity; replace with gunicorn for production
CMD ["python", "app.py"]
