import pandas as pd
import logging

def transformar_dados(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("[TRANSFORM] Aplicando limpeza e regras de negócio...")
    
    
    df_limpo = df[df['valor'] > 0].copy()
    

    df_limpo['categoria_venda'] = df_limpo['valor'].apply(
        lambda x: 'Alto Valor' if x >= 200 else 'Normal'
    )
    
    logging.info(f"[TRANSFORM] Dados transformados. Registros válidos: {len(df_limpo)}")
    
    return df_limpo

