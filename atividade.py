import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
timelive = 60

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        # Inscreve-se no mesmo tópico usado pelo dispositivo 1
        client.subscribe("/test/dispositivo1/data")
        print("Inscrito no tópico: /test/dispositivo1/data")
    else:
        print("Falha na conexão. Código de erro:", rc)

#client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1, client_id="assinante_dispositivo1")