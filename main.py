import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregar ou criar o arquivo CSV de compras
try:
    dados = pd.read_csv("compras.csv")
except FileNotFoundError:
    dados = pd.DataFrame({"PRODUTO": [], "PRECO": []})
    dados.to_csv("compras.csv", index=False)

# Título do aplicativo
st.title("Controle de Gastos")
orcamento = st.number_input("Orçamento:", min_value=0.0)

# Calcular o total de gastos
total = dados["PRECO"].sum() if not dados.empty else 0

# Formulário para adicionar nova compra
with st.form("nova_compra"):
    produto = st.text_input("Produto:")
    preco = st.number_input("Preço:", min_value=0.0)
    if st.form_submit_button("Adicionar"):
        if preco <= (orcamento - total):
            nova_linha = pd.DataFrame({"PRODUTO": [produto], "PRECO": [preco]})
            dados = pd.concat([dados, nova_linha], ignore_index=True)
            dados.to_csv("compras.csv", index=False)
            st.success("Compra adicionada!")
        else:
            st.error("Sem orçamento suficiente!")

# Exibir o gráfico e os dados
if orcamento > 0:
    fig, ax = plt.subplots(figsize=(8, 8))
    if not dados.empty:
        produtos = dados["PRODUTO"].tolist()
        valores = dados["PRECO"].tolist()
        restante = orcamento - total
        if restante > 0:
            produtos.append("Disponível")
            valores.append(restante)
        ax.pie(valores, labels=produtos, autopct='%1.1f%%', pctdistance=0.85)
        plt.title(f"Orçamento: {orcamento}€")
        centro = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centro)
        st.pyplot(fig)

    st.dataframe(dados)
    st.write(f"Total Gasto: {total}€")
    st.write(f"Resta: {orcamento - total}€")
