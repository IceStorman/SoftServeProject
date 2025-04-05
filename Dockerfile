FROM python:3.12.6

WORKDIR /app

COPY ./requirments.txt /app
RUN pip install --no-cache-dir -r requirments.txt

COPY ./api /app/
COPY ./database /app/
COPY ./dto /app/
COPY ./exept /app/
COPY ./logger /app/
COPY ./service /app/



EXPOSE 5001

CMD ["python", "api/routes/__init__.py"]