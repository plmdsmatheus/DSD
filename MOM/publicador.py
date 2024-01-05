import requests

def publicar_mensagem(conteudo):
    url = "http://localhost:8000/publicar-mensagem/"
    payload = {"conteudo": conteudo}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Mensagem publicada com sucesso!")
    else:
        print(f"Erro ao publicar mensagem. Status code: {response.status_code}")

if __name__ == "__main__":
    conteudo_mensagem = input("Digite o conteúdo da mensagem: ")
    publicar_mensagem(conteudo_mensagem)
