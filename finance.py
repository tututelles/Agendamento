import yfinance as yf
import pandas as pd
import datetime

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
    
        # Se quiser ver todo o dataframe com todos os dados
        print("\nTodos os dados baixados:")
        print(dados)
        
except Exception as e:
    print(f"Erro ao buscar dados: {str(e)}")
    print("Possíveis causas:")
    print("- Algum ticker pode estar incorreto")
    print("- Problema de conexão com a internet")
    print("- Limitação da API (muitas requisições)")

