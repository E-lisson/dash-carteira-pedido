import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Carteira de Pedido", layout="wide")

# Estilo customizado
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #0E1117;
            color: white;
        }
        .menu-button {
            display: block;
            width: 100%;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            background-color: #262730;
            color: white;
            text-align: left;
            border: none;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: bold;
        }
        .menu-button.selected {
            background-color: #1f77b4;
        }
        .menu-button:hover {
            background-color: #3e3f4b;
        }
        a {
            text-decoration: none !important;
            color: inherit !important;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar com imagem e menu estilizado
with st.sidebar:
    st.image("logomars.png", width=150)  # Logo
    st.markdown("## Navegação")
    aba_atual = st.query_params.get("aba", ["Carteira de Pedido"])[0]

    def menu_button(nome_aba):
        classe = "menu-button selected" if aba_atual == nome_aba else "menu-button"
        st.markdown(f'<a href="?aba={nome_aba}"><button class="{classe}">{nome_aba}</button></a>', unsafe_allow_html=True)

    menu_button("Carteira de Pedido")
    menu_button("Contrato")
    menu_button("Estoque")

# Captura da aba atual
aba = st.query_params.get("aba", ["Carteira de Pedido"])[0]

# Aba: Carteira de Pedido
if aba == "Carteira de Pedido":
    st.title("📦 Carteira de Pedido")

    arquivo = st.file_uploader("Envie sua planilha Excel", type=["xlsx"])

    if arquivo is not None:
        df = pd.read_excel(arquivo)

        # Corrigir nomes das colunas para garantir consistência
        df.columns = df.columns.str.strip()

        # Filtro por tipo de produto
        tipos_produto = df["Material Group"].dropna().unique()
        tipo_produto = st.selectbox("Selecione o tipo de produto", ["Todos os produtos"] + list(tipos_produto))

        if tipo_produto != "Todos os produtos":
            df = df[df["Material Group"] == tipo_produto]

        # Filtro por mês (Shipping Date)
        df["Shipping Date"] = pd.to_datetime(df["Shipping Date"], errors='coerce')
        df = df.dropna(subset=["Shipping Date"])

        df["Mês"] = df["Shipping Date"].dt.to_period("M").astype(str)
        meses = sorted(df["Mês"].unique())
        mes_selecionado = st.selectbox("Selecione o mês do pedido", ["Todos os meses"] + meses)

        if mes_selecionado != "Todos os meses":
            df = df[df["Mês"] == mes_selecionado]

        # Número total de pedidos
        num_pedidos = df["Purchase Order"].nunique()

        # Volume total
        volume_total = df["Volume"].sum()

        col1, col2 = st.columns(2)
        col1.metric("📄 Total de Pedidos", num_pedidos)
        col2.metric("📦 Volume Total", f"{volume_total:,.2f}")

        # Gráfico de rosca
        fig = px.pie(df, values="Volume", names="Material Group", hole=0.5,
                     title="Distribuição de Volume por Tipo de Produto")
        st.plotly_chart(fig, use_container_width=True)

        # Tabela com dados selecionados
        st.markdown("### 📊 Detalhamento dos Pedidos")
        colunas_desejadas = ["Delivery Date", "Purchase Order", "Volume", "MARS Material SKU", "Material Group"]
        st.dataframe(df[colunas_desejadas], use_container_width=True)

# Abas futuras
elif aba == "Contrato":
    st.title("📑 Contrato")
    st.info("Em breve, essa aba será alimentada com dados de contrato extraídos de outra planilha.")

elif aba == "Estoque":
    st.title("📦 Estoque")
    st.info("Em breve, essa aba será alimentada com dados de estoque extraídos de outra planilha.")
