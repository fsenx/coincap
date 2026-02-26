from src.coincap import CoinCap
from src.secrets import SecretManager
from src.bigquery import bqInsertData
import pandas as pd
import os


def main(requests=None) -> str:
    try: 
        projeto = os.getenv("projectId")
        dataset = os.getenv("datasetId")
        table = os.getenv("tableId")
        secret = os.getenv("secret")
        version = os.getenv("version")
        offset = os.getenv("offset")

        secret = SecretManager(projectId=projeto,secretId=secret,version=version).getSecret()
        assets = CoinCap(api=secret).getAssets(offset=offset) 
        bqInsertData(billing_project=projeto,project_id=projeto,dataset_id=dataset,table_id=table,df=pd.DataFrame(assets))
        return "200"
    
    except Exception as e:
        return e

if __name__ == "__main__":
    main()