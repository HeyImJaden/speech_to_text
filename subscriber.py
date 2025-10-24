import paho.mqtt.client as mqtt

# -- Configuration (deve essere identica per publisher e subscriber) --
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "voice/transcription"

# -- Funzioni Callback MQTT --
def on_connect(client, userdata, flags, rc):
    """
    Callback eseguita quando il client si connette.
    La sottoscrizione al topic avviene qui.
    """
    if rc == 0:
        print("Subscriber connesso al Broker MQTT!")
        print(f"In ascolto sul topic: '{MQTT_TOPIC}'")
        # Sottoscriviti al topic dopo una connessione riuscita
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connessione fallita, return code {rc}\n")

def on_message(client, userdata, msg):
    """
    Callback eseguita ogni volta che un messaggio viene ricevuto
    dal topic sottoscritto.
    """
    # Stampa il messaggio ricevuto, decodificato da byte a stringa
    print(f"   -> {msg.payload.decode('utf-8')}")

# -- Logica Principale --
if __name__ == "__main__":
    # Crea un client con un ID univoco
    mqtt_subscriber = mqtt.Client(client_id="voice_subscriber")

    # Assegna le funzioni di callback
    mqtt_subscriber.on_connect = on_connect
    mqtt_subscriber.on_message = on_message

    # Connettiti al broker
    mqtt_subscriber.connect(MQTT_BROKER, MQTT_PORT, 60)

    # loop_forever() è un ciclo bloccante che gestisce automaticamente
    # la riconnessione e l'ascolto dei messaggi.
    print("In attesa di messaggi...")
    try:
        mqtt_subscriber.loop_forever()
    except KeyboardInterrupt:
        print("\nUscita dal programma.")

        mqtt_subscriber.disconnect()
