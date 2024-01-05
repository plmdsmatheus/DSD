from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from typing import Dict
import pika

app = FastAPI()

# Configuração da conexão com RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='fila_exemplo')

def publish_message(message: Dict):
    # Publica a mensagem na fila do RabbitMQ
    channel.basic_publish(exchange='', routing_key='fila_exemplo', body=message['conteudo'])

@app.post("/publicar-mensagem/")
async def publicar_mensagem(message: Dict):
    try:
        # Publica a mensagem na fila
        publish_message(message)
        return JSONResponse(content={"mensagem": "Mensagem publicada com sucesso"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao publicar mensagem: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
