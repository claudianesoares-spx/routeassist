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

# ---------------- CARREGAR BASE PRINCIPAL ----------------
@st.cache_data(ttl=300)
def carregar_planilha():
    url = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"
    df = pd.read_excel(url, sheet_name="CONSULTA ROTAS")
    df.columns = df.columns.str.strip().str.lower()

    if "nome" not in df.columns:
        st.error("❌ Coluna 'nome' não encontrada.")
        st.stop()

    df["nome_normalizado"] = df["nome"].apply(normalizar_texto)
    return df

# ---------------- CONTROLE DE STATUS ----------------
@st.cache_data(ttl=60)
def verificar_status():
    url = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"
    df = pd.read_excel(url, sheet_name="controle")
    df.columns = df.columns.str.lower()

    if "status_consulta" not in df.columns:
        return "fechado"

    return str(df.loc[0, "status_consulta"]).strip().lower()

# ---------------- ÁREA ADMIN ----------------
st.sidebar.title("🔐 Área Administrativa")

senha = st.sidebar.text_input("Senha ADMIN", type="password")
admin = senha == "LPA2026"

if admin:
    st.sidebar.success("✅ Acesso administrativo liberado")

    if st.sidebar.button("🔄 Atualizar base agora"):
        st.cache_data.clear()
        st.rerun()

# ---------------- BLOQUEIO DE ACESSO ----------------
status = verificar_status()

if status != "aberto" and not admin:
    st.title("🚧 Consulta temporariamente indisponível")
    st.info(
        "As rotas ainda estão em processamento.\n\n"
        "⏳ Por favor, aguarde a liberação oficial."
    )
    st.stop()

# ---------------- CARREGAMENTO DA BASE ----------------
df = carregar_planilha()

st.markdown(
    f"📅 Base atualizada em **{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}**"
)

# ---------------- BUSCA ----------------
st.title("SPX | Consulta de Rotas")
st.markdown("### 🔎 Buscar rota")

nome_input = st.text_input("Digite seu nome completo")

if nome_input:
    nome_busca = normalizar_texto(nome_input)
    pattern = re.compile(nome_busca)

    resultado = df[df["nome_normalizado"].str.contains(pattern, na=False)]

    if resultado.empty:
        st.warning("⚠️ Nenhuma rota encontrada para esse nome")
    else:
        st.success(f"✅ {len(resultado)} rota(s) encontrada(s)")

        for _, row in resultado.iterrows():
            rota = row.get("rota", "Não disponível")
            bairro = row.get("bairro", "Não disponível")
            placa = row.get("placa", "—")

            st.markdown(
                f"""
                🚚 **Rota:** {rota}  
                📍 **Bairro:** {bairro}  
                🚘 **Placa:** {placa}  
                ---
                """
            )
