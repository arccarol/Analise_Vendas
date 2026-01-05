
# IMPORTAÇÕES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta
from matplotlib.ticker import FuncFormatter
import os


# FUNÇÃO PARA GERAR DADOS FICTÍCIOS


def dsa_gera_dados_ficticios(num_registros=600):
    """
    Gera um DataFrame do Pandas com dados de vendas fictícios.
    """
    print(f"\nIniciando a geração de {num_registros} registros de vendas...")

    produtos = {
        'Laptop Gamer': {'categoria': 'Eletrônicos', 'preco': 7500.00},
        'Mouse Vertical': {'categoria': 'Acessórios', 'preco': 250.00},
        'Teclado Mecânico': {'categoria': 'Acessórios', 'preco': 550.00},
        'Monitor Ultrawide': {'categoria': 'Eletrônicos', 'preco': 2800.00},
        'Cadeira Gamer': {'categoria': 'Móveis', 'preco': 1200.00},
        'Headset 7.1': {'categoria': 'Acessórios', 'preco': 800.00},
        'Placa de Vídeo': {'categoria': 'Hardware', 'preco': 4500.00},
        'SSD 1TB': {'categoria': 'Hardware', 'preco': 600.00}
    }

    cidades_estados = {
        'São Paulo': 'SP',
        'Rio de Janeiro': 'RJ',
        'Belo Horizonte': 'MG',
        'Porto Alegre': 'RS',
        'Salvador': 'BA',
        'Curitiba': 'PR',
        'Fortaleza': 'CE'
    }

    lista_produtos = list(produtos.keys())
    lista_cidades = list(cidades_estados.keys())
    dados_vendas = []

    data_inicial = datetime(2026, 1, 1)

    for i in range(num_registros):
        produto_nome = random.choice(lista_produtos)
        cidade = random.choice(lista_cidades)
        quantidade = np.random.randint(1, 8)

        data_pedido = data_inicial + timedelta(
            days=int(i / 5),
            hours=random.randint(0, 23)
        )

        if produto_nome in ['Mouse Vertical', 'Teclado Mecânico']:
            preco_unitario = produtos[produto_nome]['preco'] * np.random.uniform(0.9, 1.0)
        else:
            preco_unitario = produtos[produto_nome]['preco']

        dados_vendas.append({
            'ID_Pedido': 1000 + i,
            'Data_Pedido': data_pedido,
            'Nome_Produto': produto_nome,
            'Categoria': produtos[produto_nome]['categoria'],
            'Preco_Unitario': round(preco_unitario, 2),
            'Quantidade': quantidade,
            'ID_Cliente': np.random.randint(100, 150),
            'Cidade': cidade,
            'Estado': cidades_estados[cidade]
        })

    print("Geração de dados concluída.\n")
    return pd.DataFrame(dados_vendas)


# FUNÇÃO PARA SALVAR GRÁFICOS


def salvar_grafico(figura, nome_arquivo):
    if not os.path.exists("figuras"):
        os.makedirs("figuras")
    caminho = os.path.join("figuras", nome_arquivo)
    figura.savefig(caminho, bbox_inches='tight')
    print(f" Gráfico salvo em: {caminho}")


# FUNÇÃO PRINCIPAL


def main():
    sns.set_style("whitegrid")

    # Geração dos dados
    df_vendas = dsa_gera_dados_ficticios(500)

    # Conversão de data
    df_vendas['Data_Pedido'] = pd.to_datetime(df_vendas['Data_Pedido'])

    # Engenharia de atributos
    df_vendas['Faturamento'] = df_vendas['Preco_Unitario'] * df_vendas['Quantidade']
    df_vendas['Status_Entrega'] = df_vendas['Estado'].apply(
        lambda x: 'Rápida' if x in ['SP', 'RJ', 'MG'] else 'Normal'
    )
    df_vendas['Mes'] = df_vendas['Data_Pedido'].dt.to_period('M')

  
    # SALVAR CSV FINAL
  
    if not os.path.exists("data"):
        os.makedirs("data")
    arquivo_csv_final = "data/vendas_ficticias_modificado.csv"
    df_vendas.to_csv(arquivo_csv_final, index=False)
    print(f"\n CSV final salvo em: {arquivo_csv_final}\n")

 
    # TOP PRODUTOS

    top_produtos = df_vendas.groupby('Nome_Produto')['Quantidade'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(12,7))
    top_produtos.sort_values().plot(kind='barh', ax=ax, color='skyblue')
    ax.set_title('Top 10 Produtos Mais Vendidos')
    ax.set_xlabel('Quantidade Vendida')
    ax.set_ylabel('Produto')
    plt.tight_layout()
    plt.show()
    salvar_grafico(fig, "top_10_produtos.png")


    # FATURAMENTO MENSAL
   
    faturamento_mensal = df_vendas.groupby('Mes')['Faturamento'].sum()
    faturamento_mensal.index = faturamento_mensal.index.strftime('%Y-%m')
    fig, ax = plt.subplots(figsize=(12,6))
    faturamento_mensal.plot(marker='o', ax=ax, color='green')
    ax.set_title('Evolução do Faturamento Mensal')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Faturamento (R$)')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    salvar_grafico(fig, "faturamento_mensal.png")

    
    # FATURAMENTO POR ESTADO
  
    vendas_estado = df_vendas.groupby('Estado')['Faturamento'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12,7))
    vendas_estado.plot(kind='bar', ax=ax, color=sns.color_palette("husl", len(vendas_estado)))
    ax.set_title('Faturamento por Estado')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Faturamento (R$)')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
    salvar_grafico(fig, "faturamento_estado.png")

   
    # FATURAMENTO POR CATEGORIA
   
    faturamento_categoria = df_vendas.groupby('Categoria')['Faturamento'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12,7))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'R$ {y/1000:,.0f}K'))
    faturamento_categoria.plot(kind='bar', ax=ax, color=sns.color_palette("viridis", len(faturamento_categoria)))
    ax.set_title('Faturamento por Categoria')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Faturamento')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    salvar_grafico(fig, "faturamento_categoria.png")



# EXECUÇÃO


if __name__ == "__main__":
    main()
