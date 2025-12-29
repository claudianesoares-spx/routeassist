import streamlit as st
import pandas as pd
import unicodedata
import re
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
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
    return re.sub(r"\s+", " ", texto)

def carregar_planilha_gdrive(sheet_id: str):
    """
    Monta o link de exportação .xlsx do Google Sheets
    e tenta carregar como DataFrame.
    """
    base_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    return pd.read_excel(base_url)

# ---------------- TÍTULO ----------------
st.title("SPX | Consulta de Rotas")

# ---------------- CARREGA DADOS ----------------
SHEET_ID = "1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx"  # seu ID aqui

try:
    df = carregar_planilha_gdrive(SHEET_ID)
    df.columns = df.columns.str.strip().str.lower()

    if "nome" not in df.columns:
        st.error("❌ A coluna 'nome' não foi encontrada na planilha.")
        st.stop()

    df["nome_normalizado"] = df["nome"].apply(normalizar_texto)

    st.markdown(
        f"📅 Base carregada com sucesso! Última atualização em: **{datetime.now().strftime('%d/%m/%Y %H:%M')}**"
    )

except Exception as erro:
    st.error(f"❌ Não foi possível carregar a planilha:\n{erro}")
    st.stop()

# ---------------- BUSCA ----------------
st.markdown("### 🔎 Buscar rota")
nome_input = st.text_input("Nome completo do motorista")

if nome_input:
    nome_busca = normalizar_texto(nome_input)
    resultado = df[df["nome_normalizado"].str.contains(nome_busca, na=False)]

    if not resultado.empty:
        rota = resultado.iloc[0].get("rota", "Não disponível")
        bairro = resultado.iloc[0].get("bairro", "Não disponível")

        st.success("✅ Motorista encontrado")
        st.markdown(f"**🚚 Rota:** {rota}  \n**📍 Bairro:** {bairro}")
    else:
        st.warning("⚠️ Nenhuma rota encontrada para esse nome")
