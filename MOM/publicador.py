import pika

# Conectar ao servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Criar uma fila
channel.queue_declare(queue='testefila')

# Publicar mensagem na fila
channel.basic_publish(exchange='', routing_key='testefila', body='Teste')

print(" [x] Mensagem enviada para a fila")

# Fechar a conexão
connection.close()
