# Assinante MQTT - Recebe mensagens de um tópico público
# Instalação no terminal: pip install paho-mqtt
# Execute primeiro esse código do sub.py
import paho.mqtt.client as mqtt

# Broker MQTT público
broker = "test.mosquitto.org"
port = 1883
timelive = 60  # Keep-alive (tempo de vida da sessão)

# Função chamada quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        # Inscreve-se no mesmo tópico usado pelo dispositivo 1
        client.subscribe("/test/dispositivo1/data")
        print("Inscrito no tópico: /test/dispositivo1/data")
    else:
        print("Falha na conexão. Código de erro:", rc)

# Função chamada sempre que uma mensagem é recebida
def on_message(client, userdata, msg):
    print(f"Mensagem recebida no tópico {msg.topic}: {msg.payload.decode()}")

# Criação do cliente MQTT
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1, client_id="assinante_dispositivo1")

# Configuração dos callbacks
client.on_connect = on_connect
client.on_message = on_message

# Conexão ao broker público
print(f"Conectando ao broker MQTT {broker}:{port} ...")
client.connect(broker, port, timelive)

# Mantém o cliente ativo e ouvindo mensagens
client.loop_forever()
