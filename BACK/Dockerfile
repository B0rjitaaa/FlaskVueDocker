FROM python:3

WORKDIR /backend

RUN pip install --no-cache-dir Flask==0.10.1 flask_cors

ADD ./backend /backend
ADD ./dist /backend/dist
ADD run.py /backend

CMD ["python", "run.py"]