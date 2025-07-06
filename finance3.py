import yfinance as yf
import pandas as pd
import datetime
import numpy as np
import openpyxl
import os

np.float_ = np.float64
nomes_ativos= []
minha_lista = []
ativos = ["AMX", "AAPL", "PETR4.SA", "ITUB3.SA", "VALE3.SA", "PETR3.SA", "^BVSP"]
arquivo_excel = "valores.xlsx"

# Obter dados das ações
hoje = datetime.datetime.now()
data_inicial = hoje - datetime.timedelta(days=1)
data_final = hoje

try:
    dados = yf.download(ativos, start=data_inicial, end=data_final, group_by='ticker')
    
    if dados.empty:
        print("Nenhum dado encontrado. Verifique os tickers e sua conexão com a internet.")
    else:
        print("\nÚltimas cotações:")
        for acao in ativos:
            if acao in dados:
                ultimo_preco = dados[acao].iloc[-1]['Close']
                print(f"{acao}: {ultimo_preco:.2f}")
                z =(ultimo_preco)
                minha_lista.append(z)
                nomes_ativos.append(acao)
    
except Exception as e:
    print(f"Erro ao buscar dados: {str(e)}")

# Gerenciar o arquivo Excel
try:
    # Verifica se o arquivo existe
    if os.path.exists(arquivo_excel):
        arquivo = openpyxl.load_workbook(arquivo_excel)
        sheet = arquivo.active
        
        # Limpa apenas a coluna B mantendo outras colunas
        for row in sheet.iter_rows():
            if row[1].value:  # A coluna B é o índice 1 (0-based)
                row[1].value = None
    else:
        arquivo = openpyxl.Workbook()
        sheet = arquivo.active
        sheet.title = "Valores Ações"
    
    # Adicionar valores na coluna B
    for i, nome in enumerate(nomes_ativos, start=1):
        sheet[f'C{i}'] = nome
    for i, valor in enumerate(minha_lista, start=1):
        sheet[f'B{i}'] = valor
    
    # Salvar mantendo formatação existente
    arquivo.save(arquivo_excel)
    print(f"\nDados atualizados com sucesso no arquivo {arquivo_excel}")
    
except Exception as e:
    print(f"\nErro ao atualizar o arquivo Excel: {str(e)}")
    print("Certifique-se que o arquivo não está aberto em outro programa")

# Versão alternativa que garante a atualização mesmo se houver erros:
# with pd.ExcelWriter(arquivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
#     df = pd.DataFrame({'Valores Quadrados': minha_lista})
#     df.to_excel(writer, sheet_name='Dados', index=False, startcol=1)
