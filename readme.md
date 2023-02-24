# YoutubeChannelManager
[Gerardo Késsler](http://gera.ar)  

Este complemento permite gestionar los canales favoritos de la plataforma Youtube con atajos de teclado y con una interfaz invisible y sencilla.  

## Atajos del complemento

* Activar la interfaz invisible; sin asignar

## Atajos disponibles en la interfaz invisible

* escape; Cierra la interfaz virtual y devuelve los atajos de teclado a su función por defecto.
* Flecha derecha; Se mueve al canal siguiente.
* Flecha izquierda; Se mueve al canal anterior.
* Flecha abajo; Se mueve al siguiente video del canal con el foco.
* Flecha arriba; Se mueve al anterior video del canal con el foco.
* inicio; Se mueve al primer video del canal con el foco.
* fin; Verbaliza la posición, el nombre del canal, y el número de visualizaciones del video.
* n; Abre el diálogo para añadir un nuevo canal.
* o; Abre el link del video en el navegador por defecto.
* r; Abre el link de audio en un reproductor web personalizado.
* control + c; Abre el link del portapapeles en el reproductor web personalizado
* c; Copia el link del video al portapapeles.
* t; Copia el título del video al portapapeles.
* d; Obtiene los datos del video y los muestra en una ventana de NVDA.
* control + d; descarga el video en el formato original en la carpeta YoutubeDL del usuario actual
* control + shift + d; Descarga desde el portapapeles en el formato original en la carpeta YoutubeDL del usuario actual
* b; Activa el diálogo de búsqueda en la base de datos.
* Control + b; Activa el diálogo de búsqueda general.
* f5; Busca si existen videos nuevos en el canal con el foco.
* s; Activa la ventana de configuración del canal con el foco.
* g; Activa la ventana de opciones globales.
* Suprimir; Elimina el canal con el foco, y en la ventana de resultados elimina la columna y vuelve a la lista de canales.
* control + shift + suprimir; Elimina la base de datos.
* f1; Activa la ayuda de comandos.

## Añadir canales

Para añadir un nuevo canal a la base de datos, tan solo hay que abrir la interfaz virtual con el atajo para dicha acción, por defecto; NVDA + i griega. Y pulsar la letra n.    
La ventana solicita 2 campos. Un nombre de canal, y la dirección  URL del mismo. En este último caso, el complemento permite el ingreso de los siguientes formatos URL:

* Link de un video, que suele tener el siguiente formato:

    https://www.youtube.com/watch?v=IdDelVideo

* Link de un canal

    https://www.youtube.com/channel/IdDelCanal

Por lo que una forma de conseguirlo es abriendo algún video en la página de Youtube a través del navegador, pulsar alt y la letra d para abrir la barra de direcciones, y copiar la URL con control + c, la cual ya va a estar seleccionada por defecto.  
También pueden añadirse canales desde la lista de resultados globales. Para ello tan solo basta con realizar la búsqueda, situarse sobre el video del canal a añadir y pulsar la tecla n.  
Esto va a activar el diálogo para ingresar los datos del canal, los cuales van a ser completados automáticamente con el link  y el nombre tomados desde Youtube.

## Actualizador automático:

El complemento permite marcar canales como favoritos, y activar la verificación de novedades con un rango estipulado de tiempo.  
Para marcar o desmarcar un canal como favorito:  

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Seleccionar el canal deseado con flechas izquierda o derecha.
* Activar la ventana de configuración de canal con la letra s.
* Marcar la casilla correspondiente y pulsar sobre el botón para guardar la configuración.

La verificación de novedades en los canales favoritos está desactivada por defecto. Para modificarlo hay que seguir los siguientes pasos:

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Activar la ventana de configuración global con la letra g.
* Tabular hasta  la lista de opciones, y seleccionar con flechas arriba y abajo el rango deseado.
* Pulsar sobre el botón para guardar las configuraciones.

Al encontrar novedades, el complemento emitirá un sonido durante la actualización y un mensaje al finalizar la misma.

## Búsqueda de videos en la base de datos:

El complemento permite buscar por palabras clave entre los videos de los canales agregados a la base de datos.  

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Activar la ventana de búsqueda con la letra b.
* Escribir una palabra o frase de referencia.
* Pulsar Intro o el botón Iniciar la búsqueda.

Si no se encuentran resultados, se avisa a través de un mensaje y no se  modifica la interfaz virtual.  
En el caso de encontrar videos que se correspondan con los datos ingresados, se avisa a través de un mensaje y se activa la interfaz de resultados.  
Para navegar en ella, lo pueden hacer con flechas arriba y abajo. Están disponibles los mismos comandos que en la interfaz de canales; r para el reproductor web personalizado, o para abrir en el navegador, etcétera.  
Para volver a la interfaz de canales hay que pulsar la tecla suprimir en la interfaz de resultados, lo que eliminará esa columna y devolverá la lista de canales y videos.

## Búsqueda global:

Para realizar una búsqueda global fuera de la base de datos hay que hacer lo siguiente:

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Activar la ventana de búsqueda con el atajo control + b.
* Escribir una palabra o frase de referencia y seleccionar la cantidad de resultados a mostrar.
* Pulsar el botón Iniciar la búsqueda.

Si no se encuentran resultados, se avisa a través de un mensaje.  
Cuando se encuentran resultados, estos se agregan a la lista principal, la cual podemos recorrer con flechas arriba y abajo.  
Aquí también tenemos los mismos atajos que en la búsqueda por base de datos. O para abrir en el navegador, r para el reproductor web, c para copiar el link, etcétera.  
Si alguno de los videos está en un canal que quiera agregarse a la base de datos, al pulsar la letra n sobre esta lista va a activarse el diálogo de nuevo canal con los campos de nombre y URL ya completos. Estos campos pueden editarse si así lo prefieren.  
Al igual que en las búsquedas en la base de datos, para volver a la lista de canales tan solo hay que pulsar suprimir para eliminar los resultados y volver a la interfaz de canales.

## Historial de búsquedas

El complemento guarda en la base de datos el texto de las últimas 20 búsquedas globales. 
Para acceder al historial, tan solo hay que pulsar la tecla aplicaciones sobre el cuadro de edición de búsqueda global. Al pulsarla se activa un menú contextual con las últimas búsquedas, y al pulsar intro sobre alguna de ellas el cuadro se completa con el texto correspondiente.

## Descarga de videos

Este complemento no tiene como finalidad la converción de videos, sin embargo se ha añadido la posibilidad de descargar el video en el formato original.  
Para ello solo hay que buscar en la interfaz invisible el video a descargar, y pulsar el atajo control + d. El archivo va a descargarse en la carpeta youtubeDL del usuario actual.

## Traductores:

	Rémy Ruiz (Francés)
	Ângelo Miguel Abrantes (portugués)
	Umut KORKMAZ (Turco)
	wafiqtaher (árabe)

