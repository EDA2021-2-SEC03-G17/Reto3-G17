"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """



import config as cf
assert cf
import sys
import controller
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt

ufo="""                 _                
                /\              
                \ \  \__/ \__/  / 
                 \ \ (oo) (oo) /    
                  \_\/~~\_/~~\_
                 _.-~===========~-._
                (___/_______________)
                   /  \_______/"""

#MENU
def printMenu():
    print("")
    print(ufo)
    print("")
    print("           BIENVENIDO AL CATALOGO DE UFO's")
    print("_______________________________________________________")
    print("")
    print("1 ) Cargar información en de UFOS")
    print("2 ) Contar los avistamientos en una ciudad")
    print("3 ) Contar los avistamientos por duración")
    print("5 ) Contar los avistamientos en un rango de fechas")
    print("0 ) Salir")
    print("________________________________________________________")

#CARGA DE DATOS [1]
def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

#REQ1 [2]
def req1(catalog):
    city=input("Ingrese el nombre de la ciudad a consultar.")
    return controller.ufoporciudad(catalog,city)

#REQ2 [3] PRUEBA (30.0/150.0)
def avistamientos_duracion(catalog):
    fecha_inicio=float(input("Ingrese la duracion limite minima: "))
    fecha_fin=(float(input("Ingrese duracion limite maxima: ")))
    duracion_en_rango=controller.sightingsdurationrange(catalog,fecha_inicio,fecha_fin)
    return duracion_en_rango

#REQ4 [5] PRUEBA (1945-08-06/1984-11-15)
def avistamientos_fechas(catalog):
    fecha_inicio= int(input("Ingrese límite inferior en formato AAAA-MM-DD: ").replace("-",''))
    fecha_fin= int(input("Ingrese límite superior en formato AAAA-MM-DD: ").replace("-",''))
    fechas_en_rango=controller.sightingsperdate(catalog,fecha_inicio,fecha_fin)
    return fechas_en_rango

#CONSULTA

def listSize(listaufo):
    return controller.listsize(listaufo)

catalog = None


while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initCatalog()
        print("Cargando información de los archivos ....")
        loadData(catalog)

    elif int(inputs[0]) == 2:                                                
        listaufo=req1(catalog)
        len=listSize(listaufo)
        print("TOTAL UFOS VISTOS: "+ str(len))

    elif int(inputs[0]) == 3:
        mayor=controller.max_duration(catalog)
        muestra1,tamanio=avistamientos_duracion(catalog)
        print("The longest UFO sightings is: " + str(mayor))
        print("There are {} sightings".format(tamanio))
        print("The first 3 and last 3 UFO sightings in the duration time are: ")
        print(muestra1)

    elif int(inputs[0]) == 5:
        mayor=controller.min_date(catalog)
        muestra1,tamanio=avistamientos_fechas(catalog)
        print("The longest UFO sightings is: " + str(mayor))
        print("There are {} sightings".format(tamanio))
        print("The first 3 and last 3 UFO sightings in the duration time are: ")
        print(muestra1)
        
                        
    else:
        sys.exit(0)
sys.exit(0)
