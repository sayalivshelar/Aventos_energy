import socket   
from ast import Str
import os
import requests
import json
from inspect import Parameter
from multiprocessing.dummy import Value
import numbers
from threading import Thread
from optparse import Values
from pkgutil import get_data
import sys
import subprocess
from threading import local
from tkinter import N
from tokenize import Number
from turtle import fd
from unicodedata import name
import dbus, dbus.mainloop.glib
from gi.repository import GLib
from example_advertisement import Advertisement
from example_advertisement import register_ad_cb, register_ad_error_cb
from example_gatt_server import Service, Characteristic
from example_gatt_server import register_app_cb, register_app_error_cb
#import header1
import time
import init

Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
Dir_path= Dir_path.replace("/Bluetooth",'')
os.chdir(Dir_path)
subprocess.call(['ls'])
sys.path.insert(1,Dir_path)

# from Hotspot import hotspot_ethernet
# from Hotspot.hotspot_ethernet import Turn_on_hotspot,Turn_on_wifi
import configparser
import psutil


from login import headers, user_login
#from MainCode.Present_version.config_to_db import config_get
#from MainCode.Present_version import Master_Controller_Utils


BLUEZ_SERVICE_NAME =           'org.bluez'
DBUS_OM_IFACE =                'org.freedesktop.DBus.ObjectManager'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE =           'org.bluez.GattManager1'
GATT_CHRC_IFACE =              'org.bluez.GattCharacteristic1'
UART_SERVICE_UUID =            '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
UART_RX_CHARACTERISTIC_UUID =  '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
UART_TX_CHARACTERISTIC_UUID =  '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
LOCAL_NAME =                   '_SEM_HUSSMANN_BLE_'
mainloop = None
macro='''
start_of-frame=0
client_side=2
server_side=3
read=r
write=w
'''
#from python.enum import Parameter_name
#import json 


def config_get(API):
    r = requests.get(API, headers=headers)
    error_code = r.status_code
    error_status = r.text
    if(error_code == 401 or error_status == '{"detail":"Authentication credentials were not provided."}'):
        user_login()
        r = requests.get(API, headers=headers)
    return r


DATAthread=None

class TxCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_TX_CHARACTERISTIC_UUID,
                                ['notify'],service)
        self.notifying = False
        init.DATAthread=Thread(target=self.TXthread)
    def TXthread(self):
        time.sleep(1)
        while(1):
            if(init.Tx_Flag == True):
                init.Tx_Flag = False
                self.send_tx(init.Tx_buff)
            time.sleep(0.1)

    def send_tx(self,s):
        if not self.notifying:
            return
        value = []
        for c in s:
            value.append(dbus.Byte(c.encode()))
        self.PropertiesChanged(GATT_CHRC_IFACE, {'Value': value}, [])

    def StartNotify(self):
        if self.notifying:
            return
        
        print("it is connected")
        self.notifying = True
        init.Connection_Flag = True

    def StopNotify(self):
        if not self.notifying:
            return
        print("disconnected")
        self.notifying = False
        init.Connection_Flag = False

def RXthread():
    time.sleep(1)
    Config_present = configparser.ConfigParser()
    Config_present.read("/Hotspot/hostpot_info.ini")
    Dir_path =  os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(".")
    dir_to_sem=os.getcwd()
    dir_to_sem+='/MainCode/Present_version'
    os.chdir(dir_to_sem)
    Config_present = configparser.ConfigParser()
    Config_present.read("Controller_select.ini")
    Controller_varient= Config_present.get('CONTROLLER', 'varient')
    os.chdir(Dir_path)
    if Controller_varient == 'Xr75':
        Check_Sec_Api= "http://localhost:8000/api/xr75/sec"
        Check_Min_Api="http://localhost:8000/api/xr75/min/"
        Check_Hour_Api="http://localhost:8000/api/xr75/hour/"
        controller_name="xr75"

    if Controller_varient == 'Corelink':
        Check_Sec_Api= "http://localhost:8000/api/core-link/sec/"
        Check_Min_Api="http://localhost:8000/api/core-link/min/"
        Check_Hour_Api="http://localhost:8000/api/core-link/hour/"
        controller_name="core-link"

    if Controller_varient == 'Ir33':
        Check_Sec_Api= "http://localhost:8000/api/ir33/sec"
        Check_Min_Api="http://localhost:8000/api/ir33/min/"
        Check_Hour_Api="http://localhost:8000/api/ir33/hour/"
        controller_name="ir33"

    if Controller_varient == 'Rtn400':
        Check_Sec_Api= "http://localhost:8000/api/rtn400/sec"
        Check_Min_Api="http://localhost:8000/api/rtn400/min/"
        Check_Hour_Api="http://localhost:8000/api/rtn400/hour/"
        controller_name="rtn400"
    
    while(1):
        if(init.Rx_Flag == True):
            init.Rx_Flag = False
            data=init.Rx_buff
            p=data
            p=p.replace(',',' ')
            print(p)
            new_list=p.split(' ')
            print(new_list)
            try:
               a=(int(new_list[0] ))
               print(a,type(a))
            except:
               print("invalid input")
            if(int(new_list[0])== 0x01):
                subprocess.call("ifconfig",shell=True)
                network=psutil.net_if_stats()
                network1=psutil.net_if_addrs()
                list1=[]
                for key in network.keys():
                    list1.append(key)
                values=(list(network1.values()))
                value1=[lis[(0)] for lis in list(values)]
                list2=[value1[0][1],value1[2][1],value1[1][1]]
                IPAddr=(value1[1][1])
                if(int(new_list[1]) != ''):
                    if(int(new_list[1])== 0x01):
                        print(new_list[0],new_list[1])
                        try:
                            dict_count = response.json()
                            total_pram = (len(dict_count[0].keys()) - 3)
                            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
                            print("Total Number of Prameters in 10-Seconds Data Table:",total_pram)
                            print("Total Number of Rows(Entires) in Seconds Data Table:",row_count)
                            data_to_send=new_list[1]+","+'10'+","+str(total_pram)+","+str(row_count)
                            init.Tx_buff=data_to_send
                            init.Tx_Flag = True
                        except:
                            print("server down")
                            data_to_send=new_list[1]+","+'10'+","+'0'+","+'0'
                            init.Tx_buff=data_to_send
                            init.Tx_Flag = True
                    if(int(new_list[1])== 0x02):
                        print(new_list[0],new_list[1])
                        try:
                            response = config_get(Check_Min_Api)
                            dict_count = response.json()
                            total_pram = (len(dict_count[0].keys()) - 3)
                            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
                            print("Total Number of Prameters in 5-Minutes Data Table:",total_pram)
                            print("Total Number of Rows(Entires) in Minutes Data Table:",row_count)
                            data_to_send=new_list[1]+","+'300'+","+str(total_pram)+","+str(row_count)
                            init.Tx_buff=data_to_send
                            init.Tx_Flag = True
                        except:
                            print("server down")
                            data_to_send=new_list[1]+","+'300'+","+'0'+","+'0'
                            init.Tx_buff=data_to_send
                            init.Tx_Flag = True
                    if(int(new_list[1])== 0x03):
                        print(new_list[0],new_list[1])
                        try:
                            response = config_get(Check_Hour_Api)
                            dict_count = response.json()
                            total_pram = (len(dict_count[0].keys()) - 3)
                            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
                            print("Total Number of Prameters in 4-Hours Data Table:",total_pram)
                            print("Total Number of Rows(Entires) in Hours Data Table:",row_count)
                            data_to_send=new_list[1]+","+'14400'+","+str(total_pram)+","+str(row_count)
                            init.Tx_buff=data_to_send
                            init.Tx_Flag = True
                        except:
                            print("server down")
                            data_to_send=new_list[1]+","+'14400'+","+'0'+","+'0'
                            init.Tx_buff=data_to_send
                            init.Tx_Flag = True
                    if(int(new_list[1])== 0x04):
                        print("Read_ip_address",IPAddr)
                        data_to_send=new_list[1]+","+str(IPAddr)
                        init.Tx_buff=data_to_send
                        init.Tx_Flag = True
                    if(int(new_list[1])== 0x05):
                        os.chdir("..")
                        dir_to_sem=os.getcwd()
                        Config_present.read(dir_to_sem+"/Hotspot/hostpot_info.ini")
                        update_version = Config_present.get('hotspot', 'ssid')
                        data_to_send=new_list[1]+","+str(update_version)
                        init.Tx_buff=data_to_send
                        init.Tx_Flag = True
                        os.chdir(Dir_path)
                    if(int(new_list[1])== 0x06):
                        print("Read_WiFi acess point password")
                        os.chdir("..")
                        dir_to_sem=os.getcwd()
                        Config_present.read(Dir_path+"/Hotspot/hostpot_info.ini")
                        update_version = Config_present.get('hotspot', 'pass')
                        data_to_send=new_list[1]+","+str(update_version)
                        init.Tx_buff=data_to_send
                        init.Tx_Flag = True
                        os.chdir(Dir_path)
                    if(int(new_list[1])== 0x07):
                        config_api='http://'+IPAddr+':8000/api/'+controller_name+'/config/'
                        sec_api='http://'+IPAddr+':8000/api/'+controller_name+'/sec/'
                        min_api='http://'+IPAddr+':8000/api/'+controller_name+'/min/'
                        hour_api='http://'+IPAddr+':8000/api/'+controller_name+'/hour/'
                        print(config_api,sec_api,min_api,hour_api)
                        print("Read_SuportedREST api's")
                        min_api='http://'+IPAddr+':8000/api/'+controller_name+'/min/'
                        data_to_send=new_list[1]+","+"'"+config_api+","+"'"+sec_api+","+"'"+min_api+","+"'"+hour_api+"'"
                        init.Tx_buff=data_to_send
                        init.Tx_Flag = True
                    if(int(new_list[1])== 0x08):
                        user_name="Reas SEM Module user name = "+os.getlogin()
                        print(user_name)
                        data_to_send=new_list[1]+","+"'"+os.getlogin()+"'"
                        init.Tx_buff=data_to_send
                        init.Tx_Flag = True

            elif(int(new_list[0])== 0x02):
                Config_present = configparser.ConfigParser()
                if(int(new_list[1]) & 0xf0 == 0x80):
                    print(int(new_list[1]) & 0x0f)
                    if((int(new_list[1]) & 0x0f)== 0x01):
                        print("changing WIFI ssid")
                        if(new_list[2]):
                            os.chdir("..")
                            dir_to_sem=os.getcwd()
                            Config_present.read(dir_to_sem+"/Hotspot/hostpot_info.ini")
                            Config_present['hotspot']['SSID'] = new_list[2]
                            with open(dir_to_sem+"/Hotspot/hostpot_info.ini",'w') as config_file:
                                Config_present.write(config_file)
                                config_file.close()
                            init.Tx_buff="Updated WIFI ssid"
                            init.Tx_Flag = True
                            os.chdir(Dir_path)
                        else:
                            init.Tx_buff=" incorrect ssid"
                            init.Tx_Flag = True
                    elif((int(new_list[1]) & 0x0f)== 0x02):
                        if(new_list[2]):
                            print("changing WIFI pass")
                            os.chdir("..")
                            dir_to_sem=os.getcwd()
                            Config_present.read(dir_to_sem+"/Hotspot/hostpot_info.ini")
                            Config_present['hotspot']['pass'] = new_list[2]
                            os.chdir(".")
                            dir_to_sem=os.getcwd()
                            with open(dir_to_sem+"/Hotspot/hostpot_info.ini",'w') as config_file:
                                Config_present.write(config_file)
                                config_file.close()
                            init.Tx_buff="Updated WIFI pass"
                            init.Tx_Flag = True
                            os.chdir(Dir_path)
                        else:
                            init.Tx_buff=" incorrect pass"
                            init.Tx_Flag = True
                    elif((int(new_list[1]) & 0x0f)== 0x03):
                        print("hotspot enable wifi disable")
                        os.chdir("..")
                        dir_to_sem=os.getcwd()
                        status=hotspot_ethernet.Turn_on_hotspot(dir_to_sem)
                        if(status == 1):
                            init.Tx_buff="hotspot enable wifi disable"
                            init.Tx_Flag = True  
                        elif(status == 0):
                            init.Tx_buff="hotspot on already"
                            init.Tx_Flag = True 
                        os.chdir(Dir_path)
                    elif((int(new_list[1]) & 0x0f)== 0x04):
                        print("hotspot disable wifi enable") 
                        os.chdir("..")
                        dir_to_sem=os.getcwd()
                        status=hotspot_ethernet.Turn_on_wifi(dir_to_sem)
                        if(status == 1):
                            init.Tx_buff="hotspot disable wifi enable"
                            init.Tx_Flag = True 
                        elif(status == 0):
                            init.Tx_buff="wifi on already"
                            init.Tx_Flag = True
                        os.chdir(Dir_path)

def data_check(data):
    hostname=socket.gethostname()   
    IPAddr=socket.gethostbyname(hostname)     
    
    if data == '1':
        print("Read_db1")
        try:
            response = requests.get("http://localhost:8000/api/xr75/sec/")
            dict_count = response.json()
            total_pram = (len(dict_count[0].keys()) - 3)
            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
            print("Total Number of Prameters in 10-Seconds Data Table:",total_pram)
            print("Total Number of Rows(Entires) in Seconds Data Table:",row_count)
            data_to_send="Total Number of Prameters in 10-Seconds Data Table:"+total_pram +"Total Number of Rows(Entires) in Seconds Data Table:"+row_count
            init.Tx_buff=data_to_send
            init.Tx_Flag = True
        except:
            print("server down")
            init.Tx_buff="server down"
            init.Tx_Flag = True
            

    elif data == '2':
        print("Read_db2")
        try:
            response = requests.get("http://localhost:8000/api/xr75/min/")
            dict_count = response.json()
            total_pram = (len(dict_count[0].keys()) - 3)
            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
            print("Total Number of Prameters in 5-Minutes Data Table:",total_pram)
            print("Total Number of Rows(Entires) in Minutes Data Table:",row_count)
            data_to_send="Total Number of Prameters in 5-Minutes Data Table:"+total_pram +"Total Number of Rows(Entires) in Minutes Data Table:"+row_count
            init.Tx_buff=data_to_send
            init.Tx_Flag = True
        except:
            print("server down")
            init.Tx_buff="server down"
            init.Tx_Flag = True
    elif data == '3':
        print("Read_db3")
        try:
            response = requests.get("http://localhost:8000/api/xr75/hour/")
            dict_count = response.json()
            total_pram = (len(dict_count[0].keys()) - 3)
            row_count = (len([e for e in dict_count if isinstance(e, dict)]))
            print("Total Number of Prameters in 4-Hours Data Table:",total_pram)
            print("Total Number of Rows(Entires) in Hours Data Table:",row_count)
            data_to_send="Total Number of Prameters in 4-Hours Data Table:"+total_pram +"Total Number of Rows(Entires) in Hours Data Table:"+row_count
            init.Tx_buff=data_to_send
            init.Tx_Flag = True
        except:
            print("server down")
            init.Tx_buff="server down"
            init.Tx_Flag = True
    elif data == '4':
        print("Read_ip_address",IPAddr)
        data_to_send="Read_ip_address = "+IPAddr
        init.Tx_buff=data_to_send
        init.Tx_Flag = True
    elif data == '5':
        print("Read_WiFi acess point ssid name:",os.popen('sudo iwgetid -r').read())
    elif data == '6':
        print("Read_WiFi acess point password")
    elif data == '7':
        config_api='http://'+IPAddr+':8000/api/xr75/config/'
        sec_api='http://'+IPAddr+':8000/api/xr75/sec/'
        min_api='http://'+IPAddr+':8000/api/xr75/min/'
        hour_api='http://'+IPAddr+':8000/api/xr75/hour/'
        print(config_api,sec_api,min_api,hour_api)
        print("Read_SuportedREST api's")
        min_api='http://'+IPAddr+':8000/api/xr75/min/'
        data_to_send="1)"+config_api+" 2)"+sec_api+" 3)"+min_api+" 4)"+hour_api
        init.Tx_buff=data_to_send
        init.Tx_Flag = True
    elif data == '8':
        user_name="Reas SEM Module user name = "+os.getlogin()
        print(user_name)
        data_to_send=user_name
        init.Tx_buff=data_to_send
        init.Tx_Flag = True

def Tx_handle():
    time.sleep(1)
    while(1):

        if(init.Connection_Flag == True):
                time.sleep(10)
        time.sleep(1)

class RxCharacteristic(Characteristic):
   
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_RX_CHARACTERISTIC_UUID,
                                ['write'], service)
        

    def WriteValue(self, value, options):
      global Rx_Flag
      Recived_flag=False
      value=format(bytearray(value).decode())
      init.Rx_buff = value
      init.Rx_Flag = True

class UartService(Service):
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, UART_SERVICE_UUID, True)
        self.add_characteristic(TxCharacteristic(bus, 0, self))
        self.add_characteristic(RxCharacteristic(bus, 1, self))

class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
        return response

class UartApplication(Application):
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(UartService(bus, 0))

class UartAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(UART_SERVICE_UUID)
        self.add_local_name(LOCAL_NAME)
        self.include_tx_power = True

def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()
    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props and GATT_MANAGER_IFACE in props:
            return o
        print('Skip adapter:', o)
    return None

def Mainthread():
    time.sleep(2)
    mainloop.run()

def main():
    global mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    adapter = find_adapter(bus)
    if not adapter:
        print('BLE adapter not found')
        return

    service_manager = dbus.Interface(
                                bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    app = UartApplication(bus)
    adv = UartAdvertisement(bus, 0)

    mainloop = GLib.MainLoop()

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    ad_manager.RegisterAdvertisement(adv.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)


    init.initialization()    
    try:
        
        DATAthread1=Thread(target=RXthread)
        mainthread=Thread(target=Mainthread)
        Txthread=Thread(target=Tx_handle)
        init.DATAthread.start()
        DATAthread1.start()
        mainthread.start()
        Txthread.start()
        init.DATAthread.join()

    except Exception as e:
        print(e)
        adv.Release()

if __name__ == '__main__':
    main()