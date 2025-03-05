# Do not forget to create a variable in your console with the export command
# You can choose the city of your choice, you only need to write the name in english

# COMMANDE EXECUTER DANS LE TERMINAL AFIN DE CREER LA VARIABLE D'ENVIRONNEMENT
# CECI DOIT ETRE FAIT AVANT DE LANCER CE SCRIPT CI DESSSOUS
#    export WEATHER="96b34ee39af67e2199f1212ecb3e6757"


# You will need to create a variable WEATHER with your key of OpenWeatherMap

import os
import requests

KEY = os.getenv("WEATHER")
CITY = "New York"

r = requests.get(
    url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
        CITY, KEY
    )
)

data = r.json()
clean_data = {i: data[i] for i in ["weather", "main"]}
clean_data["weather"] = clean_data["weather"][0]


from datetime import datetime
current = datetime.now().strftime("%H:%M:%S")
clean_data["time"] = current
clean_data["city"] = CITY

from pymongo import MongoClient
client = MongoClient(host="localhost", port=27017, username="datascientest", password="dst123")
sample = client["sample"]
col = sample.create_collection(name="weather")
col.insert_one(clean_data)


def make_data(city):
    r = requests.get(
        url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
            city, KEY
        )
    )
    data = r.json()
    clean_data = {i: data[i] for i in ["weather", "main"]}
    clean_data["weather"] = clean_data["weather"][0]
    return clean_data


def add_key(data, city):
    current = datetime.now().strftime("%H:%M:%S")
    data["time"] = current
    data["city"] = city
    return data


def add_data(client, cities):
    col = client["sample"]["weather"]
    for city in cities:
        data = make_data(city)
        data = add_key(data, city)
        col.insert_one(data)

add_data(client, ["courbevoie", "puteaux", "lourdes","bourg-la-reine"])



col=client["sample"]["weather"]
for i in list(col.find({"weather.main": "Clear"}, {"_id": 0, "city": 1})):
    print(i)

col=client["sample"]["weather"]

print(
    len(
        list(
            col.find(
                {
                    "$and": [
                        {"main.temp_min": {"$gte": 287}},
                        {"main.temp_max": {"$lte": 291}},
                    ]
                }
            )
        )
    )
)
# We can use also the count_documents function : 

print(
    col.count_documents(
        {
            "$and": [
                {"main.temp_min": {"$gte": 287}},
                {"main.temp_max": {"$lte": 291}},
            ]
        }
    )
)

# With the implicit AND 

print(
    col.count_documents(
        {"main.temp_min": {"$gte": 287}, "main.temp_max": {"$lte": 291}},
    )
)


col=client["sample"]["weather"]
for i in list(col.aggregate([{"$group": {"_id": "$weather.main", "nb": {"$sum": 1}}}])):
    print(i)



# COMMANDE EXECUTER DANS LE TERMINAL AFIN DE CREER LA VARIABLE D'ENVIRONNEMENT
# CECI DOIT ETRE FAIT AVANT DE LANCER CE SCRIPT CI DESSSUS
#    export WEATHER="96b34ee39af67e2199f1212ecb3e6757"


