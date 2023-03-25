FROM python:3.9
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai
WORKDIR /app
COPY src/ src/
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "/app/src/main.py"]
