// Importa o módulo 'soap'
const soap = require('soap');

// Define a URL do WSDL para o serviço SOAP
const wsdlUrl = 'http://127.0.0.1:8000/?wsdl';

// Função para obter informações de um time de futebol a partir do ID
function getCompInfo(comp_id) {
  // Cria um cliente SOAP com base na URL do WSDL
  soap.createClient(wsdlUrl, function(err, client) {
    if (err) {
      console.error('Erro ao criar o cliente SOAP:', err);
      return;
    }

    // Chama o método 'get_comp_info' no serviço SOAP, passando o parâmetro 'comp_id'.
    client.get_comp_info({ comp_id: comp_id }, function(err, result) {
      if (err) {
        console.error('Erro ao buscar informações da competição:', err);
        return;
      }

      // Exibe as informações da competição no console.
      console.log('Competição Info:', result);
    });
  });
}

// Obtém o argumento da linha de comando que indica o endpoint desejado.
const endpoint = process.argv[2];

// Verifica o endpoint que está usando
if (endpoint === 'comp') {
    const comp_id = process.argv[3];
    getCompInfo(comp_id);
} else {
  console.error('Endpoint inválido!');
}
