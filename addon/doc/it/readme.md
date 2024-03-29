# Youtube Channel Manager
[Gerardo Kessler](http://gera.ar)

Questa estensione ti permette di gestire i tuoi canali preferiti sulla piattaforma YouTube con scorciatoie da tastiera e con un'interfaccia invisibile e semplice.

## Scorciatoie dell'estensione

* Attivare l'interfaccia invisibile; Non assegnato

## Scorciatoie disponibili nell'interfaccia invisibile

* Escape; Chiude l'interfaccia virtuale e riporta le scorciatoie alla loro funzione predefinita.
* Freccia destra; Passa al canale successivo.
* Freccia sinistra; Passa al canale precedente.
* Freccia in giù; Passa al video successivo nel canale con il focus.
* Freccia su; Passa al video precedente nel canale con il focus.
* inizio; Passa al primo video del canale con il focus.
* fine; Vocalizza la posizione, il nome del canale e il numero di visualizzazioni del video.
* n; Apre la finestra di dialogo per aggiungere un nuovo canale.
* o; Apre il link del video nel browser predefinito.
* r; Apre il link audio in un web player personalizzato.
* ctrl + c; Apri il collegamento dagli appunti nel web player personalizzato.
* c; Copia il link del video negli appunti.
* t; Copia il titolo del video negli appunti.
* d; Ottiene i dati del video e li visualizza in una finestra di NVDA.
* ctrl + d; scarica il video nel formato originale nella cartella YoutubebDL dell'utente corrente
* ctrl + shift + d; Scarica dagli appunti nel formato originale nella cartella YoutubedDL dell'utente corrente
* b; Attiva la finestra di ricerca nel database.
* CTRL + b; Attiva la finestra di ricerca generale.
* f5; Controlla se ci sono nuovi video nel canale col focus.
* s; Attiva la finestra di configurazione del canale col focus.
* g; Attiva la finestra delle opzioni globali.
* Canc; Elimina il canale con il focus e, nella finestra dei risultati, elimina la colonna e torna all'elenco dei canali.
* Ctrl + Shift + Canc; Elimina il database.
* f1; Attiva la guida dei comandi.

### Aggiungere canali

 Per aggiungere un nuovo canale al database, devi solo aprire l'interfaccia virtuale con la scorciatoia assegnata per quell'azione, di solito NVDA + y E premere la lettera n.
La finestra richiede 2 campi. Un nome di canale e l'URL del canale stesso. In quest'ultimo caso, l'estensione permette di inserire i seguenti formati di URL:

* Link di un video, che di solito ha il seguente formato:

    https://www.youtube.com/watch?v=IdDelVideo

* Link di un canale

    https://www.youtube.com/channel/IdDelCanale

Quindi un modo per ottenere ciò è aprire un video sulla pagina di YouTube tramite il browser, premere alt e la lettera d per aprire la barra degli indirizzi e copiare l'URL, che sarà già selezionato di default, con CTRL + c.
I canali possono anche essere aggiunti dall'elenco dei risultati globali. Per fare ciò, non devi fare altro che cercare, andare al video del canale da aggiungere e premere il tasto n.
Questo attiverà la finestra di dialogo per l'inserimento dei dati del canale, che verranno automaticamente compilati con il link e il nome presi da Youtube.

### Aggiornatore automatico:

L'estensione consente di contrassegnare i canali come preferiti e di attivare il controllo delle novità con un intervallo di tempo stabilito. 
Per contrassegnare o meno un canale come preferito:

* Attivare l'interfaccia virtuale con la scorciatoia assegnata, di solito NVDA + y.
* Selezionare il canale desiderato con le frecce sinistra o destra.
* Attivare la finestra di configurazione del canale con la lettera s.
* Spuntare la casella corrispondente e cliccare sul pulsante per salvare la configurazione.

La verifica delle novità sui canali preferiti è disattivata per impostazione predefinita. Per modificarla, attenersi alla seguente procedura:

* Attivare l'interfaccia virtuale con la scorciatoia assegnata, di solito NVDA + y.
* Attivare la finestra di configurazione globale con la lettera g.
* Tab per andare all'elenco delle opzioni e selezionare con le frecce su e giù l'intervallo desiderato.
* Premere sul pulsante per salvare le impostazioni.

Quando si trovano novità, l'estensione emette un suono durante l'aggiornamento e un messaggio al termine.

### Cercare i video nel database:

L'estensione permette di effettuare ricerche per parole chiave tra i video dei canali inseriti nel database.

* Attivare l'interfaccia virtuale con la scorciatoia assegnata, di solito NVDA + y.
* Attivare la finestra di ricerca con la lettera b.
* Scrivere una parola o una frase di riferimento.
* Premere Invio o il pulsante Inizia la ricerca.

Se non vengono trovati risultati, viene notificato un messaggio e l'interfaccia virtuale non viene modificata.
In caso di ricerca di video che corrispondono ai dati inseriti, viene notificato un messaggio e viene attivata l'interfaccia dei risultati.
Per navigare al suo interno, possiamo farlo con le frecce su e giù. Sono disponibili gli stessi comandi dell'interfaccia del canale; r per il web player personalizzato, o per aprire nel browser, ecc.
Per tornare all'interfaccia dei canali, premi il tasto Canc nell'interfaccia dei risultati, che rimuoverà quella colonna e restituirà l'elenco dei canali e dei video.

### Ricerca globale:

Per eseguire una ricerca globale al di fuori del database, procedere come segue:

* Attivare l'interfaccia virtuale con la scorciatoia assegnata, di solito NVDA + y.
* Attivare la finestra di ricerca con la scorciatoia CTRL + b.
* Scrivere una parola o una frase di riferimento e selezionare il numero di risultati da visualizzare.
* Premere il pulsante Inizia ricerca.

Se non vengono trovati risultati, viene notificato un messaggio.
Quando i risultati vengono trovati, vengono aggiunti all'elenco principale, che possiamo scorrere con le frecce su e giù.
Anche qui abbiamo le stesse scorciatoie della ricerca nel database. O per aprire nel browser, r per il web player, c per copiare il collegamento, ecc.
Se uno qualsiasi dei video si trova in un canale che vuoi aggiungere al database, premendo la lettera n in questo elenco si attiverà la finestra di dialogo del nuovo canale con i campi nome e URL già riempiti. Se preferisci, questi campi possono essere modificati. 
Come nelle ricerche nel database, per tornare all'elenco dei canali è sufficiente premere Canc per eliminare i risultati e tornare all'interfaccia dei canali.

### Cronologia delle ricerche

L'estensione salva il testo delle ultime 20 ricerche globali nel database.
Per accedere alla cronologia, è sufficiente premere il tasto Applicazioni nella casella di modifica della ricerca globale. Premendolo si attiva un menu contestuale con le ultime ricerche e, premendo invio su una di esse, il riquadro si completa con il testo corrispondente.

## Scaricare i video
Questa estensione non ha lo scopo di convertire i video, tuttavia è stata aggiunta la possibilità di scaricare il video nel formato originale.
Per fare ciò, devi solo cercare nell'interfaccia invisibile il video da scaricare e premere la scorciatoia ctrl + d. Il file verrà scaricato nella cartella youtubeDL dell'utente corrente.

## Traduttori:

* Remy Ruiz (francese)
* Ângelo Miguel Abrantes (portoghese)
* Umut KORKMAZ (turco)
* wafiqtaher (arabo)
* Franco La Rosa (italiano)
