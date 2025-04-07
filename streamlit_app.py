import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard - Order Tracking")

# Estilo customizado
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: gold;
            margin-bottom: 20px;
        }
        .nav-button {
            display: block;
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
            background-color: #333;
            color: white;
            text-decoration: none;
            text-align: center;
            border: 1px solid transparent;
            transition: background-color 0.3s, border 0.3s;
        }
        .nav-button:hover {
            background-color: #444;
            border: 1px solid #888;
        }
        .nav-button.selected {
            background-color: #007bff;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Navegação lateral
st.sidebar.markdown('<div class="sidebar-title">📁 Navegação</div>', unsafe_allow_html=True)

abas = {
    "carteira": "Carteira de Pedido",
    "contrato": "Contrato",
    "estoque": "Estoque"
}

query = st.query_params.to_dict()
pagina = query.get("page", "carteira")

for key, nome in abas.items():
    selected = "selected" if pagina == key else ""
    st.sidebar.markdown(
        f'<a href="/?page={key}" class="nav-button {selected}">{nome}</a>',
        unsafe_allow_html=True
    )

# Aba: Carteira de Pedido
if pagina == "carteira":
    st.title("📦 Carteira de Pedido")

    arquivo = st.file_uploader("📂 Envie sua planilha Excel", type=["xlsx"])

    if arquivo:
        df = pd.read_excel(arquivo)

        if "Material Group" in df.columns:
            tipos_prod_
