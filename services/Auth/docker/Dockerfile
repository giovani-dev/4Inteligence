FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./services/Auth/requirements.txt /code/
COPY ./services/Auth/src /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt