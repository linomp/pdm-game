FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/mvp/server
COPY .env /code/mvp/server/

CMD ["uvicorn", "mvp.server.api:app", "--host", "0.0.0.0", "--port", "8000"]