import streamlit as st
import pandas as pd
import matplotlib as plt

try:
    dados = pd.read_csv("compras.csv")
except FileNotFoundError:
    dados = pd.DataFrame({"Produto": [], "Preço": []})
    dados.to_csv("compras.csv", index=False)

st.title("Controlo de Gastos")

orcamento = st.number_input("Indique o orçamento:", min_value=0.0)
total = dados["Preço"].sum() if not dados.empty else 0

with st.form("nova_compra"):
    produto = st.text_input("Adicione o produto:")
    preco = st.number_input("Indique o preço do produto:", min_value=0.0)
    submit_button = st.form_submit_button("Adicionar")

    if submit_button:
        if preco <= (orcamento - total):
            new_line = pd.DataFrame({"Produto": [produto], "Preço": [preco]})
            dados = pd.concat([dados, new_line], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Produto adicionado")
        else:
            st.error("Orçamento Insuficiente")

if orcamento > 0:
    fig, ax = plt.subplot(figsize=(8, 8))
    produtos = dados["Produto"].tolist()
    valores = dados["Preço"].tolist()

    restante = orcamento - total
    if restante > 0:
        produtos.append("Disponível")
        valores.append(restante)

    plt.pie(
        valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85
    )

    plt.title(f"Orçamento: {orcamento}€")

    centro = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(centro)

    st.pyplot(fig)

st.dataframe(dados)
st.write(f"Total Gasto: {total}€")
st.write(f"Resta: {orcamento - total}€")
