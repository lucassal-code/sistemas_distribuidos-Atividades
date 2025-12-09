# CHAT MQTT ENTRE DOIS COMPUTADORES
# Usa TCP normal (mais estável que WebSocket)
# Instalar dependência: pip install paho-mqtt

import paho.mqtt.client as mqtt
import time

# Broker MQTT público
BROKER = "broker.hivemq.com"
PORT = 1883  # Porta correta para TCP
TOPIC = "/test/chat_mqtt_terminal"

# ==== CALLBACKS ==== #

def on_connect(client, userdata, flags, reason_code, properties):
    """
    Callback executado quando o cliente tenta conectar ao broker (API V2).
    reason_code = código de retorno (0 significa sucesso).
    """
    if reason_code == 0:
        print("\n Conectado ao broker MQTT!")
        
        # Se estiver no modo assinante, inscreve no tópico
        if userdata["mode"] == "sub":
            client.subscribe(TOPIC)
            print(f" Inscrito no tópico: {TOPIC}")
    else:
        print("Erro de conexão:", reason_code)

def on_message(client, userdata, msg):
    """
    Callback executado sempre que uma nova mensagem chega no tópico inscrito.
    """
    print(f"\n Mensagem recebida: {msg.payload.decode()}\n> ", end="")

def on_publish(client, userdata, mid):
    """
    Callback chamado quando uma mensagem é enviada.
    """
    pass

# ==== CRIA O CLIENTE MQTT ==== #

def criar_cliente(mode):
    """
    Cria e configura o cliente MQTT.
    mode = "sub" (receber) ou "pub" (enviar)
    """
    client = mqtt.Client(
        client_id=f"terminal_chat_{mode}_{time.time()}",
        userdata={"mode": mode},
        callback_api_version=mqtt.CallbackAPIVersion.VERSION1
    )

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    # Conexão usando TCP
    client.connect(BROKER, PORT, 60)

    return client

# ==== PROGRAMA PRINCIPAL ==== #

print("=== CHAT MQTT ENTRE DOIS COMPUTADORES ===")
print("[1] Modo RECEBER mensagens")
print("[2] Modo ENVIAR mensagens")
op = input("Escolha a opção (1 ou 2): ")

mode = "sub" if op == "1" else "pub"
client = criar_cliente(mode)

print("\nConectando ao broker... Aguarde...\n")

client.loop_start()

# ==== ASSINANTE ==== #
if mode == "sub":
    print("Modo RECEBER ativado. Aguardando mensagens...\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Encerrando...")
        client.loop_stop()
        client.disconnect()

# ==== PUBLICADOR ==== #
else:
    print("Modo ENVIAR ativado.")
    print("Digite mensagens para enviar. Digite 'sair' para encerrar.\n")

    try:
        while True:
            msg = input("> ")
            if msg.lower() == "sair":
                break
            client.publish(TOPIC, msg)
    except KeyboardInterrupt:
        pass

    client.loop_stop()
    client.disconnect()
    print("Publicação encerrada.")