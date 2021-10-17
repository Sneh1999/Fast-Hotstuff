FROM python:latest
WORKDIR /code
ENV SECRET_KEY=dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["stdbuf", "-oL", "python3", "server.py"]