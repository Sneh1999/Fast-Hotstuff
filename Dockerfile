FROM python:latest
WORKDIR /code
ENV FLASK_APP=node
ENV FLASK_ENV=development
ENV SECRET_KEY=dev
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]