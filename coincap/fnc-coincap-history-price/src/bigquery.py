from google.cloud import bigquery
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
def bqInsertData(billing_project: str, project_id: str , dataset_id: str, table_id: str, df: pd.DataFrame) -> str:
    """
    Insere os dados de um DataFrame na tabela do BigQuery.
    Cria a tabela se não existir e utiliza o esquema fornecido por get_schema().

    Args:
      billing_project: O ID do projeto de faturamento.
      # ... outros args

    Return:
      '200' se a inserção for bem-sucedida, ou uma lista/str de erros.
    """

    bqclient = bigquery.Client(project=billing_project)

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        create_disposition=bigquery.CreateDisposition.CREATE_NEVER,
        autodetect=False
    )

    table_id_completo = f"{project_id}.{dataset_id}.{table_id}"

    try:
        job = bqclient.load_table_from_dataframe(
            df,
            table_id_completo,
            job_config=job_config
        )

        job.result()

        if job.errors:
            logging.error(f"Erro(s) durante carregamento: {job.errors}")
            return str(job.errors)
        else:
            # Sucesso
            logging.info(f"Dados inseridos em {table_id_completo}. Linhas carregadas: {job.output_rows}")
            return '200'

    except Exception as e:
        logging.error(f"Erro no job do BigQuery: {e}")
        return str(e)
    
def bqReadData(billing_project: str, project_id: str, dataset_id: str, table_id: str) -> list:
    """
    Lê os IDs únicos de uma tabela do BigQuery e retorna uma lista.
    """
    bqclient = bigquery.Client(project=billing_project)
    table_id_completo = f"{project_id}.{dataset_id}.{table_id}"
    
    # Exemplo com o SELECT DISTINCT que você usou
    query = f"SELECT DISTINCT id FROM `{table_id_completo}`"

    try:
        logging.info(f"Iniciando leitura da tabela {table_id_completo}")
        
        query_job = bqclient.query(query)
        results = query_job.result()  

        lista_dados = [row[0] for row in results]

        logging.info(f"Leitura concluída. Total de IDs únicos: {len(lista_dados)}")
        
        return lista_dados

    except Exception as e:
        logging.error(f"Erro ao ler dados do BigQuery: {e}")
        return []