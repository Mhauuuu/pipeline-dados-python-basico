import pandas as pd
import sqlite3
import logging

def carregar_dados(df: pd.DataFrame, data_referencia: str, db_path: str = 'meu_banco.db'):
    logging.info(f"[LOAD] Conectando ao banco de destino: {db_path}...")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas_finais (
                id_transacao INTEGER,
                valor REAL,
                cliente_id INTEGER,
                data_venda TEXT,
                categoria_venda TEXT
            )
        ''')
        
        
        logging.info(f"[LOAD] Removendo dados antigos da data {data_referencia} para evitar duplicidade...")
        cursor.execute("DELETE FROM vendas_finais WHERE data_venda = ?", (data_referencia,))
        
        
        logging.info("[LOAD] Inserindo registros finais...")
        df.to_sql('vendas_finais', conn, if_exists='append', index=False)
        
    logging.info("[LOAD] Carga finalizada com sucesso!")