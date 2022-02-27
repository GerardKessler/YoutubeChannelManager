var audio_obj = document.getElementById("reproductor");
var toggle_btn = document.getElementById("toggle");
var time_obj = document.getElementById("time");
var alert_obj = document.getElementById("alert");
var audio_volume = 1;

audio_obj.addEventListener("ended", function() {
	toggle_btn.innerHTML = "Volver a reproducir";
	speak("Finalizado");
	toggle_btn.focus()}
);

function playPause() {
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

function audioTime() {
	let minutos = parseInt(audio_obj.duration / 60, 10);
	var segundos = parseInt(audio_obj.duration % 60);
	var segundos = (segundos < 10)? `0${segundos}` : segundos;
	let ACT_minutos = parseInt(audio_obj.currentTime / 60, 10);
	var ACT_segundos = parseInt(audio_obj.currentTime % 60);
	var ACT_segundos = (ACT_segundos < 10)? `0${ACT_segundos}` : ACT_segundos;
	time_obj.innerHTML = `${ACT_minutos}:${ACT_segundos} de ${minutos}:${segundos}`;
}

function timeAdvance() {
	audio_obj.currentTime += 10.0;
	let time_capture = time_obj.textContent;
	//speak(time_capture);
}

function timeBack() {
	audio_obj.currentTime -= 10;
	let time_capture = time_obj.textContent;
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
