import streamlit as st
from buildmockdb import create_db
from metrics import dashboard_loja
from charts import grafico_faturamento_loja, grafico_funil

st.set_page_config(
    page_title="Dashboard Audiologia",
    layout="wide"
)

st.title("Dashboard Comercial de Aparelhos Auditivos")


df = create_db(800)

loja_filtro = st.sidebar.multiselect(
    "Selecionar lojas",
    df["loja"].unique(),
    default=df["loja"].unique()
)

df = df[df["loja"].isin(loja_filtro)]


metrics = dashboard_loja(df)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Faturamento total",
    f"R$ {df['valor_total'].sum():,.0f}"
)

col2.metric(
    "Aparelhos vendidos",
    int(df["quantidade"].sum())
)

col3.metric(
    "Conversão média",
    f"{metrics['pct_conversao'].mean():.1%}"
)


st.subheader("Faturamento por Loja")
st.pyplot(grafico_faturamento_loja(metrics))


st.subheader("Funil Comercial")
st.pyplot(grafico_funil(df))


st.subheader("Dados detalhados")
st.dataframe(df)