
import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Notas Fiscais - Dashboard", layout="wide")
st.title("📊 Dashboard de Notas Fiscais")

# Conexão com o banco
conn = sqlite3.connect("notas.db")
df_notas = pd.read_sql_query("SELECT * FROM notas", conn)
df_itens = pd.read_sql_query("SELECT * FROM itens", conn)

# Formatação
df_notas["valor_total"] = df_notas["valor_total"].astype(float)
df_itens["valor_total"] = df_itens["valor_total"].astype(float)

# Filtro por loja
lojas = df_notas["nome_loja"].unique()
loja_selecionada = st.selectbox("🛒 Selecione a loja", lojas)

df_filtrado = df_notas[df_notas["nome_loja"] == loja_selecionada]
st.subheader("📄 Notas Fiscais")
st.dataframe(df_filtrado, use_container_width=True)

# Itens da loja
if not df_filtrado.empty:
    st.subheader("🧾 Itens das Notas")
    nota_ids = df_filtrado["id"].tolist()
    df_itens_loja = df_itens[df_itens["nota_id"].isin(nota_ids)]

    # 🔍 Campo de busca
    termo_busca = st.text_input("🔎 Buscar item por nome (ex: arroz, leite, etc.):").strip().lower()

    if termo_busca:
        df_itens_filtrados = df_itens_loja[df_itens_loja["descricao"].str.lower().str.contains(termo_busca)]
    else:
        df_itens_filtrados = df_itens_loja

    st.dataframe(df_itens_filtrados, use_container_width=True)

conn.close()
