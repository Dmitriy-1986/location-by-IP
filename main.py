import requests
from pyfiglet import Figlet
import folium


def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            print('Ошибка при получении общедоступного IP-адреса:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Ошибка при выполнении запроса:', e)
        return None


def get_info_by_ip(ip='127.0.0.1'):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        # print(response)
        
        data = {
            '[IP]': response.get('query'),
            '[Int prov]': response.get('isp'),
            '[Org]': response.get('org'),
            '[Country]': response.get('country'),
            '[Region Name]': response.get('regionName'),
            '[City]': response.get('city'),
            '[ZIP]': response.get('zip'),
            '[Lat]': response.get('lat'),
            '[Lon]': response.get('lon'),
        }
        
        for k, v in data.items():
            print(f'{k} : {v}')
        
        area = folium.Map(location=(response.get('lat'), response.get('lon')))

        # Added Marker on location so it is lots easier to see the l
        folium.Marker(location=(response.get('lat'), response.get('lon')), tooltip="Probably the location of the target.").add_to(area)

        area.save(f'{response.get("query")}_{response.get("city")}.html')

    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу.")


def main():
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('IP INFO'))

    public_ip = get_public_ip()
    if public_ip:
        print("Ваш общедоступный IP-адрес:", public_ip)
        get_info_by_ip(ip=public_ip)
    else:
        print("Не удалось получить общедоступный IP-адрес. Проверьте соединение с интернетом.")


if __name__ == '__main__':
    main()

