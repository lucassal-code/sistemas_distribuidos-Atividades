import paho.mqtt.client as mqtt
import time
import threading

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "/test/chat_mqtt_terminal"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\n Conectado ao broker MQTT!")
        client.subscribe(TOPIC)
        print(f" Inscrito no tópico: {TOPIC}\n")
    else:
        print("Erro de conexão:", rc)

def on_message(client, userdata, msg):
    texto = msg.payload.decode()
    # Evita mostrar as próprias mensagens como recebidas
    if not texto.startswith(userdata["client_id"]):
        print(f"\n {texto}\n> ", end="")

def criar_cliente(nome):
    client_id = f"chat_user_{nome}_{int(time.time())}"

    client = mqtt.Client(
        client_id=client_id,
        userdata={"client_id": nome},
    )

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    return client

def enviar_mensagens(client, nome):
    while True:
        msg = input("> ")
        if msg.lower() == "sair":
            print("Encerrando chat...")
            client.disconnect()
            break

        mensagem_final = f"{nome}: {msg}"
        client.publish(TOPIC, mensagem_final)

# ==== PROGRAMA PRINCIPAL ==== #

print("===== CHAT MQTT =====")
nome = input("Digite seu nome ou apelido: ")

client = criar_cliente(nome)

print("\nConectando ao broker...\n")
client.loop_start()

# Thread responsável por enviar mensagens
thread_envio = threading.Thread(target=enviar_mensagens, args=(client, nome))
thread_envio.start()

thread_envio.join()
client.loop_stop()
print("Chat finalizado.")