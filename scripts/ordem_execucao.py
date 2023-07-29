import carrega_banco_postgres
import extrai_csv
import extrai_banco_postgres

def main():
    try:
        # Extrair dados do banco de dados
        extrai_banco_postgres.main()

    except Exception as e:
        print(f"Ocorreu um erro na extração de dados do banco de dados: {e}")
        print("O pipeline foi interrompido devido a um erro.")
        return  # Interrompe o pipeline caso ocorra um erro

    try:
        # Extrair dados do arquivo CSV
        extrai_csv.main()

    except Exception as e:
        print(f"Ocorreu um erro na extração de dados do arquivo CSV: {e}")
        print("O pipeline foi interrompido devido a um erro.")
        return  # Interrompe o pipeline caso ocorra um erro

    try:
        # Carregar dados no banco de dados
        carrega_banco_postgres.carregar_dados_no_banco()

    except Exception as e:
        print(f"Ocorreu um erro no carregamento dos dados no banco de dados: {e}")
        print("O pipeline foi interrompido devido a um erro.")

if __name__ == "__main__":
    main()
