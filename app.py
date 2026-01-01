import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ---------------- ARQUIVOS ----------------
CONFIG_FILE = "config.json"
LOG_FILE = "logs.csv"

# ---------------- CONFIG PADRÃO ----------------
CONFIG_PADRAO = {
    "senha_master": "MASTER2026",
    "senha_operacional": "LPA2026",
    "status_site": "ABERTO"
}

# ---------------- CRIA CONFIG SE NÃO EXISTIR ----------------
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(CONFIG_PADRAO, f, indent=4)

# ---------------- CARREGA CONFIG ----------------
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

# ---------------- FUNÇÃO SALVAR CONFIG ----------------
def salvar_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

# ---------------- FUNÇÃO LOG ----------------
def registrar_log(acao, nivel):
    linha = {
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Ação": acao,
        "Acesso": nivel
    }
    df = pd.DataFrame([linha])
    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)

# ---------------- ESTILO ----------------
st.markdown("""
<style>
.stApp { background-color: #f6f7f9; }
.header-card {
    background: white;
    padding: 24px 28px;
    border-radius: 16px;
    border-left: 6px solid #ff7a00;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    margin-bottom: 30px;
}
.header-title { font-size: 32px; font-weight: 700; color: #1f2937; }
.header-sub { font-size: 14px; color: #6b7280; margin-top: 4px; }
.header-info { margin-top: 14px; font-size: 15px; color: #374151; }
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

# ---------------- LOGIN ----------------
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    nivel = None
    if senha == config["senha_master"]:
        nivel = "MASTER"
    elif senha == config["senha_operacional"]:
        nivel = "OPERACIONAL"

    if nivel:
        st.success(f"Acesso {nivel}")
        registrar_log("Login realizado", nivel)
        st.markdown(f"**🚦 Status:** `{config['status_site']}`")

        col1, col2 = st.columns(2)
        if col1.button("🟢 Abrir"):
            config["status_site"] = "ABERTO"
            salvar_config()
            st.experimental_rerun()
        if col2.button("🔴 Fechar"):
            config["status_site"] = "FECHADO"
            salvar_config()
            st.experimental_rerun()

        # MASTER ONLY
        if nivel == "MASTER":
            st.markdown("---")
            st.markdown("### 🔑 Gerenciar Senhas")
            nova_op = st.text_input("Nova senha operacional", type="password")
            if st.button("Salvar senha operacional") and nova_op:
                config["senha_operacional"] = nova_op
                salvar_config()
                st.success("Senha operacional atualizada")
            nova_master = st.text_input("Nova senha master", type="password")
            if st.button("Salvar senha master") and nova_master:
                config["senha_master"] = nova_master
                salvar_config()
                st.success("Senha master atualizada")

            st.markdown("---")
            st.markdown("### 📜 Histórico")
            if os.path.exists(LOG_FILE):
                st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)

    elif senha:
        st.error("Senha incorreta")

# ---------------- BLOQUEIO ----------------
if config["status_site"] == "FECHADO":
    st.warning("🚫 Consulta temporariamente indisponível.")
    st.stop()

# ---------------- BUSCA ----------------
nome_busca = st.text_input("Digite o **nome completo ou parcial** do motorista:")

if nome_busca:
    st.warning("⚠️ Base de dados ainda não conectada.")
