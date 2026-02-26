import requests
from time import sleep,time
from datetime import datetime, timedelta
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')

class CoinCap():
    """
    Cliente para integração com a API REST da CoinCap (v3).

    Esta classe encapsula a comunicação com a API da CoinCap:
    - Métodos para:
        Consulta de histórico via endpoint /assets/
        Consulta de histórico via endpoint /assets/{asset}/history
        Consulta de histórico via endpoint /agentfriendly/history/{slug}

    Parâmetros:
        api (str):
            Token de autenticação da API CoinCap (Bearer Token).
    """
    def __init__(self,api):
        self.api = api

    @staticmethod
    def _baseUrl() -> str: 
        """
        Retorna a URL base da API CoinCap v3.

        Returns:
            str: URL base da API.
        """
        return "https://rest.coincap.io/v3"

    def __getHeaders(self) -> dict:
        """
        Monta os headers HTTP necessários para autenticação na API.

        Returns:
            dict: Dicionário contendo os headers de requisição.
        """
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api}"
                }

    def getStartTime(self,days:int) -> datetime:
        """
        Calcula o timestamp inicial em milissegundos com base
        na quantidade de dias retroativos.

        Args:
            days (int): Número de dias anteriores ao momento atual.

        Returns:
            int: Timestamp inicial em milissegundos.
        """
        return int((datetime.now() - timedelta(days=days)).timestamp() * 1000)

    def getEndTime(self) -> datetime:
        """
        Retorna o timestamp atual em milissegundos.

        Args:
            days (int): Parâmetro mantido por consistência de assinatura
                        (não utilizado no cálculo).

        Returns:
            int: Timestamp atual em milissegundos.
        """
        return int(time() * 1000)

    def __getData(self,url:str,headers:dict,params:dict) ->dict:
        """
        Retorna lista paginada de ativos disponíveis na CoinCap.

        A paginação ocorre em blocos de 100 registros por chamada.

        Args:
            offset (int): Posição inicial para paginação.

        Returns:
            list: Lista de ativos retornados pela API.
        """
        #Setando regra de Retry
        retry = Retry(
            total=3,
            backoff_factor=2,
            status_forcelist = [429,500,502,503,504],
            allowed_methods=["GET"]
        )
        timeout = 600 #10minutos 

        adapter = HTTPAdapter(max_retries=retry)
        with requests.Session() as session:
            session.mount("https://",adapter)
            session.mount("http://",adapter)

            try:
                logging.info("Obtendo dados da API")
                response = session.get(url, headers=headers, params=params,timeout=timeout)
                if response.status_code == 200:
                    return response.json()       
                else:
                    return(response.status_code, response.text)
                    
            except Exception as e:
                logging.warning("Falha ao obter dados da API")
                return e

    def getAssets(self,offset) -> dict:
        """
        Retorna lista paginada de ativos disponíveis na CoinCap.

        A paginação ocorre em blocos de 100 registros por chamada.

        Args:
            offset (int): Posição inicial para paginação.

        Returns:
            list: Lista de ativos retornados pela API.
        """
        url = self._baseUrl() + "/assets"

        headers = self.__getHeaders()

        params = {
            "limit": 100, 
            "offset": offset
        }

        all_data = []
        while offset < 200: #Simulação de cenário com 200 Assets usando paginação, num ambiente real o código seria um While True para mapear todos ou uma lista de assets específicos.
            response = self.__getData(url,headers,params)

            if response is None:
                break

            data = response['data']

            if not data:  
                break

            all_data.extend(data)

            offset += 100
            sleep(1)

        return all_data

    def getAssetHistory(self,assets:list, days:int) -> dict:
        """
        Obtém histórico de preços utilizando o endpoint
        /agentfriendly/history/{slug}.

        O retorno contém um campo 'history' no formato string,
        onde cada linha representa:
            timestamp,preço

        Args:
            slug (str): Identificador do ativo (ex: 'bitcoin').
            days (int, optional): Quantidade de dias retroativos para consulta.

        Returns:
            dict: JSON contendo histórico em formato compactado.
        """
        end = self.getEndTime()
        start = self.getStartTime(days=days)

        headers = self.__getHeaders()

        params = {
            "interval": f"d{days}",
            "start": start,
            "end": end
        }

        all_history = []

        for asset in assets:
            url = self._baseUrl() + f"/assets/{asset}/history"

            print(f"Coletando: {asset}")

            data = self.__getData(url,headers,params)
            if data:
                all_history.append(data)

            sleep(1)  
        return all_history

    def getAgentHistory(self,slugs, days) -> dict:
        end = self.getEndTime()
        start = self.getStartTime(days=days)

        headers = self.__getHeaders()

        params = {
            "interval": f"d{days}",
            "start": start,
            "end": end
        }

        all_history = []

        for asset in slugs:
            url = self._baseUrl() + f"/agentfriendly/history/{asset}"

            print(f"Coletando: {asset}")

            data = self.__getData(url,headers,params)
            if data:
                all_history.append(data)

            sleep(1)  
        return all_history