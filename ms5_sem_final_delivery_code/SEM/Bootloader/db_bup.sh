CONTAINER_NAME='postgres_database_SEM'

CID=$(sudo docker ps -q -f status=running -f name=^/${CONTAINER_NAME}$)
echo "${CID}"
ls
# sudo docker exec -t ${CID} pg_dump -c -U postgres > /home/hussmann/Desktop/SEM/Webserver/sem_django/SEM-Backup-Hussmann--$(date +"%d-%m-%Y---%H-%M-%S").sql "SEM"
sudo docker exec -t ${CID} pg_dump -c -U postgres > SEM-Backup-Hussmann--$(date +"%d-%m-%Y---%H-%M-%S").sql "SEM"
