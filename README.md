# PPM_E-Commerce_progetto — Progetto Full Stack

**Studente:** Lapi Stefano  
**Tipo Progetto:** Full Stack Web Application  
**Framework:** Django  
**Traccia:** 1 — E-commerce Store



## Descrizione

Il progetto consiste in una applicazione e-commerce completa sviluppata con Django.  
Il sistema permette ai clienti di sfogliare un catalogo di prodotti, gestire un  
carrello ed effettuare degli ordini scegliendo tra i propri indirizzi di spedizione.  
Il gestore del negozio può gestire i prodotti, le categorie e gli ordini tramite  
una dashboard dedicata.


## Funzionalità per ruolo

### Cliente
- Registrazione e login
- Sfogliare il catalogo con ricerca e filtri (categoria e prezzo)
- Visualizzare i dettagli di ogni prodotto
- Aggiungere dei prodotti al carrello
- Gestire i propri indirizzi di spedizione (aggiungi, modifica, elimina)
- Effettuare il checkout scegliendo un indirizzo salvato
- Visualizzare lo storico dei propri ordini
- Aggiornare il proprio profilo

### Gestore Negozio
- Ha le stesse funzionalità del cliente
- Dashboard con dati generali sull'applicazione (prodotti totali, categorie, prodotti esauriti)
- Possibilità di creare, modificare ed eliminare i prodotti
- Possibilità di creare, modificare ed eliminare le categorie
- Possibilità di vedere tutti gli ordini dei clienti
- Può aggiornare lo stato degli ordini 


## Struttura del progetto
- `negozio/`: Contiene la configurazione principale del progetto
- `accounts/`: Gestisce gli utenti, i ruoli di questi e gli indirizzi di spedizione
- `accounts/models.py`: Contiene le classi del CustomUser e dell'Address
- `accounts/views.py`: Definizione del login, della registrazione, del profilo e degli indirizzi
- `accounts/form.py`: Form di registrazione e gestione degli indirizzi
- `catalogo/`: Gestisce i prodotti e le categorie (creazione, modifica, eliminazione e visualizzazione)
- `catalogo/models.py`: Contiene le classi Category e Product
- `catalogo/views.py`: Definizione della lista di prodotti e il CRUD dei prodotti e delle categorie, con la loro definizione
- `ordini/`: Gestisce il carrello (inserimento di prodotti e calcolo del prezzo, con controllo sulla quantità dello stock) e gli ordini (creazione, cancellazione, modifica e controllo dello stato)
- `ordini/carrello.py`: Gestisce la logica del carrello
- `ordini/models.py`: Contiene le classi Order e OrderItem
- `ordini/views.py`: Definisce il checkout e lo storico degli ordini
- `static/`: Contiene i file CSS usati per bootstrap e per modifica del layout fatta tramite il file style.css
- `templates/`: Contiene i templates HTML per rappresentare le pagine del sito
- `db.sqlite3`: Database SQLite che popolato con dati demo, quali categorie, prodotti, ordini e utenti con gli indirizzi associati
- `requirements.txt`: Elenco delle dipendenze Python necessarie per eseguire il progetto


## Installazione locale

Apri il terminale e inserisci quanto segue:
### 1) Clonare il repository
```bash
git clone https://github.com/SteLaps/PPM_E-Commerce_progetto.git  
cd PPM_E-Commerce_progetto
```

### 2) Crea e attiva l'ambiente virtuale
```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux  
venv\Scripts\activate       # Windows
```

### 3) Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 4) Applica le migrazioni
```bash
python manage.py migrate
```

### 5) Avvia il server
```bash
python manage.py runserver
```

Quando ti verrà fornito, apri il browser su **http://127.0.0.1:8000/**


## Database demo

Il file 'db.sqlite3' è incluso nel repository e contiene i dati già pronti:
- 3 utenti demo (l'admin, il gestore del negozio e un cliente)
- 5 categorie di prodotti
- 15 prodotti con prezzi e disponibilità nel magazzino
- 3 ordini demo da parte dell'utente in stati diversi (Consegnato, Spedito e In Attesa)
- Indirizzi di spedizione per il cliente


## Account demo

Username | Password | Ruolo

'admin_demo' | 'admin12345' | Superuser  
'manager_demo' | 'manager12345' | Gestore Negozio  
'user_demo' | 'user12345' | Cliente


## Scenario di test (se si vuole seguire, opzionale)
### Test ruolo Cliente
1) Accedi con 'user_demo' / 'user12345'
2) Sfoglia il catalogo (si possono usare i filtri per categoria o prezzo)
3) Entra nel dettaglio di un prodotto e aggiungilo poi al carrello (seleziona la quantità)
4) Vai al carrello
5) Procedi al checkout (scegli l'indirizzo e conferma l'ordine)
6) Prova ad accedere a '/catalogo/manager/' (essendo un cliente, dovrebbe dare messaggio di errore)

### Test ruolo Gestore Negozio
1) Accedi con 'manager_demo' / 'manager12345'
2) Entra nella **Dashboard Manager** dalla navbar
3) Crea un nuovo prodotto con categoria, prezzo e quantità in magazzino (la descrizione è opzionale)
4) Modifica il prezzo, la categoria o la quantità di un prodotto già presente nel catalogo
5) Entra in "Gestione ordini" e prova ad aggiornare lo stato di un ordine
6) Elimina un prodotto o una categoria


## Link di deployment

https://stefanolapi04.eu.pythonanywhere.com