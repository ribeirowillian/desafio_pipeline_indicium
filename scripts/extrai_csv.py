import os
import shutil
from datetime import datetime

# Diretório base onde os arquivos CSV serão salvos (se não existir, será criado)
DIRETORIO_BASE = os.path.join('.', 'data')

#copiando o arquivo para o diretório das demais planilhas extraidas do banco
def main():
    try:
        # Criar diretório com a data do dia da extração
        data_diretorio = datetime.now().strftime('%Y%m%d')
        diretorio_salvamento = os.path.join(DIRETORIO_BASE, data_diretorio)
        os.makedirs(diretorio_salvamento, exist_ok=True)

        # Caminho completo do arquivo CSV que você deseja copiar
        caminho_base = "C:/indicium/order_details.csv"

        # Obter o nome do arquivo original
        arquivo_original = os.path.basename(caminho_base)
        
        # Adicionar a data da extração ao nome do arquivo
        now = datetime.now()
        data_hoje = now.strftime('%Y%m%d')
        novo_nome_csv = f"{arquivo_original.split('.')[0]}_{data_hoje}.csv"
        destino_novo_csv = os.path.join(diretorio_salvamento, novo_nome_csv)

        # Copiar o arquivo CSV para o mesmo diretório das tabelas
        shutil.copy(caminho_base, destino_novo_csv)

        print("Cópia do arquivo CSV concluída com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
