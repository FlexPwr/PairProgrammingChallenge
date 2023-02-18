FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY server.py /app/
ENV PORT=5050
ENV HOST=0.0.0.0
CMD [ "python3" , "server.py"]