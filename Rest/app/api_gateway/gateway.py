from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Rotas para encaminhar solicitações para as APIs individuais
@app.route('/api/social/users', methods=['GET'])
def get_users():
    # Encaminha a solicitação para a API de usuários
    response = requests.get('http://localhost:8000/api/users')
    return jsonify(response.json())

@app.route('/api/social/posts', methods=['GET'])
def get_posts():
    # Encaminha a solicitação para a API de posts
    response = requests.get('http://localhost:8000/api/posts')
    return jsonify(response.json())


@app.route('/api/social/likes', methods=['GET'])
def get_likes():
    # Encaminha a solicitação para a API de likes
    response = requests.get('http://localhost:8000/api/likes')
    return jsonify(response.json())


@app.route('/api/social/messages', methods=['GET'])
def get_messages():
    # Encaminha a solicitação para a API de messagens
    response = requests.get('http://localhost:8000/api/messages')
    return jsonify(response.json())
    

if __name__ == '__main__':
    # Inicia o servidor da API Gateway na porta 5000
    app.run(port=5000)
