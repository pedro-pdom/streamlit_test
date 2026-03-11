import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter

sns.set_theme(style="whitegrid")

# ----------------------------
# FORMATADORES
# ----------------------------

def moeda(x, pos):
    return f"R$ {x:,.0f}"

def porcentagem(x, pos):
    return f"{x:.0%}"


# ----------------------------
# FATURAMENTO POR LOJA
# ----------------------------

def grafico_faturamento_loja(metrics):

    fig, ax = plt.subplots(figsize=(10,5))

    df = metrics.sort_values("faturamento", ascending=False)

    sns.barplot(
        data=df,
        x="faturamento",
        y="loja",
        palette="viridis",
        ax=ax
    )

    ax.xaxis.set_major_formatter(FuncFormatter(moeda))

    for i, v in enumerate(df["faturamento"]):
        ax.text(v, i, f" R$ {v:,.0f}", va="center")

    ax.set_title("Faturamento por Loja", fontsize=14, weight="bold")
    ax.set_xlabel("")
    ax.set_ylabel("")

    return fig


# ----------------------------
# FUNIL COMERCIAL
# ----------------------------

def grafico_funil(df):

    funil = df.agg({
        "agendamento":"sum",
        "comparecimento":"sum",
        "venda":"sum"
    })

    funil = funil.reset_index()
    funil.columns = ["etapa","valor"]

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        data=funil,
        x="etapa",
        y="valor",
        palette="Set2",
        ax=ax
    )

    for i, v in enumerate(funil["valor"]):
        ax.text(i, v, f"{int(v):,}", ha="center", va="bottom")

    ax.set_title("Funil Comercial")

    return fig


# ----------------------------
# HEATMAP CANAL X LOJA
# ----------------------------

def heatmap_canal_loja(df):

    pivot = df.pivot_table(
        values="valor_total",
        index="loja",
        columns="canal_lead",
        aggfunc="sum"
    )

    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        pivot,
        cmap="YlGnBu",
        annot=True,
        fmt=",.0f",
        linewidths=0.5,
        ax=ax,
        cbar_kws={"format": FuncFormatter(moeda)}
    )

    ax.set_title("Faturamento por Canal e Loja")

    return fig


# ----------------------------
# CONVERSÃO POR CANAL
# ----------------------------

def conversao_por_canal(df):

    canal = df.groupby("canal_lead").agg(
        leads=("agendamento","sum"),
        vendas=("venda","sum")
    ).reset_index()

    canal["conversao"] = canal["vendas"] / canal["leads"]

    canal = canal.sort_values("conversao", ascending=False)

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=canal,
        x="conversao",
        y="canal_lead",
        palette="magma",
        ax=ax
    )

    ax.xaxis.set_major_formatter(FuncFormatter(porcentagem))

    for i, v in enumerate(canal["conversao"]):
        ax.text(v, i, f" {v:.1%}", va="center")

    ax.set_title("Conversão por Canal")

    return fig


# ----------------------------
# RANKING DE FONOS
# ----------------------------

def ranking_fonos(df):

    fono = df.groupby("fono").agg(
        vendas=("venda","sum"),
        faturamento=("valor_total","sum")
    ).reset_index()

    fono = fono.sort_values("faturamento", ascending=False)

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=fono,
        x="faturamento",
        y="fono",
        palette="crest",
        ax=ax
    )

    ax.xaxis.set_major_formatter(FuncFormatter(moeda))

    for i, v in enumerate(fono["faturamento"]):
        ax.text(v, i, f" R$ {v:,.0f}", va="center")

    ax.set_title("Ranking de Fonoaudiólogos")

    return fig