import os
import warnings
import psycopg2
import pandas as pd
from datetime import datetime

# Ignorando mensagens do pandas
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable.*")
# Configurações do banco de dados PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'database': 'northwind',
    'user': 'northwind_user',
    'password': 'thewindisblowing'
}

# Lista das tabelas a serem extraídas
tabelas_extraidas = ['us_states', 'customers', 'orders', 'employees', 'shippers', 'categories', 'products', 'suppliers', 'region', 'territories', 'employee_territories', 'customer_demographics', 'customer_customer_demo']  # Adicione os nomes das tabelas aqui

# Diretório base onde os arquivos CSV serão salvos (se não existir, será criado)
DIRETORIO_BASE = os.path.join('.', 'data')

def extraindo_tabelas(nome_tabela, conexao, output_dir):
    query = f"SELECT * FROM {nome_tabela};"
    df = pd.read_sql_query(query, conexao)
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    os.makedirs(output_dir, exist_ok=True)
    csv_filename = f"{nome_tabela}_{date_str}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    df.to_csv(csv_path, index=False)

def main():
    try:
        # Conectando ao banco de dados
        conexao = psycopg2.connect(**DB_CONFIG)

        # Criar diretório com a data do dia da extração
        date_dir = datetime.now().strftime('%Y%m%d')
        diretorio_salvamento = os.path.join(DIRETORIO_BASE, date_dir)
        os.makedirs(diretorio_salvamento, exist_ok=True)

        # Iterar sobre as tabelas e extrair cada uma para um arquivo CSV dentro da pasta data
        for nome_tabela in tabelas_extraidas:
            extraindo_tabelas(nome_tabela, conexao, diretorio_salvamento)

        print("Extração concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

    finally:
        # Fechar a conexão com o banco de dados
        if conexao:
            conexao.close()

if __name__ == "__main__":
    main()

