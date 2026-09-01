"""
Cria a tabela 'jogos' no DynamoDB do LocalStack.
"""

# Importa a conexão com o DynamoDB
# e o nome da tabela.
from dynamodb import dynamodb, TABLE_NAME


# ============================================================
# CRIAÇÃO DA TABELA
# ============================================================

tabela = dynamodb.create_table(

    # Nome da tabela.
    TableName=TABLE_NAME,

    # Define os atributos utilizados pela chave.
    AttributeDefinitions=[
        {
            # Nome da chave primária.
            "AttributeName": "id",

            # S = String.
            "AttributeType": "S"
        }
    ],

    # Define a chave primária.
    KeySchema=[
        {
            # Nome da chave.
            "AttributeName": "id",

            # HASH = Partition Key.
            "KeyType": "HASH"
        }
    ],

    # Modo de cobrança sob demanda.
    BillingMode="PAY_PER_REQUEST"
)


# ============================================================
# AGUARDA A TABELA FICAR DISPONÍVEL
# ============================================================

tabela.meta.client.get_waiter(
    "table_exists"
).wait(
    TableName=TABLE_NAME
)


# ============================================================
# RESULTADO
# ============================================================

print("======================================")
print("Tabela criada com sucesso!")
print("======================================")

print(f"Nome:   {TABLE_NAME}")
print(f"Status: {tabela.table_status}")

print("======================================")