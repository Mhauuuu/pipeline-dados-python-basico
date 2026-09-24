import argparse
import logging
from datetime import datetime
from extract import extrair_dados
from transform import transformar_dados
from load import carregar_dados

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def executar_pipeline(data_referencia: str):
    logging.info("========================================")
    logging.info(f"INICIANDO PIPELINE DE COTACOES: {data_referencia}")
    logging.info("========================================")
    
    try:
        df_bruto = extrair_dados(data_referencia)
        df_processado = transformar_dados(df_bruto)
        carregar_dados(df_processado, data_referencia)
        
        logging.info("=== PIPELINE DE COTACOES CONCLUIDO ===")
        
    except Exception as e:
        logging.error(f"Falha na execucao: {e}")
        raise e

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Pipeline de Cotações Financeiras")
    parser.add_argument('--data', type=str, help="Data no formato YYYY-MM-DD", required=False)
    args = parser.parse_args()

    
    if args.data:
        
        data_execucao = args.data
    else:
        
        data_execucao = datetime.now().strftime("%Y-%m-%d")

    executar_pipeline(data_execucao)