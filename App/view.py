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

#MENU
def printMenu():
    print("___________________________________________")
    print("    BIENVENIDO AL CATALOGO DE UFO's")
    print("___________________________________________")
    print("")
    print("1 ) Cargar información en el catálogo")
    print("2 ) Contar los avistamientos en una ciudad")
    print("0 ) Salir")
    print("___________________________________________")

#CARGA DE DATOS [1]
def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

#REQ1 [2]
def req1(catalog):
    city=input("Ingrese el nombre de la ciudad a consultar.")
    return controller.ufoporciudad(catalog,city)

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
        print(catalog)

    if int(inputs[0]) == 2:
        listaufo=req1(catalog)
        len=listSize(listaufo)
        print("TOTAL UFOS VISTOS: "+ str(len))

    else:
        sys.exit(0)
sys.exit(0)
