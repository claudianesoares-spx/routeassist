import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- LIMPEZA DE CACHE INICIAL ----------------
st.cache_data.clear()

# ---------------- ESTILO (CSS) ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f6f7f9;
}
.header-card {
    background: white;
    padding: 24px 28px;
    border-radius: 16px;
    border-left: 6px solid #ff7a00;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
.header-title {
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
}
.header-sub {
    font-size: 14px;
    color: #6b7280;
    margin-top: 4px;
}
.header-info {
    margin-top: 14px;
    font-size: 15px;
    color: #374151;
}
.result-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 16px;
}
.result-title {
    font-size: 20px;
    font-weight: 700;
    color: #ff7a00;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CABEÇALHO ----------------
st.markdown("""
<div class="header-card">
    <div class="header-title">🚚 SPX | Consulta de Rotas</div>
    <div class="header-sub">Shopee Express • Operação Logística</div>
    <div class="header-info">
        Consulta disponível <strong>somente após a alocação das rotas</strong>.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- CONFIGURAÇÕES ----------------
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1F8HC2D8UxRc5R_QBdd-zWu7y6Twqyk3r0NTPN0HCWUI/export?format=xlsx"
SENHA_ADMIN = "LPA2026"
ARQUIVO_STATUS = "status_site.json"

# ---------------- STATUS PERSISTENTE ----------------
def carregar_status():
    if not os.path.exists(ARQUIVO_STATUS):
        salvar_status("ABERTO")
    with open(ARQUIVO_STATUS, "r") as f:
        return json.load(f)["status"]

def salvar_status(status):
    with open(ARQUIVO_STATUS, "w") as f:
        json.dump({"status": status}, f)

status_site = carregar_status()

# ---------------- BASE PRINCIPAL + TIMESTAMP ----------------
@st.cache_data(ttl=300)
def carregar_base():
    df = pd.read_excel(URL_PLANILHA)
    df.columns = df.columns.str.strip()
    df = df.fillna("")
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return df, timestamp

df, ultima_atualizacao = carregar_base()

# ---------------- SIDEBAR ADMIN ----------------
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    st.markdown("---")

    senha = st.text_input("Senha ADMIN", type="password")

    if senha == SENHA_ADMIN:
        st.success("Acesso liberado")

        st.markdown(f"**🚦 Status da consulta:** `{status_site}`")
        st.markdown(f"**🕒 Última atualização:** `{ultima_atualizacao}`")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🟢 Abrir consulta"):
                salvar_status("ABERTO")
                st.success("Consulta ABERTA")
                st.rerun()

        with col2:
            if st.button("🔴 Fechar consulta"):
                salvar_status("FECHADO")
                st.warning("Consulta FECHADA")
                st.rerun()

        st.markdown("---")
        st.markdown("📊 **Base completa**")
        st.dataframe(df, use_container_width=True)

    elif senha:
        st.error("Senha incorreta")

# ---------------- BLOQUEIO PARA USUÁRIO COMUM ----------------
if status_site == "FECHADO":
    st.warning("🚫 Consulta temporariamente indisponível. Aguarde a liberação das rotas.")
    st.stop()

# ---------------- CONFERÊNCIA DAS COLUNAS ----------------
colunas_necessarias = ["Placa", "Nome", "Bairro", "Rota", "Cidade"]

for col in colunas_necessarias:
    if col not in df.columns:
        st.error(f"Coluna obrigatória não encontrada: {col}")
        st.stop()

# ---------------- CAMPO DE BUSCA ----------------
nome_busca = st.text_input(
    "Digite o **nome completo ou parcial** do motorista:",
    placeholder="Ex: Luan de Oliveira"
)

# ---------------- RESULTADO (INALTERADO) ----------------
if nome_busca:
    resultado = df[df["Nome"].str.contains(nome_busca, case=False, na=False)]

    if resultado.empty:
        st.warning("❌ Nenhuma rota atribuída para este motorista.")
    else:
        st.success(f"🚚 {len(resultado)} rota(s) encontrada(s)")

        for _, row in resultado.iterrows():
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">🚚 Rota {row['Rota']}</div>
                <strong>👤 Motorista:</strong> {row['Nome']}<br>
                <strong>🚗 Placa:</strong> {row['Placa']}<br>
                <strong>🏙️ Cidade:</strong> {row['Cidade']}<br>
                <strong>📍 Bairro:</strong> {row['Bairro']}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("Digite um nome para consultar a rota.")
