import streamlit as st
import pandas as pd

from buildmockdb import create_db
from metrics import dashboard_loja

from charts import (
    grafico_faturamento_loja,
    grafico_funil,
    heatmap_canal_loja,
    conversao_por_canal,
    ranking_fonos
)

st.set_page_config(
    page_title="Dashboard Audivida",
    layout="wide"
)

st.title("Dashboard Marketing Audivida")

# --------------------
# CACHE
# --------------------

@st.cache_data
def carregar_dados():
    return create_db(1000)

df = carregar_dados()

df['data_atendimento'] = pd.to_datetime(df['data_atendimento'])

# --------------------
# SIDEBAR
# --------------------

st.sidebar.header("Filtros")

lojas = sorted(df["loja"].unique())
canais = sorted(df["canal_lead"].unique())

loja_filtro = st.sidebar.multiselect(
    "Loja",
    lojas,
    default=lojas
)

canal_filtro = st.sidebar.multiselect(
    "Canal",
    canais,
    default=canais
)

data_min = df["data_atendimento"].min()
data_max = df["data_atendimento"].max()

data_range = st.sidebar.date_input(
    "Período",
    [data_min, data_max]
)

# --------------------
# FILTROS
# --------------------

df_filtrado = df[
    (df["loja"].isin(loja_filtro)) &
    (df["canal_lead"].isin(canal_filtro)) &
    (df["data_atendimento"] >= pd.to_datetime(data_range[0])) &
    (df["data_atendimento"] <= pd.to_datetime(data_range[1]))
]

metrics = dashboard_loja(df_filtrado)

# --------------------
# KPIs
# --------------------

faturamento = df_filtrado["valor_total"].sum()
aparelhos = df_filtrado["quantidade_aparelhos"].sum()
ticket = faturamento / aparelhos if aparelhos else 0
conversao = metrics["pct_conversao"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Faturamento", f"R$ {faturamento:,.0f}")
col2.metric("Aparelhos vendidos", int(aparelhos))
col3.metric("Ticket médio", f"R$ {ticket:,.0f}")
col4.metric("Conversão média", f"{conversao:.1%}")

st.divider()


#Styles

st.dataframe(
    metrics.style.format({
        "faturamento": "R$ {:,.0f}",
        "ticket_medio": "R$ {:,.0f}",
        "pct_conversao": "{:.1%}",
        "pct_comparecimento": "{:.1%}"
    })
)

# --------------------
# GRÁFICOS
# --------------------

colA, colB = st.columns(2)

with colA:
    st.subheader("Faturamento por Loja")
    st.pyplot(grafico_faturamento_loja(metrics))

with colB:
    st.subheader("Funil de Vendas")
    st.pyplot(grafico_funil(df_filtrado))

colC, colD = st.columns(2)

with colC:
    st.subheader("Heatmap Canal × Loja")
    st.pyplot(heatmap_canal_loja(df_filtrado))

with colD:
    st.subheader("Conversão por Canal")
    st.pyplot(conversao_por_canal(df_filtrado))

st.subheader("Ranking de Fonoaudiólogos")
st.pyplot(ranking_fonos(df_filtrado))

st.divider()

st.subheader("Dados detalhados")
st.dataframe(df_filtrado, use_container_width=True)


# -------------------------
# TABELAS
# -------------------------

# Formatação dos dados para mostrar na tabela
# metrics['faturamento'] = metrics['faturamento'].map('R${:,.2f}'.format)
# metrics['ticket_medio'] = metrics['ticket_medio'].map('R${:,.2f}'.format)
# metrics['pct_comparecimento'] = metrics['pct_comparecimento'].astype(float).map('{:.2%}'.format)
# metrics['pct_conversao'] = metrics['pct_conversao'].astype(float).map('{:.2%}'.format)

# st.subheader("Métricas por loja")
# st.dataframe(metrics, use_container_width=True)