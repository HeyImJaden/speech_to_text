import speech_recognition as sr
import paho.mqtt.client as mqtt
import time

# -- Configuration (deve essere identica per publisher e subscriber) --
TRIGGER_WORD = "start"
STOP_WORD = "stop"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "voice/transcription"

# -- Funzioni MQTT --
def on_connect(client, userdata, flags, rc):
    """Callback per la connessione al broker MQTT."""
    if rc == 0:
        print("Publisher connesso al Broker MQTT!")
    else:
        print(f"Connessione fallita, return code {rc}\n")

def setup_mqtt():
    """Imposta e restituisce un client MQTT."""
    client = mqtt.Client(client_id="voice_publisher")
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    return client

# -- Logica di Speech-to-Text --
def listen_and_publish(mqtt_client):
    """
    Ascolta continuamente, rileva trigger/stop word e pubblica la trascrizione.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Inizializzazione del microfono...")
    with microphone as source:
        # Calibrazione iniziale sul rumore di fondo
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True: # Loop principale per ascoltare sempre
            print("\nIn ascolto per la parola di attivazione ('start')...")
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="it-IT").lower()
                print(f"Rilevato: '{text}'")

                # -- Rilevamento Parola di Attivazione --
                if TRIGGER_WORD in text:
                    print("Parola di attivazione rilevata! Avvio trascrizione...")
                    mqtt_client.publish(MQTT_TOPIC, "--- INIZIO TRASCRIZIONE ---")

                    # -- Loop di Trascrizione --
                    while True:
                        try:
                            print("Parla ora...")
                            audio_to_transcribe = recognizer.listen(source)
                            transcribed_text = recognizer.recognize_google(audio_to_transcribe, language="it-IT")
                            print(f"Trascritto: '{transcribed_text}'")

                            # Pubblica il testo trascritto sul topic MQTT
                            mqtt_client.publish(MQTT_TOPIC, transcribed_text)

                            # -- Rilevamento Parola di Stop --
                            if STOP_WORD in transcribed_text.lower():
                                print("Parola di stop rilevata. Interrompo la trascrizione.")
                                mqtt_client.publish(MQTT_TOPIC, "--- FINE TRASCRIZIONE ---")
                                break  # Esce dal loop di trascrizione e torna ad ascoltare il trigger

                        except sr.UnknownValueError:
                            print("Audio non comprensibile, riprova.")
                        except sr.RequestError as e:
                            print(f"Errore API Google: {e}")
                            break # In caso di errore di rete, esce dal loop di trascrizione

            except sr.UnknownValueError:
                # Ignora se non capisce nulla mentre aspetta il trigger
                pass
            except sr.RequestError as e:
                print(f"Errore API Google principale: {e}")
                time.sleep(3) # Pausa prima di riprovare

if __name__ == "__main__":
    mqtt_publisher = setup_mqtt()
    # Avvia il loop di rete MQTT in un thread separato.
    # Questo gestisce l'invio e la ricezione dei messaggi in background.
    mqtt_publisher.loop_start()

    try:
        listen_and_publish(mqtt_publisher)
    except KeyboardInterrupt:
        print("\nUscita dal programma.")
    finally:
        mqtt_publisher.loop_stop()

        mqtt_publisher.disconnect()
