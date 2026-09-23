import requests
import pandas as pd
import logging

def extrair_dados(data_referencia: str) -> pd.DataFrame:
    logging.info(f"[EXTRACT] Consultando cotacoes na API para {data_referencia}...")
    
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados_json = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"[EXTRACT] Falha na requisicao HTTP: {e}")
        raise e

    registros = []
    for chave, info in dados_json.items():
        registros.append({
            'par_moeda': info.get('name'),
            'codigo': chave,
            'cotacao_compra': float(info.get('bid', 0.0)),
            'cotacao_venda': float(info.get('ask', 0.0)),
            'variacao_percentual': float(info.get('pctChange', 0.0)),
            'data_consulta': data_referencia
        })
        
    df_bruto = pd.DataFrame(registros)
    logging.info(f"[EXTRACT] {len(df_bruto)} cotacoes extraidas com sucesso.")
    return df_bruto