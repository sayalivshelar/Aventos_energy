import subprocess
import psutil

subprocess.call("ifconfig",shell=True)
network=psutil.net_if_stats()
print(network)
network1=psutil.net_if_addrs()
print(network1)
list1=[]
for key in network.keys():
   list1.append(key)
print(list1)
values=(list(network1.values()))
print(values)


value1=[lis[(0)] for lis in list(values)]
print(value1)
list2=[value1[0][1],value1[2][1],value1[1][1]]
#print(list2)
print(list2[2])

interface={}
for key in list1:
   for value in list2:
      interface[key]=value
      list2.remove(value)
      break

# print(interface)


























# import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
# from time import sleep # Import the sleep function from the time module

# GPIO.setwarnings(False) # Ignore warning for now
# GPIO.setmode(GPIO.BOARD)
# Pin_num=40
# GPIO.setup(Pin_num, GPIO.OUT, initial=GPIO.LOW)
# while 1:   
#    GPIO.output(Pin_num,GPIO.HIGH) 
#    sleep(1)
#    GPIO.output(Pin_num,GPIO.LOW) 
#    sleep(1)
