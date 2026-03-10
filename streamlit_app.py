import streamlit as st
from buildmockdb import create_db
from metrics import dashboard_loja
from charts import grafico_faturamento_loja, grafico_funil, grafico_dashboardlojas
import pandas as pd

st.set_page_config(
    page_title="Dashboard Audivida",
    layout="wide"
)

st.title("Dashboard Comercial de Aparelhos Auditivos")

# -------------------------
# CACHE DOS DADOS
# -------------------------

@st.cache_data
def carregar_dados():
    return create_db(800)

df = carregar_dados()

df["data_atendimento"] = pd.to_datetime(df["data_atendimento"])

# -------------------------
# SIDEBAR FILTROS
# -------------------------

st.sidebar.header("Filtros")

lojas = sorted(df["loja"].unique())
canais = sorted(df["canal_lead"].unique())

loja_filtro = st.sidebar.multiselect(
    "Selecionar lojas",
    options=lojas,
    default=lojas
)

canal_filtro = st.sidebar.multiselect(
    "Selecionar canais",
    options=canais,
    default=canais
)

# filtro de data
data_min = df["data_atendimento"].min()
data_max = df["data_atendimento"].max()

data_range = st.sidebar.date_input(
    "Período",
    [data_min, data_max]
)

# -------------------------
# APLICAR FILTROS
# -------------------------

df_filtrado = df[
    (df["loja"].isin(loja_filtro)) &
    (df["canal_lead"].isin(canal_filtro)) &
    df["data_atendimento"].between(
        pd.to_datetime(data_range[0]),
        pd.to_datetime(data_range[1])
    )
]

metrics = dashboard_loja(df_filtrado)

# -------------------------
# MÉTRICAS PRINCIPAIS
# -------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Faturamento total",
    f"R$ {df_filtrado['valor_total'].sum():,.0f}"
)

col2.metric(
    "Aparelhos vendidos",
    int(df_filtrado["quantidade_aparelhos"].sum())
)

col3.metric(
    "Agendamentos",
    int(df_filtrado["agendamento"].sum())
)

col4.metric(
    "Conversão média",
    f"{metrics['pct_conversao'].mean():.1%}"
)

# -------------------------
# GRÁFICOS
# -------------------------

colA, colB = st.columns(2)

with colA:
    st.subheader("Faturamento por loja")
    st.pyplot(grafico_dashboardlojas(metrics))

with colB:
    st.subheader("Funil Comercial")
    st.pyplot(grafico_funil(df_filtrado))


# -------------------------
# TABELAS
# -------------------------

st.subheader("Métricas por loja")
st.dataframe(metrics, use_container_width=True)

st.subheader("Dados detalhados")
st.dataframe(df_filtrado, use_container_width=True)