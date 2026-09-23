import pandas as pd
import sqlite3
import logging

def carregar_dados(df: pd.DataFrame, data_referencia: str, db_path: str = 'meu_banco.db'):
    logging.info(f"[LOAD] Conectando ao banco {db_path}...")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # 1. Cria a tabela com a nova estrutura de cotacoes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cotacoes_mercado (
                codigo TEXT,
                par_moeda TEXT,
                cotacao_compra REAL,
                cotacao_venda REAL,
                variacao_percentual REAL,
                spread REAL,
                status_oscilacao TEXT,
                data_consulta TEXT
            )
        ''')
        
        # 2. Idempotencia: remove dados da mesma data antes de reinserir
        logging.info(f"[LOAD] Removendo registros antigos da data {data_referencia}...")
        cursor.execute("DELETE FROM cotacoes_mercado WHERE data_consulta = ?", (data_referencia,))
        
        # 3. Insere os registros processados
        logging.info("[LOAD] Gravando cotacoes tratadas no banco...")
        df.to_sql('cotacoes_mercado', conn, if_exists='append', index=False)
        
    logging.info("[LOAD] Carga finalizada com sucesso!")