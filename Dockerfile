FROM python:3.11
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app2 /app


EXPOSE 4000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]