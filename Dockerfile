FROM python:3.7-alpine
WORKDIR /code
ADD . /code
ENV FLASK_APP app.py 
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV=development
RUN pip install -r requirements.txt
# CMD ["flask", "run"]
CMD gunicorn --bind 0.0.0.0:$PORT app