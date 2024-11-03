from azure.storage.blob import BlobClient
from azure.storage.blob import BlobServiceClient
import json
import http.client
import psycopg

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "7b30ce5132b8f28ee7cf0d2e6150fa03"
    }

conn.request("GET", "/fixtures?live=all", headers=headers)
res = conn.getresponse()
data = res.read()
json_data = json.loads(data.decode("utf-8"))
print(json_data)

# Запис до блоб сховища
sas_token = "sp=racwdl&st=2024-11-01T14:47:22Z&se=2024-11-08T22:47:22Z&spr=https&sv=2022-11-02&sr=c&sig=owmo2YurDuSbhEl2cGTyTM6Ik7pPkVx5jID%2BMS8fXPo%3D"
account_url = "https://kuisportblobgarage.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)


container_client = blob_service_client.get_container_client("apidata")
blob_name = "sport_data.json"  # Унікальний індекс для блоба. Можна запит апішки за нього брати
blob_client = container_client.get_blob_client(blob_name)
blob_client.upload_blob(json.dumps(json_data), overwrite=True)
print("JSON успішно збережено в Blob Storage.")

# Додавання унікальних значень ключів до основної бд
with psycopg.connect("dbname=your_db user=your_user password=your_password") as db_connection:
    with db_connection.cursor() as cursor:
        cursor.execute("UPDATE sports SET blob_index = %s WHERE sport_name = %s", (blob_name, 'назва_виду_спорту'))
    db_connection.commit()
print("Інформацію успішно збережено.")

# Читання без проміжного ключа
container_client = blob_service_client.get_container_client("apidata")
blob_client = container_client.get_blob_client("fixtures-live=all.json")
blob_data = blob_client.download_blob()
json_data = blob_data.readall().decode("utf-8")
print(json_data)

# Отримання індекса блоба з бд
sport_name = 'sport_name'
with psycopg.connect("dbname=your_db user=your_user password=your_password") as db_connection:
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT blob_index FROM sports WHERE sport_name = %s", (sport_name,))
        blob_index = cursor.fetchone()[0]

# Завантаження JSON з Blob Storage
blob_service_client = BlobServiceClient(account_url=account_url, credential=sas_token)
container_client = blob_service_client.get_container_client("apidata")
blob_client = container_client.get_blob_client(blob_index)

blob_data = blob_client.download_blob()
json_data = blob_data.readall().decode("utf-8")

# Виведення результату
print(json_data)
