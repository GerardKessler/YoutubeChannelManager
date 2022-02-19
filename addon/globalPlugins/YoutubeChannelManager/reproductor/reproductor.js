// Reproductor de audio simple y accesible para lectores de pantalla
// Autor: Gerardo Késsler (http://gera.ar)
// This file is covered by the GNU General Public License.

// variables
var audio_id, audio_obj, audio_volume = 1.0, toggle_btn, back_btn, time_p, advance_btn, alert_obj, volume_up, volume_down;

//ejecutamos las instrucciones al terminar de cargarse el documento
document.addEventListener("DOMContentLoaded", function () {
	// creamos un array con todos los elementos  audio
	var elements = document.querySelectorAll("audio");
	// recorremos el array para crear las asignaciones por elemento
	for (element of elements) {
		//guardamos en la variable id, el id de cada eqtiqueta audio
		let id = element.id;
		//añadimos al elemento audio el evento onTimeUpdate.
		element.setAttribute("onTimeUpdate", `audioTime("${id}");`);
		//añadimos la lista con botones de control luego del elemento audio. Primero creamos un nodo nuevo, le añadimos la lista de controles html y finalmente lo añadimos seguidamente al elemento audio con la función insertAfter.
		let new_element = document.createElement("div");
		new_element.innerHTML = `<ul style="list-style:none;margin-left:auto;margin-right:auto;">
			<li><button accesskey="k" id="${id}_toggle" onClick='playPause("${id}");'>reproducir</button></li>
			<li><button accesskey="j" id="${id}_back" onClick='timeBack();'>Retroceder 10 segundos</button></li>
			<li><p accesskey="i" id="${id}_time" onClick='speak(this.textContent);'>0:00</p></li>
			<li><button accesskey="l" id="${id}_advance" onClick='timeAdvance();'>Adelantar 10 segundos</button></li>
			<li><label>Velocidad de reproducción><input type="range" min="0" max="100" step="10" value="50" onChange='audioRate(this.value)' /></label></li>
			<li><button accesskey="o" id="${id}_down" onClick='volumeDown();'>Bajar volúmen</button></li>
			<li><button accesskey="m" id="${id}_toggle_mute" onClick='toggleMute();'>Silenciar, Quitar silencio</button></li>
			<li><button accesskey="u" id="${id}_up" onClick='volumeUp();'>Subir volúmen</button></li>
			<div id="${id}_alert" aria-live="assertive"></div>
		</ul>`;
	insertAfter(element, new_element);
	}
});

function insertAfter(element, new_element) {
	if (element.nextSibling) {
		element.parentNode.insertBefore(new_element, element.nextSibling);
	} else {
		element.parentNode.appendChild(new_element);
	}
}

// función que asigna las variables globales los elementos a través de su id
function getElements(id) {
	audio_id = id;
	audio_obj = document.querySelector(`#${id}`);
	toggle_btn = document.querySelector(`#${id}_toggle`);
	back_btn = document.querySelector(`#${id}_back`);
	time_p = document.querySelector(`#${id}_time`);
	advance_btn = document.querySelector(`#${id}_advance`);
	alert_obj = document.querySelector(`#${id}_alert`);
	volume_up = document.querySelector(`#${id}_up`);
	toggle_mute = document.querySelector(`#${id}_toggle_mute`);
	volume_down = document.querySelector(`#${id}_down`);
}

function addHotkeys(id) {
	audio_obj.addEventListener("ended", function() {
		toggle_btn.innerHTML = "Volver a reproducir";
		speak("Finalizado");
		toggle_btn.focus()}
	);
}

function playPause(id) {
	if (id != audio_id) {
		getElements(id);
		addHotkeys(id);
	}
	(audio_obj.paused)? play() : pause()
}

function play() {
	audio_obj.play();
	toggle_btn.innerHTML = "Pausar";
}

function pause() {
	audio_obj.pause();
	toggle_btn.innerHTML = "Reproducir";
}

function audioTime(id) {
	let minutos = parseInt(audio_obj.duration / 60, 10);
	var segundos = parseInt(audio_obj.duration % 60);
	var segundos = (segundos < 10)? `0${segundos}` : segundos;
	let ACT_minutos = parseInt(audio_obj.currentTime / 60, 10);
	var ACT_segundos = parseInt(audio_obj.currentTime % 60);
	var ACT_segundos = (ACT_segundos < 10)? `0${ACT_segundos}` : ACT_segundos;
	time_p.innerHTML = `${ACT_minutos}:${ACT_segundos} de ${minutos}:${segundos}`;
}

function timeAdvance() {
	audio_obj.currentTime += 10.0;
	let time_capture = time_p.textContent;
	//speak(time_capture);
}

function timeBack() {
	audio_obj.currentTime -= 10;
	let time_capture = time_p.textContent;
	//speak(time_capture);
}

function speak(str) {
	alert_obj.textContent = str;
	setTimeout(() => alert_obj.textContent = "", 50);
}

function audioRate(value) {
	let values = {"0":0.75, "10":0.80, "20":0.85, "30":0.90, "40":0.95, "50":1.0, "60":1.1, "70":1.2, "80":1.3, "90":1.4, "100":1.5};
	audio_obj.playbackRate = values[value];
}

function volumeUp() {
	if (audio_volume < 1.0) {
		audio_volume += 0.1;
		audio_obj.volume = audio_volume;
	} else {
		speak("volúmen máximo");
	}
}

function volumeDown() {
	if (audio_volume > 0.2) {
		audio_volume -= 0.1;
		audio_obj.volume = audio_volume;
	} else {
		speak("Volúmen mínimo");
	}
}

function toggleMute() {
	if (audio_obj.muted == false) {
		audio_obj.muted = true;
		speak("silenciado");
	} else {
		audio_obj.muted = false;
		speak("no silenciado");
	}
}

function hotkeys(id, text) {
	if (text == "Mostrar los atajos del reproductor") {
		document.getElementById(`${id}_hksbtn`).textContent = "Ocultar los atajos del reproductor";
		document.getElementById(`${id}_hks`).removeAttribute("style");
	} else {
			document.getElementById(`${id}_hksbtn`).textContent = "Mostrar los atajos del reproductor";
			document.getElementById(`${id}_hks`).setAttribute("style", "display:none");
	}
}