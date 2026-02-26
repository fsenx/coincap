from google.cloud import secretmanager
import json

class SecretManager():
    def __init__(self, projectId: str, secretId:str, version:str):
        """ Inicializa o objeto Secret Manager que obtém as chaves do Secret Manager.
        """
        self.projectId = projectId
        self.secretId = secretId
        self.version = version

    def getSecret(self) -> json:
        """ Recupera o valor de um segredo do Secret Manager.
            Return:
                Chaves do secret manager
        """
        # Cria o cliente do Secret Manager.
        client = secretmanager.SecretManagerServiceClient()

        # Constrói o nome do recurso da versão do segredo.
        name = f"projects/{self.projectId}/secrets/{self.secretId}/versions/{self.version}"

        # Acessa a versão do segredo.
        response = client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')