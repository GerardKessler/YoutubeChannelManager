# YoutubeChannelsManager
[Gerardo Késsler](http://gera.ar)  

Este complemento permite gestionar los canales favoritos de la plataforma Youtube en una interfaz amigable.  

## Atajos del complemento

* NVDA + y; Activa y desactiva la interfaz invisible

## Atajos disponibles en la interfaz invisible

* escape; cierra la interfaz virtual y devuelve los atajos de teclado a su función por defecto.
* Flecha derecha; se mueve al canal siguiente.
* Flecha izquierda; se mueve al canal anterior.
* Flecha abajo; se mueve al siguiente video del canal con el foco.
* Flecha arriba; se mueve al anterior video del canal con el foco.
* inicio; Se mueve al primer video del canal con el foco.
* fin; verbaliza la posición, el nombre del canal, y el número de visualizaciones del video.
* n; abre el diálogo para añadir un nuevo canal.
* s; Activa la ventana de configuración del canal con el foco.
* g; Activa la ventana de opciones globales.
* Suprimir; elimina el canal con el foco, y en la ventana de resultados elimina la columna y vuelve a la vista de canales.
* control + shift + suprimir; Elimina la base de datos.
* o; abre el link del video en el navegador por defecto.
*r; Abre el link de audio en un reproductor web personalizado.
* c; copia el link del video al portapapeles.
* d; obtiene los datos del video y los muestra en una ventana de NVDA
* f5; Busca si existen videos nuevos en el canal con el foco.
* f1; activa la ayuda de comandos.

### Añadir canales

Para añadir un nuevo canal a la base de datos, tan solo hay que abrir la interfaz virtual con el atajo para dicha acción, por defecto; NVDA + i griega.  
La ventana solicita 2 campos. Un nombre de canal, y la dirección  URL del mismo. En este último caso, el complemento permite el ingreso de los siguientes formatos URL:

* link de un video, que suele tener el siguiente formato:

    https://www.youtube.com/watch?v=IdDelVideo

* Link de un canal

    https://www.youtube.com/channel/IdDelCanal

Por lo que una forma de conseguirlo es abriendo algún video en la página de Youtube a través del navegador, pulsar alt y la letra d para abrir la barra de direcciones, y copiar la URL con control + c, la cual ya va a estar seleccionada por defecto.  

### Actualizador automático:

El complemento permite marcar canales como favoritos, y activar la verificación de novedades con un rango estipulado de tiempo.  
Para marcar o desmarcar un canal como favorito:  

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Seleccionar el canal deseado con flechas izquierda o derecha.
* Activar la ventana de configuración de canal con la letra s.
* Marcar la casilla correspondiente y pulsar sobre el botón para guardar la configuración.

La verificación de novedades en los canales favoritos está desactivada por defecto. Para modificarlo hay que seguir los siguientes pasos:

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Activar la ventana de configuración global con la letra g.
* tabular hasta  la lista de opciones, y seleccionar con flechas arriba y abajo el rango deseado.
* Pulsar sobre el botón para guardar las configuraciones.

Al encontrar novedades, el complemento emitirá un sonido durante la actualización y un mensaje al finalizar la misma.

### Búsqueda de videos:

El complemento permite buscar por palabras clave entre el nombre de todos los videos en los canales agregados.  

* Activar la interfaz virtual con el gesto asignado, por defecto, NVDA + i griega.
* Activar la ventana de búsqueda con la letra b.
* Escribir una palabra o algo de referencia.
* pulsar intro o el botón iniciar la búsqueda.

Si no se encuentran resultados, se avisa a través de un mensaje y no se  modifica la interfaz virtual.  
En el caso de encontrar videos que se correspondan con los datos ingresados, se avisa a través de un mensaje y se activa la interfaz de resultados.  
Para navegar en ella, lo pueden hacer con flechas arriba y abajo. Están disponibles los mismos comandos que en la interfaz de canales; r para el reproductor web personalizado, o para abrir en el navegador, etcétera.  
Para volver a la interfaz de canales hay que pulsar la tecla suprimir en la interfaz de resultados, lo que eliminará esa columna y devolverá la lista de canales y videos.


