# Architettura Pub/Sub per Trascrizione Vocale

## Panoramica
Questo progetto implementa un sistema di trascrizione vocale in tempo reale usando l'architettura **Publisher-Subscriber (Pub/Sub)** con **MQTT**.  
Il Publisher trascrive l’audio in testo e lo invia a uno o più Subscriber tramite un broker MQTT.

## Componenti

### Publisher
- Ascolta il microfono e rileva la parola di attivazione (`start`).  
- Trascrive il parlato in tempo reale con `speech_recognition`.  
- Pubblica ogni trascrizione sul topic `voice/transcription`.  
- Termina la trascrizione alla parola di stop (`stop`).  

### Subscriber
- Si sottoscrive al topic `voice/transcription`.  
- Riceve e mostra le trascrizioni in tempo reale.  
- Gestione basata su callback per connessione e ricezione dei messaggi.

## Architettura
- **Publisher** invia messaggi senza conoscere i destinatari.  
- **Broker MQTT** media i messaggi tra publisher e subscriber.  
- **Subscriber** riceve solo i messaggi dei topic sottoscritti.  

## Tecnologie
- `speech_recognition` per trascrizione vocale  
- `paho-mqtt` per gestione MQTT  
- Broker pubblico `broker.hivemq.com`  

## Flusso Principale
1. Publisher ascolta continuamente l’audio.  
2. Alla parola `start`, inizia a trascrivere e pubblicare.  
3. Subscriber riceve e mostra i messaggi.  
4. Alla parola `stop`, il Publisher termina la sessione.  

## Vantaggi
- Modularità: publisher e subscriber indipendenti.  
- Scalabilità: più subscriber possono ricevere simultaneamente.  
- Flessibilità: facile aggiungere nuovi comandi o integrazioni.
