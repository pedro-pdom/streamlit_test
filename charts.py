import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

def grafico_dashboardlojas(df):
    fig, ax = plt.subplots(figsize=(12,6))

    df_plot = df.sort_values("faturamento", ascending=False)

    sns.barplot(
        data=df_plot,
        x="faturamento",
        y="loja",
        palette="viridis",
        ax=ax
    )

    for i, v in enumerate(df_plot["faturamento"]):
        ax.text(v + 5000, i, f"R$ {v:,.0f}", va="center")

    ax.set_title("Faturamento por Loja", fontsize=16, weight="bold")
    ax.set_xlabel("Faturamento (R$)")
    ax.set_ylabel("")

    fig.tight_layout()

    return fig

def grafico_faturamento_loja(df):

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=df.sort_values("faturamento",ascending=False),
        x="faturamento",
        y="loja",
        palette="viridis",
        ax=ax
    )

    ax.set_title("Faturamento por Loja")

    return fig


def grafico_funil(df):

    funil = df.groupby("loja").agg(
        agendamentos=("agendamento","sum"),
        comparecimentos=("comparecimento","sum"),
        vendas=("venda","sum")
    ).reset_index()

    funil_long = funil.melt(id_vars="loja")

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=funil_long,
        x="loja",
        y="value",
        hue="variable",
        palette="Set2",
        ax=ax
    )

    ax.set_title("Funil Comercial")

    return fig