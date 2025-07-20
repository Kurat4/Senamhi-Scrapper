
#Script de Web Scraping del Clima del Dia 

###*Precisar que se uso la informacion del Senamhi*

Este pequeño script usa playwright ya que el metodo convencional de Requests para hacer peticiones http
no contempla paginas con contenido generado dinamicamente con JS, es decir todo el HTML a usar debe de estar
precargado en la pagina inicial y se usa BeatifulSoup para manejar el HTML que se obtiene y presentar 
solamente la informacion necesaria

<img width="386" height="63" alt="image" src="https://github.com/user-attachments/assets/fd5c8697-05f0-4321-ab71-35ec1a7e8773" />

Inicialmente se espera que la pagina se cargue, para luego esperar por el iframe que esta precargado en el
html inicial de la pagina, ahora dentro de este iframe hay otro doc html, que es basicamente otra pagina,
es por eso que no se puede scrapear (obtener el contenido html) solo seleccionandolo, es necesaria usar
content_frame() para ver el contenido html del iframe. 

<img width="472" height="88" alt="image" src="https://github.com/user-attachments/assets/f180b986-bd2a-414d-915b-beb7c70cb499" />

Esta parte del codigo, basicamente es un bucle para que selecciona los iconos de las distintas zonas dentro del mapa
basicamente son pop-ups que al darles click generan la tabla dinamicamente ( esto gracias a JS) por temas del
navegador fue necesario ir centrando el mapa porque al abrir un icono pasaba que en algunos casos el boton
para poder cerrar esa ventana emergente salia de la vista del navegador haciendo que a mitad del bucle
el selector del pop-up para una zona no se pueda cerrar haciendo que la siguiente zona no se pueda recopilar. 

Este pequeño script usa playwright ya que el metodo convencional de Requests para hacer peticiones http
no contempla paginas con contenido generado dinamicamente con JS, es decir todo el HTML a usar debe de estar
precargado en la pagina inicial y se usa BeatifulSoup para manejar el HTML que se obtiene y presentar 
solamente la informacion necesaria. 

<img width="862" height="511" alt="image" src="https://github.com/user-attachments/assets/586e9950-f244-4eef-b014-8f94f8d22031" />

En esta parte final simplemente se guarda la informacion en un csv, lista para ser usada o presentada. 

<img width="676" height="173" alt="image" src="https://github.com/user-attachments/assets/cdfd1303-ed40-4e52-b138-e42923d32f5d" />

