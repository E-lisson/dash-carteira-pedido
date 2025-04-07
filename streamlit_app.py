import streamlit as st
import pandas as pd
import plotly.express as px

# ======= Estilo da Página =======
st.set_page_config(page_title="Dashboard", layout="wide")

st.markdown("""
    <style>
        body {
            color: white;
            background-color: #0f0f11;
        }
        .sidebar .sidebar-content {
            background-color: #1c1c1f;
        }
        .sidebar-title {
            font-weight: bold;
            font-size: 20px;
            color: #f1c40f;
            padding-bottom: 10px;
        }
        .nav-button {
            display: block;
            width: 100%;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
            background-color: #2c2f33;
            border-radius: 10px;
            border: 1px solid #444;
            color: white;
            text-align: center;
            text-decoration: none;
            font-weight: 500;
        }
        .nav-button:hover {
            background-color: #555;
            color: #fff;
        }
        .nav-button-active {
            background-color: #1e90ff;
            color: white;
            font-weight: bold;
        }
        .nav-button:visited {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ======= Função para Navegação =======
def menu_lateral():
    st.sidebar.markdown('<div class="sidebar-title">📂 Navegação</div>', unsafe_allow_html=True)
    aba = st.query_params.get("aba", ["Carteira de Pedido"])[0]

    def botao_nav(nome):
        classe = "nav-button"
        if aba == nome:
            classe += " nav-button-active"
        link = f"?aba={nome}"
        st.sidebar.markdown(f'<a href="{link}" class="{classe}">{nome}</a>', unsafe_allow_html=True)

    botoes = ["Carteira de Pedido", "Contrato", "Estoque"]
    for nome in botoes:
        botao_nav(nome)
    return aba

# ======= Página Principal =======
aba = menu_lateral()

# ======= Conteúdo por Página =======
if aba == "Carteira de Pedido":
    st.title("📦 Carteira de Pedido")

    arquivo = st.file_uploader("📤 Envie sua planilha Excel", type=["xlsx"])
    if arquivo:
        try:
            df = pd.read_excel(arquivo, skiprows=11)
            df = df.dropna(subset=["Purchase Order", "Volume", "MARS Material SKU"])

            # Normalizar o campo de tipo de produto
            df["Tipo de Produto"] = df["MARS Material SKU"].astype(str)

            tipos = df["Tipo de Produto"].unique().tolist()
            tipo_selecionado = st.selectbox("📌 Selecione o tipo de produto:", tipos)

            df_filtrado = df[df["Tipo de Produto"] == tipo_selecionado]

            col1, col2 = st.columns(2)

            with col1:
                total_pedidos = df_filtrado["Purchase Order"].nunique()
                st.metric("Total de Pedidos", total_pedidos)

            with col2:
                # Converter volume para float
                df_filtrado["Volume"] = (
                    df_filtrado["Volume"].astype(str)
                    .str.replace(".", "")
                    .str.replace(",", ".")
                    .astype(float)
                )

                fig = px.pie(
                    df_filtrado,
                    names="Purchase Order",
                    values="Volume",
                    title="Distribuição de Volume por Pedido",
                    hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao processar arquivo: {e}")

elif aba == "Contrato":
    st.title("📑 Contrato")
    st.info("Página de contratos em construção...")

elif aba == "Estoque":
    st.title("📦 Estoque")
    st.info("Página de estoque em construção...")