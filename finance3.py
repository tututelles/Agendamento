import yfinance as yf
import pandas as pd
import datetime
import numpy as np
import openpyxl
import os

np.float_ = np.float64
nomes_ativos= []
minha_lista = []
ativos = ["ABEV3", "ALPA4","ALUP11",
"ANIM3",
"ASAI3",
"AURE3",
"B3SA3",
"BBAS3",
"BBDC4",
"BBSE3",
"BEEF3",
"BHIA3",
"BLAU3",
"BRAP4",
"BRAV3",
"BRFS3",
"BRSR6",
"CASH3",
"CEAB3",
"CMIG4",
"CMIN3",
"COGN3",
"CSED3",
"CSNA3",
"CURY3",
"CVCB3",
"CXSE3",
"CYRE3",
"DIRR3",
"DXCO3",
"EGIE3",
"ELET3",
"EMBR3",
"EQTL3",
"EZTC3",
"FLRY3",
"GFSA3",
"GGBR4",
"GMAT3",
"GOAU4",
"HAPV3",
"HBSA3",
"HYPE3",
"ITSA4",
"ITUB4",
"JALL3",
"JBSS3",
"KEPL3",
"KLBN11",
"LEVE3",
"LREN3",
"LWSA3",
"MDIA3",
"MGLU3",
"MLAS3",
"MOVI3",
"MRFG3",
"MRVE3",
"NATU3",
"ONCO3",
"PCAR3",
"PETR4",
"PETZ3",
"PLPL3",
"PNVL3",
"POMO4",
"POSI3",
"PRIO3",
"PSSA3",
"QUAL3",
"RADL3",
"RAIL3",
"RAIZ4",
"RANI3",
"RAPT4",
"RECV3",
"RENT3",
"ROXO34",
"SANB11",
"SBFG3",
"SBSP3",
"SEER3",
"SIMH3",
"SLCE3",
"SMTO3",
"SUZB3",
"TEND3",
"TIMS3",
"TOTS3",
"TTEN3",
"TUPY3",
"UGPA3",
"USIM5",
"VALE3",
"VAMO3",
"VITT3",
"VIVA3",
"VULC3",
"WEGE3",
"YDUQ3",
]
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
        
    else:
        arquivo = openpyxl.Workbook()
        sheet = arquivo.active
        sheet.title = "Valores Ações"
    
    # Adicionar valores na coluna B
    
    for i, valor in enumerate(minha_lista, start=1):
        sheet[f'H{i}'] = valor
    
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
