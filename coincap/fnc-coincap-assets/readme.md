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

### coincap.py


### Configuração
Para executar localmente foi utilizado o gcloud CLI para se conectar ao ambiente GCP localmente.
Após a conexão foi executado o comando abaixo para criar as variaveis de ambiente local.

$env:projectId="seu projeto"                   
$env:datasetId="seu dataset"
$env:tableId="sua tabela"
$env:secret=" sua secret"
$env:version="latest"
$env:offset="0"

Em seguida foi executado a unção main.py para realizar a carga dos dados.
