import requests

ESKIZ_EMAIL = "shohruhbek007dev@gmail.com"
ESKIZ_PASSWORD = "HKjQcZcGIAmC5BD5F9uff1DNd8m75x4qkP5r4FHk"
ESKIZ_TOKEN = None

# def get_eskiz_token():
#     global ESKIZ_TOKEN
#     if not ESKIZ_TOKEN:
#         response = requests.post("https://notify.eskiz.uz/api/auth/login", data={
#             "email": ESKIZ_EMAIL,
#             "password": ESKIZ_PASSWORD
#         })
#         ESKIZ_TOKEN = response.json()["data"]["token"]
#     return ESKIZ_TOKEN

def send_sms(phone, message):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTUwNzQ4NjEsImlhdCI6MTc1MjQ4Mjg2MSwicm9sZSI6InVzZXIiLCJzaWduIjoiZGI1NjYwNWVjMTQ2ZjMzNzVjOWYyMDA0N2ZlNzY1M2MxYzlkMzQ4NTZjM2FmODBlZjljYWI3MGE5NDE3YmJkZCIsInN1YiI6IjExMzgxIn0.xnq9eceY3j8rwF2B2UPkwUsi_ntwEVSI-Ni-VftFStw"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "mobile_phone": phone,
        "message": message,
        "from": "4546"  # или другой short code
    }
    response = requests.post("https://notify.eskiz.uz/api/message/sms/send", data=data, headers=headers)
    print("SMS RESPONSE:", response.status_code)
    print("SMS RESPONSE BODY:", response.json())
    return response.status_code == 200
