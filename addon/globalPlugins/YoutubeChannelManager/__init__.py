# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

from datetime import timedelta
import speech
from collections import OrderedDict
import core
import gui
import re
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
dirAddon=os.path.dirname(__file__)
sys.path.append(dirAddon)
sys.path.append(os.path.join(dirAddon, "lib"))
import xml
xml.__path__.append(os.path.join(dirAddon, "lib", "xml"))
import html
html.__path__.append(os.path.join(dirAddon, "lib", "html"))
import sqlite3 as sql
sql.__path__.append(os.path.join(dirAddon, "lib", "sqlite3"))
import youtube_dl
del sys.path[-2:]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		if globalVars.appArgs.secure: return
		self.connect = None
		self.cursor = None
		self.options = {'ignoreerrors': True, 'quiet': True, 'extract_flat': 'in_playlist', 'dump_single_json': True}
		self.switch = False
		self.channels = []
		self.videos = []
		self.index = []
		self.channels_temp = []
		self.videos_temp = []
		self.index_temp = []
		self.y = 0
		self.z = 1
		self.sounds = None
		self.update_time = None
		core.postNvdaStartup.register(self.startDB)

	def startDB(self):
		self.mainThread = HiloComplemento()
		self.mainThread.start()
		if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "channels")):
			self.connect = sql.connect(os.path.join(globalVars.appArgs.configPath, "channels"), check_same_thread= False)
			self.cursor = self.connect.cursor()
			self.cursor.execute('create table channels(name text, url text, channel_id text, favorite bin, id integer primary key autoincrement)')
			self.connect.commit()
			self.cursor.execute('create table videos(title text, url text, video_id text, channel_id text, view_count integer, channel_name text, id integer primary key autoincrement)')
			self.connect.commit()
			self.cursor.execute('create table settings(sounds bit, update_time integer, id integer primary key autoincrement)')
			self.connect.commit()
			self.cursor.execute('insert into settings(sounds, update_time) values(1, 0)')
			self.connect.commit()
			self.cursor.execute('VACUUM')
			self.connect.commit()
		else:
			self.connect = sql.connect(os.path.join(globalVars.appArgs.configPath, "channels"), check_same_thread= False)
			self.cursor = self.connect.cursor()
		Thread(target=self.start, daemon= True).start()

	def start(self, speak= False):
		self.channels = []
		self.videos = []
		self.index = []
		self.cursor.execute('select * from channels')
		self.channels = self.cursor.fetchall()
		self.cursor.execute('select * from settings')
		settings = self.cursor.fetchall()
		self.sounds = settings[0][0]
		self.update_time = settings[0][1]
		for channel in self.channels:
			self.cursor.execute(f'select * from videos where channel_id = "{channel[2]}" order by id desc')
			videos = self.cursor.fetchall()
			videos_r = videos
			self.videos.append(videos_r)
			self.index.append(0)
		if speak:
			ui.message(speak)

	def script_channelSettings(self, gesture):
		if len(self.channels) == 0: return
		if self.channels[0][1] == None: return
		self.desactivar(False)
		self.dlg = ChannelSettings(gui.mainFrame, "Configuración de canal", self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_globalSettings(self, gesture):
		self.desactivar(False)
		self.dlg = GlobalSettings(gui.mainFrame, "Configuraciones", self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_newChannel(self, gesture):
		if len(self.channels) > 0:
			if self.channels[0][1] == None: return
		self.desactivar(False)
		self.dlg = NewChannel(gui.mainFrame, "Añadir canal", self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_newSearch(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		self.desactivar(False)
		if self.channels[0][1] == None:
			self.channels = self.channels_temp
			self.videos = self.videos_temp
			self.index = self.index_temp
		self.dlg = NewSearch(gui.mainFrame, "Nueva búsqueda", self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_removeChannel(self, gesture):
		try:
			if len(self.channels) == 0:
				ui.message("Ningún canal seleccionado")
				return
			elif self.channels[0][1] == None:
				self.channels = self.channels_temp
				self.videos = self.videos_temp
				self.index = self.index_temp
				self.x = 0
				self.y = 0
				ui.message("Búsqueda eliminada")
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "recicled.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				return
			Thread(target=self.startRemoveChannel, daemon= True).start()
			self.desactivar(False)
		except:
			pass
	def startRemoveChannel(self):
		modal = wx.MessageDialog(None, f'¿Quieres eliminar el canal {self.channels[self.y][0]}?', _("Atención"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if modal.ShowModal() == wx.ID_YES:
			self.cursor.execute(f'delete from videos where channel_id = "{self.channels[self.y][2]}"')
			self.cursor.execute(f'delete from channels where channel_id = "{self.channels[self.y][2]}"')
			self.connect.commit()
			self.channels.pop(self.y)
			self.videos.pop(self.y)
			self.index.pop(self.y)
			self.y = 0
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "recicled.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
		else:
			modal.Destroy()

	def speak(self, str, pause):
		Thread(target=self.tSpeak, args=(str, pause), daemon= True).start()

	def tSpeak(self, str, pause):
		speech.setSpeechMode(speech.SpeechMode.off)
		time.sleep(pause)
		speech.setSpeechMode(speech.SpeechMode.talk)
		ui.message(str)

	@script(gesture="kb:NVDA+y", description="Activa y desactiva la interfaz invisible", category= "YoutubeChannelManager")
	def script_toggle(self, gesture):
		self.desactivar() if self.switch else self.activar()

	def activar(self, speak= True):
			self.switch = True
			if speak: ui.message("Atajos activados")
			self.bindGestures(
				{"kb:downArrow":"nextItem",
				"kb:upArrow":"previousItem",
				"kb:rightArrow":"nextSection",
				"kb:leftArrow":"previousSection",
				"kb:o":"open",
				"kb:s":"channelSettings",
				"kb:g":"globalSettings",
				"kb:r":"openAudio",
				"kb:home":"firstItem",
				"kb:end":"positionAnnounce",
				"kb:n":"newChannel",
				"kb:b":"newSearch",
				"kb:c":"copyLink",
				"kb:d":"viewData",
				"kb:delete":"removeChannel",
				"kb:f5":"reloadChannel",
				"kb:f1":"helpCommands",
				"kb:escape":"toggle"}
			)

	def desactivar(self, speak=True):
		self.switch = False
		if speak: ui.message("Atajos desactivados")
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)

	def script_helpCommands(self, gesture):
		self.desactivar(False)
		help_text="""
Escape; desactiva la interfaz virtual.
n; Activa el diálogo para añadir un nuevo canal.
s; Activa la ventana de configuración del canal actual.
g; Activa la ventana de opciones globales.
o; abre el link del video actual en el navegador por defecto.
r; Carga el audio en un reproductor web personalizado.
d; abre una ventana con datos del video actual.
b; Activa el cuadro de búsqueda.
suprimir; Activa el diálogo para eliminar el canal actual, y en la ventana de resultados, elimina la columna y vuelve a la lista de canales.
f5; Busca videos nuevos en el canal actual.
		"""
		ui.browseableMessage(help_text, "Ayuda de comandos")


	def script_nextItem(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.z += 1
			if self.z < len(self.videos[self.y]):
				ui.message(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}')
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.z = 0
				ui.message(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}')
		except IndexError:
			pass

	def script_previousItem(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.z -= 1
			if self.z >= 0:
				ui.message(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}')
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.z = len(self.videos[self.y]) - 1
				ui.message(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}')
		except IndexError:
			pass

	def script_nextSection(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.index[self.y] = self.z
			self.y += 1
			if self.y < len(self.index):
				self.z = self.index[self.y]
				ui.message(f'{self.channels[self.y][0]}, {self.videos[self.y][self.z][0]}')
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.y = 0
				self.z = self.index[self.y]
				ui.message(f'{self.channels[self.y][0]}, {self.videos[self.y][self.z][0]}')
		except IndexError:
			ui.message("No hay canales en la base de datos")

	def script_previousSection(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.index[self.y] = self.z
			self.y -= 1
			if self.y >= 0:
				self.z = self.index[self.y]
				ui.message(f'{self.channels[self.y][0]}, {self.videos[self.y][self.z][0]}')
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.y = len(self.index) - 1
				self.z = self.index[self.y]
				ui.message(f'{self.channels[self.y][0]}, {self.videos[self.y][self.z][0]}')
		except IndexError:
			ui.message("No hay canales en la base de datos")

	def script_open(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		ui.message("Abriendo el link en el navegador...")
		webbrowser.open(self.videos[self.y][self.z][1], new=0, autoraise=True)
		self.desactivar(False)

	def script_firstItem(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		self.z = 0
		ui.message(self.videos[self.y][self.z][0])

	def script_positionAnnounce(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		ui.message(f'{self.z+1} de {len(self.videos[self.y])}, {self.videos[self.y][self.z][4]} reproducciones. {self.videos[self.y][self.z][5]}. Pulsa f1 para ver la ayuda de comandos')

	def script_reloadChannel(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		Thread(target=self.startReload, daemon= True).start()

	def startReload(self):
		new_videos = []
		videos_list = self.getVideosList(self.channels[self.y][1])
		for video in videos_list:
			if self.videos[self.y][0][2] != video:
				new_videos.append(video)
			else:
				break
		if len(new_videos) == 0:
			ui.message("No se han encontrado videos nuevos para este canal")
		elif len(new_videos) == 1:
			Thread(target=self.downloadNewVideos, args=(new_videos, "Se ha encontrado un video nuevo. ¿Quieres actualizar la base de datos?"), daemon= True).start()
		elif len(new_videos) > 1:
			Thread(target=self.downloadNewVideos, args=(new_videos, f"Se han encontrado {len(new_videos)} videos nuevos. ¿Quieres actualizar la base de datos?"), daemon= True).start()

	def getVideosList(self, channel_url):
		content = urllib.request.urlopen(channel_url).read().decode('utf-8')
		ids_list = re.findall(r'(?<="videoId":")[\w\d\-\.\,]+(?=")', content)
		# Método que elimina las duplicaciones de una lista manteniendo el órden de los elementos
		final_list = list(OrderedDict.fromkeys(ids_list))
		return final_list

	def downloadNewVideos(self, new_videos, message_text):
		modal = wx.MessageDialog(None, message_text, "⬆", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if modal.ShowModal() == wx.ID_YES:
			if self.sounds: winsound.PlaySound("C:\\Windows\\Media\\Alarm05.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
			list_videos = list(reversed(new_videos))
			for video in list_videos:
				data = self.getData(f'https://www.youtube.com/watch?v={video}')
				self.insert_videos((data["title"], f'https://www.youtube.com/watch?v={video}', video, self.channels[self.y][2], data["view_count"], self.channels[self.y][0]))
			if self.sounds: winsound.PlaySound(None, winsound.SND_PURGE)
			ui.message("Proceso finalizado")
			self.connect.close()
			self.startDB()
		else:
			modal.Destroy()

	def insert_videos(self, entities):
		self.cursor.execute(f'insert into videos(title, url, video_id, channel_id, view_count, channel_name) values(?, ?, ?, ?, ?, ?)', entities)
		self.connect.commit()

	def script_copyLink(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		self.desactivar(False)
		api.copyToClip(self.videos[self.y][self.z][1])
		if self.sounds: winsound.PlaySound("C:\\Windows\\Media\\Windows Recycle.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

	def terminate(self):
		pass

	def script_viewData(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		self.desactivar(False)
		ui.message("Obteniendo los datos del video...")
		Thread(target=self.startViewData, daemon= True).start()

	def getData(self, url):
		with youtube_dl.YoutubeDL(self.options) as ydl:
			data_dict = ydl.extract_info(url, download= False)
		return data_dict

	def startViewData(self):
		p = self.getData(self.videos[self.y][self.z][1])
		upload_date = f'{p["upload_date"][6:][:2]}.{p["upload_date"][4:][:2]}.{p["upload_date"][:4]}'
		time = self.timeFormat(p["duration"])
		data = f'''Duración: {time}
Fecha de subida: {upload_date}
Reproducciones: {p["view_count"]}
Me gusta: {p["like_count"]}
Descripción: {p["description"]}'''
		ui.browseableMessage(data, "Datos del video")

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

	def script_openAudio(self, gesture):
		if len(self.channels) == 0:
			ui.message("Ningún canal seleccionado")
			return
		self.desactivar(False)
		Thread(target=self.startOpenAudio, daemon= True).start()
		ui.message("Activando el reproductor web...")

	def startOpenAudio(self, time= False):
		audio_url = self.getAudioUrl(self.videos[self.y][self.z][1])
		self.openPlayer(self.videos[self.y][self.z][0], audio_url)

	def openPlayer(self, title, url):
		code = f'''
<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="reproductor.js"></script>
</head>
<body>
<audio src="{url}" id="reproductor" preload="metadata">
</audio>
</body>
</html>
		'''
		with open(os.path.join(dirAddon, "reproductor", "index.html"), "w", encoding="utf-8") as file:
			file.write(code)
		webbrowser.open(f"file://{dirAddon}/reproductor/index.html", new=2)

	def getAudioUrl(self, url, tiempo=False):
		ydl = youtube_dl.YoutubeDL({'format': "bestaudio/best", 'logger': MyLogger()})
		ydl.add_default_info_extractors()
		result = ydl.extract_info(url, download=False)
		video = result['entries'][0] if 'entries' in result else result
		for format in video['formats']:
			if format['ext'] == 'm4a':
				audioUrl = format['url']
		tiempoTotal = str(timedelta(seconds=int(str(video['duration']).split(".")[0])))
		return [audioUrl, tiempoTotal] if tiempo else audioUrl

class HiloComplemento(Thread):
	def __init__(self):
		super(HiloComplemento, self).__init__()
		self.daemon = True

	def run(self):
		def chkActualizacion():
			url = "https://api.github.com/repos/ytdl-org/youtube-dl/releases"
			req = urllib.request.Request(url)
			r = urllib.request.urlopen(req).read()
			gitJson = json.loads(r.decode('utf-8'))
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
						archive = zipfile.ZipFile(os.path.join(dirAddon, "temp.zip"))
						root = archive.namelist()[0]
						filtro = [item for item in archive.namelist() if "youtube_dl".lower() in item.lower()]
						for file in archive.namelist():
							if file.startswith(filtro[0]):
								archive.extract(file, dirAddon)
						archive.close()
						os.remove(os.path.join(dirAddon, "temp.zip"))
						shutil.rmtree(os.path.join(dirAddon, "lib", "youtube_dl"))
						shutil.move(os.path.join(dirAddon, root, "youtube_dl"), os.path.join(dirAddon, "lib", "youtube_dl"))
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

			msg = _("Descarga finalizada. Cierre la ventana para terminar de instalar la librería y reiniciar NVDA.")
			wx.CallAfter(self.frame.done, msg)
		except Exception as e:
			wx.CallAfter(self.frame.error, _("Algo salió mal.\n") + _("Compruebe que tiene conexión a internet y vuelva a intentarlo.\n") + _("Ya puede cerrar esta ventana."))

class MyLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		pass

class NewChannel(wx.Dialog):
	def __init__(self, parent, titulo, frame, connect, cursor):
		super(NewChannel, self).__init__(parent, -1, title=titulo)
		self.options = {'ignoreerrors': True, 'quiet': True, 'extract_flat': 'in_playlist', 'dump_single_json': True}
		self.frame = frame
		self.connect = connect
		self.cursor = cursor
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
		channel_name = self.channelName.GetValue()
		if channel_name == "":
			ui.message("Debes ingresar algún nombre para este canal")
			self.channelName.SetFocus()
			return
		channel_url = self.getChannelUrl(self.channelLink.GetValue())
		if not channel_url:
			ui.message("La url ingresada no es válida")
			self.channelLink.SetValue("")
			self.channelLink.SetFocus()
			return
		channel_id = "".join([chard for chard in channel_name if re.search(r"[a-zA-Z0-9]", chard)])
		if channel_url[-7:] != "/videos":
			channel_url = f"{channel_url}/videos"
		Thread(target=self.getVideos, args=(channel_name, channel_url, channel_id), daemon= True).start()
		self.Close()

	def getChannelUrl(self, url):
		if not re.search(r'http(s)?...(www)?.?youtube.com.', url): return None
		if re.search(r'http(s)?...(www)?.?youtube.com.channel.', url): return url
		content = urllib.request.urlopen(url).read().decode()
		channelUrl = re.search(r'(?<=")\/channel\/[\w\-\?\.]+(?=")', content)
		if channelUrl:
			return f'https://www.youtube.com/{channelUrl[0]}'
		# else:
			# return None

	def getVideos(self, channelName, channelUrl, channelID):
		if self.frame.sounds: winsound.PlaySound("C:\\Windows\\Media\\Alarm05.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
		self.insert_channel((channelName, channelUrl, channelID, 0))
		with youtube_dl.YoutubeDL(self.options) as ydl:
			data_dict = ydl.extract_info(channelUrl, download= False)
		data = data_dict['entries']
		for i in reversed(range(len(data))):
			self.insert_videos((data[i]["title"], "https://www.youtube.com/watch?v=" + data[i]["id"], data[i]["id"], channelID, data[i]["view_count"], channelName))
		self.connect.close()
		self.frame.startDB()
		if self.frame.sounds: winsound.PlaySound(None, winsound.SND_PURGE)
		ui.message("Proceso Finalizado")

	def insert_channel(self, entities):
		self.cursor.execute(f'insert into channels(name, url, channel_id, favorite) values(?, ?, ?, ?)', entities)
		self.connect.commit()

	def insert_videos(self, entities):
		self.cursor.execute(f'insert into videos(title, url, video_id, channel_id, view_count, channel_name) values(?, ?, ?, ?, ?, ?)', entities)
		self.connect.commit()

	def onSalir(self, event):
		if event.GetEventType() == 10012:
			self.Destroy()
			gui.mainFrame.postPopup()
		elif event.GetActive() == False:
			self.Destroy()
			gui.mainFrame.postPopup()
		event.Skip()

class NewSearch(wx.Dialog):
	def __init__(self, parent, titulo, frame, connect, cursor):
		super(NewSearch, self).__init__(parent, -1, title=titulo)
		self.frame = frame
		self.connect = connect
		self.cursor = cursor
		self.Panel = wx.Panel(self)
		wx.StaticText(self.Panel, wx.ID_ANY, "Ingresa el término de búsqueda y pulsa intro")
		self.searchText = wx.TextCtrl(self.Panel,wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
		self.searchBTN = wx.Button(self.Panel, wx.ID_ANY, "&Iniciar la búsqueda")
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, "&Cancelar")
		self.searchText.Bind(wx.EVT_CONTEXT_MENU, self.onPass)
		self.searchText.Bind(wx.EVT_TEXT_ENTER, self.startSearch)
		self.searchBTN.Bind(wx.EVT_BUTTON, self.startSearch)
		self.Bind(wx.EVT_ACTIVATE, self.onSalir)
		self.Bind(wx.EVT_BUTTON, self.onSalir, id=wx.ID_CANCEL)

	def onPass(self, event):
		pass

	def startSearch(self, evt):
		text = self.searchText.GetValue()
		self.cursor.execute(f'select * from videos where title like "%{text}%" order by id desc')
		results = self.cursor.fetchall()
		if results:
			self.frame.channels_temp = self.frame.channels
			self.frame.videos_temp = self.frame.videos
			self.frame.index_temp = self.frame.index
			self.frame.channels = [("Resultados de búsqueda", None)]
			self.frame.videos = [results]
			self.frame.index = [0]
			self.frame.y = 0
			self.frame.z = 0
			self.frame.activar(False)
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "yResults.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.frame.speak(f"Se han encontrado {len(results)} resultados", 0.2)
		else:
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "nResults.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.frame.speak("No se han encontrado resultados", 0.2)
			self.frame.activar(False)
		self.Close()

	def onSalir(self, event):
		if event.GetEventType() == 10012:
			self.Destroy()
			gui.mainFrame.postPopup()
		elif event.GetActive() == False:
			self.Destroy()
			gui.mainFrame.postPopup()
		event.Skip()

class ChannelSettings(wx.Dialog):
	def __init__(self, parent, titulo, frame, connect, cursor):
		super(ChannelSettings, self).__init__(parent, -1, title=titulo)
		self.frame = frame
		self.connect = connect
		self.cursor = cursor
		self.Panel = wx.Panel(self)
		wx.StaticText(self.Panel, wx.ID_ANY, "Nombre del canal")
		self.channelName = wx.TextCtrl(self.Panel,wx.ID_ANY)
		self.channelName.SetValue(self.frame.channels[self.frame.y][0])
		self.checkbox = wx.CheckBox(self.Panel, wx.ID_ANY, _("Canal favorito"))
		self.checkbox.SetValue(self.frame.channels[self.frame.y][3])
		self.saveBTN = wx.Button(self.Panel, wx.ID_ANY, "&Guardar los cambios")
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, "&Descartar cambios y cerrar")
		self.channelName.Bind(wx.EVT_CONTEXT_MENU, self.onPass)
		self.saveBTN.Bind(wx.EVT_BUTTON, self.saveSettings)
		self.Bind(wx.EVT_ACTIVATE, self.onSalir)
		self.Bind(wx.EVT_BUTTON, self.onSalir, id=wx.ID_CANCEL)

	def onPass(self, event):
		pass

	def onSalir(self, event):
		if event.GetEventType() == 10012:
			self.Destroy()
			gui.mainFrame.postPopup()
		elif event.GetActive() == False:
			self.Destroy()
			gui.mainFrame.postPopup()
		event.Skip()

	def saveSettings(self, evt):
		self.Close()
		text = self.channelName.GetValue()
		favorite = self.checkbox.GetValue()
		if text != self.frame.channels[self.frame.y][0] or int(favorite) != self.frame.channels[self.frame.y][3]:
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "finish.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.cursor.execute(f'update channels set name = "{text}", favorite = "{int(favorite)}" where name = "{self.frame.channels[self.frame.y][0]}"')
			self.connect.commit()
			self.connect.close()
			self.frame.startDB()
		self.frame.activar(False)
		self.frame.speak("Configuración guardada", 1)

class GlobalSettings(wx.Dialog):
	def __init__(self, parent, titulo, frame, connect, cursor):
		super(GlobalSettings, self).__init__(parent, -1, title=titulo)
		self.frame = frame
		self.connect = connect
		self.cursor = cursor
		self.Panel = wx.Panel(self)
		self.checkbox = wx.CheckBox(self.Panel, wx.ID_ANY, _("Activar los sonidos del complemento"))
		self.checkbox.SetValue(self.frame.sounds)
		wx.StaticText(self.Panel, wx.ID_ANY, "Selecciona el intervalo de tiempo para la verificación de nuevas subidas en los canales favoritos")
		self.listbox = wx.ListBox(self.Panel, wx.ID_ANY, choices=["Desactivado", "24 horas", "12 horas", "8 horas", "4 horas", "2 horas", "1 hora"])
		self.listbox.SetSelection(self.frame.update_time)
		self.saveBTN = wx.Button(self.Panel, wx.ID_ANY, "&Guardar los cambios")
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, "&Descartar cambios y cerrar")
		self.saveBTN.Bind(wx.EVT_BUTTON, self.saveSettings)
		self.Bind(wx.EVT_ACTIVATE, self.onSalir)
		self.Bind(wx.EVT_BUTTON, self.onSalir, id=wx.ID_CANCEL)

	def onPass(self, event):
		pass

	def onSalir(self, event):
		if event.GetEventType() == 10012:
			self.Destroy()
			gui.mainFrame.postPopup()
		elif event.GetActive() == False:
			self.Destroy()
			gui.mainFrame.postPopup()
		event.Skip()

	def saveSettings(self, evt):
		self.Close()
		sounds = int(self.checkbox.GetValue())
		update_time = self.listbox.GetSelection()
		if self.frame.sounds != sounds or self.frame.update_time != update_time:
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "finish.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.cursor.execute(f'update settings set sounds = {sounds}, update_time = {update_time}')
			self.connect.commit()
			self.connect.close()
			self.frame.startDB()
			self.frame.speak("Configuraciones guardadas", 1)

