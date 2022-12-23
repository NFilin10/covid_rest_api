import json

from covid import Covid
from bs4 import BeautifulSoup
import requests

#info about covid
covid = Covid()

def get_country_id(country):
    all_countries = list(covid.get_data())
    for i in range(0, len(all_countries)):
        while all_countries[i]['country'] != country:
            break
        else:
            id = (all_countries[i]['id'])
            return cov(id, country)



def cov(id, country):
    covid = Covid()
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.310'}
    response = requests.get("https://coronavirus-monitor.info/country/" + country.lower(), headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_='info_blk stat_block confirmed')
    comps = []
    location = covid.get_status_by_country_id(id)

    try:
        for item in items:
            comps.append({
                'cases': item.find('sup').get_text()
            })
        for title in comps:
            new_cases = (title['cases'])

    except AttributeError:
        new_cases = 0


    data = {
            "confirmed": location['confirmed'],
            "active": location['active'],
            "recovered": location['recovered'],
            "deaths": location['deaths'],
            "new_cases": new_cases
            }

    if data['confirmed'] == None:
        data['confirmed'] = 0
    if data['active'] == None:
        data['active'] = 0
    if data['recovered'] == None:
        data['recovered'] = 0
    if data['deaths'] == None:
        data['deaths'] = 0
    if data['new_cases'] == None:
        data['new_cases'] = 0

    return data


