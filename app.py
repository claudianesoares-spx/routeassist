import streamlit as st
import pandas as pd

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="SPX | Consulta de Rotas",
    page_icon="🚚",
    layout="centered"
)

st.title("🚚 SPX | Consulta de Rotas")

# ---------------- LINK DA PLANILHA ----------------
url = "https://docs.google.com/spreadsheets/d/1x4P8sHQ8cdn7tJCDRjPP8qm4aFIKJ1tx/export?format=xlsx"

# ---------------- FUNÇÃO DE LEITURA ----------------
@st.cache_data(ttl=300)
def carregar_dados():
    # Lê a aba correta
    df = pd.read_excel(
        url,
        sheet_name="BASE IMPORTAÇÃO",
        dtype=str
    )

    # Padroniza nomes das colunas
    df.columns = df.columns.str.strip()

    return df

# ---------------- CARREGAR DADOS ----------------
try:
    df = carregar_dados()
except Exception as e:
    st.error("Erro ao carregar a base de dados.")
    st.stop()

# ---------------- CONFERÊNCIA DAS COLUNAS ----------------
colunas_necessarias = ["Placa", "Nome", "Bairro", "Rota", "Cidade"]

for col in colunas_necessarias:
    if col not in df.columns:
        st.error(f"Coluna obrigatória não encontrada: {col}")
        st.stop()

# ---------------- FILTRO ----------------
nome_busca = st.text_input(
    "Digite o nome completo ou parcial do motorista:",
    placeholder="Ex: Adriana Cardoso"
)

if nome_busca:
    resultado = df[df["Nome"].str.contains(nome_busca, case=False, na=False)]

    if resultado.empty:
        st.warning("Nenhuma rota encontrada para este nome.")
    else:
        st.success(f"{len(resultado)} rota(s) encontrada(s):")

        st.dataframe(
            resultado[[
                "Placa",
                "Nome",
                "Bairro",
                "Rota",
                "Cidade"   # 👈 GARANTIDO AQUI
            ]],
            use_container_width=True
        )
else:
    st.info("Digite um nome para consultar a rota.")
