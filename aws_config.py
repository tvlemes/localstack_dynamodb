"""
============================================================
CONFIGURAÇÕES AWS / LOCALSTACK
============================================================

Este arquivo centraliza as configurações utilizadas
pela aplicação para acessar o DynamoDB.

As configurações são carregadas do arquivo .env.

No LocalStack utilizamos credenciais fictícias:
    Access Key: test
    Secret Key: test
"""

import os

from dotenv import load_dotenv


# ============================================================
# CARREGAR VARIÁVEIS DO .ENV
# ============================================================

# Carrega as variáveis existentes no arquivo .env.
load_dotenv()


# ============================================================
# CONFIGURAÇÕES AWS
# ============================================================

# Access Key utilizada pelo LocalStack.
AWS_ACCESS_KEY_ID = os.getenv(
    "AWS_ACCESS_KEY_ID",
    "test"
)


# Secret Key utilizada pelo LocalStack.
AWS_SECRET_ACCESS_KEY = os.getenv(
    "AWS_SECRET_ACCESS_KEY",
    "test"
)


# Região AWS.
AWS_REGION = os.getenv(
    "AWS_DEFAULT_REGION",
    "us-east-1"
)


# Endpoint do LocalStack.
AWS_ENDPOINT_URL = os.getenv(
    "AWS_ENDPOINT_URL",
    "http://localhost:4566"
)