def dashboard_loja(df):

    d = df.groupby("loja").agg(

        agendamentos=("agendamento","sum"),
        comparecimentos=("comparecimento","sum"),
        vendas=("venda","sum"),
        aparelhos=("quantidade_aparelhos","sum"),
        faturamento=("valor_total","sum")

    ).reset_index()

    d["pct_comparecimento"] = d["comparecimentos"]/d["agendamentos"]

    d["pct_conversao"] = d["vendas"]/d["comparecimentos"]

    d["oportunidades"] = d["comparecimentos"] - d["vendas"]

    d["ticket_medio"] = d["faturamento"]/d["aparelhos"]

    return d