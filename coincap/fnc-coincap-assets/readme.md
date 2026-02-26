# Documentação do código criado para Ingestão de Dados da API Coinmap
Autor: Felipe Sena

## Metodologia Aplicada
Esse código tem como intuito a extração de dados da API do Coinmap para consumo e ingestão de Dados no BigQuery.
Ele foi estruturado seguindo o princípio de Orientação a Objeto e a Metodologia SOLID.

Single Responsibility Principle - Princípio da Responsabilidade Única:
Open-Closed Principle - Princípio Aberto-Fechado
Liskov Substitution Principle - Princípio da Substituição de Liskov
Interface Segregation Principle - Princípio da Segregação da Interface
Dependency Inversion Principle - Princípio da Inversão da Dependência

Com isso as classes criadas como um quebra-cabeça que se auto encaixa, retirando a dependência de repetição de código e segregando seu propósito para simplificar o debug do código, assim quando um erro ocorrer, o desenvolvedor(a) identifica facilmente o trecho com problema para correção.

## Funções
Trecho para comentar os arquivos desenvolvidos

### main.py
Função principal responsável por instanciar variáveis e parâmetros que realizam a extração dos dados da API para inserir do Bigquery.

## coincap.py

init: Inicializa a classe configurando os parâmetros de identificação do projeto, o nome do segredo e a versão específica a ser acessada no Google Cloud.

_baseUrl: Define o endereço raiz da API CoinCap v3 para todas as chamadas.

__getHeaders: Configura os cabeçalhos de autenticação utilizando o token Bearer.

__getData: Gerencia a execução das requisições, aplicando regras de repetição automática (retry) em caso de falhas e controlando o tempo limite (timeout).

getStartTime: Calcula o momento exato de início para a busca de dados, convertendo dias retroativos em milissegundos.

getEndTime: Captura o horário atual no formato de milissegundos para encerrar a janela de consulta.

getAssets: Coleta a lista de criptoativos disponíveis, gerenciando a paginação para consolidar múltiplos registros em uma única estrutura.

getAssetHistory: Recupera o histórico de preços e variações de um ativo específico através de seu identificador principal.

getAgentHistory: Realiza a extração de dados históricos utilizando o endpoint otimizado para slugs, retornando informações de performance temporal.

## bigquery.py
bqInsertData: Realiza o carregamento de dados de um DataFrame Pandas diretamente para uma tabela específica no BigQuery.
bqReadData: Realiza a leitura de ids distintos de criptos de uma tabela específica no BigQuery.

## secrets.py
init: Inicializa a classe configurando os parâmetros de identificação do projeto, o nome do segredo e a versão específica a ser acessada no Google Cloud.

getSecret: Estabelece conexão com o serviço Secret Manager para recuperar informações sensíveis de forma segura.

## Configuração
Para executar localmente foi utilizado o gcloud CLI para se conectar ao ambiente GCP localmente.
Após a conexão foi executado o comando abaixo para criar as variaveis de ambiente local.

$env:projectId="seu projeto"
$env:datasetId="seu dataset"
$env:tableId="sua tabela"
$env:secret=" sua secret"
$env:version="latest"
$env:offset="0"

Em seguida foi executado a unção main.py para realizar a carga dos dados.
