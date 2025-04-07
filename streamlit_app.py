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

        if "material group" in df.columns:
            tipos_produto = df["material group"].dropna().unique()
            tipo_selecionado = st.selectbox("Selecione o tipo de produto:", tipos_produto)

            df_filtrado = df[df["material group"] == tipo_selecionado]

            qtd_pedidos = len(df_filtrado)
            st.metric("Total de pedidos", qtd_pedidos)

            if "Volume" in df_filtrado.columns:
                st.subheader("🔘 Distribuição do Volume")
                fig = px.pie(
                    df_filtrado,
                    names="material group",
                    values="Volume",
                    hole=0.5,
                    title="Volume total por tipo de produto"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("A coluna 'Volume' não foi encontrada.")

            # Tabela com colunas desejadas
            st.subheader("📋 Tabela de Pedidos")
            colunas_desejadas = ["Delivery Date", "Purchase Order", "Volume", "MARS Material SKU", "material group"]
            colunas_disponiveis = [col for col in colunas_desejadas if col in df_filtrado.columns]

            if colunas_disponiveis:
                st.dataframe(df_filtrado[colunas_disponiveis], use_container_width=True)
            else:
                st.warning("Nenhuma das colunas desejadas foi encontrada nos dados.")
        else:
            st.warning("A coluna 'material group' não foi encontrada na planilha.")

# Aba: Contrato
elif pagina == "contrato":
    st.title("📑 Contrato")
    st.info("A aba 'Contrato' será implementada em breve.")

# Aba: Estoque
elif pagina == "estoque":
    st.title("📦 Estoque")
    st.info("A aba 'Estoque' será implementada em breve.")