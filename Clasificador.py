from skimage.io import imread
from skimage.io import imsave
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt

# Función que mide el ancho de la hoja a una altura dada
def anchura(img,ancho,altura):
    i = 0
    anchura = 0
    while True:
        pixel = img[altura,i]
        if pixel == 0:
            anchura = anchura +1
        i = i+1
        if i == ancho:
            break
    return anchura

# Función que mide la longitud de la hoja
def longitud(img,alto,ancho):
    i = 0
    j = 0
    count = 0
    while True:
        pixel = img[j,i]
        if pixel == 0 and i != 0:
            ppixel = img[j,i-1]
            if ppixel == 0:
                count = count +1
        if count == 3:
            superior = j
            break
        i = i+1
        if i == ancho:
            count = 0
            i = 0
            j = j+1

    i = 0
    j = alto-1
    count = 0
    while True:
        pixel = img[j,i]
        if pixel == 0 and i != 0:
            ppixel = img[j,i-1]
            if ppixel == 0:
                count = count +1
        if count == 3:
            intefior = j
            break
        i = i+1
        if i == ancho:
            count = 0
            i = 0
            j = j-1
            
    longitud = intefior-superior
    
    return longitud

# Numeración del tipo de hoja
# A = 5
# B = 7
# C = 11
# D = 4
# E = 13
tipos = {"A": "5", "B": "7", "C": "11", "D": "4", "E": "13"}
tipo = "A"

# Función de clasificación
def clasifica(tipo):
    #Declación de variable internas
    fail = 0
    tallo = 0
    j = 10
    # Loop buscas las imagen para la clasificación
    while True:
        # Carga y preprocesado
        numero = str(j)
        img = imread('Archivos/hojasvegetales/leaf' + tipo + '/l' + tipos[tipo] + 'nr0' + numero + '.tif')
        gray = rgb2gray(img)
        binary = gray > 0.85
        alto,ancho = binary.shape
        grupo = "-"
        # Primer parametro para divisicón de subgrupos
        pripunto = int(alto*3/4)
        grosor = anchura(binary,ancho,pripunto)
    
        if grosor <= 30:
            # Medición del peciolo
            decima = int(alto/10)
            segpunto = pripunto+decima
            terpunto = pripunto-decima
            while True:
                if segpunto >= alto:
                    break
                grosor2 = anchura(binary,ancho,segpunto)
                if grosor2 == 0:
                    break
                segpunto = segpunto+decima
   
            while True:
                if terpunto <= alto/2:
                    break
                grosor3 = anchura(binary,ancho,terpunto)
                if grosor2 > 50:
                    break
                terpunto = terpunto-decima           

            tallo = segpunto-terpunto

            if tallo >= 650:
                grupo = "E"
            elif tallo < 650:
                grupo = "A"
        # Clasificación subgrupo 2
        elif grosor > 30:
            # Calculo de parametro
            segpunto = int(alto/2)
            terpunto = int(alto/4)
            grosor2 = anchura(binary,ancho,segpunto)
            grosor3 = anchura(binary,ancho,terpunto)
            largo = longitud(binary,alto,ancho)
            razon = grosor2/largo*100
            razon2 = grosor3/largo*100
            # Clasicación tipo D, con comportamiento creciente
            if razon2 > razon:
                grupo = "D"
            # Clasificación tipo C por relación ancho-largo,, y comportamiento decreciente
            elif razon > 30 and razon > razon2:
                grupo = "C"
                total = np.sum(binary==False)
                por = total/(alto*ancho)*100
                # Excepciones para corregir elementos confusos tipo D
                if por < 36:
                    grupo = "D"
                cuapunto = int(alto*7/16)
                grosor4 = anchura(binary,ancho,cuapunto)
                dif = abs(grosor2-grosor4)
                if dif >= 65:
                    grupo = "D"
            # Claficación hojas tipo B por relación ancho-largo
            elif razon < 18 and razon > razon2:
                grupo = "B"
            else:
                grupo = "D"
                
        
        if grupo != tipo:
            
            print(j, grupo)
            fail = fail+1
            
        if numero == "19": #En el original, era '75'
            break
        j = j+1
    
    return fail

fallos = clasifica(tipo)
print("Fallos:", fallos)

    


