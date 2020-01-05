"""
Created on Wed Nov 20 08:02:08 2019

@author: daniel
"""
###############################################################################
###############################################################################
        #########           ###########                ###########            
        #        #      @        #                          # 
        #        #               #                          #
        #        #      #        #         #########        #
        #########       #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #########       #   ###########    #########        #
###############################################################################
###############################################################################
import time
import serial
import pynmea2

def parseGPS(dato):
    if dato.find('GGA') > 0:
        msg = pynmea2.parse(dato)
        if(msg.latitude != 0.0 and msg.longitude != 0.0):
            mensaje = str(msg.latitude)+","+str(msg.longitude)
            guardar_valores("/home/pi/CodRaspV1/UBICACION/UBICACION.txt",mensaje)
            time.sleep(500)
def guardar_valores(archivo,mensaje):
        print(mensaje)
        f = open(archivo,'w+')
        f.write(mensaje)
        f.close()         
print("EJECUTANDO LECTURA DE GPS")
while True:
    try:
        serialPort = serial.Serial("/dev/ttyS0", 9600, timeout = 10)
        dato = serialPort.readline()
        dato = dato.decode()
        dato = dato.replace("\r\n","")
        #print(dato)
        parseGPS(dato)
    except:
        pass
        #serialPort.close()
###############################################################################
###############################################################################
        #########           ###########                ###########            
        #        #      @        #                          # 
        #        #               #                          #
        #        #      #        #         #########        #
        #########       #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #        #      #        #        #         #       #
        #########       #   ###########    #########        #
###############################################################################
###############################################################################
