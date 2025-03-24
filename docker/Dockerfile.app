FROM python:3.13-slim

WORKDIR /usr/src/app

COPY requirements ./requirements
RUN pip install --no-cache-dir -r requirements/app.txt

COPY . .

CMD [ "tail", "-f", "/dev/null" ]
