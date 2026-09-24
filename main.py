import argparse
import logging
from datetime import datetime
from extract import extrair_dados
from transform import transformar_dados
from load import carregar_dados
from notify import enviar_notificacao_telegram

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def executar_pipeline(data_referencia: str):
    logging.info("========================================")
    logging.info(f"INICIANDO PIPELINE DE COTACOES: {data_referencia}")
    logging.info("========================================")
    
    try:
        # 1. Extração
        df_bruto = extrair_dados(data_referencia)
        
        # 2. Transformação
        df_tratado = transformar_dados(df_bruto)
        
        # 3. Carga
        carregar_dados(df_tratado, data_referencia)
        
        logging.info("=== PIPELINE DE COTACOES CONCLUIDO ===")
        
        # 4. Notificação de Sucesso
        msg_sucesso = f"✅ *Pipeline Finalizado!*\nData ref: `{data_referencia}`\nRegistros processados: {len(df_tratado)}"
        enviar_notificacao_telegram(msg_sucesso)

    except Exception as e:
        logging.error(f"Falha na execucao: {e}")
        
        # 4. Notificação de Falha
        msg_erro = f"❌ *Erro no Pipeline!*\nData ref: `{data_referencia}`\nDetalhe: `{e}`"
        enviar_notificacao_telegram(msg_erro)
        
        raise e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de Cotações Financeiras")
    parser.add_argument("--data", type=str, help="Data de referencia no formato YYYY-MM-DD", 
                        default=datetime.now().strftime("%Y-%m-%d"))
    
    args = parser.parse_args()
    data_execucao = args.data
    
    executar_pipeline(data_execucao)