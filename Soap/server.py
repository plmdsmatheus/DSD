from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json
import requests

# URL base da API de Futebol
base_url = "https://api.football-data.org/v2/competitions"

# Chave de API para autenticar as solicitações à API de Futebol
api_key = "625ecf846d2e4fb49866cb1aaa03db92"

# Define a classe do serviço que será exposto pelo servidor SOAP
class FootballComp(ServiceBase):
    # Define um método remoto chamado 'get_comp_info' que recebe o ID de uma competição e retorna informações sobre ela
    @rpc(Unicode, _returns=Unicode)
    def get_comp_info(self, comp_id):
        # Define o cabeçalho da solicitação com a chave de API
        headers = {"X-Auth-Token": api_key}

        # Faz uma requisição HTTP GET à API de Futebol para obter os dados do time
        response = requests.get(f"{base_url}/{comp_id}", headers=headers)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Converte o JSON da resposta para um dicionário Python
            comp_data = response.json()

            # Extrai o tipo de competição
            comp_type = comp_data.get("type", "")
            # Extrai qual rodada 
            comp_matchday = comp_data.get("currentSeason", {}).get("currentMatchday", "")
            # Extrai quando começou a temporada
            comp_start = comp_data.get("currentSeason", {}).get("startDate", "")
            # Extrai quando termina a temporada
            comp_finish = comp_data.get("currentSeason", {}).get("endDate", "")
            # Extrai quem foi o campeão
            comp_winner = comp_data.get("currentSeason", {}).get("winner", "")

            # Cria uma string de resultado com as informações da competição
            result = f"Tipo de liga: {comp_type}, Rodada: {comp_matchday}, Quando começou: {comp_start},  Quando termina: {comp_finish}, Vencendor: {comp_winner}"
        else:
            result = f"Failed to retrieve team information. Status code: {response.status_code}"

        return result


# Cria uma instância da aplicação SOAP e registra o serviço 'FootballTeam' nela
soap_app = Application([FootballComp],
                       tns="soap.server",
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# Cria uma aplicação WSGI a partir da aplicação SOAP
application = WsgiApplication(soap_app)

# Executa o servidor se o script estiver sendo executado diretamente
if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    # Configuração do nível de log para DEBUG
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    # Imprime as informações sobre o servidor na console
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    # Cria um servidor WSGI na porta 8000 e o coloca para ouvir
    server = make_server('127.0.0.1', 8000, application)
    server.serve_forever()
