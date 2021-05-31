FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./services/User/requirements.txt /code/
COPY ./services/User/src /code/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt