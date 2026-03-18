import requests

TOKEN = "2ea2903e2ea2903e2ea2903e032d9cdb1422ea22ea2903e47fa3cffb74f0cbbfb2efc22"
GROUP_ID = 193532348  
API_VERSION = "5.131"

url = "https://api.vk.com/method/wall.get"
params = {
    "owner_id": -GROUP_ID,
    "count": 1,
    "access_token": TOKEN,
    "v": API_VERSION,
}

response = requests.get(url, params=params).json()
print(response)
