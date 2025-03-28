FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements/app.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "tail", "-f", "/dev/null" ]
