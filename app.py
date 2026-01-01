import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ================== CONFIGURAÇÃO DA PÁGINA ==================
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

# ================== ARQUIVOS ==================
CONFIG_FILE = "config.json"
LOG_FILE = "logs.csv"

# ================== CONFIG PADRÃO ==================
CONFIG_PADRAO = {
    "senha_master": "MASTER2026",
    "senha_operacional": "LPA2026",
    "status_site": "ABERTO"
}

# ================== CRIA CONFIG SE NÃO EXISTIR ==================
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(CONFIG_PADRAO, f, indent=4)

# ================== CARREGA CONFIG ==================
with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

# ================== FUNÇÃO SALVAR CONFIG ==================
def salvar_config():
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

# ================== FUNÇÃO LOG ==================
def registrar_log(acao, nivel):
    log = {
        "Data": datetime.now().strftime("%d/%m/%Y"),
        "Hora": datetime.now().strftime("%H:%M:%S"),
        "Ação": acao,
        "Nível": nivel
    }

    df = pd.DataFrame([log])

    if not os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)

# ================== ESTILO ==================
st.markdown("""
<style>
.stApp { background-color: #f6f7f9; }
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border-left: 6px solid #ff7a00;
}
</style>
""", unsafe_allow_html=True)

# ================== CABEÇALHO ==================
st.markdown("""
<div class="card">
<h2>🚚 SPX | Consulta de Rotas</h2>
<p>Consulta disponível somente após a alocação.</p>
</div>
""", unsafe_allow_html=True)

# ================== LOGIN ==================
nivel = None

with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    if senha == config["senha_master"]:
        nivel = "MASTER"
        registrar_log("Login realizado", nivel)
        st.success("Acesso MASTER")

    elif senha == config["senha_operacional"]:
        nivel = "OPERACIONAL"
        registrar_log("Login realizado", nivel)
        st.success("Acesso OPERACIONAL")

    elif senha:
        st.error("Senha incorreta")

    # ================== PAINEL MASTER ==================
    if nivel == "MASTER":
        st.markdown("---")
        st.markdown("### ⚙️ Controles")

        novo_status = st.radio(
            "Status da Consulta",
            ["ABERTO", "FECHADO"],
            index=0 if config["status_site"] == "ABERTO" else 1
        )

        if st.button("Salvar Status"):
            config["status_site"] = novo_status
            salvar_config()
            st.success("Status atualizado")

        st.markdown("### 🔑 Alterar Senhas")

        nova_master = st.text_input("Nova senha MASTER", type="password")
        nova_operacional = st.text_input("Nova senha OPERACIONAL", type="password")

        if st.button("Salvar Senhas"):
            if nova_master:
                config["senha_master"] = nova_master
            if nova_operacional:
                config["senha_operacional"] = nova_operacional
            salvar_config()
            st.success("Senhas atualizadas")

        st.markdown("### 📜 Histórico de Acessos")
        if os.path.exists(LOG_FILE):
            st.dataframe(pd.read_csv(LOG_FILE), use_container_width=True)
        else:
            st.info("Nenhum log registrado")

# ================== BLOQUEIO ==================
if config["status_site"] == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ================== CONSULTA (SIMPLES) ==================
st.markdown("### 🔍 Consulta")

nome = st.text_input("Digite o nome do motorista")

if nome:
    st.warning("⚠️ Base de dados ainda não conectada.")
