from src.coincap import CoinCap
from src.secrets import SecretManager
from src.bigquery import bqInsertData, bqReadData
import pandas as pd
import os

def main(requests=None) -> str:
    try: 
        projeto = os.getenv("projectId")
        dataset = os.getenv("datasetId")
        tableRead = os.getenv("tableRead")
        tableInsert = os.getenv("tableInsert")
        secret = os.getenv("secret")
        version = os.getenv("version")
        days = os.getenv("days")

        secret = SecretManager(projectId=projeto,secretId=secret,version=version).getSecret()
        slugs = bqReadData(billing_project=projeto,project_id=projeto,dataset_id=dataset,table_id=tableRead)
        agent = CoinCap(api=secret).getAgentHistory(slugs=slugs,days=days) 
        bqInsertData(billing_project=projeto,project_id=projeto,dataset_id=dataset,table_id=tableInsert,df=pd.DataFrame(agent))
        return "200"
    
    except Exception as e:
        print(e)
        return e

if __name__ == "__main__":
    main()