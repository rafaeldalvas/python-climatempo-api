import requests
import json
import PySimpleGUI as sg

iTOkEN = "12cbb9df8039b84e50359459977c1695"

layout = [[sg.Text('informe a cidade:'), sg.InputText()],
          [sg.Text('informe o estado:'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# sg.preview_all_look_and_feel_themes()
sg.theme('Light Blue 7')
window = sg.Window('Climatempo', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    city = values[0]
    state = values[1]

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

        result = [[sg.Text("\n" + str(return_weather["name"]) + " em " + str(return_weather['data']["date"]))],
                  [sg.Text("Temperatura: " + str(return_weather['data']["temperature"]) + "ºC")],
                  [sg.Text("Umidade: " + str(return_weather['data']["humidity"]) + "%")],
                  [sg.Text("Céu: " + str(return_weather['data']["condition"]))]]

        window = sg.Window('Climatempo', result)
        event, values = window.read()