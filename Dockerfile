FROM python:3.6-stretch
WORKDIR /code
ADD . /code
ENV FLASK_APP app.py 
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV=development
RUN pip install -r requirements.txt
# CMD ["flask", "run"]
# CMD gunicorn --bind 0.0.0.0:$PORT app:app
CMD gunicorn app:app --worker-class eventlet -w 1 --bind 0.0.0.0:5000 --reload