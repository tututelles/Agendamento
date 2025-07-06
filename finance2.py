import yfinance as yf
import pandas as pd
import datetime
import numpy as np
np.float_ = np.float64

minha_lista = []
# Definir os ativos (incluindo AMX, AAPL e PETR4)
ativos = ["AMX", "AAPL", "PETR4.SA", "ITUB3.SA", "VALE3.SA", "PETR3.SA", "^BVSP"]

# Definir o período para hoje (tempo real)
hoje = datetime.datetime.now()
data_inicial = hoje - datetime.timedelta(days=1)  # Últimos 2 dias
data_final = hoje

try:
    # Baixar os dados
    dados = yf.download(ativos, start=data_inicial, end=data_final, group_by='ticker')
    
    if dados.empty:
        print("Nenhum dado encontrado. Verifique os tickers e sua conexão com a internet.")
    else:
        # Mostrar os dados mais recentes (último pregão)
        print("\nÚltimas cotações:")
        for acao in ativos:
            if acao in dados:
                ultimo_preco = dados[acao].iloc[-1]['Close']
                print(f"{acao}: {ultimo_preco:.2f}")
                
                # Adicionar o quadrado do último preço à lista
                x = ultimo_preco
                y = np.power(x,2)

                z = y.item()
                minha_lista.append(z)
    
        # Se quiser ver todo o dataframe com todos os dados
        #print("\nTodos os dados baixados:")
        #print(dados)
        
except Exception as e:
    print(f"Erro ao buscar dados: {str(e)}")
    print("Possíveis causas:")
    print("- Algum ticker pode estar incorreto")
    print("- Problema de conexão com a internet")
    print("- Limitação da API (muitas requisições)")

# Exibir a lista com os valores quadrados
print("Valores quadrados das ações:", minha_lista)

# Salvar os valores em um arquivo Excel
import openpyxl

# Criar ou abrir o arquivo Excel
arquivo = openpyxl.Workbook()
sheet = arquivo.active
sheet.title = "Valores Ações"

# Adicionar os valores à planilha
for i, valor in enumerate(minha_lista, start=1):
    sheet[f'A{i}'] = valor

# Salvar o arquivo
arquivo.save("valores.xlsx")
print("Dados salvos em 'valores.xlsx'.")
