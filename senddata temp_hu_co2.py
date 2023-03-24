from machine import Pin, SoftI2C
import machine
import network
import time
from i2c_lcd import I2cLcd
import socket
import dht
################################
serverip = '192.168.1.6'
port = 9000
################################
#########LCD########
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=1000000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
time.sleep(1)

lcd.clear() # clear LCD
text = 'Starting...'
lcd.putstr(text)
##################################################

def send_data(data):
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send(data.encode('utf-8'))
	data_server = server.recv(1024).decode('utf-8')
	print('Server:' , data_server)
	server.close()
	
################wifi##############
wifi = 'PKROAMING_2.4G'
password = 'pakorn18126'
wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
time.sleep(10)
wlan.connect(wifi, password)
time.sleep(10)
print(wlan.isconnected())
status = wlan.isconnected()
ip,_,_,_ = (wlan.ifconfig())

if status == True:
    lcd.clear()
    text = 'IP:{}'.format(ip)
    lcd.putstr(text)
    time.sleep(2)
    lcd.clear()
    lcd.putstr('Wifi Connected')
    time.sleep(2)
   
else:
    lcd.clear
    lcd.putstr('Wifi disconnected')
######################################


##################temp & CO2##################
print('temperature checking...')
d = dht.DHT22(Pin(16))
adc = machine.ADC(machine.Pin(36))

def read_co():
    value = adc.read()
    voltage = (value * 3.3) / 4096
    concentration = (voltage - 0.4) * 100 / 0.6
    return concentration

while True:
    d.measure()
    time.sleep(2)
    temp = d.temperature()
    humid = d.humidity()
    co_concentration = read_co()
    formatco = "{:.2f}".format(co_concentration)
    print("CO concentration: {:.2f} ppm".format(co_concentration))
    print(temp)
    print(humid)
    '''text ='TEMP-HUMID:{} and {}:{}'.format(temp,humid,co_concentration)'''
    text ='TEMP-HUMID-CO2...{}/{}/{}'.format(temp,humid,formatco)
    send_data(text)
    time.sleep(3)
    print('-------------------------------') 
    
    lcd.clear()
    lcd.putstr(text)
    time.sleep(2)
    
########################################################


    



