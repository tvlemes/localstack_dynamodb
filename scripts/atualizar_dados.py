"""
Atualiza os dados de um jogo no DynamoDB do LocalStack.
"""

# Importa a referência da tabela DynamoDB.
from dynamodb import tabela


# ============================================================
# CONFIGURAÇÃO
# ============================================================

# ID do jogo que queremos atualizar.
id_jogo = "2"


# Novos valores que serão utilizados na atualização.
nova_classificacao = 5


# ============================================================
# ATUALIZAÇÃO
# ============================================================

print("======================================")
print("ATUALIZAÇÃO DE JOGO")
print("======================================")

print(f"Atualizando o jogo com ID: {id_jogo}")


# Atualiza o registro no DynamoDB.
#
# Key:
# identifica qual registro será alterado.
#
# UpdateExpression:
# informa qual atributo será atualizado.
#
# ExpressionAttributeValues:
# informa o valor que será colocado no atributo.
#
# ReturnValues:
# solicita que o DynamoDB devolva o registro
# depois da atualização.
resposta = tabela.update_item(

    # Identifica o registro através da chave primária.
    Key={
        "id": id_jogo
    },

    # Define o atributo que será atualizado.
    UpdateExpression="SET classificacao = :classificacao",

    # Define o novo valor da classificação.
    ExpressionAttributeValues={
        ":classificacao": nova_classificacao
    },

    # Retorna todos os atributos depois da atualização.
    ReturnValues="ALL_NEW"
)


# ============================================================
# RESULTADO
# ============================================================

# Obtém os dados atualizados.
jogo_atualizado = resposta.get("Attributes")


# Verifica se o DynamoDB retornou o registro.
if jogo_atualizado:

    print()
    print("Jogo atualizado com sucesso!")
    print()

    print("--------------------------------------")

    print(f"ID: {jogo_atualizado.get('id')}")

    print(f"Nome: {jogo_atualizado.get('nome')}")

    print(
        f"Categoria: {jogo_atualizado.get('categoria')}"
    )

    print(
        f"Gratuito: {jogo_atualizado.get('gratuito')}"
    )

    print(
        f"Classificação: {jogo_atualizado.get('classificacao')}"
    )

    print("--------------------------------------")

else:

    print()
    print("Não foi possível atualizar o jogo.")


print()
print("Processo finalizado.")