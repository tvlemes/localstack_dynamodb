"""
Remove um jogo do DynamoDB do LocalStack.
"""

# Importa a referência da tabela DynamoDB.
from dynamodb import tabela


# ============================================================
# CONFIGURAÇÃO
# ============================================================

# ID do jogo que será excluído.
id_jogo = "2"


# ============================================================
# EXCLUSÃO
# ============================================================

print("======================================")
print("EXCLUSÃO DE JOGO")
print("======================================")

print(f"Procurando o jogo com ID: {id_jogo}")


# Antes de excluir, vamos consultar o registro.
#
# Isso permite verificar se o jogo realmente existe.
resposta = tabela.get_item(

    # Informa a chave primária.
    Key={
        "id": id_jogo
    }
)


# Obtém o jogo encontrado.
jogo = resposta.get("Item")


# ============================================================
# VERIFICA SE O JOGO EXISTE
# ============================================================

if not jogo:

    print()
    print("Jogo não encontrado.")
    print(f"ID informado: {id_jogo}")

else:

    # Mostra os dados antes da exclusão.
    print()
    print("Jogo encontrado:")

    print("--------------------------------------")

    print(f"ID: {jogo.get('id')}")

    print(f"Nome: {jogo.get('nome')}")

    print(
        f"Categoria: {jogo.get('categoria')}"
    )

    print(
        f"Gratuito: {jogo.get('gratuito')}"
    )

    print("--------------------------------------")


    # ========================================================
    # EXCLUI O REGISTRO
    # ========================================================

    print()
    print("Excluindo jogo...")


    # Remove o registro do DynamoDB.
    tabela.delete_item(

        # Identifica o registro pela chave primária.
        Key={
            "id": id_jogo
        }
    )


    # ========================================================
    # RESULTADO
    # ========================================================

    print()
    print("Jogo excluído com sucesso!")


print()
print("Processo finalizado.")