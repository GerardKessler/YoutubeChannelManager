import subprocess
import core
import gui
from re import search
import api
import webbrowser
import globalPluginHandler
import addonHandler
import globalVars
import ui
from scriptHandler import script
import urllib.request
import json
import zipfile
import winsound
from threading import Thread
import socket
import time
import shutil
import wx
import sys
import os
# Pillamos ruta de nuestro addon.
dirAddon=os.path.dirname(__file__)
# Agregamos a la variante path nuestro directorio del addon.
sys.path.append(dirAddon)
# Añadimos el directorio lib a la variable path.
sys.path.append(os.path.join(dirAddon, "lib"))
# importamos libreria y agregamos al path para que pueda ser usada desde cualquier sitio.
import xml
xml.__path__.append(os.path.join(dirAddon, "lib", "xml"))
import html
html.__path__.append(os.path.join(dirAddon, "lib", "html"))
import youtube_dl
# borramos del path ya que no lo necesitamos.
del sys.path[-2:]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if globalVars.appArgs.secure: return
		self.options = {'ignoreerrors': True, 'quiet': True, 'extract_flat': 'in_playlist', 'dump_single_json': True}
		self.switch = False
		self.channels = []
		self.index = []
		self.y = 0
		self.z = 1
		core.postNvdaStartup.register(self.firstRun)

	def firstRun(self):
		self.checkUpdate()
		self.start()

	def start(self, speak= False):
		self.channels = []
		self.index = []
		channelsPath = f"{dirAddon}\\channels"
		files = os.listdir(channelsPath)
		for file in files:
			with open(f"{channelsPath}\\{file}", "r") as archivo:
				lista = json.load(archivo)
			self.channels.append(lista)
			self.index.append(1)
		if speak:
			ui.message(speak)

	def getVideos(channelName, channelID, fileName):
		list = [{"name": channelName, "link": channelID, "file": fileName}]
		with youtube_dl.YoutubeDL(self.options) as ydl:
			p = ydl.extract_info(channelID, download=False)
		titles = [p["entries"][i]["title"] for i in range(len(p["entries"]))]
		links = [f"https://www.youtube.com/watch?v={p['entries'][i]['url']}" for i in range(len(p["entries"]))]
		for i in range(len(titles)):
			list.append({'title': titles[i], 'link': links[i]})
		return list

	def script_newChannel(self, gesture):
		self.desactivar(False)
		self.dlg = NewChannel(gui.mainFrame, "Añadir canal", self)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_removeChannel(self, gesture):
		Thread(target=self.startRemoveChannel, daemon= True).start()
		self.desactivar(False)

	def startRemoveChannel(self):
		modal = wx.MessageDialog(None, f'¿Quieres eliminar el canal {self.channels[self.y][0]["name"]}?', _("Pregunta"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if modal.ShowModal() == wx.ID_YES:
			os.remove(os.path.join(dirAddon, "channels", self.channels[self.y][0]["file"]))
			winsound.PlaySound("C:\\Windows\\Media\\Windows Recycle.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.channels.pop(self.y)
			self.index.pop(self.y)
			self.y = 0
		else:
			modal.Destroy()

	# Función que verifica si ya cargaron los canales y activa o desactiva los atajos a través de un operador ternario
	@script(gesture="kb:NVDA+y", description="Activa y desactiva la interfaz invisible", category= "YoutubeChannelManager")
	def script_toggle(self, gesture):
		if self.channels == None:
			ui.message("Cargando los canales, por favor espere...")
			return
		self.desactivar() if self.switch else self.activar()

	# función que crea todos los gestos de la ventana invisible
	def activar(self):
			self.switch = True
			ui.message("Atajos activados")
			self.bindGestures(
				{"kb:downArrow":"nextItem",
				"kb:upArrow":"previousItem",
				"kb:rightArrow":"nextSection",
				"kb:leftArrow":"previousSection",
				"kb:o":"open",
				"kb:home":"firstItem",
				"kb:end":"positionAnnounce",
				"kb:n":"newChannel",
				"kb:c":"copyLink",
				"kb:d":"viewData",
				"kb:v":"playVLC",
				"kb:delete":"removeChannel",
				"kb:f5":"reloadChannels",
				"kb:control+f5":"reloadAllChannels",
				"kb:escape":"toggle"}
			)

	# función que elimina los gestos
	def desactivar(self, speak=True):
			self.switch = False
			if speak: ui.message("Atajos desactivados")
			self.clearGestureBindings()
			self.bindGestures(self.__gestures)

	# función que avanza entre los valores de los diccionarios de la lista a través de la variable y
	def script_nextItem(self, gesture):
		try:
			self.z += 1
			if self.z < len(self.channels[self.y]):
				ui.message(self.channels[self.y][self.z]["title"])
			else:
				self.z = 1
				ui.message(self.channels[self.y][self.z]["title"])
		except IndexError:
			pass

	# lo mismo que la anterior, pero alrevés
	def script_previousItem(self, gesture):
		try:
			self.z -= 1
			if self.z > 0:
				ui.message(self.channels[self.y][self.z]["title"])
			else:
				self.z = len(self.channels[self.y]) - 1
				ui.message(self.channels[self.y][self.z]["title"])
		except IndexError:
			pass

	# Esta función recorre la lista canales, y va guardando y recuperando los valores de la lista index para conservar la posición al cambiar de lista
	def script_nextSection(self, gesture):
		try:
			self.index[self.y] = self.z
			self.z = -1
			self.y += 1
			if self.y < len(self.index):
				ui.message(self.channels[self.y][0]["name"])
				self.z = self.index[self.y]
			else:
				self.y = 0
				ui.message(self.channels[self.y][0]["name"])
				self.z = self.index[self.y]
		except IndexError:
			pass

	# Igual que la anterior pero alverre
	def script_previousSection(self, gesture):
		try:
			self.index[self.y] = self.z
			self.z = -1
			self.y -= 1
			if self.y >= 0:
				ui.message(self.channels[self.y][0]["name"])
				self.z = self.index[self.y]
			else:
				self.y = len(self.index) - 1
				ui.message(self.channels[self.y][0]["name"])
				self.z = self.index[self.y]
		except IndexError:
			pass

	# función que abre el valor del link en el elemento seleccionado en las listas y desactiva los atajos
	def script_open(self, gesture):
		webbrowser.open(self.channels[self.y][self.z]["link"], new=0, autoraise=True)
		self.desactivar(False)

	def script_firstItem(self, gesture):
		self.z = 1
		ui.message(self.channels[self.y][self.z]["title"])

	def script_positionAnnounce(self, gesture):
		ui.message(f'{self.z} de {len(self.channels[self.y]) - 1}, {self.channels[self.y][0]["name"]}')

	def script_reloadChannels(self, gesture):
		Thread(target=self.startReload, daemon= True).start()
		ui.message(f'Recargando los videos de {self.channels[self.y][0]["name"]}...')

	def startReload(self):
		content = self.getVideos(self.channels[self.y][0]["name"], self.channels[self.y][0]["link"], self.channels[self.y][0]["file"])
		self.channels[self.y] = content
		with open(f'{dirAddon}\\channels\\{self.channels[self.y][0]["file"]}', 'w') as archivo:
			json.dump(content, archivo, indent=2)
		ui.message("proceso finalizado")

	def script_reloadAllChannels(self, gesture):
		Thread(target=self.startReloadAll, daemon= True).start()

	def startReloadAll(self):
		modal = wx.MessageDialog(None, "¿Quieres refrescar todas las listas? Puede demorarse un poco...", "Atención", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if modal.ShowModal() == wx.ID_NO:
			modal.Destroy()
			return
		self.desactivar(False)
		ui.message("Recargando datos...")
		self.channels = []
		self.index = []
		channelsPath = f"{dirAddon}\\channels"
		files = os.listdir(channelsPath)
		for file in files:
			with open(f"{channelsPath}\\{file}", "r") as archivo:
				lista = json.load(archivo)
				content = self.getVideos(lista[0]["name"], lista[0]["link"], lista[0]["file"])
				self.channels.append(content)
				self.index.append(1)
		ui.message("Proceso finalizado")

	def getVideos(self, channelName, channelID, fileName):
		list = [{"name": channelName, "link": channelID, "file": fileName}]
		with youtube_dl.YoutubeDL(self.options) as ydl:
			p = ydl.extract_info(channelID, download=False)
		titles = [p["entries"][i]["title"] for i in range(len(p["entries"]))]
		links = [f"https://www.youtube.com/watch?v={p['entries'][i]['url']}" for i in range(len(p["entries"]))]
		for i in range(len(titles)):
			list.append({'title': titles[i], 'link': links[i]})
		return list

	def script_copyLink(self, gesture):
		self.desactivar(False)
		api.copyToClip(self.channels[self.y][self.z]["link"])
		winsound.PlaySound("C:\\Windows\\Media\\Windows Recycle.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

	def script_playVLC(self, gesture):
		if os.path.isfile("C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"):
			self.desactivar(False)
			Thread(target=self.startPlayVLC, daemon= True).start()
		else:
			ui.message("No se encuentra el programa VLC")

	def startPlayVLC(self):
		ui.message("Reproduciendo en vlc...")
		subprocess.call(['C:\\Program Files\\VideoLAN\\VLC\\vlc.exe', self.channels[self.y][self.z]["link"]])

	def terminate(self):
		pass

	def script_viewData(self, gesture):
		self.desactivar(False)
		ui.message("Obteniendo los datos del video...")
		with youtube_dl.YoutubeDL(self.options) as ydl:
			p = ydl.extract_info(self.channels[self.y][self.z]["link"], download=False)
		upload_date = f'{p["upload_date"][6:][:2]}.{p["upload_date"][4:][:2]}.{p["upload_date"][:4]}'
		time = self.timeFormat(p["duration"])
		data = f'''Duración: {time}
Fecha de subida: {upload_date}
Reproducciones: {p["view_count"]}
Me gusta: {p["like_count"]}
Descripción: {p["description"]}'''
		ui.browseableMessage(data, p["title"])

	def timeFormat(self, seconds):
		hs = int(seconds/3600)
		ms = int(seconds/60)
		ss = seconds%60
		if ss < 10:
			ss = f"0{ss}"
		if ms < 10:
			ms = f"0{ms}"
		if hs > 0:
			ms = ms%60
			if ms < 10:
				ms = f"0{ms}"
			return f"{hs}:{ms}:{ss}"
		else:
			return f"{ms}:{ss}"

	def checkUpdate(self):
		self.mainThread = HiloComplemento()
		self.mainThread.start()

class HiloComplemento(Thread):
	def __init__(self):
		super(HiloComplemento, self).__init__()
		self.daemon = True

	def run(self):
		def chkActualizacion():
			# Url para obtener el json y obtener el archivo de descarga de la ultima versión desde el repo oficial de YouTube-Dl
			url = "https://api.github.com/repos/ytdl-org/youtube-dl/releases"
			req = urllib.request.Request(url)
			# Vamos a obtener el json y a leerlo.
			r = urllib.request.urlopen(req).read()
			gitJson = json.loads(r.decode('utf-8'))
			# Vamos a comprobar si la versión de Github es mayor que la que tenemos instalada si lo es descargamos
			if gitJson[0]["tag_name"] > youtube_dl.version.__version__:
				urlDescarga = gitJson[0]['zipball_url']
				xguiMsg = "Existe una nueva versión de la librería youtube_dl. ¿Quieres actualizarla?"
				msg = wx.MessageDialog(None, xguiMsg, "Atención", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				ret = msg.ShowModal()
				if ret == wx.ID_YES:
					msg.Destroy()
					dlg = DescargaDialogo(urlDescarga)
					result = dlg.ShowModal()
					if result == 1:
						dlg.Destroy()
						# Ahora leemos el archivo zip descargado que hemos llamado temp.zip
						archive = zipfile.ZipFile(os.path.join(dirAddon, "temp.zip"))
						# Obtenemos el nombre del directorio raiz del zip, necesario por que cada nueva versión tendra un nombre.
						root = archive.namelist()[0]
						# Esto siguiente buscara el directorio que nos interesa para extraer que es el Youtube_dl. No es necesario por que podemos construirlo con el root pero prefiero por si algun día cambiase.
						filtro = [item for item in archive.namelist() if "youtube_dl".lower() in item.lower()]
						# Ahora vamos a extraer solo el directorio de YouTube-Dl.
						for file in archive.namelist():
							if file.startswith(filtro[0]):
								archive.extract(file, dirAddon)
						archive.close()
						# Borramos el archivo descargado
						os.remove(os.path.join(dirAddon, "temp.zip"))
								# Ahora vamos a borrar el directorio de la libreria de youtube_dl del complemento
						shutil.rmtree(os.path.join(dirAddon, "lib", "youtube_dl"))
						# Ahora vamos a copiar el directorio extraido de youtube_dl a la raiz de nuestro proyecto.
						shutil.move(os.path.join(dirAddon, root, "youtube_dl"), os.path.join(dirAddon, "lib", "youtube_dl"))
						# Ahora vamos a borrar el directorio que extraimos.
						shutil.rmtree(os.path.join(dirAddon, root))
						core.restart()
					else:
						dlg.Destroy()
				else:
					msg.Destroy()
					return

		wx.CallAfter(chkActualizacion)


class DescargaDialogo(wx.Dialog):
	def __init__(self, url):

		WIDTH = 550
		HEIGHT = 400

		super(DescargaDialogo, self).__init__(None, -1, title=_("Actualizando la librería..."), size = (WIDTH, HEIGHT))

		self.CenterOnScreen()

		self.url = url

		self.Panel = wx.Panel(self)

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)

		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.aceptarBTN = wx.Button(self.Panel, 1, _("&Aceptar"))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.aceptarBTN.GetId())
		self.aceptarBTN.Disable()

		self.cerrarBTN = wx.Button(self.Panel, 2, _("&Cerrar"))
		self.Bind(wx.EVT_BUTTON, self.onCerrar, id=self.cerrarBTN.GetId())
		self.cerrarBTN.Disable()

		self.Bind(wx.EVT_CLOSE, self.onNull)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

		sizer.Add(self.progressBar, 0, wx.EXPAND)
		sizer.Add(self.textorefresco, 1, wx.EXPAND)

		sizer_botones.Add(self.aceptarBTN, 2, wx.CENTER)
		sizer_botones.Add(self.cerrarBTN, 2, wx.CENTER)

		sizer.Add(sizer_botones, 0, wx.EXPAND)

		self.Panel.SetSizer(sizer)

		self.textorefresco.SetFocus()
		HiloDescarga(self, self.url)

	def skip(self, event):
		return

	def onNull(self, event):
		return

	def next(self, event):
		self.progressBar.SetValue(event)

	def TextoRefresco(self, event):
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)

	def done(self, event):
		winsound.MessageBeep(0)
		self.aceptarBTN.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 
		self.aceptarBTN.SetFocus()
	def error(self, event):
		winsound.MessageBeep(16)
		self.cerrarBTN.Enable()
		self.textorefresco.Clear()
		self.textorefresco.AppendText(event)
		self.textorefresco.SetInsertionPoint(0) 
		self.cerrarBTN.SetFocus()

	def onAceptar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

	def onCerrar(self, event):
		if self.IsModal():
			self.EndModal(event.EventObject.Id)
		else:
			self.Close()

class HiloDescarga(Thread):
	def __init__(self, frame, url):
		super(HiloDescarga, self).__init__()

		self.frame = frame
		self.url = url

		self.daemon = True
		self.start()

	def humanbytes(self, B): # Convierte bytes
		B = float(B)
		KB = float(1024)
		MB = float(KB ** 2) # 1,048,576
		GB = float(KB ** 3) # 1,073,741,824
		TB = float(KB ** 4) # 1,099,511,627,776

		if B < KB:
			return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
		elif KB <= B < MB:
			return '{0:.2f} KB'.format(B/KB)
		elif MB <= B < GB:
			return '{0:.2f} MB'.format(B/MB)
		elif GB <= B < TB:
			return '{0:.2f} GB'.format(B/GB)
		elif TB <= B:
			return '{0:.2f} TB'.format(B/TB)


	def __call__(self, block_num, block_size, total_size):
		readsofar = block_num * block_size
		if total_size > 0:
			percent = readsofar * 1e2 / total_size
			wx.CallAfter(self.frame.next, percent)
			time.sleep(1 / 995)
			wx.CallAfter(self.frame.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(readsofar))
			if readsofar >= total_size: # Si queremos hacer algo cuando la descarga termina.
				pass
		else: # Si la descarga es solo el tamaño
			wx.CallAfter(self.frame.TextoRefresco, _("Espere por favor...\n") + _("Descargando: %s") % self.humanbytes(readsofar))

	def run(self):
		try:
			socket.setdefaulttimeout(30) # Dara error si pasan 30 seg sin internet
			try:
				req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
				obj = urllib.request.urlopen(req).geturl()
				urllib.request.urlretrieve(self.url, os.path.join(dirAddon, "temp.zip"), reporthook=self.__call__)
			except Exception as e:
				urllib.request.urlretrieve(self.url, os.path.join(dirAddon, "temp.zip"), reporthook=self.__call__)

			msg = \
_("""La descarga termino.

Cierre la ventana para terminar de instalar la librería y reiniciar NVDA.""")
			wx.CallAfter(self.frame.done, msg)
		except Exception as e:
			wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Compruebe que tiene conexión a internet y vuelva a intentarlo.\n") + _("Ya puede cerrar esta ventana."))

class NewChannel(wx.Dialog):
	def __init__(self, parent, titulo, frame):
		super(NewChannel, self).__init__(parent, -1, title=titulo)
		self.options = {'ignoreerrors': True, 'quiet': True, 'extract_flat': 'in_playlist', 'dump_single_json': True}
		self.frame = frame
		self.Panel = wx.Panel(self)
		wx.StaticText(self.Panel, wx.ID_ANY, "Ingresa el nombre del canal")
		self.channelName = wx.TextCtrl(self.Panel,wx.ID_ANY)
		wx.StaticText(self.Panel, wx.ID_ANY, "Ingresa la URL del canal")
		self.channelLink = wx.TextCtrl(self.Panel,wx.ID_ANY)
		self.addBTN = wx.Button(self.Panel, wx.ID_ANY, "&Añadir canal")
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, "&Cancelar")
		self.channelName.Bind(wx.EVT_CONTEXT_MENU, self.onPass)
		self.channelLink.Bind(wx.EVT_CONTEXT_MENU, self.onPass)
		self.addBTN.Bind(wx.EVT_BUTTON, self.addChannel)
		self.Bind(wx.EVT_ACTIVATE, self.onSalir)
		self.Bind(wx.EVT_BUTTON, self.onSalir, id=wx.ID_CANCEL)

	def onPass(self, event):
		pass

	def addChannel(self, event):
		name = self.channelName.GetValue()
		link = self.channelLink.GetValue()
		if not search(r"https\:\/\/www\.youtube\.com\/channel\/[\w\-]+", link):
			ui.message("La url ingresada no es válida")
			self.channelLink.SetFocus()
			return
		fileName = [chard for chard in name if search(r"[a-zA-Z0-9\-\_]", chard)]
		fileName = "".join(fileName)
		if link[-7:] != "/videos":
			link = f"{link}/videos"
		self.Close()
		Thread(target=self.getVideos, args=(name, link, fileName), daemon= True).start()

	def getVideos(self, channelName, channelID, fileName):
		winsound.PlaySound("C:\\Windows\\Media\\Alarm08.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
		list = [{"name": channelName, "link": channelID, "file": fileName}]
		with youtube_dl.YoutubeDL(self.options) as ydl:
			p = ydl.extract_info(channelID, download=False)
		titles = [p["entries"][i]["title"] for i in range(len(p["entries"]))]
		links = [f"https://www.youtube.com/watch?v={p['entries'][i]['url']}" for i in range(len(p["entries"]))]
		for i in range(len(titles)):
			list.append({'title': titles[i], 'link': links[i]})
		with open(f"{dirAddon}\\channels\\{fileName}", "w") as f:
			json.dump(list, f, indent=2)
		winsound.PlaySound(None, winsound.SND_PURGE)
		self.frame.start(f"{channelName} añadido correctamente")

	def onSalir(self, event):
		if event.GetEventType() == 10012:
			self.Destroy()
			gui.mainFrame.postPopup()
		elif event.GetActive() == False:
			self.Destroy()
			gui.mainFrame.postPopup()
		event.Skip()
