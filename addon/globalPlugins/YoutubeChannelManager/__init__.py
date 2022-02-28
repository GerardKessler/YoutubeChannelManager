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
from threading import Thread, Timer
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
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Translatable Strings
	unselected = _('Ningún canal seleccionado')
	noDatabase = _('No hay canales en la base de datos')
	attention = _('Atención')
	saveChanges = _('&Guardar los cambios')
	discard = _('&Descartar cambios y cerrar')
	itemsData = [_('Duración'), _('Fecha de subida'), _('Reproducciones'), _('Me gusta'), _('Descripción'), _('Datos del video')]
	html_elements = [_('Reproducir'), _('Retroceder 10 segundos'), _('Adelantar 10 segundos'), _('Velocidad de reproducción'), _('Bajar volúmen'), _('Silenciar, quitar silencio'), _('Subir volúmen')]


	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if globalVars.appArgs.secure: return
		self.connect = None
		self.cursor = None
		self.options = {
			'ignoreerrors': True,
			'quiet': True,
			'extract_flat': 'in_playlist',
			'dump_single_json': True
		}
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
		self.order_by = None
		self.order = ["id desc", "id asc", "view_count desc", "view_count asc"]
		self.startTimer = None
		core.postNvdaStartup.register(self.firstRun)

	def firstRun(self):
		Thread(target=self.updatedYoutube_dl, daemon= True).start()
		self.startDB()

	def updatedYoutube_dl(self):
		time.sleep(10)
		self.mainThread = AddonThread(self)
		self.mainThread.start()

	def startDB(self, read= True):
		if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "channels")):
			self.connect = sql.connect(os.path.join(globalVars.appArgs.configPath, "channels"), check_same_thread= False)
			self.cursor = self.connect.cursor()
			self.cursor.execute('create table channels(name text, url text, channel_id text, favorite bin, id integer primary key autoincrement)')
			self.connect.commit()
			self.cursor.execute('create table videos(title text, url text, video_id text, channel_id text, view_count integer, channel_name text, id integer primary key autoincrement)')
			self.connect.commit()
			self.cursor.execute('create table settings(sounds bit, update_time integer, order_by integer, id integer primary key autoincrement)')
			self.connect.commit()
			self.cursor.execute('insert into settings(sounds, update_time, order_by) values(1, 0, 0)')
			self.connect.commit()
			self.cursor.execute('VACUUM')
			self.connect.commit()
		else:
			self.connect = sql.connect(os.path.join(globalVars.appArgs.configPath, "channels"), check_same_thread= False)
			self.cursor = self.connect.cursor()
		if read:
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
		self.order_by = settings[0][2]
		for channel in self.channels:
			self.cursor.execute(f'select * from videos where channel_id = "{channel[2]}" order by {self.order[self.order_by]}')
			videos = self.cursor.fetchall()
			videos_r = videos
			self.videos.append(videos_r)
			self.index.append(0)
		self.setTimer()
		if speak:
			ui.message(speak)

	def setTimer(self):
		if self.update_time > 0:
			times = [False, 86400, 43200, 28800, 14400, 7200, 3600]
			self.startTimer = StartTimer(times[self.update_time], self.checkUpdate)

	def checkUpdate(self):
		for i in range(len(self.channels)):
			if self.channels[i][3]:
				self.cursor.execute(f'select video_id from videos where channel_id = "{self.channels[i][2]}"')
				last_video = self.cursor.fetchall()
				self.startReload(self.channels[i], i, last_video[-1][0], False)
				time.sleep(20)

	def script_channelSettings(self, gesture):
		if len(self.channels) == 0: return
		if self.channels[0][1] == None: return
		self.desactivar(False)
		self.dlg = ChannelSettings(gui.mainFrame, _('Configuración de canal'), self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_globalSettings(self, gesture):
		self.desactivar(False)
		self.dlg = GlobalSettings(gui.mainFrame, _('Configuraciones'), self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_newChannel(self, gesture):
		if len(self.channels) > 0:
			if self.channels[0][1] == None: return
		self.desactivar(False)
		self.dlg = NewChannel(gui.mainFrame, _('Añadir canal'), self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_newSearch(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		self.desactivar(False)
		if self.channels[0][1] == None:
			self.channels = self.channels_temp
			self.videos = self.videos_temp
			self.index = self.index_temp
		self.dlg = NewSearch(gui.mainFrame, _('Nueva búsqueda'), self, self.connect, self.cursor)
		gui.mainFrame.prePopup()
		self.dlg.Show()

	def script_globalSearch(self, gesture):
		self.desactivar(False)
		if self.channels[0][1] == None:
			self.channels = self.channels_temp
			self.videos = self.videos_temp
			self.index = self.index_temp
		gSearch = GlobalSearch(gui.mainFrame, _('Búsqueda global'), self)
		gui.mainFrame.prePopup()
		gSearch.Show()

	def script_removeDatabase(self, gesture):
		Thread(target=self.startRemoveDatabase, daemon= True).start()

	def startRemoveDatabase(self):
		modal = wx.MessageDialog(None, _(f'¿Seguro que quieres eliminar la base de datos?'), _('¡Atención!'), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if modal.ShowModal() == wx.ID_YES:
			self.connect.close()
			os.remove(os.path.join(globalVars.appArgs.configPath, "channels"))
			self.startDB(True)
			self.speak(_('Base de datos eliminada'), 0.3)

	def script_removeChannel(self, gesture):
		try:
			if len(self.channels) == 0:
				ui.message(unselected)
				return
			elif self.channels[0][1] == None:
				self.channels = self.channels_temp
				self.videos = self.videos_temp
				self.index = self.index_temp
				self.x = 0
				self.y = 0
				ui.message(_('Búsqueda eliminada'))
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "recicled.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				return
			Thread(target=self.startRemoveChannel, daemon= True).start()
			self.desactivar(False)
		except:
			pass
	def startRemoveChannel(self):
		modal = wx.MessageDialog(None, _(f'¿Quieres eliminar el canal {self.channels[self.y][0]}?'), attention, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
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

	@script(
		category= "YoutubeChannelManager",
		# Translators: Descripción del elemento en el diálogo gestos de entrada
		description= _('Activa y desactiva la interfaz invisible'),
		gesture="kb:NVDA+y"
	)
	def script_toggle(self, gesture):
		self.desactivar() if self.switch else self.activar()

	def activar(self, speak= True):
			self.switch = True
			if speak: ui.message(_('Atajos activados'))
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
				"kb:control+b":"globalSearch",
				"kb:c":"copyLink",
				"kb:d":"viewData",
				"kb:delete":"removeChannel",
				"kb:control+shift+delete":"removeDatabase",
				"kb:f5":"reloadChannel",
				"kb:f1":"helpCommands",
				"kb:escape":"toggle"}
			)

	def desactivar(self, speak=True):
		self.switch = False
		if speak: ui.message(_('Atajos desactivados'))
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)

	def script_helpCommands(self, gesture):
		self.desactivar(False)
		# Translators: Ayuda de teclado
		help_text= _("""
Escape; desactiva la interfaz virtual.
n; Activa el diálogo para añadir un nuevo canal.
s; Activa la ventana de configuración del canal actual.
g; Activa la ventana de opciones globales.
o; abre el link del video actual en el navegador por defecto.
r; Carga el audio en un reproductor web personalizado.
c; copia el link del video actual al portapapeles.
d; abre una ventana con datos del video actual.
b; Activa el cuadro de búsqueda de videos en la base de datos.
control + b; Activa el cuadro de búsqueda de videos en la página de Youtube.
suprimir; Activa el diálogo para eliminar el canal actual, y en la ventana de resultados, elimina la columna y vuelve a la lista de canales.
control + shift + suprimir; elimina la base de datos.
f5; Busca videos nuevos en el canal actual.""")
		ui.browseableMessage(help_text, _('Ayuda de comandos'))

	def script_nextItem(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.z += 1
			if self.z < len(self.videos[self.y]):
				ui.message(_(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}'))
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.z = 0
				ui.message(_(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}'))
		except IndexError:
			pass

	def script_previousItem(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.z -= 1
			if self.z >= 0:
				ui.message(_(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}'))
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.z = len(self.videos[self.y]) - 1
				ui.message(_(f'{self.videos[self.y][self.z][0]}- {self.z+1} de {len(self.videos[self.y])}'))
		except IndexError:
			pass

	def script_nextSection(self, gesture):
		try:
			if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.index[self.y] = self.z
			self.y += 1
			if self.y < len(self.index):
				self.z = self.index[self.y]
				ui.message(_(f'{self.channels[self.y][0]}, {self.videos[self.y][self.z][0]}'))
			else:
				if self.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "click.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				self.y = 0
				self.z = self.index[self.y]
				ui.message(_(f'{self.channels[self.y][0]}, {self.videos[self.y][self.z][0]}'))
		except IndexError:
			ui.message(noDatabase)

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
			ui.message(noDatabase)

	def script_open(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		ui.message(_('Abriendo el link en el navegador...'))
		webbrowser.open(self.videos[self.y][self.z][1], new=0, autoraise=True)
		self.desactivar(False)

	def script_firstItem(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		self.z = 0
		ui.message(self.videos[self.y][self.z][0])

	def script_positionAnnounce(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		ui.message(_(f'{self.z+1} de {len(self.videos[self.y])}, {self.videos[self.y][self.z][4]} reproducciones. {self.videos[self.y][self.z][5]}. Pulsa f1 para ver la ayuda de comandos'))

	def script_reloadChannel(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		self.cursor.execute(f'select video_id from videos where channel_id = "{self.channels[self.y][2]}"')
		last_video = self.cursor.fetchall()
		Thread(target=self.startReload, args=(self.channels[self.y], self.y, last_video[-1][0]), daemon= True).start()

	def startReload(self, channel, index, last_video, messages= True):
		new_videos = []
		videos_list = self.getVideosList(channel[1])
		for video in videos_list:
			if last_video != video:
				new_videos.append(video)
			else:
				break
		if len(new_videos) == 0:
			if messages: ui.message(_('No se han encontrado videos nuevos para este canal'))
		elif len(new_videos) == 1:
			Thread(target=self.downloadNewVideos, args=(new_videos, _(f'Se ha añadido un video nuevo en {channel[0]}'), channel), daemon= True).start()
		elif len(new_videos) > 1:
			Thread(target=self.downloadNewVideos, args=(new_videos, _(f'Se han añadido {len(new_videos)} videos nuevos en {channel[0]}'), channel), daemon= True).start()

	def getVideosList(self, channel_url):
		content = urllib.request.urlopen(channel_url).read().decode('utf-8')
		ids_list = re.findall(r'(?<="videoId":")[\w\d\-\.\,]+(?=")', content)
		# Método que elimina las duplicaciones de una lista manteniendo el órden de los elementos
		final_list = list(OrderedDict.fromkeys(ids_list))
		return final_list

	def downloadNewVideos(self, new_videos, message_text, channel):
		if self.sounds: winsound.PlaySound("C:\\Windows\\Media\\Alarm05.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
		list_videos = list(reversed(new_videos))
		for video in list_videos:
			data = self.getData(f'https://www.youtube.com/watch?v={video}')
			self.insert_videos((data["title"], f'https://www.youtube.com/watch?v={video}', video, channel[2], data["view_count"], channel[0]))
		if self.sounds: winsound.PlaySound(None, winsound.SND_PURGE)
		ui.message(message_text)
		self.connect.close()
		self.startDB()

	def insert_videos(self, entities):
		self.cursor.execute(f'insert into videos(title, url, video_id, channel_id, view_count, channel_name) values(?, ?, ?, ?, ?, ?)', entities)
		self.connect.commit()

	def script_copyLink(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		self.desactivar(False)
		api.copyToClip(self.videos[self.y][self.z][1])
		if self.sounds: winsound.PlaySound("C:\\Windows\\Media\\Windows Recycle.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

	def terminate(self):
		pass

	def script_viewData(self, gesture):
		if len(self.channels) == 0:
			ui.message(unselected)
			return
		self.desactivar(False)
		ui.message(_('Obteniendo los datos del video...'))
		Thread(target=self.startViewData, daemon= True).start()

	def getData(self, url):
		with youtube_dl.YoutubeDL(self.options) as ydl:
			data_dict = ydl.extract_info(url, download= False)
		return data_dict

	def startViewData(self):
		p = self.getData(self.videos[self.y][self.z][1])
		upload_date = f'{p["upload_date"][6:][:2]}.{p["upload_date"][4:][:2]}.{p["upload_date"][:4]}'
		time = self.timeFormat(p["duration"])
		data = f'''{self.itemsData[0]}: {time}
{self.itemsData[1]}: {upload_date}
{self.itemsData[2]}: {p["view_count"]}
{self.itemsData[3]}: {p["like_count"]}
{self.itemsData[4]}: {p["description"]}'''
		ui.browseableMessage(data, self.itemsData[5])

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
			ui.message(unselected)
			return
		self.desactivar(False)
		Thread(target=self.startOpenAudio, daemon= True).start()
		ui.message(_('Activando el reproductor web...'))

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
</head>
<body>
<audio onTimeUpdate='audioTime();' src="{url}" id="reproductor" preload="auto">
</audio>
<ul style="list-style:none;margin-left:auto;margin-right:auto;">
<li><button accesskey="k" id="toggle" onClick='playPause();'>{self.html_elements[0]}</button></li>
<li><button accesskey="j" id="back" onClick='timeBack();'>{self.html_elements[1]}</button></li>
<li><p accesskey="i" id="time" onClick='speak(this.textContent);'>0:00</p></li>
<li><button accesskey="l" id="advance" onClick='timeAdvance();'>{self.html_elements[2]}</button></li>
<li><label>{self.html_elements[3]}<input type="range" min="0" max="100" step="10" value="50" onChange='audioRate(this.value)' /></label></li>
<li><button accesskey="o" onClick='volumeDown();'>{self.html_elements[4]}</button></li>
<li><button accesskey="m" onClick='toggleMute();'>{self.html_elements[5]}</button></li>
<li><button accesskey="u" onClick='volumeUp();'>{self.html_elements[6]}</button></li>
<div id="alert" aria-live="assertive"></div>
</ul>

</body>
<script src="reproductor.js"></script>
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

class AddonThread(Thread):
	def __init__(self, frame):
		super(AddonThread, self).__init__(frame)
		self.frame = frame
		self.daemon = True

	def run(self):
		def chkActualizacion():
			url = "https://api.github.com/repos/ytdl-org/youtube-dl/releases"
			req = urllib.request.Request(url)
			r = urllib.request.urlopen(req).read()
			gitJson = json.loads(r.decode('utf-8'))
			if gitJson[0]["tag_name"] > youtube_dl.version.__version__:
				urlDescarga = gitJson[0]['zipball_url']
				xguiMsg = _('Existe una nueva versión de la librería youtube_dl. ¿Quieres actualizarla?')
				msg = wx.MessageDialog(None, xguiMsg, self.frame.attention, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
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

		super(DescargaDialogo, self).__init__(None, -1, title=_('Actualizando la librería...'), size = (WIDTH, HEIGHT))

		self.CenterOnScreen()

		self.url = url

		self.Panel = wx.Panel(self)

		self.progressBar=wx.Gauge(self.Panel, wx.ID_ANY, range=100, style = wx.GA_HORIZONTAL)

		self.textorefresco = wx.TextCtrl(self.Panel, wx.ID_ANY, style =wx.TE_MULTILINE|wx.TE_READONLY)
		self.textorefresco.Bind(wx.EVT_CONTEXT_MENU, self.skip)

		self.aceptarBTN = wx.Button(self.Panel, 1, _('&Aceptar'))
		self.Bind(wx.EVT_BUTTON, self.onAceptar, id=self.aceptarBTN.GetId())
		self.aceptarBTN.Disable()

		self.cerrarBTN = wx.Button(self.Panel, 2, _('&Cerrar'))
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
			wx.CallAfter(self.frame.TextoRefresco, _('Espere por favor...\n') + _('Descargando: %s') % self.humanbytes(readsofar))

	def run(self):
		try:
			socket.setdefaulttimeout(30) # Error si pasan 30 segundos sin internet
			try:
				req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
				obj = urllib.request.urlopen(req).geturl()
				urllib.request.urlretrieve(self.url, os.path.join(dirAddon, "temp.zip"), reporthook=self.__call__)
			except Exception as e:
				urllib.request.urlretrieve(self.url, os.path.join(dirAddon, "temp.zip"), reporthook=self.__call__)

			msg = _('Descarga finalizada. Cierre la ventana para terminar de instalar la librería y reiniciar NVDA.')
			wx.CallAfter(self.frame.done, msg)
		except Exception as e:
			wx.CallAfter(self.frame.error, _('Algo salió mal.\n') + _('Compruebe si tiene conexión a internet y vuelva a intentarlo.\n') + _('Ya puede cerrar esta ventana.'))

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
		wx.StaticText(self.Panel, wx.ID_ANY, _('Ingresa el nombre del canal'))
		self.channelName = wx.TextCtrl(self.Panel,wx.ID_ANY)
		wx.StaticText(self.Panel, wx.ID_ANY, _('Ingresa la URL del canal'))
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
			ui.message(_('Debes ingresar algún nombre para este canal'))
			self.channelName.SetFocus()
			return
		channel_url = self.getChannelUrl(self.channelLink.GetValue())
		if not channel_url:
			ui.message(_('La url ingresada no es válida'))
			self.channelLink.SetValue("")
			self.channelLink.SetFocus()
			return
		channel_id = "".join([chard for chard in channel_name if re.search(r"[a-zA-Z0-9]", chard)])
		if channel_url[-7:] != "/videos":
			channel_url = f"{channel_url}/videos"
		Thread(target=self.getVideos, args=(channel_name, channel_url, channel_id), daemon= True).start()
		self.Close()

	def getChannelUrl(self, url):
		if not re.search(r'https?...(www.)?youtube.com.', url): return None
		if re.search(r'https?...(www.)?youtube.com.channel.', url): return url
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
		ui.message(_('Proceso Finalizado'))

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
		wx.StaticText(self.Panel, wx.ID_ANY, _('Ingresa el término de búsqueda y pulsa intro'))
		self.searchText = wx.TextCtrl(self.Panel,wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
		self.searchBTN = wx.Button(self.Panel, wx.ID_ANY, _('&Iniciar la búsqueda'))
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, _('&Cancelar'))
		self.searchText.Bind(wx.EVT_CONTEXT_MENU, self.onPass)
		self.searchText.Bind(wx.EVT_TEXT_ENTER, self.startSearch)
		self.searchBTN.Bind(wx.EVT_BUTTON, self.startSearch)
		self.Bind(wx.EVT_ACTIVATE, self.onSalir)
		self.Bind(wx.EVT_BUTTON, self.onSalir, id=wx.ID_CANCEL)

	def onPass(self, event):
		pass

	def startSearch(self, evt):
		text = self.searchText.GetValue()
		self.cursor.execute(f'select * from videos where title like "%{text}%" order by {self.frame.order[self.frame.order_by]}')
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
			self.frame.speak(_(f'Se han encontrado {len(results)} resultados'), 0.2)
		else:
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "nResults.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			self.frame.speak(_('No se han encontrado resultados'), 0.2)
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
		wx.StaticText(self.Panel, wx.ID_ANY, _('Nombre del canal'))
		self.channelName = wx.TextCtrl(self.Panel,wx.ID_ANY)
		self.channelName.SetValue(self.frame.channels[self.frame.y][0])
		self.checkbox = wx.CheckBox(self.Panel, wx.ID_ANY, _('Canal favorito'))
		self.checkbox.SetValue(self.frame.channels[self.frame.y][3])
		self.saveBTN = wx.Button(self.Panel, wx.ID_ANY, self.frame.saveChanges)
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, self.frame.discard)
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
			self.frame.speak(_('Configuración guardada'), 1)
		self.frame.activar(False)
		try:
			if self.frame.startTimer.is_running:
				self.frame.startTimer.stop()
		except:
			pass

class GlobalSettings(wx.Dialog):
	def __init__(self, parent, titulo, frame, connect, cursor):
		super(GlobalSettings, self).__init__(parent, -1, title=titulo)
		self.frame = frame
		self.connect = connect
		self.cursor = cursor
		self.Panel = wx.Panel(self)
		self.checkbox = wx.CheckBox(self.Panel, wx.ID_ANY, _('Activar los sonidos del complemento'))
		self.checkbox.SetValue(self.frame.sounds)
		self.listbox = wx.RadioBox(self.Panel, wx.ID_ANY, _('Selecciona el intervalo de tiempo para la verificación de nuevas subidas en los canales favoritos'), choices=[_('Desactivado'), _('24 horas'), _('12 horas'), _('8 horas'), _('4 horas'), _('2 horas'), _('1 hora')])
		self.listbox.SetSelection(self.frame.update_time)
		self.radio = wx.RadioBox(self.Panel, wx.ID_ANY, _('Seleccione el órden de aparición de los videos del canal'), choices=[_('Del último al primero'), _('Del primero al último'), _('Del más visto al menos visto'), _('Del menos visto al mas visto')])
		self.radio.SetSelection(self.frame.order_by)
		self.saveBTN = wx.Button(self.Panel, wx.ID_ANY, self.frame.saveChanges)
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, self.frame.discard)
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
		order_by = self.radio.GetSelection()
		if self.frame.sounds != sounds or self.frame.update_time != update_time or self.frame.order_by != order_by:
			self.cursor.execute(f'update settings set sounds = {sounds}, update_time = {update_time}, order_by = {order_by}')
			self.connect.commit()
			self.connect.close()
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "finish.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			if self.frame.update_time != update_time:
				modal = wx.MessageDialog(None, _(f'Es necesario reiniciar NVDA para aplicar los cambios. ¿Quieres reiniciar ahora?'), attention, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				if modal.ShowModal() == wx.ID_YES:
					core.restart()
				else:
					modal.Destroy()
			else:
				self.frame.startDB()
				self.frame.speak(_('Configuraciones aplicadas'), 1)

class StartTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer = None
		self.interval = interval
		self.function   = function
		self.args = args
		self.kwargs = kwargs
		self.is_running = False
		self.daemon = True
		self.start()

	def _run(self):
		self.is_running = False
		self.start()
		self.function(*self.args, **self.kwargs)

	def start(self):
		if not self.is_running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.is_running = True

	def stop(self):
		self._timer.cancel()
		self.is_running = False

class MyLogger(object):
	def debug(self, msg):
		pass
	def warning(self, msg):
		pass
	def error(self, msg):
		pass

class GlobalSearch(wx.Dialog):
	def __init__(self, parent, title, frame):
		super(GlobalSearch, self).__init__(parent, -1, title= title)
		self.YDL_OPTIONS = {
			'format': 'bestaudio',
			'extract_flat': 'in_playlist',
			'dump_single_json': True,
			'noplaylist':'True',
			'logger': MyLogger()
		}
		self.frame = frame
		self.Panel = wx.Panel(self)
		wx.StaticText(self.Panel, wx.ID_ANY, _('Ingresa los términos de búsqueda'))
		self.textSearch = wx.TextCtrl(self.Panel,wx.ID_ANY)
		self.radiobox = wx.RadioBox(self.Panel, wx.ID_ANY, _('Selecciona el número de resultados  a mostrarse'), choices=[_('10 resultados'), _('20 resultados'), _('30 resultados'), _('40 resultados'), _('50 resultados')])
		self.radiobox.SetSelection(2)
		self.searchBTN = wx.Button(self.Panel, wx.ID_ANY, _('Iniciar la búsqueda'))
		self.cerrarBTN = wx.Button(self.Panel, wx.ID_CANCEL, _('Cancelar'))
		self.searchBTN.Bind(wx.EVT_BUTTON, self.search)
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

	def search(self, evt):
		str = self.textSearch.GetValue()
		if len(str) > 0:
			if self.frame.sounds: winsound.PlaySound("C:\\Windows\\Media\\Alarm05.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
			self.Close()
			Thread(target=self.startSearch, args=(str,), daemon= True).start()
		else:
			ui.message("Debes ingresar algún texto de búsqueda")
			self.textSearch.SetFocus()

	def startSearch(self, str):
		count = (self.radiobox.GetSelection() + 1) * 10
		with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
			try:
				results = ydl.extract_info(f'ytsearch{count}:{str}', download= False)
			except:
				if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "yResults.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
				ui.message(_('No se han encontrado resultados'))
				return
		if not len(results['entries']):
			if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "yResults.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
			ui.message(_('No se han encontrado resultados'))
			return
		self.frame.channels_temp = self.frame.channels
		self.frame.videos_temp = self.frame.videos
		self.frame.index_temp = self.frame.index
		self.frame.channels = [("Resultados globales", None)]
		self.frame.index = [0]
		self.frame.videos = []
		videos = []
		for video in results['entries']:
			videos.append((video['title'], f"https://www.youtube.com/watch?v={video['url']}", video['id'], "Resultados globales", video['view_count'], "Resultados"))
		self.frame.videos = [videos]
		if self.frame.sounds: winsound.PlaySound(os.path.join(dirAddon, "sounds", "finish.wav"), winsound.SND_FILENAME | winsound.SND_ASYNC)
		self.frame.activar(False)
		