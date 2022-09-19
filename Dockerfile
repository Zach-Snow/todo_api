FROM python:3

RUN apt-get update -y \
    && apt-get install -y curl wget
RUN pip3 install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

EXPOSE 80 5000

CMD [ "bash", "start.sh" ]