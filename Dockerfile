FROM python:3.12.6

WORKDIR /QSPORT

COPY ./requirements.txt /QSPORT

RUN pip install --no-cache-dir -r requirements.txt

COPY ./api /QSPORT/api
COPY ./database /QSPORT/database
COPY ./dto /QSPORT/dto
COPY ./exept /QSPORT/exept
COPY ./logger /QSPORT/logger
COPY ./service /QSPORT/service
COPY .env /QSPORT/.env


ENV PYTHONPATH="/QSPORT:$PYTHONPATH"


EXPOSE 5001

CMD ["python", "api/routes/app.py"]