import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard de Pedidos", layout="wide")

# Estilização do menu lateral
st.markdown("""
    <style>
    .sidebar-buttons a {
        display: block;
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        background-color: #2c3e50;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    .sidebar-buttons a.selected {
        background-color: #1abc9c !important;
    }
    .sidebar-buttons a:hover {
        background-color: #16a085;
    }
    .css-1d391kg {  /* Cor da fonte na página principal */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar com logo e navegação
with st.sidebar:
    st.image("logomars.png", use_container_width=True)  # Logo
    st.markdown("## 🧭 Navegação", unsafe_allow_html=True)

    selected = st.session_state.get("selected_page", "Carteira de Pedido")

    st.markdown(
        f"""
        <div class="sidebar-buttons">
            <a href="?page=Carteira+de+Pedido" class="button {'selected' if selected == 'Carteira de Pedido' else ''}">Carteira de Pedido</a>
            <a href="?page=Contrato" class="button {'selected' if selected == 'Contrato' else ''}">Contrato</a>
            <a href="?page=Estoque" class="button {'selected' if selected == 'Estoque' else ''}">Estoque</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Atualiza página com base na navegação
query_params = st.query_params
page = query_params.get("page", ["Carteira de Pedido"])[0]
st.session_state["selected_page"] = page

# -------------------- ABA CARTEIRA DE PEDIDO --------------------
if page == "Carteira de Pedido":
    st.title("📦 Carteira de Pedido")

    arquivo = st.file_uploader("📂 Envie sua planilha Excel", type=["xlsx"])
    if arquivo:
        df = pd.read_excel(arquivo)

        df["Shipping Date"] = pd.to_datetime(df["Shipping Date"], errors="coerce")
        df["Month"] = df["Shipping Date"].dt.strftime('%B/%Y')  # ex: April/2025

        # Filtro por tipo de produto
        tipos_produto = df["Material Group"].dropna().unique()
        tipos_produto = sorted(tipos_produto)
        tipos_produto.insert(0, "Todos os produtos")
        tipo_selecionado = st.selectbox("🎯 Tipo de Produto", tipos_produto)

        # Filtro por mês
        meses_disponiveis = df["Month"].dropna().unique()
        meses_disponiveis = sorted(meses_disponiveis, key=lambda x: datetime.strptime(x, "%B/%Y"))
        mes_selecionado = st.selectbox("📅 Mês do Embarque", ["Todos os meses"] + list(meses_disponiveis))

        # Aplicar filtros
        df_filtrado = df.copy()
        if tipo_selecionado != "Todos os produtos":
            df_filtrado = df_filtrado[df_filtrado["Material Group"] == tipo_selecionado]
        if mes_selecionado != "Todos os meses":
            df_filtrado = df_filtrado[df_filtrado["Month"] == mes_selecionado]

        # Métricas
        qtd_pedidos = df_filtrado["Purchase Order"].nunique()
        volume_total = df_filtrado["Volume"].sum()

        col1, col2 = st.columns(2)
        col1.metric("📌 Nº de Pedidos", qtd_pedidos)
        col2.metric("📦 Volume Total", f"{volume_total:,.0f}")

        # Gráfico de rosca
        graf_donut = px.pie(df_filtrado, names="Material Group", values="Volume", hole=0.5,
                            title="Distribuição de Volume por Tipo de Produto")
        st.plotly_chart(graf_donut, use_container_width=True)

        # Tabela com colunas selecionadas
        st.subheader("📄 Detalhamento dos Pedidos")
        colunas_exibir = ["Delivery Date", "Purchase Order", "Volume", "MARS Material SKU", "Material Group"]
        st.dataframe(df_filtrado[colunas_exibir], use_container_width=True)

# -------------------- ABA CONTRATO --------------------
elif page == "Contrato":
    st.title("📑 Contrato")
    st.info("Em desenvolvimento...")

# -------------------- ABA ESTOQUE --------------------
elif page == "Estoque":
    st.title("📊 Estoque")
    st.info("Em desenvolvimento...")