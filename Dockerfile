FROM python:slim


RUN useradd dolimore

WORKDIR /home/dolimore

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install waitress

COPY app app
COPY migrations migrations
COPY dolimore.py ./
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app

RUN chown -R dolimore:dolimore ./
USER dolimore

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]