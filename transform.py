import pandas as pd
import logging

def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("[TRANSFORM] Processando indicadores financeiros...")
    
    df_tratado = df.copy()
    
    
    df_tratado['spread'] = (df_tratado['cotacao_venda'] - df_tratado['cotacao_compra']).round(4)
    
    
    def classificar_oscilacao(pct):
        if pct > 1.0:
            return 'Alta Forte'
        elif pct < -1.0:
            return 'Queda Forte'
        return 'Estavel'
    
    df_tratado['status_oscilacao'] = df_tratado['variacao_percentual'].apply(classificar_oscilacao)
    
    logging.info(f"[TRANSFORM] {len(df_tratado)} registros transformados e enriquecidos.")
    return df_tratado 