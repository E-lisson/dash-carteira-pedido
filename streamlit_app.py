
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Pedidos", layout="wide")

# Estilo personalizado
st.markdown("""
    <style>
    /* Remove aparência de link */
    .sidebar-button a {
        text-decoration: none !important;
        color: white !important;
        display: block;
        width: 100%;
        text-align: center;
    }

    /* Estilo dos botões do menu */
    .sidebar-button {
        background-color: #1f1f1f;
        padding: 0.75rem;
        border-radius: 12px;
        margin-bottom: 10px;
        font-weight: bold;
        transition: 0.3s;
        border: 1px solid #444;
    }

    .sidebar-button:hover {
        background-color: #444;
    }

    .sidebar-button.active {
        background-color: #3399FF;
        color: white !important;
        border: none;
    }

    .sidebar-button.active a {
        color: white !important;
    }

    .css-1d391kg {  /* Texto no sidebar */
        color: white !important;
    }

    .css-1v0mbdj {  /* Fundo geral */
        background-color: #121212;
    }
    </style>
""", unsafe_allow_html=True)

# Navegação
abas = {
    "Carteira de Pedido": "📦",
    "Contrato": "📄",
    "Estoque": "📊"
}

# Controle via query params
query_params = st.query_params
aba_atual = query_params.get("page", "Carteira de Pedido")

with st.sidebar:
    st.markdown("### 📁 <span style='color:gold;'>Navegação</span>", unsafe_allow_html=True)
    for aba in abas:
        classe = "sidebar-button"
        if aba == aba_atual:
            classe += " active"
        st.markdown(
            f'<div class="{classe}"><a href="?page={aba}">{abas[aba]} {aba}</a></div>',
            unsafe_allow_html=True
        )

# Conteúdo da página
st.title(f"{abas[aba_atual]} {aba_atual}")

if aba_atual == "Carteira de Pedido":
    arquivo = st.file_uploader("📂 Envie sua planilha Excel", type=["xlsx"])
    if arquivo:
        df = pd.read_excel(arquivo, skiprows=11)

        tipos_produto = df["TIPO DE PRODUTO"].dropna().unique()
        tipo_selecionado = st.selectbox("Filtrar por tipo de produto", tipos_produto)

        df_filtrado = df[df["TIPO DE PRODUTO"] == tipo_selecionado]

        qtd_pedidos = df_filtrado.shape[0]
        volume_total = df_filtrado["VL TOTAL"].sum()

        col1, col2 = st.columns(2)
        col1.metric("Quantidade de Pedidos", qtd_pedidos)
        fig = px.pie(
            values=[volume_total, 0.01],
            names=[f"{tipo_selecionado}", ""],
            hole=0.5,
            color_discrete_sequence=["#3399FF", "#e0e0e0"]
        )
        fig.update_layout(showlegend=False)
        col2.plotly_chart(fig, use_container_width=True)

elif aba_atual == "Contrato":
    st.write("🔧 Página de Contrato em construção...")

elif aba_atual == "Estoque":
    st.write("📦 Página de Estoque em construção...")
