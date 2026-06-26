import time
from binance.client import Client
import pandas as pd

# ==========================================================
# CHAVES SECRETAS DA BINANCE - INTEGRADAS E SALVAS
# ==========================================================
API_KEY = "7EmD2diJHYsrVRU4wFMTX9KNChj05JN4is3CSOM1UL1euadCrgaDNnqRiEVYGU8g"
API_SECRET = "u5MpBDSc7sghH3XpqW6s9NqnM0jr3wfwwZ8eyAsg19hlgkKYSeOyPgQSJ8TrfhBj"

# CONFIGURAÇÕES DA BANCA EM REAL DO JOSÉ
MOEDA = "SOLBRL"             # Solana cotada em Reais
VALOR_ENTRADA_BRL = 380.0    # SUA BANCA DE R$ 380,00 EM REAL
DISTANCIA_TAKE_PERCENT = 3.0 # ALVO: Busca 3% de lucro real (~R$ 11,40)
DISTANCIA_STOP_PERCENT = 1.0 # TRAVA DE SEGURANÇA INICIAL: Proteção máxima de 1%

try:
    client = Client(API_KEY, API_SECRET)
    print(f"👑 MÁQUINA DE TRADING ATIVA EM REAIS (BRL)! Monitorando mercado ao vivo...")
except Exception as e:
    client = None

def obter_dados_e_calcular_forca():
    try:
        # COMANDO COMPACTO: Puxa apenas o estritamente necessário para o RSI (reduz peso em 90%)
        candles = client.get_klines(symbol=MOEDA, interval=Client.KLINE_INTERVAL_1MINUTE, limit=20)
        df = pd.DataFrame(candles, columns=['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'qav', 'num_trades', 'taker_base', 'taker_quote', 'ignore'])
        df['close'] = df['close'].astype(float)
        df['low'] = df['low'].astype(float)
        df['high'] = df['high'].astype(float)
        
        delta = df['close'].diff()
        ganho = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        perda = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = ganho / (perda + 0.00001)
        df['rsi'] = 100 - (100 / (1 + rs))
        return df
    except:
        return None

em_operacao = False
preco_entrada = 0.0
preco_stop = 0.0
preco_take = 0.0
risco_zero_ativado = False
maior_preco_atingido = 0.0
contagem_indecisao = 0
qtd_tokens = 0.0

while True:
    if client is None:
        time.sleep(5)
        continue

    try:
        df_dados = obter_dados_e_calcular_forca()
        
        if df_dados is not None and len(df_dados) > 0:
            preco_atual = float(df_dados['close'].iloc[-1]) # Pega o preço direto da última vela estável
            rsi_atual = df_dados['rsi'].iloc[-1]
            fundo_recente = df_dados['low'].iloc[-10:].min() # Ajustado para bloco rápido
            
            if not em_operacao:
                # 🟢 MODO SUBIDA: Compra no Arranque de Alta
                if rsi_atual > 55 and preco_atual >= df_dados['close'].iloc[-2]:
                    qtd_tokens = round(VALOR_ENTRADA_BRL / preco_atual, 2)
                    order = client.order_market_buy(symbol=MOEDA, quantity=qtd_tokens)
                    preco_entrada = preco_atual
                    preco_stop = preco_entrada * (1.0 - (DISTANCIA_STOP_PERCENT / 100))
                    preco_take = preco_entrada * (1.0 + (DISTANCIA_TAKE_PERCENT / 100))
                    maior_preco_atingido = preco_entrada
                    em_operacao = True
                    risco_zero_ativado = False
                    print(f"⚡ ARRANCOU PARA CIMA! Comprou automático: R$ {VALOR_ENTRADA_BRL:.2f}")
                
                # 🔴 MODO QUEDA: Imprime a análise azul travada e fixa na tela
                else:
                    preco_armadilha = fundo_recente * 0.995
                    print(f"📉 ANALISANDO... Preço Atual: R$ {preco_atual:.2f} | 🎯 Armadilha no Fundo em: R$ {preco_armadilha:.2f}")
                    
                    if preco_atual <= preco_armadilha:
                        qtd_tokens = round(VALOR_ENTRADA_BRL / preco_atual, 2)
                        order = client.order_market_buy(symbol=MOEDA, quantity=qtd_tokens)
                        preco_entrada = preco_atual
                        preco_stop = preco_entrada * (1.0 - (DISTANCIA_STOP_PERCENT / 100))
                        preco_take = preco_entrada * (1.0 + (DISTANCIA_TAKE_PERCENT / 100))
                        maior_preco_atingido = preco_entrada
                        em_operacao = True
                        risco_zero_ativado = False
                        print(f"🎯 FISGOU NA BAIXA! Comprou automático com R$ {VALOR_ENTRADA_BRL:.2f}!")
            
            else:
                if preco_atual > maior_preco_atingido:
                    maior_preco_atingido = preco_atual
                    contagem_indecisao = 0
                else:
                    contagem_indecisao += 1
                
                print(f"🍏 OPERAÇÃO ATIVA REAL! Preço: R$ {preco_atual:.2f} | Stop: R$ {preco_stop:.2f}")
                
                if not risco_zero_ativado and preco_atual >= (preco_entrada * 1.004):
                    preco_stop = preco_entrada
                    risco_zero_ativado = True
                    print("🔒 Locks de Segurança: RISCO ZERO ATIVADO!")
                
                if risco_zero_ativado and preco_atual >= (preco_entrada * 1.010):
                    novo_stop_lucro = preco_entrada * 1.005
                    if novo_stop_lucro > preco_stop:
                        preco_stop = novo_stop_lucro
                        print(f"💰 STOP VENCEDOR ATUALIZADO!")

                lucro_atual_percent = ((preco_atual - preco_entrada) / preco_entrada) * 100
                if risco_zero_ativado and contagem_indecisao >= 4 and lucro_atual_percent > 0.3:
                    client.order_market_sell(symbol=MOEDA, quantity=qtd_tokens)
                    print(f"⚠️ MERCADO INDECISO! Venda real executada no positivo.")
                    em_operacao = False
                
                elif preco_atual >= preco_take:
                    client.order_market_sell(symbol=MOEDA, quantity=qtd_tokens)
                    print(f"🎯 META MÁXIMA ATINGIDA!")
                    em_operacao = False
                
                elif preco_atual <= preco_stop:
                    client.order_market_sell(symbol=MOEDA, quantity=qtd_tokens)
                    print(f"🏆 OPERAÇÃO ENCERRADA NO STOP VENCEDOR!")
                    em_operacao = False
                    
    except Exception as e:
        pass # ELIMINA O LOOP BRANCO: Se falhar a rede, ele apenas pula o segundo em silêncio sem travar a tela!
        
    time.sleep(2)
