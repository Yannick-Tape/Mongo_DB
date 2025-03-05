from pymongo import MongoClient

client = MongoClient(
    host = "127.0.0.1",
    port = 27017,
    username = "datascientest",
    password = "dst123"
)

sample = client["sample"]
c_zips = sample["zips"]

rand = sample.get_collection(name="rand")

# We can check the creation of the collection with this
print(sample.list_collection_names())

data = [
  {"name": "Melthouse","bread":"Wheat","sauce": "Ceasar"},
  {"name": "Italian BMT", "extras": ["pickles","onions","lettuce"],"sauce":["Chipotle", "Aioli"]},
  {"name": "Steakhouse Melt","bread":"Parmesan Oregano"},
  {"name": "Germinal", "author":"Emile Zola"},
  {"pastry":"cream puff","flavour":"chocolate","size":"big"}
]

rand.insert_many(data)

# Afficher tous les documents de la collection rand
for doc in rand.find():
    print(doc)

print("########################################################################################################################################################")


zips = client["sample"]["zips"]

for i in list(zips.find({},{"_id":0,"city":1}).limit(12)):
    print(i)


print("########################################################################################################################################################")

zips = client["sample"]["zips"]

print(zips.find().distinct("state"))


print("########################################################################################################################################################")

from pprint import pprint

pprint(client["sample"]["cie"].find_one())


print("########################################################################################################################################################")

import re 

zips = client["sample"]["zips"]

exp = re.compile("^[0-9]*$")
pprint(list(zips.find({"city": exp}, {"city": 1})))

print("########################################################################################################################################################")

pprint(
    list(
        client["sample"]["cie"].aggregate(
            [
                {"$match": {"acquisitions.company.name": "Tumblr"}},
                {"$project": {"_id": 1, "society": "$name"}}
            ]
        )
    )
)



print("########################################################################################################################################################")








