import os,sys
import requests
import json

# global headers
headers = {}

#dir_path_1= os.getcwd()
# Dir_path = os.getcwd()
Dir_path = os.path.abspath(os.path.dirname(sys.argv[0]))
# Dir_path_1= Dir_path.replace("/MainCode/Present_version",'')
print(Dir_path)

# if(Dir_path=='/home/hussmann/Desktop/SEM/MainCode'):
#     secret_file = str(Dir_path) + "/"+ "user.json"

# else:
secret_file = str(Dir_path) + "/" + "user.json"
    
#secret_file = str(Dir_path) + "/" + "user.json"
print(secret_file)
# /home/hussmann/Desktop/SEM/MainCode/Present_version/user.json

with open(secret_file, 'r') as f:
    secret = json.loads(f.read())

login_data = dict(email=secret['EMAIL'], password=secret['PASSWORD'])

def user_login():
    login = requests.post('http://localhost:8000/auth/jwt/create/', data=login_data)
    token = json.loads(login.content)
    #print(login.status_code, login.content)
    access_token = {"Authorization": ("JWT" + " " + str(token['access']))}
    headers.update(access_token)
    # print(headers)

# user_login()

    
