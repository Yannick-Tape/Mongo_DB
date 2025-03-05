# Mongo_DB
Cours base de données NoSQL de DS



# Créer dossier (Mongo_DB_VM)
mkdir Mongo_DB_VM
cd Mongo_DB_VM
# clowner le repo (Mongo_DB) dans Mongo_DB_VM
git clone
# entrer dans le repo Mongo_DB (on voir bien le README.md et le .git caché)
# créer le dossier sample_training dans lequel on stockera les données .json
cd sample_training
sudo wget https://dst-de.s3.eu-west-3.amazonaws.com/mongo_fr/companies.json
sudo wget https://dst-de.s3.eu-west-3.amazonaws.com/mongo_fr/grades.json
sudo wget https://dst-de.s3.eu-west-3.amazonaws.com/mongo_fr/zips.json
ls -l    (on verifie que les 3 fichiers .json ont étés bien uploader)

ls -l && cd ..     (on revient au niveau du README.md)
# créer le docker-compose.yml 

version: "3.3"
services:
  mongodb:
    image : mongo:7.0
    container_name: my_mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: datascientest
      MONGO_INITDB_ROOT_PASSWORD: dst123
    volumes:
      - ./sample_training:/data/db
    ports:
      - 27017:27017

# lancer les conteneurs et verifier qu'ils tournent bien
docker-compose up -d
docker ps -a

# enter dans le conteneur MongoDB
docker exec -it my_mongo bash 
# importer un fichier JSON contenant des documents dans une base de données MongoDB.
mongoimport -d sample -c grades --authenticationDatabase admin -u datascientest -p dst123 --file /data/db/grades.json
exit
docker exec -it my_mongo ls -la /data/db/ | grep grades   (on verifie que le fichier a bien été importée)

# enter dans le conteneur MongoDB
docker exec -it my_mongo bash
# importer un fichier JSON contenant des documents dans une base de données MongoDB.
mongoimport -d sample -c zips --authenticationDatabase admin --username datascientest --password dst123 --file /data/db/zips.json
exit
docker exec -it my_mongo ls -la /data/db/ | grep zips   (on verifie que le fichier a bien été importée)

# enter dans le conteneur MongoDB
docker exec -it my_mongo bash
# se connecter un shell-mogoDB pour manipuler les collections 
mongosh -u datascientest -p dst123

# par défaut on se trouve sur la base de données "test". on se place sur sur la bonne base de données à l'aide de "use" et on affiche un document de la collection "zips"
use sample
db.zips.findOne()



























































