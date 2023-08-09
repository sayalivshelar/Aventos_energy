clear
echo "................................................................................"
echo "............................... SEM PROJECT....................................."
echo "................................................................................"

echo "Python version check"
python --version > output.txt 2>&1
VAR=$(awk '{print $2}' output.txt)
python --version




var1=0
code --version > var1 2>&1                  #EXTRACTING THE VERSION NUMBER FORM THE COMMANDS
VAR=$(awk '{print $0}' var1 | tr -d '.'' ')
if [ $VAR ]
then
	echo " "
else 
  	echo "Installing the visual studio code......"
	sudo apt install code
fi

#####################################################
#   	  			DOCKER CHECK					#
#####################################################
# which docker
echo "...........Checking Docker version ........" 
var1=0
docker --version
docker --version > var1 2>&1                  #EXTRACTING THE VERSION NUMBER FORM THE COMMANDS
VAR=$(awk '{print $3}' var1 | tr -d '.'',')
# echo "docker version="$VAR
# docker --version > output.txt 2>&1                  #EXTRACTING THE VERSION NUMBER FORM THE COMMANDS
# VAR=$(awk '{print $3}' output.txt | tr -d '.'',')
# echo "docker version="$VAR



if [ $VAR ]
then
    # docker --version | grep "Docker version"
    if [ $VAR -gt 201016 ]
    then
        echo "Docker existing"
    else
		echo "Installing the DOCKER please wait it may take time depending on the internet speed......."
		sudo apt update                                      #uncomment all below lines	# commands to install docker
		sudo apt upgrade -y
		curl -fsSL https://get.docker.com -o get-docker.sh
		sudo bash get-docker.sh
		echo "Warning Wrong User name are not allowed"
		echo "Enter raspberry pi user name "
		read raspberry_pi_name
		sudo usermod -aG docker $raspberry_pi_name
		docker version
		sudo apt install python3-pip -y
		sudo pip3 install docker-compose
		docker-compose version
    fi
else
	echo "Installing the DOCKER please wait it may take time depending on the internet speed......."
	sudo apt update                                      #uncomment all below lines	# commands to install docker
	sudo apt upgrade -y
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo bash get-docker.sh
	echo "Warning Wrong User name are not allowed"
	echo "Enter raspberry pi user name "
	read raspberry_pi_name
	sudo usermod -aG docker $raspberry_pi_name
	docker version
	sudo apt install python3-pip -y
	sudo pip3 install docker-compose
	docker-compose version
fi
#####################################################
#   			PYMODBUS CHECK						#
#####################################################

echo "Checking PyModbus is present or not.."

#EXTRACTING THE VERSION NUMBER FORM THE COMMANDS
pymodbus.console --version | grep "-" > output.txt 2>&1
VAR=$(awk '{print $5}' output.txt | tr -d '.'']')
# echo "PyModbus version="$VAR'abcd'
pymodbus.console --version
if [ $VAR ]
then
	echo "PyModbus existing "
    if [ $VAR -ge 253 ]
    then
        echo "Required PyModbus existing :)"
    else
		echo "Installing the PyModbus......."
		sudo pip install pymodbus
    fi
else 
  	echo "Installing the PyModbus.......1"
	sudo pip install pymodbus
fi
 
# 
python - << EOF
import sys
import subprocess
try:
	import schedule
except:
	subprocess.call(['pip','install','schedule']),
	pass

try:
    import psycopg2
except:
    subprocess.call(['pip','install','psycopg2']),

try:
	import tqdm
except:
	subprocess.call(['pip','install','tqdm']),


EOF




# spinner()
# {
#     local pid=$!
#     local delay=0.75
#     local spinstr='|/-\'
#     while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
#         local temp=${spinstr#?}
#         printf " [%c]  " "$spinstr"
#         local spinstr=$temp${spinstr%"$temp"}
#         sleep $delay
#         printf "\b\b\b\b\b\b"
#     done
#     printf "    \b\b\b\b"
# }
# (a_long_running_task) & spinner

python - << EOF
import sys
import subprocess
import os
import time
Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
os.chdir(Dir_path+"/sem_django")
print("Building the docker")
subprocess.call(['pip','install','--upgrade','pip']),  
# subprocess.call(['pip','install','--upgrade','pip','--no-warn','-script,'-location']), 
subprocess.call(['sudo','docker-compose','build']),
subprocess.call(['sudo','docker-compose','up','-d']),
print("Server is taking some time to get up")
EOF
# server_up_time=120
# while(server_up_time != 0):
# 	# print("=",end="")
# 	subprocess.call(['echo','-n','.']),
# 	time.sleep(1)
# 	server_up_time-=1
# print("")

# print("Server is up")
# EOF
count=0
total=120
pstr="[=======================================================================]"

while [ $count -lt $total ]; do
  sleep 1 # this is work
  count=$(( $count + 1 ))
  pd=$(( $count * 73 / $total ))
  printf "\r%3d.%1d%% %.${pd}s" $(( $count * 100 / $total )) $(( ($count * 1000 / $total) % 10 )) $pstr
done
echo ''


cd sem_django/sem
ls


CONTAINER_NAME='container_django_SEM'

CID=$(sudo docker ps -q -f status=running -f name=^/${CONTAINER_NAME}$)
echo "${CID}"
if [ ! "${CID}" ]
then
  	echo "Container doesn't exist"

else
    echo "creating USER..."
    sudo docker exec -it $CID python manage.py createsuperuser 
fi
unset CID

sudo docker-compose down
