import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from faker import Faker
import random

# ---------------------------
    # CONFIGURAÇÕES
    # ---------------------------
lojas = [
    "Shopping Recife",
    "Shopping Guararapes",
    "Shopping Paulista",
    "Praça do Derby"
]

produtos = [
    "Aparelho Basic",
    "Aparelho Premium",
    "Aparelho Recarga",
    "Aparelho Invisível"
]

canais_lead = [
    "Internet",
    "Passante",
    "Médico",
    "Indicação",
    "Campanha TV",
    "Instagram",
    "Google Ads"
]

fonos = [
    "Dra. Ana",
    "Dr. Carlos",
    "Dra. Juliana",
    "Dr. Marcos"
]

def create_db(n=800):
    fake = Faker("pt_BR")

    dados = []

    for _ in range(n):

        quantidade = np.random.choice([1,2,2,4])

        valor_unitario = np.random.randint(2000, 9000)

        loja = random.choice(lojas)

        comparecimento = np.random.choice([0,1], p=[0.3,0.7])

        venda = 1 if comparecimento and np.random.rand() < 0.55 else 0

        valor_total = quantidade * valor_unitario if venda else 0

        dados.append({
            "data_atendimento": fake.date_between("-30d","today"),
            "paciente": fake.name(),
            "loja": loja,
            "produto": random.choice(produtos),
            "quantidade_aparelhos": quantidade if venda else 0,
            "valor_unitario": valor_unitario if venda else 0,
            "valor_total": valor_total,
            "canal_lead": random.choice(canais_lead),
            "indicacao": fake.name() if np.random.rand() < 0.2 else None,
            "fono": random.choice(fonos),
            "agendamento": 1,
            "comparecimento": comparecimento,
            "venda": venda
        })
    
    return pd.DataFrame(dados)