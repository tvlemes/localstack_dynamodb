"""
Consulta todos os jogos existentes no DynamoDB.
"""

# Importa a tabela do DynamoDB.
from dynamodb import tabela


# ============================================================
# CONSULTA
# ============================================================

print("Consultando DynamoDB...")
print()


# Executa um SCAN na tabela.
resposta = tabela.scan()


# Obtém os itens retornados.
jogos = resposta.get("Items", [])


# ============================================================
# VERIFICAÇÃO
# ============================================================

# Verifica se nenhum registro foi encontrado.
if not jogos:

    print("Nenhum jogo encontrado.")

else:

    print(f"Quantidade de jogos encontrados: {len(jogos)}")
    print()

    # Percorre todos os jogos.
    for jogo in jogos:

        print("--------------------------------")

        print(f"ID: {jogo.get('id')}")

        print(f"Nome: {jogo.get('nome')}")

        print(f"Categoria: {jogo.get('categoria')}")

        print(f"Gratuito: {jogo.get('gratuito')}")

        # Verifica se existe classificação.
        if "classificacao" in jogo:
            print(
                f"Classificação: {jogo.get('classificacao')}"
            )

        print("--------------------------------")


print()
print("Consulta finalizada.")