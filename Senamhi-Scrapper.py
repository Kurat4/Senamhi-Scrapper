from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd 

#Diccionario para guardar la informacion recopilada 
resultados={"Zona1":{"Nombre":"","Horas":[],"Temperaturas":[],"Humedades":[]},
             "Zona2":{"Nombre":"","Horas":[],"Temperaturas":[],"Humedades":[]},
             "Zona3":{"Nombre":"","Horas":[],"Temperaturas":[],"Humedades":[]},
             "Zona4":{"Nombre":"","Horas":[],"Temperaturas":[],"Humedades":[]},
             "Zona5":{"Nombre":"","Horas":[],"Temperaturas":[],"Humedades":[]}
             }
#Iniciando el navegador
playwright=sync_playwright().start()
browser=playwright.chromium.launch(headless=False)
#Yendo a la pagina 
page=browser.new_page()
url="https://www.senamhi.gob.pe/?p=pronostico-lima"
page.goto(url)
"""
Inicialmente se espera que la pagina se cargue, para luego esperar por el iframe que esta precargado en el
html inicial de la pagina, ahora dentro de este iframe hay otro doc html, que es basicamente otra pagina,
es por eso que no se puede scrapear (obtener el contenido html) solo seleccionandolo, es necesaria usar
content_frame() para ver el contenido html del iframe. 

"""
page.wait_for_load_state("load")
page.wait_for_selector("iframe#ifrMap")
mapa_sin_contenido = page.query_selector("iframe#ifrMap")
mapa_real=mapa_sin_contenido.content_frame()

"""
Esta parte del codigo, basicamente es un bucle para que selecciona los iconos de las distintas zonas dentro del mapa
basicamente son pop-ups que al darles click generan la tabla dinamicamente ( esto gracias a JS) por temas del
navegador fue necesario ir centrando el mapa porque al abrir un icono pasaba que en algunos casos el boton
para poder cerrar esa ventana emergente salia de la vista del navegador haciendo que a mitad del bucle
el selector del pop-up para una zona no se pueda cerrar haciendo que la siguiente zona no se pueda recopilar. 

Este pequeño script usa playwright ya que el metodo convencional de Requests para hacer peticiones http
no contempla paginas con contenido generado dinamicamente con JS, es decir todo el HTML a usar debe de estar
precargado en la pagina inicial y se usa BeatifulSoup para manejar el HTML que se obtiene y presentar 
solamente la informacion necesaria. 

"""
for i in range(1,6):
        centrar=mapa_real.query_selector("#mapid > div.leaflet-control-container > div.leaflet-top.leaflet-left > div.leaflet-control-zoomhome.leaflet-bar.leaflet-control > a.leaflet-control-zoomhome-home")
        centrar.click()
        zona=mapa_real.query_selector(f"#mapid > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-marker-pane > div:nth-child({i})")
        zona.click()
        page.wait_for_timeout(1000)
        informacion=mapa_real.query_selector("#mapid > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-popup-pane > div")
        soup=BeautifulSoup(informacion.inner_html(),"html.parser")
        nombre_zona=soup.find("span",class_="labelTable font-weight-bold text-secondary")
        
        resultados[f"Zona{i}"]["Nombre"]=nombre_zona.text

        horas=soup.find_all("th",class_="text-center align-middle text-muted")
        resultados[f"Zona{i}"]["Horas"]= [th.get_text(strip=True) for th in horas]

        temperaturas=soup.find_all("td",class_="text-center align-middle text-primary")
  
        resultados[f"Zona{i}"]["Temperaturas"]= [td.get_text(strip=True) for td in temperaturas]

        humedades=soup.find_all("td",class_="text-center align-middle text-secondary")      
        
        resultados[f"Zona{i}"]["Humedades"]= [td.get_text(strip=True) for td in humedades]

        page.wait_for_timeout(1000)
        cerrar_zona=mapa_real.query_selector("#mapid > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-popup-pane > div > a")
        cerrar_zona.click()



"""
En esta parte final simplemente se guarda la informacion en un csv, lista para ser usada o presentada. 

"""

data=[]

for zona in resultados.values():
        for hor,tem,hum in zip(zona["Horas"],zona["Temperaturas"],zona["Humedades"]):
                data.append([zona["Nombre"],hor,tem,hum])

df=pd.DataFrame(data,columns=["Zona","Hora","Temperatura","Humedad"])
df.to_csv("zonas.csv",index=False)





            
        