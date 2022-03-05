# -*- coding: utf-8 -*-
# Copyright (C) 2021 Gerardo Kessler <ReaperYOtrasYerbas@gmail.com>
# This file is covered by the GNU General Public License.

import webbrowser
import os
import addonHandler

# Lína de traducción
addonHandler.initTranslation()

class PlayerCode():
	def __init__(self, title, url):
		super(PlayerCode, self).__init__()
		self.title = title
		self.url = url
		self.strings = (
			self.title, self.url,
			# Translators: Cadenas del documento html. Título, botones y mensajes
			_('Reproducir'),
			_('Retroceder'),
			_('Avanzar'),
			_('Velocidad de reproducción'),
			_('Bajar volúmen'),
			_('Silenciar'),
			_('Subir volúmen'),
			_('Volver a reproducir'),
			_('Finalizado'),
			_('Pausar'),
			_('Reproducir'),
			_('Volúmen mínimo'),
			_('Silenciado'),
			_('No silenciado'),
			_('volúmen máximo')
		)

	def createFile(self):
		html_code = '''<!doctype html>
<head>
<meta charset="UTF-8">
<title>%s</title>
</head>
<body>
<audio onTimeUpdate='audioTime();' src="%s" id="reproductor" preload="auto">
</audio>
<ul style="list-style:none;margin-left:auto;margin-right:auto;">
<li><button accesskey="k" id="toggle" onClick='playPause();'>%s</button></li>
<li><button accesskey="j" id="back" onClick='timeBack();'>%s</button></li>
<li><button accesskey="i" id="time" onClick="speak(this.textContent);">0:00</button></li>
<li><button accesskey="l" id="advance" onClick="timeAdvance();">%s</button></li>
<li><label>%s<input type="range" min="0" max="100" step="10" value="50" onChange="audioRate(this.value)" /></label></li>
<li><button accesskey="o" onClick="volumeDown();">%s</button></li>
<li><button accesskey="m" onClick="toggleMute();">%s</button></li>
<li><button accesskey="u" onClick="volumeUp();">%s</button></li>
<div id="alert" aria-live="assertive"></div>
</ul>
</body>
<script>
var audio_obj = document.getElementById("reproductor");
var toggle_btn = document.getElementById("toggle");
var time_obj = document.getElementById("time");
var alert_obj = document.getElementById("alert");
var audio_volume = 1;

audio_obj.addEventListener("ended", function() {
	toggle_btn.innerHTML = "%s";
	speak("%s");
	toggle_btn.focus()}
);

function playPause() {
	(audio_obj.paused)? play() : pause()
}

function play() {
	audio_obj.play();
	toggle_btn.innerHTML = "%s";
}

function pause() {
	audio_obj.pause();
	toggle_btn.innerHTML = "%s";
}

function timeBack() {
	audio_obj.currentTime -= 10;
	let time_capture = time_obj.textContent;
}

function audioTime() {
	var duration = audio_obj.duration;
	currentTime = audio_obj.currentTime;
	var minutos = parseInt(duration / 60, 10);
	var segundos = parseInt(duration - (parseInt(duration/60)*60));
	var segundos = (segundos < 10)? `0${segundos}` : segundos;
	var ACT_minutos = parseInt(currentTime / 60, 10);
	var ACT_segundos = parseInt(currentTime - (parseInt(currentTime/60)*60));
	var ACT_segundos = (ACT_segundos < 10)? `0${ACT_segundos}` : ACT_segundos;
	time_obj.innerHTML = `${ACT_minutos}:${ACT_segundos} de ${minutos}:${segundos}`;
}

function timeAdvance() {
	audio_obj.currentTime += 10.0;
	let time_capture = time_obj.textContent;
}

function speak(str) {
	alert_obj.textContent = str;
	setTimeout(() => alert_obj.textContent = "", 50);
}

function audioRate(value) {
	let values = {"0":0.75, "10":0.80, "20":0.85, "30":0.90, "40":0.95, "50":1.0, "60":1.1, "70":1.2, "80":1.3, "90":1.4, "100":1.5};
	audio_obj.playbackRate = values[value];
}

function volumeDown() {
	if (audio_volume > 0.2) {
		audio_volume -= 0.1;
		audio_obj.volume = audio_volume;
	} else {
		speak("%s");
	}
}

function toggleMute() {
	if (audio_obj.muted == false) {
		audio_obj.muted = true;
		speak("%s");
	} else {
		audio_obj.muted = false;
		speak("%s");
	}
}

function volumeUp() {
	if (audio_volume < 1.0) {
		audio_volume += 0.1;
		audio_obj.volume = audio_volume;
	} else {
		speak("%s");
	}
}
</script>
</html>
		''' % self.strings
		with open(os.path.join(os.getenv('TEMP'), "index.html"), "w", encoding="utf-8") as file:
			file.write(html_code)
			webbrowser.open(f"file://{os.getenv('TEMP')}/index.html", new=2)
