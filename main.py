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
        texto_cotacoes = ""
        for indice, linha in df_bruto.iterrows():
            moeda = linha['codigo'].replace('BRL', '') 
            valor = linha['cotacao_compra']
            
            texto_cotacoes += f"🔹 {moeda}: R$ {valor:,.2f}\n"
        
        # 4. Notificação de Sucesso
        msg_sucesso = (
            "🚀 *NOVA CARGA DE DADOS!*\n\n"
            f"📅 *Data:* `{data_referencia}`\n"
            f"💰 *Cotações Salvas:* {len(df_tratado)} moedas\n"
            f"💰 *Valores Obtidos:*\n"
            f"{texto_cotacoes}\n"
            "📊 *Status:* Tudo rodou perfeitamente no servidor!"
        )
        enviar_notificacao_telegram(msg_sucesso)

    except Exception as e:
        logging.error(f"Falha na execucao: {e}")
        
        # 4. Notificação de Falha
        msg_erro = (
            "🚨 *ALERTA VERMELHO NO PIPELINE!*\n\n"
            f"📅 *Data:* `{data_referencia}`\n"
            f"💥 *O que quebrou:* `{e}`\n"
            "🛠️ Hora de abrir o GitHub e investigar o log!"
        )
        enviar_notificacao_telegram(msg_erro)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de Cotações Financeiras")
    parser.add_argument("--data", type=str, help="Data de referencia no formato YYYY-MM-DD", 
                        default=datetime.now().strftime("%Y-%m-%d"))
    
    args = parser.parse_args()
    data_execucao = args.data
    
    executar_pipeline(data_execucao)