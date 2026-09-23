import logging
from extract import extrair_dados
from transform import transformar_dados
from load import carregar_dados


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def executar_pipeline(data_referencia: str):
    logging.info("====================================")
    logging.info(f"INICIANDO PIPELINE: {data_referencia}")
    logging.info("====================================")
    
    try:
        
        df_bruto = extrair_dados(data_referencia)
        df_processado = transformar_dados(df_bruto)
        carregar_dados(df_processado, data_referencia)
        
        logging.info("=== PIPELINE CONCLUÍDO COM SUCESSO ===")
        
    except Exception as e:
        logging.error(f"!!! FALHA NO PIPELINE !!! Erro: {e}")
        raise e

if __name__ == "__main__":
    data_de_hoje = "2026-09-23"
    executar_pipeline(data_de_hoje)