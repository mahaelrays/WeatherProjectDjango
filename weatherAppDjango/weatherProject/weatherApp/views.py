from django.shortcuts import render
import ipinfo
import requests
import urllib.request
import json

# Create your views here.
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def index(request):
    ip_address = get_ip()
    
    handler = ipinfo.getHandler()
    details = handler.getDetails(ip_address)
    city = details.city
    if request.method == 'GET':
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric&appid=b5a859826870b28db320d6530c804510' %city).read()
        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            'city': city,
            "Weather": str(list_of_data['weather'][0]['main']),
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                        + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        return render(request, 'index.html', data )
    elif request.method == 'POST':
        city = request.POST['city']
        # source contain JSON data from API
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=718bfb40fec2a75aee7767677f367613').read()

        # converting JSON data to a dictionary
        list_of_data = json.loads(source)

        # data for variable list_of_data
        data = {
            'city': city,
            "Weather": str(list_of_data['weather'][0]['main']),
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + ' '
                        + str(list_of_data['coord']['lat']),
            
            "temp": str(list_of_data['main']['temp']) + 'k',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
        }
        print(data)
    else:
        data ={}
    return render(request, "index.html", data)
    