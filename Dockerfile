FROM python:3.12.6

WORKDIR /SportHuinia

COPY ./requirements.txt /SportHuinia

RUN pip install --no-cache-dir -r requirements.txt --verbose

COPY ./api /SportHuinia/api
COPY ./database /SportHuinia/database
COPY ./dto /SportHuinia/dto
COPY ./exept /SportHuinia/exept
COPY ./logger /SportHuinia/logger
COPY ./service /SportHuinia/service
COPY .env /SportHuinia/.env


ENV PYTHONPATH="/SportHUYnya:$PYTHONPATH"


EXPOSE 5001

CMD ["python", "api/routes/app.py"]