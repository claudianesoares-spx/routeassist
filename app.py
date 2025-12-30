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

# ---------------- ESTILO GLOBAL | SHOPEE ----------------
st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #EE4D2D !important;
        font-family: Arial, sans-serif;
        font-weight: 700;
    }

    h4, h5, h6 {
        color: #E65100 !important;
        font-family: Arial, sans-serif;
    }

    div.stButton > button {
        background-color: #EE4D2D;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.45em 1em;
        font-weight: 600;
        font-family: Arial, sans-serif;
    }

    div.stButton > button:hover {
        background-color: #D84315;
        color: white;
    }

    input {
        border: 1px solid #EE4D2D !important;
        border-radius: 6px !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #EE4D2D !important;
    }

    div[data-testid="stSuccess"] {
        border-left: 6px solid #EE4D2D;
    }
    </style>
    """,
    unsafe_allow_html=True
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

# ---------------- STATUS ----------------
status = verificar_status()

# ---------------- INDICADOR VISUAL | SPX / SHOPEE ----------------
if status == "aberto":
    st.markdown(
        """
        <div style="
            background-color:#FFF3E0;
            border-left:8px solid #FB8C00;
            padding:14px 16px;
            border-radius:8px;
            margin-bottom:18px;
            font-family: Arial, sans-serif;
        ">
            🟠 <strong style="color:#E65100;">Consulta ABERTA</strong><br>
            <span style="color:#5D4037;">Rotas liberadas para consulta.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <div style="
            background-color:#FDECEA;
            border-left:8px solid #D32F2F;
            padding:14px 16px;
            border-radius:8px;
            margin-bottom:18px;
            font-family: Arial, sans-serif;
        ">
            🔴 <strong style="color:#B71C1C;">Consulta FECHADA</strong><br>
            <span style="color:#5F2120;">Aguardando liberação oficial das rotas.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- BLOQUEIO PARA DRIVERS ----------------
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
