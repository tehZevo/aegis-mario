FROM python:3.8

WORKDIR /app

RUN mkdir -p /app/roms

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 80
VOLUME ["/app/roms"]

CMD [ "python", "-u", "main.py" ]
