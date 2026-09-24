import os
import requests
import logging

def enviar_notificacao_telegram(mensagem: str):
    
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        logging.error("[NOTIFY] Ignorado: Credenciais do Telegram nao configuradas.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("[NOTIFY] Mensagem enviada com sucesso para o Telegram!")
    except Exception as e:
        logging.error(f"[NOTIFY] Erro ao enviar mensagem para o Telegram: {e}")