import json

from covid_parser import get_country_id
import requests

menu = input(
'''
Select what You want to do:
1. Add country
2. See country information
3. Delete country
4. Update country data
5. Show all countries
''')

def add_country():
    country = input("Which country You would like to add? ")
    result = (get_country_id(country.capitalize()))
    add = requests.post("http://127.0.0.1:5000/countries/" + country.lower(), result)
    print(add.json())

def see_country_info():
    country = input("Which country You would like to see? ")
    get_country = requests.get("http://127.0.0.1:5000/countries/" + country.lower())
    print(get_country.json())

def delete_country():
    country = input("Which country You would like to delete? ")
    del_country = requests.delete("http://127.0.0.1:5000/countries/" + country.lower())
    print(del_country.json())

def update_country():
    country = input("Which country You would like to update? ")
    what_to_update = input('''
    Please insert data to update in json 
    ''')
    what_to_update = json.loads(what_to_update)
    print(what_to_update)
    print(type(what_to_update))
    res = requests.patch("http://127.0.0.1:5000/countries/" + country.lower(), what_to_update)
    print(res.json())

def show_all():
    result = requests.get("http://127.0.0.1:5000/all")
    print(result.json())

if menu == '1':
    add_country()

if menu == '2':
    see_country_info()

if menu == '3':
    delete_country()

if menu == '4':
    update_country()

if menu == '5':
    show_all()