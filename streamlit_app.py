import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard - Carteira de Pedido")

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

# Sidebar navigation
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

# Página: Carteira de Pedido
if pagina == "carteira":
    st.title("📦 Carteira de Pedido")

    arquivo = st.file_uploader("📂 Envie sua planilha Excel", type=["xlsx"])

    if arquivo:
        df = pd.read_excel(arquivo)  # << sem skiprows!

        if "TIPO DE PRODUTO" in df.columns:
            tipos_produto = df["TIPO DE PRODUTO"].dropna().unique()
            tipo_selecionado = st.selectbox("Selecione o tipo de produto:", tipos_produto)

            df_filtrado = df[df["TIPO DE PRODUTO"] == tipo_selecionado]

            qtd_pedidos = len(df_filtrado)
            st.metric("Quantidade total de pedidos", qtd_pedidos)

            if "VOLUME" in df_filtrado.columns:
                volume_total = df_filtrado["VOLUME"].sum()
                fig = px.pie(
                    df_filtrado,
                    names="TIPO DE PRODUTO",
                    values="VOLUME",
                    hole=0.5,
                    title="Volume total por tipo de produto"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("A coluna 'VOLUME' não foi encontrada.")
        else:
            st.warning("A coluna 'TIPO DE PRODUTO' não foi encontrada na planilha.")

# Página: Contrato
elif pagina == "contrato":
    st.title("📑 Contrato")
    st.info("Conteúdo da aba 'Contrato' ainda será implementado.")

# Página: Estoque
elif pagina == "estoque":
    st.title("📦 Estoque")
    st.info("Conteúdo da aba 'Estoque' ainda será implementado.")