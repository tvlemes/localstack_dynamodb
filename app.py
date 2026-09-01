"""
Autor: Thiago Vilarinho Lemes
Engenheiro de Dados
Data: 2026-08-31

============================================================
APRENDENDO LOCALSTACK
============================================================

Interface gráfica para gerenciamento genérico do DynamoDB.

Tecnologias:

    Python
    Streamlit
    boto3
    DynamoDB
    LocalStack

Funcionalidades:

    - Testar conexão
    - Criar múltiplas tabelas
    - Listar tabelas
    - Selecionar tabela
    - Visualizar schema
    - Inserir registros
    - Consultar registros
    - Atualizar registros
    - Deletar registros

IMPORTANTE:

A aplicação não depende de uma estrutura específica.

As tabelas podem ter diferentes:

    Partition Keys
    Sort Keys
    atributos

Os registros são informados através de JSON.
"""


# ============================================================
# IMPORTAÇÕES
# ============================================================

import json

import pandas as pd

import streamlit as st

from botocore.exceptions import ClientError


from dynamodb import (
    dynamodb,
    client,
    obter_tabela
)

from aws_config import (
    AWS_ENDPOINT_URL,
    AWS_REGION
)


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(

    page_title="LocalStack com DynamoDB",

    page_icon="☁️",

    layout="wide"
)


# ============================================================
# FUNÇÃO: LISTAR TABELAS
# ============================================================

def listar_tabelas():
    """
    Retorna todas as tabelas existentes no DynamoDB.
    """

    try:

        # Consulta o DynamoDB.
        resposta = client.list_tables()

        # Obtém os nomes.
        tabelas = resposta.get(
            "TableNames",
            []
        )

        # Ordena alfabeticamente.
        tabelas.sort()

        return tabelas

    except Exception as erro:

        st.error(
            f"Erro ao listar tabelas: {erro}"
        )

        return []


# ============================================================
# FUNÇÃO: OBTER INFORMAÇÕES DA TABELA
# ============================================================

def obter_schema(nome_tabela):
    """
    Retorna as informações estruturais da tabela.
    """

    resposta = client.describe_table(
        TableName=nome_tabela
    )

    return resposta["Table"]


# ============================================================
# FUNÇÃO: CONVERTER TEXTO PARA JSON
# ============================================================

def converter_json(texto):
    """
    Converte um texto JSON em um dicionário Python.

    Retorna:

        objeto, None

    """

    try:

        objeto = json.loads(
            texto
        )

        if not isinstance(objeto, dict):

            return None

        return objeto

    except json.JSONDecodeError:

        return None


# ============================================================
# TÍTULO
# ============================================================

st.title(
    "☁️ LocalStack com DynamoDB"
)

st.subheader(
    "DynamoDB + LocalStack + Python + Streamlit"
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title(
    "⚙️ Configuração"
)


st.sidebar.write(
    "**Endpoint:**"
)

st.sidebar.code(
    AWS_ENDPOINT_URL
)


st.sidebar.write(
    "**Região:**"
)

st.sidebar.code(
    AWS_REGION
)


# ============================================================
# TESTAR CONEXÃO
# ============================================================

st.sidebar.divider()

st.sidebar.subheader(
    "🔌 LocalStack"
)


if st.sidebar.button(
    "Testar conexão"
):

    try:

        resposta = client.list_tables()

        tabelas = resposta.get(
            "TableNames",
            []
        )

        st.sidebar.success(
            "Conexão funcionando!"
        )

        st.sidebar.write(
            f"Tabelas encontradas: {len(tabelas)}"
        )

    except Exception as erro:

        st.sidebar.error(
            f"Erro de conexão: {erro}"
        )


# ============================================================
# LISTA ATUAL DE TABELAS
# ============================================================

tabelas = listar_tabelas()


# ============================================================
# ABAS
# ============================================================

aba_criar, aba_inserir, aba_consultar, aba_atualizar, aba_deletar_registro, aba_deletar_tabela = st.tabs(

    [
        "🗄️ Criar tabela",
        "➕ Inserir",
        "🔎 Consultar",
        "✏️ Atualizar",
        "🗑️ Deletar Registro",
        "⚠️ Deletar tabela"
    ]
)


# ============================================================
# ABA CRIAR TABELA
# ============================================================

with aba_criar:

    st.header(
        "🗄️ Criar nova tabela"
    )


    st.write(
        "Crie uma tabela DynamoDB definindo suas chaves."
    )


    # --------------------------------------------------------
    # NOME
    # --------------------------------------------------------

    nome_tabela = st.text_input(

        "Nome da tabela",

        placeholder="Exemplo: jogos"
    )


    # --------------------------------------------------------
    # PARTITION KEY
    # --------------------------------------------------------

    st.subheader(
        "Partition Key"
    )


    partition_key = st.text_input(

        "Nome da Partition Key",

        value="id"
    )


    partition_type = st.selectbox(

        "Tipo da Partition Key",

        [
            "S - String",
            "N - Number",
            "B - Binary"
        ]
    )


    # --------------------------------------------------------
    # SORT KEY
    # --------------------------------------------------------

    possui_sort_key = st.checkbox(

        "Adicionar Sort Key"
    )


    sort_key = None

    sort_type = None


    if possui_sort_key:

        sort_key = st.text_input(

            "Nome da Sort Key",

            value="data"
        )


        sort_type = st.selectbox(

            "Tipo da Sort Key",

            [
                "S - String",
                "N - Number",
                "B - Binary"
            ]
        )


    # --------------------------------------------------------
    # BOTÃO
    # --------------------------------------------------------

    if st.button(

        "🗄️ Criar tabela",

        key="criar_tabela"
    ):

        # Validação do nome.
        if not nome_tabela.strip():

            st.warning(
                "Informe o nome da tabela."
            )

        elif not partition_key.strip():

            st.warning(
                "Informe a Partition Key."
            )

        elif possui_sort_key and not sort_key.strip():

            st.warning(
                "Informe a Sort Key."
            )

        else:

            try:

                # Verifica tabelas existentes.
                tabelas_existentes = listar_tabelas()


                if nome_tabela in tabelas_existentes:

                    st.warning(
                        f"A tabela '{nome_tabela}' já existe."
                    )

                else:

                    # ------------------------------------------------
                    # CONVERTE OS TIPOS
                    # ------------------------------------------------

                    tipo_partition = partition_type[0]

                    # Lista de atributos utilizados pelas chaves.
                    atributos = [
                        {
                            "AttributeName": partition_key,
                            "AttributeType": tipo_partition
                        }
                    ]


                    # ------------------------------------------------
                    # SCHEMA DA CHAVE
                    # ------------------------------------------------

                    key_schema = [

                        {
                            "AttributeName": partition_key,
                            "KeyType": "HASH"
                        }
                    ]


                    # ------------------------------------------------
                    # ADICIONA SORT KEY
                    # ------------------------------------------------

                    if possui_sort_key:

                        tipo_sort = sort_type[0]


                        atributos.append(

                            {
                                "AttributeName": sort_key,
                                "AttributeType": tipo_sort
                            }
                        )


                        key_schema.append(

                            {
                                "AttributeName": sort_key,
                                "KeyType": "RANGE"
                            }
                        )


                    # ------------------------------------------------
                    # CRIA A TABELA
                    # ------------------------------------------------

                    nova_tabela = dynamodb.create_table(

                        TableName=nome_tabela,

                        AttributeDefinitions=atributos,

                        KeySchema=key_schema,

                        BillingMode="PAY_PER_REQUEST"
                    )


                    # Aguarda a tabela ficar disponível.
                    waiter = client.get_waiter(
                        "table_exists"
                    )


                    waiter.wait(

                        TableName=nome_tabela
                    )


                    st.success(
                        f"Tabela '{nome_tabela}' criada com sucesso!"
                    )


                    st.json(

                        {
                            "Tabela": nome_tabela,
                            "PartitionKey": partition_key,
                            "SortKey": sort_key,
                            "Status": "ACTIVE"
                        }
                    )


                    # Atualiza a aplicação.
                    st.rerun()


            except Exception as erro:

                st.error(
                    f"Erro ao criar tabela: {erro}"
                )


# ============================================================
# ABA INSERIR
# ============================================================

with aba_inserir:

    st.header(
        "➕ Inserir registro"
    )


    tabelas = listar_tabelas()


    if not tabelas:

        st.info(
            "Nenhuma tabela encontrada. "
            "Crie uma tabela primeiro."
        )

    else:

        # ----------------------------------------------------
        # SELETOR
        # ----------------------------------------------------

        tabela_selecionada = st.selectbox(

            "Selecione a tabela",

            tabelas,

            key="tabela_inserir"
        )


        # Obtém a tabela.
        tabela = obter_tabela(
            tabela_selecionada
        )


        st.success(
            f"Tabela selecionada: "
            f"**{tabela_selecionada}**"
        )


        # ----------------------------------------------------
        # SCHEMA
        # ----------------------------------------------------

        schema = obter_schema(
            tabela_selecionada
        )


        st.write(
            "### 🔑 Chaves da tabela"
        )


        st.json(

            {
                "KeySchema": schema["KeySchema"],
                "AttributeDefinitions": schema[
                    "AttributeDefinitions"
                ]
            }
        )


        # ----------------------------------------------------
        # JSON
        # ----------------------------------------------------

        st.write(
            "### 📄 Registro"
        )


        st.write(
            "Informe o registro no formato JSON."
        )


        json_inserir = st.text_area(

            "JSON",

            value='{\n    "id": "1",\n    "nome": "Genshin Impact"\n}',

            height=200,

            key="json_inserir"
        )


        if st.button(

            "➕ Inserir registro",

            key="botao_inserir"
        ):

            registro = converter_json(
                json_inserir
            )


            if registro is None:

                st.error(
                    "JSON inválido."
                )

            else:

                try:

                    # Insere o registro.
                    tabela.put_item(

                        Item=registro
                    )


                    st.success(
                        "Registro inserido com sucesso!"
                    )


                    st.json(
                        registro
                    )


                except Exception as erro:

                    st.error(
                        f"Erro ao inserir: {erro}"
                    )


# ============================================================
# ABA CONSULTAR
# ============================================================

with aba_consultar:

    st.header(
        "🔎 Consultar registros"
    )

    # --------------------------------------------------------
    # CARREGA AS TABELAS
    # --------------------------------------------------------

    tabelas = listar_tabelas()

    if not tabelas:

        st.info(
            "Nenhuma tabela encontrada."
        )

    else:

        # ----------------------------------------------------
        # SELETOR DE TABELA
        # ----------------------------------------------------

        tabela_selecionada = st.selectbox(

            "Selecione a tabela",

            tabelas,

            key="tabela_consultar"
        )

        # Obtém a tabela selecionada.
        tabela = obter_tabela(
            tabela_selecionada
        )

        st.success(
            f"Tabela: **{tabela_selecionada}**"
        )

        # ----------------------------------------------------
        # CONSULTAR
        # ----------------------------------------------------

        if st.button(

            "🔎 Consultar",

            key="botao_consultar"
        ):

            try:

                # ------------------------------------------------
                # OBTÉM O SCHEMA DA TABELA
                # ------------------------------------------------

                schema = obter_schema(
                    tabela_selecionada
                )

                # ------------------------------------------------
                # IDENTIFICA AS CHAVES
                # ------------------------------------------------

                chaves = []

                for chave in schema["KeySchema"]:

                    chaves.append(
                        chave["AttributeName"]
                    )

                # ------------------------------------------------
                # EXECUTA O SCAN
                # ------------------------------------------------

                resposta = tabela.scan()

                registros = resposta.get(
                    "Items",
                    []
                )

                # ------------------------------------------------
                # VERIFICA SE EXISTEM DADOS
                # ------------------------------------------------

                if not registros:

                    st.info(
                        "Nenhum registro encontrado."
                    )

                else:

                    st.success(
                        f"{len(registros)} "
                        f"registro(s) encontrado(s)."
                    )

                    # ------------------------------------------------
                    # CRIA DATAFRAME
                    # ------------------------------------------------

                    dataframe = pd.DataFrame(
                        registros
                    )

                    # ------------------------------------------------
                    # ORGANIZA AS COLUNAS
                    # ------------------------------------------------

                    # Lista final que receberá a ordem das colunas.
                    ordem_colunas = []

                    # Primeiro adicionamos as chaves da tabela.
                    for chave in chaves:

                        if chave in dataframe.columns:

                            ordem_colunas.append(
                                chave
                            )

                    # Depois adicionamos os demais atributos.
                    for coluna in dataframe.columns:

                        if coluna not in ordem_colunas:

                            ordem_colunas.append(
                                coluna
                            )

                    # Aplica a nova ordem.
                    dataframe = dataframe[
                        ordem_colunas
                    ]

                    # ------------------------------------------------
                    # EXIBE A TABELA
                    # ------------------------------------------------

                    st.dataframe(

                        dataframe,

                        use_container_width=True,

                        hide_index=True
                    )

                    # ------------------------------------------------
                    # MOSTRA A ORDEM UTILIZADA
                    # ------------------------------------------------

                    with st.expander(
                        "📋 Ordem das colunas"
                    ):

                        st.write(
                            ordem_colunas
                        )

                    # ------------------------------------------------
                    # JSON
                    # ------------------------------------------------

                    with st.expander(
                        "📄 Ver JSON"
                    ):

                        st.json(
                            registros
                        )

            except Exception as erro:

                st.error(
                    f"Erro ao consultar: {erro}"
                )


# ============================================================
# ABA ATUALIZAR
# ============================================================

with aba_atualizar:

    st.header(
        "✏️ Atualizar registro"
    )


    tabelas = listar_tabelas()


    if not tabelas:

        st.info(
            "Nenhuma tabela encontrada."
        )

    else:

        # ----------------------------------------------------
        # SELETOR
        # ----------------------------------------------------

        tabela_selecionada = st.selectbox(

            "Selecione a tabela",

            tabelas,

            key="tabela_atualizar"
        )


        tabela = obter_tabela(
            tabela_selecionada
        )


        # ----------------------------------------------------
        # SCHEMA
        # ----------------------------------------------------

        schema = obter_schema(
            tabela_selecionada
        )


        st.write(
            "### 🔑 Chaves"
        )


        st.json(
            schema["KeySchema"]
        )


        # ----------------------------------------------------
        # CHAVE
        # ----------------------------------------------------

        st.write(
            "### Identificação do registro"
        )


        chave_json = st.text_area(

            "Informe as chaves em JSON",

            value='{\n    "id": "1"\n}',

            height=150,

            key="chave_atualizar"
        )


        # ----------------------------------------------------
        # ATRIBUTOS
        # ----------------------------------------------------

        st.write(
            "### ✏️ Dados para atualização"
        )


        atualizacao_json = st.text_area(

            "Informe os atributos que deseja atualizar",

            value='{\n    "nome": "Novo nome"\n}',

            height=180,

            key="atualizacao_json"
        )


        if st.button(

            "✏️ Atualizar registro",

            key="botao_atualizar"
        ):

            chave = converter_json(
                chave_json
            )


            atualizacao = converter_json(
                atualizacao_json
            )


            if chave is None:

                st.error(
                    "JSON da chave inválido."
                )

            elif atualizacao is None:

                st.error(
                    "JSON da atualização inválido."
                )

            elif not atualizacao:

                st.warning(
                    "Informe pelo menos um atributo."
                )

            else:

                try:

                    # ------------------------------------------------
                    # CONSTRÓI A EXPRESSÃO
                    # ------------------------------------------------

                    expressao = []

                    valores = {}


                    for indice, (atributo, valor) in enumerate(
                        atualizacao.items()
                    ):

                        # Nome utilizado na expressão.
                        nome_placeholder = (
                            f"#attr{indice}"
                        )


                        # Valor utilizado na expressão.
                        valor_placeholder = (
                            f":valor{indice}"
                        )


                        expressao.append(

                            f"{nome_placeholder} = "
                            f"{valor_placeholder}"
                        )


                        valores[
                            valor_placeholder
                        ] = valor


                    # ------------------------------------------------
                    # MAPA DE ATRIBUTOS
                    # ------------------------------------------------

                    nomes_atributos = {

                        f"#attr{indice}": atributo

                        for indice, atributo
                        in enumerate(
                            atualizacao.keys()
                        )
                    }


                    # ------------------------------------------------
                    # ATUALIZA
                    # ------------------------------------------------

                    resposta = tabela.update_item(

                        Key=chave,

                        UpdateExpression=(
                            "SET "
                            + ", ".join(
                                expressao
                            )
                        ),

                        ExpressionAttributeNames=(
                            nomes_atributos
                        ),

                        ExpressionAttributeValues=(
                            valores
                        ),

                        ReturnValues="ALL_NEW"
                    )


                    st.success(
                        "Registro atualizado com sucesso!"
                    )


                    st.json(
                        resposta.get(
                            "Attributes",
                            {}
                        )
                    )


                except Exception as erro:

                    st.error(
                        f"Erro ao atualizar: {erro}"
                    )


# ============================================================
# ABA DELETAR Registro
# ============================================================

with aba_deletar_registro:

    st.header(
        "🗑️ Deletar registro"
    )


    tabelas = listar_tabelas()


    if not tabelas:

        st.info(
            "Nenhuma tabela encontrada."
        )

    else:

        # ----------------------------------------------------
        # SELETOR
        # ----------------------------------------------------

        tabela_selecionada = st.selectbox(

            "Selecione a tabela",

            tabelas,

            key="tabela_deletar"
        )


        tabela = obter_tabela(
            tabela_selecionada
        )


        # ----------------------------------------------------
        # SCHEMA
        # ----------------------------------------------------

        schema = obter_schema(
            tabela_selecionada
        )


        st.write(
            "### 🔑 Chaves da tabela"
        )


        st.json(
            schema["KeySchema"]
        )


        # ----------------------------------------------------
        # CHAVE
        # ----------------------------------------------------

        chave_json = st.text_area(

            "Informe a chave do registro em JSON",

            value='{\n    "id": "1"\n}',

            height=150,

            key="chave_deletar"
        )


        # ----------------------------------------------------
        # BOTÃO
        # ----------------------------------------------------

        if st.button(

            "🗑️ Deletar registro",

            key="botao_deletar"
        ):

            chave = converter_json(
                chave_json
            )


            if chave is None:

                st.error(
                    "JSON inválido."
                )

            else:

                try:

                    # Primeiro verifica se existe.
                    resposta = tabela.get_item(

                        Key=chave
                    )


                    registro = resposta.get(
                        "Item"
                    )


                    if not registro:

                        st.warning(
                            "Registro não encontrado."
                        )

                    else:

                        st.write(
                            "Registro que será excluído:"
                        )


                        st.json(
                            registro
                        )


                        # Remove o registro.
                        tabela.delete_item(

                            Key=chave
                        )


                        st.success(
                            "Registro deletado com sucesso!"
                        )


                except Exception as erro:

                    st.error(
                        f"Erro ao deletar: {erro}"
                    )
# ============================================================
# ABA DELETAR TABELA
# ============================================================

with aba_deletar_tabela:

    st.header(
        "⚠️ Deletar tabela"
    )

    st.warning(
        """
        ATENÇÃO!

        Deletar uma tabela remove permanentemente:

        • A tabela
        • Todos os registros
        • Todos os dados armazenados nela

        Esta operação não pode ser desfeita.
        """
    )

    # --------------------------------------------------------
    # LISTAR TABELAS
    # --------------------------------------------------------

    tabelas = listar_tabelas()

    if not tabelas:

        st.info(
            "Nenhuma tabela encontrada."
        )

    else:

        # ----------------------------------------------------
        # SELECIONAR TABELA
        # ----------------------------------------------------

        tabela_selecionada = st.selectbox(

            "Selecione a tabela que deseja excluir",

            tabelas,

            key="tabela_deletar_tabela"
        )

        # Mostra a tabela escolhida.
        st.info(
            f"Tabela selecionada: **{tabela_selecionada}**"
        )

        # ----------------------------------------------------
        # CONFIRMAÇÃO
        # ----------------------------------------------------

        confirmar = st.checkbox(

            "Confirmo que quero excluir esta tabela "
            "e todos os seus dados.",

            key="confirmar_deletar_tabela"
        )

        # ----------------------------------------------------
        # BOTÃO DE EXCLUSÃO
        # ----------------------------------------------------

        if st.button(

            "⚠️ DELETAR TABELA",

            key="botao_deletar_tabela",

            disabled=not confirmar
        ):

            try:

                # ------------------------------------------------
                # EXCLUI A TABELA
                # ------------------------------------------------

                client.delete_table(

                    TableName=tabela_selecionada
                )

                # ------------------------------------------------
                # MENSAGEM DE SUCESSO
                # ------------------------------------------------

                st.success(

                    f"Tabela '{tabela_selecionada}' "
                    "deletada com sucesso!"
                )

                # ------------------------------------------------
                # ATUALIZA A INTERFACE
                # ------------------------------------------------

                st.rerun()

            except ClientError as erro:

                st.error(
                    f"Erro ao deletar tabela: {erro}"
                )

            except Exception as erro:

                st.error(
                    f"Erro inesperado: {erro}"
                )