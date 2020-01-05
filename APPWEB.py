# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 17:21:21 2018

@author: Daniel Delgado Rodrìguez
         Juan Fernando Guerrero F.  
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
#-------------------------IMPORTAR LÌBRERIAS-----------------------------------
import time
import urllib3
import certifi
import urllib.request
from urllib.parse import urlencode
from datetime import datetime
#------------------------CLASE COMUNICACION------------------------------------
class comunicacion(object):
    #-----------------------CONSTRUCTOR----------------------------------------
    def __init__(self):
        self.id_nodo = "bote0001"
        self.dato = ""
        self.estado = True
        self.latitud = 0
        self.longitud = 0
        self.tiempo_muestra = 10
    #----------------------------------------------------------------------
    def leer_valores(self,archivo):
        f = open(archivo)
        linea = f.readline()
        f.close()
        return linea
    def guardar_valores(self,archivo,mensaje):
        f = open(archivo,'w+')
        f.write(mensaje)
        f.close()
    def obtener_fecha(self):
        hora_actual = datetime.now()
        fecha = hora_actual.strftime(""+str(hora_actual.year)+"/%m/%d-%H:%M:%S")
        return fecha
    #-----------------------------ENVIO DE DATOS APP WEB-----------------------
    def envio_APP_WEB(self,archivo):
        datos = []
        mensaje_n = ""
        with open(archivo, 'r') as reader:
            for line in reader.readlines():
                try:
                    dato = line.split(",")
                    #print(dato)
                    datos= urlencode({'ID':self.id_nodo,'latitud':dato[6],'longitud':dato[7],'c_pa':dato[0],'c_pla':dato[1],'c_org':dato[2],'c_vi':dato[3],'c_met':dato[4],'c_otro':dato[5],'c_acum':"",'lleno':dato[9],'fecha':dato[8]})
                    #print(datos)
                    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
                    r = http.request('GET',"https://botesinteractivoscali.000webhostapp.com/capturar_datos_hw.php?"+datos,retries=False)
                    print(r.data)
                    #datos = r.data
                except:
                    mensaje_n+=line;
            reader.close()
        print(mensaje_n)
        f = open(archivo,'w+')
        f.write(mensaje_n)
        f.close()
    def Separar(self,dato):
        dato = dato.split(",")
        return(dato[0],dato[1])
        
    def concatenar_dato(self, archivo):
        lleno = []
        dato_pa,a = self.Separar(self.leer_valores("/home/pi/CodRaspV1/MEDIDA_CONTENEDORES/CPC.txt"))
        lleno.append(a)
        dato_pl,a= self.Separar(self.leer_valores("/home/pi/CodRaspV1/MEDIDA_CONTENEDORES/CP.txt"))
        lleno.append(a)
        dato_or,a = self.Separar(self.leer_valores("/home/pi/CodRaspV1/MEDIDA_CONTENEDORES/COR.txt"))
        lleno.append(a)
        dato_vi,a = self.Separar(self.leer_valores("/home/pi/CodRaspV1/MEDIDA_CONTENEDORES/CV.txt"))
        lleno.append(a)
        dato_me,a = self.Separar(self.leer_valores("/home/pi/CodRaspV1/MEDIDA_CONTENEDORES/CM.txt"))
        lleno.append(a)
        dato_ot,a = self.Separar(self.leer_valores("/home/pi/CodRaspV1/MEDIDA_CONTENEDORES/CO.txt"))
        lleno.append(a)
        fecha = self.obtener_fecha()
        cont_lleno = "-"
        for i in range(len(lleno)):
            if lleno[i] == "*":
                cont_lleno = "*"
                break
        latitud,longitud = self.Separar(self.leer_valores("/home/pi/CodRaspV1/UBICACION/UBICACION.txt"))
        longitud = longitud.replace("\n","")
        mensaje = dato_pa+","+dato_pl+","+dato_or+","+dato_vi+","+dato_me+","+dato_ot+","+latitud+","+longitud+","+fecha+","+cont_lleno+",\n"
        mensaje_n=""
        with open(archivo, 'r') as reader:
            for line in reader.readlines():
                mensaje_n+=line
            reader.close()
        mensaje_n+=mensaje
        f = open(archivo,'w+')
        f.write(mensaje_n)
        f.close()
    #-------------------------VERIFICACIÒN CONEXIÒN INTERNET-------------------
    def sondeo(self):
        try:
            urllib.request.urlopen('http://google.com')
            return True
        except:
            return False

AppWeb = comunicacion()
envio = 0
print("EJECUTANDO ENVIO DATOS APPWEB")
while True:
    try:
        time.sleep(60*AppWeb.tiempo_muestra)
        AppWeb.concatenar_dato("/home/pi/CodRaspV1/HISTORIAL/HISTORIAL.txt")
        if(AppWeb.sondeo() is True):
            print("DATO ENVIADO")
            AppWeb.envio_APP_WEB("/home/pi/CodRaspV1/HISTORIAL/HISTORIAL.txt")
    except:
        pass

#-------------------------FIN DEL PROGRAMA-------------------------------------
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
