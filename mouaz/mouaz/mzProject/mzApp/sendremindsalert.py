import requests

api_url = "http://192.168.30.20/mz/api/reminds/sendalerts/"
response = requests.get(api_url)


print(response.status_code) 