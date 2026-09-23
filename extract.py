import pandas as pd
import logging

def extrair_dados(data_referencia: str) -> pd.DataFrame:
    logging.info(f"[EXTRACT] Iniciando extração para a data: {data_referencia}")
    
    
    dados_mock = {
        'id_transacao': [1, 2, 3],
        'valor': [150.50, -20.00, 300.00], 
        'cliente_id': [101, 102, 103],
        'data_venda': [data_referencia, data_referencia, data_referencia]
    }
    
    df_bruto = pd.DataFrame(dados_mock)
    logging.info(f"[EXTRACT] {len(df_bruto)} registros extraídos.")
    
    return df_bruto