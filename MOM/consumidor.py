import pika

# Configuração da conexão com RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='fila_exemplo')

def callback(ch, method, properties, body):
    print(f" [x] Recebido: {body}")

# Configuração da função de callback para processar as mensagens
channel.basic_consume(queue='fila_exemplo', on_message_callback=callback, auto_ack=True)

print(' [*] Aguardando mensagens. Para sair, pressione Ctrl+C')
channel.start_consuming()
