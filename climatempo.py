import requests
import json

iTOkEN = "12cbb9df8039b84e50359459977c1695"

city = input("informe a cidade: ")
state = input("informe o estado: ")
city_url = "http://apiadvisor.climatempo.com.br/api/v1/locale/city?name=" + str(city) + "&state=" + str(state) + "&token=" + str(iTOkEN)
response = requests.request("GET", city_url)
return_request  = json.loads(response.text)
# print(return_request)

for key in return_request:
    city_id = key['id']

    register_url = "http://apiadvisor.climatempo.com.br/api-manager/user-token/" + str(iTOkEN) + "/locales"
    payload = "localeId[]=" + str(city_id)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("PUT", register_url, headers=headers, data=payload)

    weather_url = "http://apiadvisor.climatempo.com.br/api/v1/weather/locale/" + str(city_id) + "/current?token=" + str(iTOkEN)
    weather = requests.request("GET", weather_url)
    return_weather = json.loads(weather.text)
    # print(return_weather)
    print("\n" + str(return_weather["name"]) + " em " + str(return_weather['data']["date"]))
    print("Temperatura: " + str(return_weather['data']["temperature"]) + "ºC")
    print("Umidade: " + str(return_weather['data']["humidity"]) + "%")
    print("Céu: " + str(return_weather['data']["condition"]))
