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
    """Normaliza o texto para busca (lowercase, sem acentos, sem espaços extras)"""
    if not isinstance(texto, str):
        return ""
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r"\s+", " ", texto)
    return texto

# ---------------- TÍTULO ----------------
st.title("SPX | Consulta de Rotas")
st.markdown(f"📅 Base atualizada em: **{datetime.now().strftime('%d/%m/%Y %H:%M')}**")

# ---------------- CARREGAR BASE ----------------
try:
    # URL da planilha no Google Drive (export como XLSX)
    url = "https://docs.google.com/spreadsheets/d/1WiOCZsbHzIODwnP8Io3c8rPFCy1YI5t9SqguiWn3krw/export?format=xlsx"
    df = pd.read_excel(url)

    # Normaliza nomes das colunas
    df.columns = df.columns.str.strip().str.lower()

    # Verifica se a coluna 'nome' existe
    if "nome" not in df.columns:
        st.error("❌ A coluna 'nome' não foi encontrada na planilha.")
        st.stop()

    # Cria coluna normalizada para busca
    df["nome_normalizado"] = df["nome"].apply(normalizar_texto)

except Exception as e:
    st.error(f"❌ Erro ao carregar a base: {e}")
    st.stop()

# ---------------- BUSCA ----------------
st.markdown("### 🔎 Buscar rota")
nome = st.text_input("Nome completo do motorista")

if nome:
    nome_busca = normalizar_texto(nome)
    resultado = df[df["nome_normalizado"].str.contains(nome_busca, na=False)]

    if not resultado.empty:
        # Pega o primeiro resultado encontrado
        rota = resultado.iloc[0]["rota"] if "rota" in df.columns else "Não disponível"
        bairro = resultado.iloc[0]["bairro"] if "bairro" in df.columns else "Não disponível"

        st.success("✅ Motorista encontrado")
        st.markdown(f"""
        **🚚 Rota:** {rota}  
        **📍 Bairro:** {bairro}
        """)
    else:
        st.warning("⚠️ Nenhuma rota encontrada para este nome")






