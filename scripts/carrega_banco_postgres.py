import os
import shutil
import psycopg2
import pandas as pd
from datetime import datetime

# Configurações do banco de dados PostgreSQL de destino
CONFIG_BD_DESTINO = {
    'host': 'localhost',
    'database': 'northwind',
    'user': 'northwind_user',
    'password': 'thewindisblowing'
}

# Diretório base onde os arquivos CSV foram salvos
DIRETORIO_BASE = os.path.join('.', 'data', datetime.now().strftime('%Y%m%d'))

# Obter o dia de hoje para puxar os arquivos com a data corrente.
data_corrente = datetime.now().strftime('%Y%m%d')

# Dicionário com o mapeamento entre nome do arquivo CSV e nome da tabela
MAPEAMENTO_ARQUIVO_TABELA = {
    f'orders_{data_corrente}.csv': 'orders',
    f'order_details_{data_corrente}.csv': 'order_details'
}
# Trucando a tabela antes de carregar novamenta para não ocorrer erro, isso pode mudar de acordo com as condições
# do projeto, sendo incremental ou full.
def truncar_tabelas(conexao):
    with conexao.cursor() as cursor:
        for nome_tabela in MAPEAMENTO_ARQUIVO_TABELA.values():
            consulta_truncate = f"TRUNCATE TABLE datawarehouse.{nome_tabela} CASCADE;"
            cursor.execute(consulta_truncate)
        conexao.commit()

# Carregando dados dos arquivos csv para o banco de dados 
def carregar_dados_no_banco():
    conexao_destino = None
    try:
        # Conectar ao banco de dados de destino
        conexao_destino = psycopg2.connect(**CONFIG_BD_DESTINO)

        # Criar o esquema (schema) caso não exista
        with conexao_destino.cursor() as cursor:
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS datawarehouse;")
        conexao_destino.commit()

        # Truncar as tabelas antes de carregar os dados
        truncar_tabelas(conexao_destino)

        for nome_arquivo, nome_tabela in MAPEAMENTO_ARQUIVO_TABELA.items():
            # Caminho completo do arquivo CSV a ser carregado
            caminho_arquivo_csv = os.path.join(DIRETORIO_BASE, nome_arquivo)

            # Carregar o arquivo CSV em um DataFrame
            df = pd.read_csv(caminho_arquivo_csv)

            # Substituir valores "NaN" por "None" no DataFrame
            df = df.where(pd.notna(df), None)

            # Converter o DataFrame em uma lista de tuplas
            dados = [tuple(row) for row in df.values]

            # Preparar o comando SQL para inserção dos dados na tabela especificada
            placeholders = ",".join(["%s"] * len(df.columns))
            consulta_insercao = f"INSERT INTO datawarehouse.{nome_tabela} VALUES ({placeholders});"

            # Executar a inserção dos dados
            with conexao_destino.cursor() as cursor:
                cursor.executemany(consulta_insercao, dados)

            conexao_destino.commit()

            print(f"Dados carregados na tabela {nome_tabela} com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro durante o carregamento dos dados: {e}")

    finally:
        # Fechar a conexão com o banco de dados de destino
        if conexao_destino:
            conexao_destino.close()

if __name__ == "__main__":
    carregar_dados_no_banco()

