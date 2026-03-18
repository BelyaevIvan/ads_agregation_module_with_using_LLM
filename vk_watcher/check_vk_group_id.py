import requests

TOKEN = "2ea2903e2ea2903e2ea2903e032d9cdb1422ea22ea2903e47fa3cffb74f0cbbfb2efc22"
GROUP_SCREEN_NAME = "club226109228"  # часть после vk.com/

url = "https://api.vk.com/method/groups.getById"
params = {
    "group_id": GROUP_SCREEN_NAME,
    "access_token": TOKEN,
    "v": "5.131",
}

response = requests.get(url, params=params).json()
print(response)
