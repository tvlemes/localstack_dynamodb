"""
Insere jogos no DynamoDB do LocalStack.
"""

# Importa a tabela configurada no arquivo dynamodb.py.
from dynamodb import tabela


# ============================================================
# DADOS DOS JOGOS
# ============================================================

jogo_1 = {
    "id": "1",
    "nome": "Genshin Impact",
    "categoria": "Mundo Aberto",
    "gratuito": True
}


jogo_2 = {
    "id": "2",
    "nome": "Tower of Fantasy",
    "categoria": "Mundo Aberto",
    "gratuito": True
}


# ============================================================
# INSERÇÃO
# ============================================================

print("Inserindo jogo 1...")

resposta_1 = tabela.put_item(
    Item=jogo_1
)

print("Jogo 1 inserido!")
print(resposta_1)


print()
print("Inserindo jogo 2...")

resposta_2 = tabela.put_item(
    Item=jogo_2
)

print("Jogo 2 inserido!")
print(resposta_2)


print()
print("Todos os jogos foram inseridos com sucesso!")