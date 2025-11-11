# Simulador de dispositivo 1 para publicação de mensagens MQTT
# Instalação no terminal: pip install paho-mqtt
# Execute primeiro o outro código do sub.py
import paho.mqtt.client as paho
import time
import random

# Servidor MQTT público (Eclipse Mosquitto)
broker = "test.mosquitto.org"
port = 1883  # Porta padrão sem TLS

# Função callback chamada quando uma publicação é concluída
def on_publish(client, userdata, result):
    print("Dispositivo 1: Dados publicados com sucesso.")

# Criação do cliente MQTT (compatível com paho-mqtt >= 2.0)
client = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION1,
                     client_id="dispositivo1_admin")

# Associação da função callback
client.on_publish = on_publish

# Conexão ao broker público
print(f"Conectando ao broker MQTT {broker}:{port} ...")
client.connect(broker, port)
print("Conectado com sucesso!")

# Loop de envio de mensagens
for i in range(20):
    intervalo = random.randint(1, 5)
    message = f"Dispositivo 1: Dado número {i}"
    
    # Publica no tópico desejado
    ret = client.publish("/test/dispositivo1/data", message)
    print(f"Mensagem enviada: {message}")
    
    time.sleep(intervalo)

print("Publicação encerrada.")
client.disconnect()
