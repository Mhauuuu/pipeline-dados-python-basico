import streamlit as st
import pandas as pd
import sqlite3

# 1. Configuração da página Web
st.set_page_config(page_title="Dashboard de Cotações", page_icon="📈", layout="wide")

st.title("📊 Painel de Cotações de Moedas")
st.write("Visualização dos dados extraídos automaticamente pelo nosso pipeline.")

# 2. Conectar ao banco e ler os dados
@st.cache_data 
def carregar_dados():
    try:
        conn = sqlite3.connect("meu_banco.db")
        df = pd.read_sql("SELECT * FROM cotacoes_mercado ORDER BY data_consulta DESC", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o banco de dados: {e}")
        return pd.DataFrame()

df = carregar_dados()

# 3. Construção dos gráficos e tabelas na tela
if not df.empty:
    ultima_data = df['data_consulta'].max()
    st.subheader(f"Última atualização: {ultima_data}")

    df_recente = df[df['data_consulta'] == ultima_data]


    col1, col2, col3 = st.columns(3)
    
    with col1:
        usd = df_recente[df_recente['codigo'] == 'USDBRL']
        if not usd.empty:
            st.metric(label="Dólar (USD)", value=f"R$ {usd['cotacao_compra'].values[0]:.2f}")

    with col2:
        eur = df_recente[df_recente['codigo'] == 'EURBRL']
        if not eur.empty:
            st.metric(label="Euro (EUR)", value=f"R$ {eur['cotacao_compra'].values[0]:.2f}")

    with col3:
        btc = df_recente[df_recente['codigo'] == 'BTCBRL']
        if not btc.empty:
            
            st.metric(label="Bitcoin (BTC)", value=f"R$ {btc['cotacao_compra'].values[0]:,.2f}")

    st.divider() 

    
    st.subheader("Histórico Completo do Banco de Dados")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
else:
    st.warning("⚠️ Nenhum dado encontrado. Certifique-se de que o arquivo 'meu_banco.db' está na mesma pasta.")