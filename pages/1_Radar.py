import streamlit as st
import pandas as pd

# Configuração premium de layout amplo (Ocupa 100% da largura da tela)
st.set_page_config(page_title="Adriel-AI Pro - Radar de Produtos", layout="wide", initial_sidebar_state="collapsed")

# Reaplica o estilo Black de luxo e remove as margens nativas do Streamlit
st.markdown("""
<style>
    .stApp { background-color: #0b111e !important; color: #ffffff !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    [data-testid="stSidebar"] { display: none !important; width: 0px !important; }
    [data-testid="stHeader"] { display: none !important; }
    
    @keyframes sinal-pulsante {
        0% { border-color: #00E5FF; box-shadow: 0 0 8px rgba(0, 229, 255, 0.2); }
        50% { border-color: #00FF87; box-shadow: 0 0 18px rgba(0, 255, 135, 0.4); }
        100% { border-color: #00E5FF; box-shadow: 0 0 8px rgba(0, 229, 255, 0.2); }
    }
    .header-box-real { background-color: #0f172a !important; border: 1px solid #1e293b !important; border-radius: 8px !important; padding: 14px 20px !important; margin-bottom: 15px !important; }
    .subtitulo-bloco-real { font-size: 13px !important; font-weight: bold !important; color: #60a5fa !important; margin-bottom: 15px; text-transform: uppercase; }
    .kpi-box { background: #0f172a; padding: 12px 15px; border-radius: 8px; border: 1px solid #1e293b; text-align: center; }
    
    /* BOTÕES DE LINKS DA ESTEIRA */
    div.stButton > button {
        background: #0f172a !important; color: #cbd5e1 !important; font-weight: bold !important; font-size: 14px !important;
        border: 2px solid #1e293b !important; padding: 12px 15px !important; border-radius: 6px !important; width: 100% !important; cursor: pointer !important;
    }
    div.stButton > button:hover {
        animation: sinal-pulsante 2s infinite ease-in-out !important; background: #1e293b !important; color: #00FF87 !important; transform: scale(1.03) !important;
    }
    /* Estilo exclusivo para o botão verde de baixar planilha */
    .btn-verde div.stButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important; color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 💎 CABEÇALHO DA LOGO + MENU HORIZONTAL
st.markdown("<h2 style='color: #60a5fa; font-size: 26px; font-weight: 800; margin-bottom:0;'>🤖 Adriel-AI <span style='background:#00E5FF; color:#050814; padding:2px 8px; font-size:12px; border-radius:4px; vertical-align:middle;'>PRO</span></h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 11px; margin-top:-5px; letter-spacing:1px;'>SaaS PLATFORM MASTER • CONEXÃO SÍNCRONA VIA REPOSITÓRIO</p>", unsafe_allow_html=True)

st.write("")
col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
with col_nav1: st.page_link("app.py", label="🎛️ Dashboard Geral")
with col_nav2: st.page_link("pages/1_Radar.py", label="🛰️ 1. Radar de Produtos")
with col_nav3: st.page_link("pages/2_Auditor.py", label="🔬 2. Auditor de Mercado")
with col_nav4: st.page_link("pages/4_Cacador.py", label="🏹 4. Caçador Ativo")

st.write("---")

# Divisão exata das colunas paralelas na horizontal ocupando toda a tela limpa
col_centro, col_direita = st.columns([1.4, 1.0])

with col_centro:
    st.markdown('<div class="header-box-real">👤 Comandante: <b>José Marques</b> | Mapeamento de Mercado PRO</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitulo-bloco-real">MÓDULO 1: RADAR DE PRODUTOS [FILTRO XEQUE-MATE]</p>', unsafe_allow_html=True)
    
    dados_tabela = {
        "Name": ["Sugar Defender", "Java Burn", "Puravive", "Prodentim", "GlucoBerry", "Citrus Burn", "Metanail Complex"],
        "Plataforma": ["BuyGoods us", "ClickBank us", "ClickBank us", "BuyGoods us", "Hotmart BR", "ClickBank us", "BuyGoods us"],
        "Comissão": ["$ 118.20", "$ 135.00", "$ 142.50", "$ 125.00", "R$ 247,00", "$ 95.00", "$ 107.40"],
        "Veredito da IA": ["APROVADO (Risco Baixo)"] * 7
    }
    st.dataframe(pd.DataFrame(dados_tabela), use_container_width=True, hide_index=True)
    
    st.write("")
    st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
    if st.button("📄 [BAIXAR PLANILHA DE INTELIGÊNCIA EM LOTE .CSV]", key="btn_radar_csv_inside"):
        st.success("Reforço concluído! Extração processada com sucesso.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_direita:
    st.markdown('<div class="header-box-real" style="text-align: right;">Filtro Especial: <b>Top 22 Ativos</b></div>', unsafe_allow_html=True)
    
    col_mini1, col_mini2 = st.columns(2)
    with col_mini1: st.markdown('<div class="kpi-box"><span style="font-size:11px;color:#64748b;font-weight:bold;">🔥 CLIQUES HOJE</span><br><span style="font-size:20px;color:#00FF87;font-weight:800;">14.250 mil</span></div>', unsafe_allow_html=True)
    with col_mini2: st.markdown('<div class="kpi-box"><span style="font-size:11px;color:#64748b;font-weight:bold;">📡 OFERTAS ATIVAS</span><br><span style="font-size:20px;color:#00E5FF;font-weight:800;">1.840 mil</span></div>', unsafe_allow_html=True)
        
    st.write("---")
    st.info("🔥 **Módulo Espião Operando**\n\nVarredura contínua rastreando lotes de Gravidade e Temperatura acima de 140+ nas redes dos EUA.")

st.markdown('<div style="clear: both; text-align: center; font-size: 11px; color: #475569; padding-top: 45px;"><hr style="border-color: #1e293b;">© 2026 Adriel-AI Pro - Todos os Direitos Reservados.</div>', unsafe_allow_html=True)
