import streamlit as st
import json
import os
from datetime import datetime

# ================= CONFIGURAÇÃO =================
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

ARQUIVO_STATUS = "status.json"

# ================= CONFIG PADRÃO =================
CONFIG_PADRAO = {
    "status_site": "FECHADO",
    "senha_master": "MASTER2026",
    "historico": []
}

# ================= CARREGAR / CRIAR STATUS =================
if not os.path.exists(ARQUIVO_STATUS):
    with open(ARQUIVO_STATUS, "w", encoding="utf-8") as f:
        json.dump(CONFIG_PADRAO, f, indent=4)

with open(ARQUIVO_STATUS, "r", encoding="utf-8") as f:
    config = json.load(f)

# ================= FUNÇÃO SALVAR =================
def salvar():
    with open(ARQUIVO_STATUS, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def registrar_acao(usuario, acao):
    config["historico"].append({
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "usuario": usuario,
        "acao": acao
    })
    salvar()

# ================= CABEÇALHO =================
st.title("🚚 SPX | Consulta de Rotas")
st.markdown("Consulta disponível **somente após a alocação das rotas**.")
st.divider()

# ================= ÁREA ADMIN =================
with st.sidebar:
    st.markdown("## 🔒 Área Administrativa")
    senha = st.text_input("Senha", type="password")

    nivel = None

    if senha == config["senha_master"]:
        nivel = "MASTER"
        st.success("Acesso MASTER liberado")
    elif senha == "LPA2026":
        nivel = "ADMIN"
        st.success("Acesso ADMIN liberado")
    elif senha:
        st.error("Senha incorreta")

    if nivel in ["ADMIN", "MASTER"]:
        st.markdown("---")
        st.markdown("### ⚙️ Controle da Consulta")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔓 ABRIR"):
                config["status_site"] = "ABERTO"
                registrar_acao(nivel, "ABRIU CONSULTA")
                st.success("Consulta ABERTA")

        with col2:
            if st.button("🔒 FECHAR"):
                config["status_site"] = "FECHADO"
                registrar_acao(nivel, "FECHOU CONSULTA")
                st.warning("Consulta FECHADA")

    if nivel == "MASTER":
        st.markdown("---")
        st.markdown("### 🔑 Trocar senha MASTER")
        nova = st.text_input("Nova senha MASTER", type="password")

        if st.button("Salvar nova senha"):
            if nova:
                config["senha_master"] = nova
                registrar_acao("MASTER", "ALTEROU SENHA MASTER")
                st.success("Senha atualizada")
            else:
                st.error("Senha inválida")

        st.markdown("---")
        st.markdown("### 📜 Histórico")
        for h in reversed(config["historico"]):
            st.markdown(f"- {h['data']} | **{h['usuario']}** | {h['acao']}")

# ================= STATUS GLOBAL =================
st.markdown(f"### 📌 Status atual: **{config['status_site']}**")
st.divider()

# ================= BLOQUEIO =================
if config["status_site"] == "FECHADO":
    st.warning("🚫 Consulta indisponível no momento.")
    st.stop()

# ================= CONSULTA =================
st.markdown("### 🔍 Consulta")
nome = st.text_input("Digite o nome do motorista")

if nome:
    st.info("⚠️ Base de dados ainda não conectada.")
