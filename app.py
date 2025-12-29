
import streamlit as st
import pandas as pd
import unicodedata
import re
from datetime import datetime

# ⚠️ SEMPRE PRIMEIRO
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    layout="centered"
)

# ---------------- FUNÇÕES ----------------
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"\s+", " ", texto)  # remove espaços extras
    return texto

# ---------------- TÍTULO ----------------
st.title("SPX | Consulta de Rotas")
st.markdown(
    f"📅 Base atualizada em: **{datetime.now().strftime('%d/%m/%Y %H:%M')}**"
)

# ---------------- CARREGAR BASE ----------------
try:
    
url = "https://docs.google.com/spreadsheets/d/1WiOCZsbHzIODwnP8Io3c8rPFCy1YI5t9SqguiWn3krw/export?format=xlsx"
df = pd.read_excel(url)

    # normalizar coluna nome
    df["nome_normalizado"] = df["nome"].apply(normalizar_texto)

except Exception as e:
    st.error("❌ Erro ao carregar o arquivo rotas.xlsx")
    st.stop()

# ---------------- BUSCA ----------------
st.markdown("### 🔎 Buscar rota")
nome = st.text_input("Nome completo do motorista")

if nome:
    nome_busca = normalizar_texto(nome)

    resultado = df[
    df["nome_normalizado"].str.contains(nome_busca, na=False)
]

    if not resultado.empty:
        rota = resultado.iloc[0]["rota"]
        bairro = resultado.iloc[0]["bairro"]

        st.success("✅ Motorista encontrado")
        st.markdown(f"""
        **🚚 Rota:** {rota}  
        **📍 Bairro:** {bairro}
        """)
    else:
        st.warning("⚠️ Nenhuma rota encontrada para este nome")




