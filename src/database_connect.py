import os
import sqlite3
import pandas as pd


DATA_RAW_DIR = "data_raw"
DB_PATH = "database/ecommerce.db"

def importar_csv_para_sqlite():
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
   
    print(f"Conectando ao banco de dados em: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    
    if not os.path.exists(DATA_RAW_DIR):
        print(f"Erro: A pasta '{DATA_RAW_DIR}' não foi encontrada na raiz do projeto.")
        return

    arquivos = [f for f in os.listdir(DATA_RAW_DIR) if f.endswith('.csv')]
    
    if not arquivos:
        print(f"Nenhum arquivo .csv encontrado dentro de '{DATA_RAW_DIR}'.")
        return

    for arquivo in arquivos:
        
        nome_tabela = arquivo.replace('_dataset.csv', '').replace('olist_', '')
        caminho_csv = os.path.join(DATA_RAW_DIR, arquivo)
        
        print(f"Importando {arquivo} para a tabela '{nome_tabela}'...")
        
        
        df = pd.read_csv(caminho_csv)
        
       
        df.to_sql(nome_tabela, conn, if_exists='replace', index=False)
        
    
    conn.close()
    

if __name__ == "__main__":
    importar_csv_para_sqlite()
