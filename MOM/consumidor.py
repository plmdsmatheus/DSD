import pika

def callback(ch, method, properties, body):
    print(f" [x] Recebido: {body}")

# Conectar ao servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criar uma fila
channel.queue_declare(queue='testefila')

# Definir a função de retorno de chamada (callback) para processar as mensagens
channel.basic_consume(queue='testefila', on_message_callback=callback, auto_ack=True)

print(' [*] Aguardando mensagens. Para sair, pressione Ctrl+C')
channel.start_consuming()
