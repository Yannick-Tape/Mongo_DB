from pymongo import MongoClient
from pprint import pprint

# Connexion à MongoDB
client = MongoClient(
    host="127.0.0.1",
    port=27017,
    username="datascientest",
    password="dst123",
    authSource="admin"
)

db = client["sample"]
books = db["books"]

print("\n===================================")
print("# (b) Liste des bases de données")
print("===================================\n")
print(client.list_database_names())

print("\n==============================")
print("# (c) Liste des collections")
print("==============================\n")
print(db.list_collection_names())

print("\n==========================================")
print("# (d) Un document de la collection books")
print("==========================================\n")
pprint(books.find_one())

print("\n===================================")
print("# (e) Nombre total de documents")
print("===================================\n")
print(books.count_documents({}))

print("\n======================================")
print("# (a) Livres avec plus de 400 pages")
print("======================================\n")
print(books.count_documents({"pageCount": {"$gt": 400}}))
print("\n# (a) Livres avec plus de 400 pages et publiés")
print(books.count_documents({"pageCount": {"$gt": 400}, "status": "PUBLISH"}))

print("\n=======================================================")
print("# (b) Livres contenant 'Android' dans la description")
print("=======================================================\n")
print(books.count_documents({"$or": [
    {"shortDescription": {"$regex": "Android", "$options": "i"}},
    {"longDescription": {"$regex": "Android", "$options": "i"}}
]}))

print("\n===================================")
print("# (c) Regrouper les catégories")
print("===================================\n")
pprint(list(books.aggregate([
    {"$group": {
        "_id": None,
        "categories": {"$addToSet": "$categories"}
    }}
])))

print("\n=====================================================")
print("# (d) Livres mentionnant Python, Java, C++, Scala")
print("=====================================================\n")
print(books.count_documents({
    "$or": [
        {"longDescription": {"$regex": "Python", "$options": "i"}},
        {"longDescription": {"$regex": "Java", "$options": "i"}},
        {"longDescription": {"$regex": "C\\+\\+", "$options": "i"}},
        {"longDescription": {"$regex": "Scala", "$options": "i"}}
    ]
}))

print("\n=================================================")
print("# (e) Statistiques sur les pages par catégorie")
print("=================================================\n")
pprint(list(books.aggregate([
    {"$unwind": "$categories"},
    {"$group": {
        "_id": "$categories",
        "max_pages": {"$max": "$pageCount"},
        "min_pages": {"$min": "$pageCount"},
        "avg_pages": {"$avg": "$pageCount"}
    }}
])))

print("\n==============================================")
print("# (f) Extraction des dates de publication")
print("==============================================\n")
pprint(list(books.aggregate([
    {"$match": {"publishedDate": {"$exists": True}}},
    {"$project": {
        "title": 1,
        "year": {"$year": "$publishedDate"}
    }},
    {"$match": {"year": {"$gt": 2009}}},
    {"$limit": 20}
])))

print("\n=================================")
print("# (g) Extraction des auteurs")
print("=================================\n")
pprint(list(books.aggregate([
    {"$project": {
        "title": 1,
        "first_author": {"$arrayElemAt": ["$authors", 0]}
    }}
])))

print("\n====================================================")
print("# (h) Nombre de publications par auteur (top 10)")
print("=====================================================\n")
pprint(list(books.aggregate([
    {"$group": {"_id": {"$arrayElemAt": ["$authors", 0]}, "nb_books": {"$sum": 1}}},
    {"$sort": {"nb_books": -1}},
    {"$limit": 10}
])))

