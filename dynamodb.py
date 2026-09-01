"""
============================================================
CONEXÃO COM DYNAMODB
============================================================

Este módulo cria a conexão boto3 com o DynamoDB
executado pelo LocalStack.
"""

import boto3

from aws_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_ENDPOINT_URL
)


# ============================================================
# CONEXÃO
# ============================================================

# Cria o recurso DynamoDB.
dynamodb = boto3.resource(

    # Serviço AWS.
    "dynamodb",

    # Região.
    region_name=AWS_REGION,

    # Credenciais.
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,

    # Endpoint do LocalStack.
    endpoint_url=AWS_ENDPOINT_URL
)


# ============================================================
# CLIENT
# ============================================================

# O client permite executar operações administrativas,
# como listar tabelas e consultar o schema.
client = dynamodb.meta.client


# ============================================================
# FUNÇÃO PARA OBTER UMA TABELA
# ============================================================

def obter_tabela(nome_tabela):
    """
    Retorna um objeto boto3 referente à tabela informada.

    Exemplo:

        tabela = obter_tabela("jogos")
    """

    return dynamodb.Table(
        nome_tabela
    )