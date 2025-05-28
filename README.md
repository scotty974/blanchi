## Mettre dataset sur docker

docker cp <name_dataset> <container_id>:/var/lib/neo4j

## Mettre le dataset sur la bdd

Dans le Exec de votre container exécuté la commande suivante : 

cypher-shell -f <name_dataset>

