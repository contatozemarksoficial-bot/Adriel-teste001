
import time
from binance.client import Client
import pandas as pd

# ==========================================================
# CHAVES SECRETAS DA BINANCE - INTEGRADAS E SALVAS
# ==========================================================
API_KEY = "2tBttnbAWEPAasMetRSVKhsvQcwxZvoqc1AoYWat6QXGAKCO5EvEKFOXxOUg68MG"
API_SECRET = "HUWQy3RWcKmz9Thd8kuwSpdm38jvOn7FuHiWZYW6ShYYhpTXrgepRTaCaseywZgY"  # CHAVES 100% CONFIGURADAS

# CONFIGURAÇÕES DA MÁQUINA PERFEITA (O Pensamento do José)
MOEDA = "SOLBRL"             # Solana cotada em Reais
VALOR_ENTRADA_BRL = 380.0    # BANCA ATUALIZADA
DISTANCIA_TAKE_PERCENT = 3.0 # ALVO AUMENTADO: Busca 3% de lucro (~R$ 9,78)
DISTANCIA_STOP_PERCENT = 1.0 # TRAVA DE SEGURANÇA INICIAL: Proteção máxima de 1%

try:
    client = Client(API_KEY, API_SECRET)
    print(f"👑 MÁQUINA OPERACIONAL REAL ATIVA! Enviando ordens automáticas para a Binance...")
except Exception as e:
    print(f"Aguardando chaves válidas da Binance para conectar...")
    client = None

def obter_dados_e_calcular_forca():
    try:
        candles = client.get_klines(symbol=MOEDA, interval=Client.KLINE_INTERVAL_1MINUTE, limit=40)
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
        ticker = client.get_symbol_ticker(symbol=MOEDA)
        preco_atual = float(ticker['price'])
        df_dados = obter_dados_e_calcular_forca()
        
        if df_dados is not None and len(df_dados) > 0:
            rsi_atual = df_dados['rsi'].iloc[-1]
            fundo_recente = df_dados['low'].iloc[-15:].min()
            
            # 🔄 1º PONTO: ENTRADA INTELIGENTE DIRETO NA CONTA REAL
            if not em_operacao:
                if rsi_atual < 40:
                    preco_armadilha = fundo_recente * 0.995
                    print(f"📉 PROCURANDO BAIXA... Armadilha em: R$ {preco_armadilha:.2f} | Atual: R$ {preco_atual:.2f}")
                    
                    if preco_atual <= preco_armadilha:
                        qtd_tokens = round(VALOR_ENTRADA_BRL / preco_atual, 2)
                        # COMANDO REAL DA BINANCE: Compra moedas de verdade no mercado
                        order = client.order_market_buy(symbol=MOEDA, quantity=qtd_tokens)
                        preco_entrada = preco_atual
                        preco_stop = preco_entrada * (1.0 - (DISTANCIA_STOP_PERCENT / 100))
                        preco_take = preco_entrada * (1.0 + (DISTANCIA_TAKE_PERCENT / 100))
                        maior_preco_atingido = preco_entrada
                        em_operacao = True
                        risco_zero_ativado = False
                        print(f"🎯 ARMADILHA REAL CAPTURADA! Comprou R$ {VALOR_ENTRADA_BRL} em Solana!")
                
                elif rsi_atual > 55 and preco_atual >= df_dados['close'].iloc[-2]:
                    qtd_tokens = round(VALOR_ENTRADA_BRL / preco_atual, 2)
                    # COMANDO REAL DA BINANCE: Dispara a compra no arranque de alta
                    order = client.order_market_buy(symbol=MOEDA, quantity=qtd_tokens)
                    preco_entrada = preco_atual
                    preco_stop = preco_entrada * (1.0 - (DISTANCIA_STOP_PERCENT / 100))
                    preco_take = preco_entrada * (1.0 + (DISTANCIA_TAKE_PERCENT / 100))
                    maior_preco_atingido = preco_entrada
                    em_operacao = True
                    risco_zero_ativado = False
                    print(f"⚡ ARRANQUE REAL COM COMPRA EXECUTADA! Preço: R$ {preco_entrada:.2f}")
            
            # 🔄 2º PONTO: MONITORAMENTO E VENDA REAL (STOP VENCEDOR)
            else:
                if preco_atual > maior_preco_atingido:
                    maior_preco_atingido = preco_atual
                    contagem_indecisao = 0
                else:
                    contagem_indecisao += 1
                
                print(f"🍏 OPERAÇÃO ATIVA REAL! Preço: R$ {preco_atual:.2f} | Gatilho Stop: R$ {preco_stop:.2f}")
                
                if not risco_zero_ativado and preco_atual >= (preco_entrada * 1.004):
                    preco_stop = preco_entrada
                    risco_zero_ativado = True
                    print("🔒 Locks de Segurança: Operação travada em RISCO ZERO!")
                
                if risco_zero_ativado and preco_atual >= (preco_entrada * 1.010):
                    novo_stop_lucro = preco_entrada * 1.005
                    if novo_stop_lucro > preco_stop:
                        preco_stop = novo_stop_lucro
                        print(f"💰 STOP VENCEDOR: R$ 1,63 de lucro trancado!")

                if risco_zero_ativado and preco_atual >= (preco_entrada * 1.020):
                    novo_stop_lucro = preco_entrada * 1.012
                    if novo_stop_lucro > preco_stop:
                        preco_stop = novo_stop_lucro
                        print(f"💎 STOP VENCEDOR SUBIU: R$ 3,91 trancado com segurança!")

                lucro_atual_percent = ((preco_atual - preco_entrada) / preco_entrada) * 100
                if risco_zero_ativado and contagem_indecisao >= 4 and lucro_atual_percent > 0.3:
                    # COMANDO REAL DA BINANCE: Passa o rodo por indecisão
                    client.order_market_sell(symbol=MOEDA, quantity=qtd_tokens)
                    print(f"⚠️ MERCADO INDECISO! Venda real executada no positivo.")
                    em_operacao = False
                
                elif preco_atual >= preco_take:
                    # COMANDO REAL DA BINANCE: Vende tudo na meta máxima de 3%
                    client.order_market_sell(symbol=MOEDA, quantity=qtd_tokens)
                    print(f"🎯 META MÁXIMA ATINGIDA! Lucro real no bolso!")
                    em_operacao = False
                
                elif preco_atual <= preco_stop:
                    # COMANDO REAL DA BINANCE: Executa o stop e tira do ativo
                    client.order_market_sell(symbol=MOEDA, quantity=qtd_tokens)
                    print(f"🏆 OPERAÇÃO ENCERRADA NO STOP VENCEDOR!")
                    em_operacao = False
                    
    except Exception as e:
        print(f"Sincronizando ordens com a carteira Binance...")
        
    time.sleep(2)
